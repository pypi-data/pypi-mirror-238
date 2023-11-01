from void_terminal.toolbox import update_ui
from void_terminal.toolbox import CatchException, report_execption
from void_terminal.toolbox import write_history_to_file, promote_file_to_downloadzone
from void_terminal.crazy_functions.crazy_utils import request_gpt_model_in_new_thread_with_ui_alive
fast_debug = False

def GenerateFunctionComments(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt):
    import time, os
    print('begin analysis on:', file_manifest)
    for index, fp in enumerate(file_manifest):
        with open(fp, 'r', encoding='utf-8', errors='replace') as f:
            file_content = f.read()

        i_say = f'Please provide an overview of the program file below，And generate comments for all functions in the file，Output the results using markdown tables，The file name is{os.path.relpath(fp, project_folder)}，The file content is ```{file_content}```'
        i_say_show_user = f'[{index}/{len(file_manifest)}] Please provide an overview of the program file below，And generate comments for all functions in the file: {os.path.abspath(fp)}'
        chatbot.append((i_say_show_user, "[Local Message] waiting gpt response."))
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page

        if not fast_debug: 
            msg = 'Normal'
            # ** gpt request **
            gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
                i_say, i_say_show_user, llm_kwargs, chatbot, history=[], sys_prompt=system_prompt)   # With timeout countdown

            chatbot[-1] = (i_say_show_user, gpt_say)
            history.append(i_say_show_user); history.append(gpt_say)
            yield from update_ui(chatbot=chatbot, history=history, msg=msg) # Refresh the page
            if not fast_debug: time.sleep(2)

    if not fast_debug: 
        res = write_history_to_file(history)
        promote_file_to_downloadzone(res, chatbot=chatbot)
        chatbot.append(("Are you done?？", res))
        yield from update_ui(chatbot=chatbot, history=history, msg=msg) # Refresh the page



@CatchException
def BatchGenerateFunctionComments(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    history = []    # Clear history，To avoid input overflow
    import glob, os
    if os.path.exists(txt):
        project_folder = txt
    else:
        if txt == "": txt = 'Empty input field'
        report_execption(chatbot, history, a = f"Parsing project: {txt}", b = f"Cannot find local project or do not have access: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return
    file_manifest = [f for f in glob.glob(f'{project_folder}/**/*.py', recursive=True)] + \
                    [f for f in glob.glob(f'{project_folder}/**/*.cpp', recursive=True)]

    if len(file_manifest) == 0:
        report_execption(chatbot, history, a = f"Parsing project: {txt}", b = f"Cannot find any .tex files: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return
    yield from GenerateFunctionComments(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt)
