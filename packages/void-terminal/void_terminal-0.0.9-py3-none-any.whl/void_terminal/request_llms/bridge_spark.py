
import time
import threading
import importlib
from void_terminal.toolbox import update_ui, get_conf, update_ui_lastest_msg
from multiprocessing import Process, Pipe

model_name = 'Spark Cognitive Big Model'

def validate_key():
    XFYUN_APPID = get_conf('XFYUN_APPID')
    if XFYUN_APPID == '00000000' or XFYUN_APPID == '': 
        return False
    return True

def predict_no_ui_long_connection(inputs, llm_kwargs, history=[], sys_prompt="", observe_window=[], console_slience=False):
    """
        ⭐Multi-threaded method
        For function details, please see request_llms/bridge_all.py
    """
    watch_dog_patience = 5
    response = ""

    if validate_key() is False:
        raise RuntimeError('Please configure XFYUN_APPID for the Xunfei Starfire model, XFYUN_API_KEY, XFYUN_API_SECRET')

    from void_terminal.request_llms.com_sparkapi import SparkRequestInstance
    sri = SparkRequestInstance()
    for response in sri.generate(inputs, llm_kwargs, history, sys_prompt):
        if len(observe_window) >= 1:
            observe_window[0] = response
        if len(observe_window) >= 2:
            if (time.time()-observe_window[1]) > watch_dog_patience: raise RuntimeError("Program terminated。")
    return response

def predict(inputs, llm_kwargs, plugin_kwargs, chatbot, history=[], system_prompt='', stream = True, additional_fn=None):
    """
        ⭐Single-threaded method
        For function details, please see request_llms/bridge_all.py
    """
    chatbot.append((inputs, ""))
    yield from update_ui(chatbot=chatbot, history=history)

    if validate_key() is False:
        yield from update_ui_lastest_msg(lastmsg="[Local Message] Please configure XFYUN_APPID for the Xunfei Starfire model, XFYUN_API_KEY, XFYUN_API_SECRET", chatbot=chatbot, history=history, delay=0)
        return

    if additional_fn is not None:
        from void_terminal.core_functional import handle_core_functionality
        inputs, history = handle_core_functionality(additional_fn, inputs, history, chatbot)

    # Start receiving replies    
    from void_terminal.request_llms.com_sparkapi import SparkRequestInstance
    sri = SparkRequestInstance()
    for response in sri.generate(inputs, llm_kwargs, history, system_prompt):
        chatbot[-1] = (inputs, response)
        yield from update_ui(chatbot=chatbot, history=history)

    # Summary output
    if response == f"[Local Message] Waiting{model_name}Responding ...":
        response = f"[Local Message] {model_name}Response exception ..."
    history.extend([inputs, response])
    yield from update_ui(chatbot=chatbot, history=history)