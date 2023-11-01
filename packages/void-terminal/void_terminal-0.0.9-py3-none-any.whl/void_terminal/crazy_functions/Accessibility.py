# encoding: utf-8
# @Time   : 2023/4/19
# @Author : Spike
# @Descr   :
from void_terminal.toolbox import update_ui, get_conf
from void_terminal.toolbox import CatchException
from void_terminal.crazy_functions.crazy_utils import request_gpt_model_in_new_thread_with_ui_alive


@CatchException
def 猜你想Ask(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    if txt:
        show_say = txt
        prompt = txt+'\nAfter answering the question，List three more questions that the user might ask。'
    else:
        prompt = history[-1]+"\nAnalyze the above answer，List three more questions that the user might ask。"
        show_say = 'Analyze the above answer，List three more questions that the user might ask。'
    gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
        inputs=prompt,
        inputs_show_user=show_say,
        llm_kwargs=llm_kwargs,
        chatbot=chatbot,
        history=history,
        sys_prompt=system_prompt
    )
    chatbot[-1] = (show_say, gpt_say)
    history.extend([show_say, gpt_say])
    yield from update_ui(chatbot=chatbot, history=history)  # Refresh the page


@CatchException
def ClearCache(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    chatbot.append(['Clear local cache data', 'Executing. Deleting data'])
    yield from update_ui(chatbot=chatbot, history=history)  # Refresh the page

    import shutil, os
    PATH_PRIVATE_UPLOAD, PATH_LOGGING = get_conf('PATH_PRIVATE_UPLOAD', 'PATH_LOGGING')
    shutil.rmtree(PATH_LOGGING, ignore_errors=True)
    shutil.rmtree(PATH_PRIVATE_UPLOAD, ignore_errors=True)

    chatbot.append(['Clear local cache data', 'Execution completed'])
    yield from update_ui(chatbot=chatbot, history=history)  # Refresh the page