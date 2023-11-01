from void_terminal.toolbox import update_ui
from void_terminal.toolbox import CatchException, report_execption
from void_terminal.toolbox import write_history_to_file, promote_file_to_downloadzone
from void_terminal.crazy_functions.crazy_utils import request_gpt_model_in_new_thread_with_ui_alive


def ParsePaper(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt):
    import time, glob, os
    print('begin analysis on:', file_manifest)
    for index, fp in enumerate(file_manifest):
        with open(fp, 'r', encoding='utf-8', errors='replace') as f:
            file_content = f.read()

        prefix = "Next, please analyze the following paper files one by one，Summarize its content" if index==0 else ""
        i_say = prefix + f'Please summarize the following article in Chinese，The file name is{os.path.relpath(fp, project_folder)}，The content of the article is ```{file_content}```'
        i_say_show_user = prefix + f'[{index}/{len(file_manifest)}] Please summarize the following article: {os.path.abspath(fp)}'
        chatbot.append((i_say_show_user, "[Local Message] waiting gpt response."))
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page

        msg = 'Normal'
        gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(i_say, i_say_show_user, llm_kwargs, chatbot, history=[], sys_prompt=system_prompt)   # With timeout countdown
        chatbot[-1] = (i_say_show_user, gpt_say)
        history.append(i_say_show_user); history.append(gpt_say)
        yield from update_ui(chatbot=chatbot, history=history, msg=msg) # Refresh the page
        time.sleep(2)

    all_file = ', '.join([os.path.relpath(fp, project_folder) for index, fp in enumerate(file_manifest)])
    i_say = f'According to your own analysis above，Summarize the entire text，Write a Chinese abstract in academic language，Then write an English abstract（Including{all_file}）。'
    chatbot.append((i_say, "[Local Message] waiting gpt response."))
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page

    msg = 'Normal'
    # ** gpt request **
    gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(i_say, i_say, llm_kwargs, chatbot, history=history, sys_prompt=system_prompt)   # With timeout countdown

    chatbot[-1] = (i_say, gpt_say)
    history.append(i_say); history.append(gpt_say)
    yield from update_ui(chatbot=chatbot, history=history, msg=msg) # Refresh the page
    res = write_history_to_file(history)
    promote_file_to_downloadzone(res, chatbot=chatbot)
    chatbot.append(("Are you done?？", res))
    yield from update_ui(chatbot=chatbot, history=history, msg=msg) # Refresh the page



@CatchException
def ReadArticleWriteSummary(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    history = []    # Clear history，To avoid input overflow
    import glob, os
    if os.path.exists(txt):
        project_folder = txt
    else:
        if txt == "": txt = 'Empty input field'
        report_execption(chatbot, history, a = f"Parsing project: {txt}", b = f"Cannot find local project or do not have access: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return
    file_manifest = [f for f in glob.glob(f'{project_folder}/**/*.tex', recursive=True)] # + \
                    # [f for f in glob.glob(f'{project_folder}/**/*.cpp', recursive=True)] + \
                    # [f for f in glob.glob(f'{project_folder}/**/*.c', recursive=True)]
    if len(file_manifest) == 0:
        report_execption(chatbot, history, a = f"Parsing project: {txt}", b = f"Cannot find any .tex files: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return
    yield from ParsePaper(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt)
