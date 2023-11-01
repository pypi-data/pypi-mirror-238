# Referenced from https://github.com/GaiZhenbiao/ChuanhuChatGPT 项目

"""
    This file mainly contains three functions

    Functions without multi-threading capability：
    1. predict: Used in normal conversation，Fully interactive，Not multi-threaded

    Functions with multi-threading capability
    2. predict_no_ui：Calling advanced experimental function modules，Will not be displayed on the interface in real time，The parameters are simple，Can be multi-threaded and parallel，Convenient for implementing complex functional logic
    3. predict_no_ui_long_connection：It was found during the experiment that when calling predict_no_ui to process long documents,，Connection to OpenAI is prone to disconnection，This function solves the problem using stream，Also supports multi-threading
"""

import json
import time
import gradio as gr
import logging
import traceback
import requests
import importlib

# Put your own secrets such as API and proxy address in config_private.py
# When reading, first check if there is a private config_private configuration file（Not controlled by git），If there is，Then overwrite the original config file
from void_terminal.toolbox import get_conf, update_ui, is_any_api_key, select_api_key, what_keys, clip_history, trimmed_format_exc
proxies, TIMEOUT_SECONDS, MAX_RETRY, API_ORG = \
    get_conf('proxies', 'TIMEOUT_SECONDS', 'MAX_RETRY', 'API_ORG')

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
    watch_dog_patience = 5 # The patience of the watchdog, Set 5 seconds
    headers, payload = generate_payload(inputs, llm_kwargs, history, system_prompt=sys_prompt, stream=True)
    retry = 0
    while True:
        try:
            # make a POST request to the API endpoint, stream=False
            from void_terminal.request_llms.bridge_all import model_info
            endpoint = model_info[llm_kwargs['llm_model']]['endpoint']
            response = requests.post(endpoint, headers=headers, proxies=proxies,
                                    json=payload, stream=True, timeout=TIMEOUT_SECONDS); break
        except requests.exceptions.ReadTimeout as e:
            retry += 1
            traceback.print_exc()
            if retry > MAX_RETRY: raise TimeoutError
            if MAX_RETRY!=0: print(f'Request timed out，Retrying ({retry}/{MAX_RETRY}) ……')

    stream_response =  response.iter_lines()
    result = ''
    while True:
        try: chunk = next(stream_response).decode()
        except StopIteration: 
            break
        except requests.exceptions.ConnectionError:
            chunk = next(stream_response).decode() # Failed，Retry once？If it fails again, there is no way。
        if len(chunk)==0: continue
        if not chunk.startswith('data:'): 
            error_msg = get_full_error(chunk.encode('utf8'), stream_response).decode()
            if "reduce the length" in error_msg:
                raise ConnectionAbortedError("OpenAI rejected the request:" + error_msg)
            else:
                raise RuntimeError("OpenAI rejected the request：" + error_msg)
        if ('data: [DONE]' in chunk): break # api2d completed normally
        json_data = json.loads(chunk.lstrip('data:'))['choices'][0]
        delta = json_data["delta"]
        if len(delta) == 0: break
        if "role" in delta: continue
        if "content" in delta: 
            result += delta["content"]
            if not console_slience: print(delta["content"], end='')
            if observe_window is not None: 
                # Observation window，Display the data already obtained
                if len(observe_window) >= 1: observe_window[0] += delta["content"]
                # Watchdog，If the dog is not fed beyond the deadline，then terminate
                if len(observe_window) >= 2:  
                    if (time.time()-observe_window[1]) > watch_dog_patience:
                        raise RuntimeError("User canceled the program。")
        else: raise RuntimeError("Unexpected JSON structure："+delta)
    if json_data['finish_reason'] == 'content_filter':
        raise RuntimeError("Due to Azure filtering out questions containing non-compliant content.。")
    if json_data['finish_reason'] == 'length':
        raise ConnectionAbortedError("Normal termination，But shows insufficient token，Resulting in incomplete output，Please reduce the amount of text input per request。")
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
    if additional_fn is not None:
        from void_terminal.core_functional import handle_core_functionality
        inputs, history = handle_core_functionality(additional_fn, inputs, history, chatbot)

    raw_input = inputs
    logging.info(f'[raw_input] {raw_input}')
    chatbot.append((inputs, ""))
    yield from update_ui(chatbot=chatbot, history=history, msg="Waiting for response") # Refresh the page

    try:
        headers, payload = generate_payload(inputs, llm_kwargs, history, system_prompt, stream)
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
            endpoint = model_info[llm_kwargs['llm_model']]['endpoint']
            response = requests.post(endpoint, headers=headers, proxies=proxies,
                                    json=payload, stream=True, timeout=TIMEOUT_SECONDS);break
        except:
            retry += 1
            chatbot[-1] = ((chatbot[-1][0], timeout_bot_msg))
            retry_msg = f"，Retrying ({retry}/{MAX_RETRY}) ……" if MAX_RETRY > 0 else ""
            yield from update_ui(chatbot=chatbot, history=history, msg="Request timed out"+retry_msg) # Refresh the page
            if retry > MAX_RETRY: raise TimeoutError

    gpt_replying_buffer = ""
    
    is_head_of_the_stream = True
    if stream:
        stream_response =  response.iter_lines()
        while True:
            try:
                chunk = next(stream_response)
            except StopIteration:
                # such errors occur in non-OpenAI official interfaces，OpenAI and API2D will not go here
                chunk_decoded = chunk.decode()
                error_msg = chunk_decoded
                chatbot, history = handle_error(inputs, llm_kwargs, chatbot, history, chunk_decoded, error_msg)
                yield from update_ui(chatbot=chatbot, history=history, msg="Non-Openai official interface returned an error:" + chunk.decode()) # Refresh the page
                return
            
            # print(chunk.decode()[6:])
            if is_head_of_the_stream and (r'"object":"error"' not in chunk.decode()):
                # The first frame of the data stream does not carry content
                is_head_of_the_stream = False; continue
            
            if chunk:
                try:
                    chunk_decoded = chunk.decode()
                    # The former is the termination condition of API2D，The latter is the termination condition of OPENAI
                    if 'data: [DONE]' in chunk_decoded:
                        # Judged as the end of the data stream，gpt_replying_buffer is also written
                        logging.info(f'[response] {gpt_replying_buffer}')
                        break
                    # Processing the body of the data stream
                    chunkjson = json.loads(chunk_decoded[6:])
                    status_text = f"finish_reason: {chunkjson['choices'][0]['finish_reason']}"
                    delta = chunkjson['choices'][0]["delta"]
                    if "content" in delta:
                        gpt_replying_buffer = gpt_replying_buffer + delta["content"]
                    history[-1] = gpt_replying_buffer
                    chatbot[-1] = (history[-2], history[-1])
                    yield from update_ui(chatbot=chatbot, history=history, msg=status_text) # Refresh the page
                except Exception as e:
                    yield from update_ui(chatbot=chatbot, history=history, msg="Json parsing is not normal") # Refresh the page
                    chunk = get_full_error(chunk, stream_response)
                    chunk_decoded = chunk.decode()
                    error_msg = chunk_decoded
                    chatbot, history = handle_error(inputs, llm_kwargs, chatbot, history, chunk_decoded, error_msg)
                    yield from update_ui(chatbot=chatbot, history=history, msg="Json exception" + error_msg) # Refresh the page
                    print(error_msg)
                    return

def handle_error(inputs, llm_kwargs, chatbot, history, chunk_decoded, error_msg):
    from void_terminal.request_llms.bridge_all import model_info
    openai_website = ' Please log in to OpenAI to view details at https://platform.openai.com/signup'
    if "reduce the length" in error_msg:
        if len(history) >= 2: history[-1] = ""; history[-2] = "" # Clear the current overflow input：history[-2] It is the input of this time, history[-1] It is the output of this time
        history = clip_history(inputs=inputs, history=history, tokenizer=model_info[llm_kwargs['llm_model']]['tokenizer'], 
                                               max_token_limit=(model_info[llm_kwargs['llm_model']]['max_token'])) # Release at least half of the history
        chatbot[-1] = (chatbot[-1][0], "[Local Message] Reduce the length. The input is too long this time, Or the historical data is too long. Historical cached data has been partially released, You can try again. (If it fails again, it is more likely due to input being too long.)")
                        # history = []    # Clear the history
    elif "does not exist" in error_msg:
        chatbot[-1] = (chatbot[-1][0], f"[Local Message] Model {llm_kwargs['llm_model']} Model does not exist, Or you do not have the qualification for experience.")
    elif "Incorrect API key" in error_msg:
        chatbot[-1] = (chatbot[-1][0], "[Local Message] Incorrect API key. OpenAI claims that an incorrect API_KEY was provided, Service refused. " + openai_website)
    elif "exceeded your current quota" in error_msg:
        chatbot[-1] = (chatbot[-1][0], "[Local Message] You exceeded your current quota. OpenAI claims that the account balance is insufficient, Service refused." + openai_website)
    elif "account is not active" in error_msg:
        chatbot[-1] = (chatbot[-1][0], "[Local Message] Your account is not active. OpenAI states that it is due to account expiration, Service refused." + openai_website)
    elif "associated with a deactivated account" in error_msg:
        chatbot[-1] = (chatbot[-1][0], "[Local Message] You are associated with a deactivated account. OpenAI considers it as an account expiration, Service refused." + openai_website)
    elif "bad forward key" in error_msg:
        chatbot[-1] = (chatbot[-1][0], "[Local Message] Bad forward key. API2D account balance is insufficient.")
    elif "Not enough point" in error_msg:
        chatbot[-1] = (chatbot[-1][0], "[Local Message] Not enough point. API2D account points are insufficient.")
    else:
        from void_terminal.toolbox import regular_txt_to_markdown
        tb_str = '```\n' + trimmed_format_exc() + '```'
        chatbot[-1] = (chatbot[-1][0], f"[Local Message] Exception \n\n{tb_str} \n\n{regular_txt_to_markdown(chunk_decoded)}")
    return chatbot, history

def generate_payload(inputs, llm_kwargs, history, system_prompt, stream):
    """
    Integrate all information，Select LLM model，Generate http request，Prepare to send request
    """
    if not is_any_api_key(llm_kwargs['api_key']):
        raise AssertionError("You provided an incorrect API_KEY。\n\n1. Temporary Solution：Enter the api_key Directly in the Input Area，Submit after pressing Enter。\n\nLong-term solution：Configure in config.py。")

    headers = {
        "Content-Type": "application/json",
    }

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

    payload = {
        "model": llm_kwargs['llm_model'].strip('api2d-'),
        "messages": messages, 
        "temperature": llm_kwargs['temperature'],  # 1.0,
        "top_p": llm_kwargs['top_p'],  # 1.0,
        "n": 1,
        "stream": stream,
        "presence_penalty": 0,
        "frequency_penalty": 0,
    }
    try:
        print(f" {llm_kwargs['llm_model']} : {conversation_cnt} : {inputs[:100]} ..........")
    except:
        print('There may be garbled characters in the input。')
    return headers,payload


