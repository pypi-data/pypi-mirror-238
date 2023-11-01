# Referenced from https://github.com/GaiZhenbiao/ChuanhuChatGPT 项目

"""
    There are mainly 2 functions in this file

    Functions without multi-threading capability：
    1. predict: Used in normal conversation，Fully interactive，Not multi-threaded

    Functions with multi-threading capability
    2. predict_no_ui_long_connection：It was found during the experiment that when calling predict_no_ui to process long documents,，Connection to OpenAI is prone to disconnection，This function solves the problem using stream，Also supports multi-threading
"""

import os
import json
import time
import gradio as gr
import logging
import traceback
import requests
import importlib

# Put your own secrets such as API and proxy address in config_private.py
# When reading, first check if there is a private config_private configuration file（Not controlled by git），If there is，Then overwrite the original config file
from void_terminal.toolbox import get_conf, update_ui, trimmed_format_exc, ProxyNetworkActivate
proxies, TIMEOUT_SECONDS, MAX_RETRY, ANTHROPIC_API_KEY = \
    get_conf('proxies', 'TIMEOUT_SECONDS', 'MAX_RETRY', 'ANTHROPIC_API_KEY')

timeout_bot_msg = '[Local Message] Request timeout. Network error. Please check proxy settings in config.py.' + \
                  'Network error，Check if the proxy server is available，And if the format of the proxy settings is correct，The format must be[Protocol]://[Address]:[Port]，All parts are necessary。'

def get_full_error(chunk, stream_response):
    """
        Get the complete error message returned from OpenAI
    """
    while True:
        try:
            chunk += next(stream_response)
        except:
            break
    return chunk


def predict_no_ui_long_connection(inputs, llm_kwargs, history=[], sys_prompt="", observe_window=None, console_slience=False):
    """
    Send to chatGPT，Waiting for reply，Completed in one go，Do not display intermediate processes。But internally use the stream method to avoid the network being cut off midway。
    inputs：
        This is the input of this inquiry
    sys_prompt:
        System silent prompt
    llm_kwargs：
        Internal tuning parameters of chatGPT
    history：
        history is the list of previous conversations
    observe_window = None：
        Used to transfer the already output part across threads，Most of the time it`s just for fancy visual effects，Leave it blank。observe_window[0]：Observation window。observe_window[1]：Watchdog
    """
    from anthropic import Anthropic
    watch_dog_patience = 5 # The patience of the watchdog, Set 5 seconds
    prompt = generate_payload(inputs, llm_kwargs, history, system_prompt=sys_prompt, stream=True)
    retry = 0
    if len(ANTHROPIC_API_KEY) == 0:
        raise RuntimeError("ANTHROPIC_API_KEY option is not set")

    while True:
        try:
            # make a POST request to the API endpoint, stream=False
            from void_terminal.request_llms.bridge_all import model_info
            anthropic = Anthropic(api_key=ANTHROPIC_API_KEY)
            # endpoint = model_info[llm_kwargs['llm_model']]['endpoint']
            # with ProxyNetworkActivate()
            stream = anthropic.completions.create(
                prompt=prompt,
                max_tokens_to_sample=4096,       # The maximum number of tokens to generate before stopping.
                model=llm_kwargs['llm_model'],
                stream=True,
                temperature = llm_kwargs['temperature']
            )
            break
        except Exception as e:
            retry += 1
            traceback.print_exc()
            if retry > MAX_RETRY: raise TimeoutError
            if MAX_RETRY!=0: print(f'Request timed out，Retrying ({retry}/{MAX_RETRY}) ……')
    result = ''
    try: 
        for completion in stream:
            result += completion.completion
            if not console_slience: print(completion.completion, end='')
            if observe_window is not None: 
                # Observation window，Display the data already obtained
                if len(observe_window) >= 1: observe_window[0] += completion.completion
                # Watchdog，If the dog is not fed beyond the deadline，then terminate
                if len(observe_window) >= 2:  
                    if (time.time()-observe_window[1]) > watch_dog_patience:
                        raise RuntimeError("User canceled the program。")
    except Exception as e:
        traceback.print_exc()

    return result


def predict(inputs, llm_kwargs, plugin_kwargs, chatbot, history=[], system_prompt='', stream = True, additional_fn=None):
    """
    Send to chatGPT，Get output in a streaming way。
    Used for basic conversation functions。
    inputs are the inputs for this inquiry
    top_p, Temperature is an internal tuning parameter of chatGPT
    history is the list of previous conversations（Note that both inputs and history，An error of token overflow will be triggered if the content is too long）
    chatbot is the conversation list displayed in WebUI，Modify it，Then yield it out，You can directly modify the conversation interface content
    additional_fn represents which button is clicked，See functional.py for buttons
    """
    from anthropic import Anthropic
    if len(ANTHROPIC_API_KEY) == 0:
        chatbot.append((inputs, "ANTHROPIC_API_KEY is not set"))
        yield from update_ui(chatbot=chatbot, history=history, msg="Waiting for response") # Refresh the page
        return
    
    if additional_fn is not None:
        from void_terminal.core_functional import handle_core_functionality
        inputs, history = handle_core_functionality(additional_fn, inputs, history, chatbot)

    raw_input = inputs
    logging.info(f'[raw_input] {raw_input}')
    chatbot.append((inputs, ""))
    yield from update_ui(chatbot=chatbot, history=history, msg="Waiting for response") # Refresh the page

    try:
        prompt = generate_payload(inputs, llm_kwargs, history, system_prompt, stream)
    except RuntimeError as e:
        chatbot[-1] = (inputs, f"The api-key you provided does not meet the requirements，Does not contain any that can be used for{llm_kwargs['llm_model']}api-key。You may have selected the wrong model or request source。")
        yield from update_ui(chatbot=chatbot, history=history, msg="API key does not meet requirements") # Refresh the page
        return

    history.append(inputs); history.append("")

    retry = 0
    while True:
        try:
            # make a POST request to the API endpoint, stream=True
            from void_terminal.request_llms.bridge_all import model_info
            anthropic = Anthropic(api_key=ANTHROPIC_API_KEY)
            # endpoint = model_info[llm_kwargs['llm_model']]['endpoint']
            # with ProxyNetworkActivate()
            stream = anthropic.completions.create(
                prompt=prompt,
                max_tokens_to_sample=4096,       # The maximum number of tokens to generate before stopping.
                model=llm_kwargs['llm_model'],
                stream=True,
                temperature = llm_kwargs['temperature']
            )
            
            break
        except:
            retry += 1
            chatbot[-1] = ((chatbot[-1][0], timeout_bot_msg))
            retry_msg = f"，Retrying ({retry}/{MAX_RETRY}) ……" if MAX_RETRY > 0 else ""
            yield from update_ui(chatbot=chatbot, history=history, msg="Request timed out"+retry_msg) # Refresh the page
            if retry > MAX_RETRY: raise TimeoutError

    gpt_replying_buffer = ""
    
    for completion in stream:
        try:
            gpt_replying_buffer = gpt_replying_buffer + completion.completion
            history[-1] = gpt_replying_buffer
            chatbot[-1] = (history[-2], history[-1])
            yield from update_ui(chatbot=chatbot, history=history, msg='Normal') # Refresh the page

        except Exception as e:
            from void_terminal.toolbox import regular_txt_to_markdown
            tb_str = '```\n' + trimmed_format_exc() + '```'
            chatbot[-1] = (chatbot[-1][0], f"[Local Message] Exception \n\n{tb_str}")
            yield from update_ui(chatbot=chatbot, history=history, msg="Json exception" + tb_str) # Refresh the page
            return
        



# https://github.com/jtsang4/claude-to-chatgpt/blob/main/claude_to_chatgpt/adapter.py
def convert_messages_to_prompt(messages):
    prompt = ""
    role_map = {
        "system": "Human",
        "user": "Human",
        "assistant": "Assistant",
    }
    for message in messages:
        role = message["role"]
        content = message["content"]
        transformed_role = role_map[role]
        prompt += f"\n\n{transformed_role.capitalize()}: {content}"
    prompt += "\n\nAssistant: "
    return prompt

def generate_payload(inputs, llm_kwargs, history, system_prompt, stream):
    """
    Integrate all information，Select LLM model，Generate http request，Prepare to send request
    """
    from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

    conversation_cnt = len(history) // 2

    messages = [{"role": "system", "content": system_prompt}]
    if conversation_cnt:
        for index in range(0, 2*conversation_cnt, 2):
            what_i_have_asked = {}
            what_i_have_asked["role"] = "user"
            what_i_have_asked["content"] = history[index]
            what_gpt_answer = {}
            what_gpt_answer["role"] = "assistant"
            what_gpt_answer["content"] = history[index+1]
            if what_i_have_asked["content"] != "":
                if what_gpt_answer["content"] == "": continue
                if what_gpt_answer["content"] == timeout_bot_msg: continue
                messages.append(what_i_have_asked)
                messages.append(what_gpt_answer)
            else:
                messages[-1]['content'] = what_gpt_answer['content']

    what_i_ask_now = {}
    what_i_ask_now["role"] = "user"
    what_i_ask_now["content"] = inputs
    messages.append(what_i_ask_now)
    prompt = convert_messages_to_prompt(messages)

    return prompt


