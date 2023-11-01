"""
========================================================================
First part：From EdgeGPT.py
https://github.com/acheong08/EdgeGPT
========================================================================
"""
from void_terminal.request_llms.edge_gpt_free import Chatbot as NewbingChatbot
load_message = "Waiting for NewBing response。"

"""
========================================================================
Second part：Child process Worker（Call subject）
========================================================================
"""
import time
import json
import re
import logging
import asyncio
import importlib
import threading
from void_terminal.toolbox import update_ui, get_conf, trimmed_format_exc
from multiprocessing import Process, Pipe

def preprocess_newbing_out(s):
    pattern = r'\^(\d+)\^' # Match ^number^
    sub = lambda m: '('+m.group(1)+')' # Replace the matched number as the replacement value
    result = re.sub(pattern, sub, s) # Replacement operation
    if '[1]' in result:
        result += '\n\n```reference\n' + "\n".join([r for r in result.split('\n') if r.startswith('[')]) + '\n```\n'
    return result

def preprocess_newbing_out_simple(result):
    if '[1]' in result:
        result += '\n\n```reference\n' + "\n".join([r for r in result.split('\n') if r.startswith('[')]) + '\n```\n'
    return result

class NewBingHandle(Process):
    def __init__(self):
        super().__init__(daemon=True)
        self.parent, self.child = Pipe()
        self.newbing_model = None
        self.info = ""
        self.success = True
        self.local_history = []
        self.check_dependency()
        self.start()
        self.threadLock = threading.Lock()
        
    def check_dependency(self):
        try:
            self.success = False
            import certifi, httpx, rich
            self.info = "Dependency check passed，Waiting for NewBing response。Note that currently multiple people cannot call the NewBing interface at the same time（There is a thread lock），Otherwise, each person`s NewBing inquiry history will penetrate each other。When calling NewBing，the configured proxy will be automatically used。"
            self.success = True
        except:
            self.info = "Missing dependencies，If you want to use Newbing，In addition to the basic pip dependencies，You also need to run`pip install -r request_llms/requirements_newbing.txt`Install the dependencies for Newbing。"
            self.success = False

    def ready(self):
        return self.newbing_model is not None

    async def async_run(self):
        # Read configuration
        NEWBING_STYLE = get_conf('NEWBING_STYLE')
        from void_terminal.request_llms.bridge_all import model_info
        endpoint = model_info['newbing']['endpoint']
        while True:
            # Waiting
            kwargs = self.child.recv()
            question=kwargs['query']
            history=kwargs['history']
            system_prompt=kwargs['system_prompt']

            # Whether to reset
            if len(self.local_history) > 0 and len(history)==0:
                await self.newbing_model.reset()
                self.local_history = []

            # Start asking questions
            prompt = ""
            if system_prompt not in self.local_history:
                self.local_history.append(system_prompt)
                prompt += system_prompt + '\n'

            # Append history
            for ab in history:
                a, b = ab
                if a not in self.local_history:
                    self.local_history.append(a)
                    prompt += a + '\n'

            # Question
            prompt += question
            self.local_history.append(question)
            print('question:', prompt)
            # Submit
            async for final, response in self.newbing_model.ask_stream(
                prompt=question,
                conversation_style=NEWBING_STYLE,     # ["creative", "balanced", "precise"]
                wss_link=endpoint,                    # "wss://sydney.bing.com/sydney/ChatHub"
            ):
                if not final:
                    print(response)
                    self.child.send(str(response))
                else:
                    print('-------- receive final ---------')
                    self.child.send('[Finish]')
                    # self.local_history.append(response)

    
    def run(self):
        """
        This function runs in a child process
        """
        # First run，Load parameters
        self.success = False
        self.local_history = []
        if (self.newbing_model is None) or (not self.success):
            # Proxy settings
            proxies, NEWBING_COOKIES = get_conf('proxies', 'NEWBING_COOKIES')
            if proxies is None: 
                self.proxies_https = None
            else: 
                self.proxies_https = proxies['https']

            if (NEWBING_COOKIES is not None) and len(NEWBING_COOKIES) > 100:
                try:
                    cookies = json.loads(NEWBING_COOKIES)
                except:
                    self.success = False
                    tb_str = '\n```\n' + trimmed_format_exc() + '\n```\n'
                    self.child.send(f'[Local Message] NEWBING_COOKIES is not filled in or has a format error。')
                    self.child.send('[Fail]'); self.child.send('[Finish]')
                    raise RuntimeError(f"NEWBING_COOKIES is not filled in or has a format error。")
            else:
                cookies = None

            try:
                self.newbing_model = NewbingChatbot(proxy=self.proxies_https, cookies=cookies)
            except:
                self.success = False
                tb_str = '\n```\n' + trimmed_format_exc() + '\n```\n'
                self.child.send(f'[Local Message] Cannot load Newbing components，Please noteNewbing组件已不再维护。{tb_str}')
                self.child.send('[Fail]')
                self.child.send('[Finish]')
                raise RuntimeError(f"Cannot load Newbing components，Please noteNewbing组件已不再维护。")

        self.success = True
        try:
            # Enter task waiting state
            asyncio.run(self.async_run())
        except Exception:
            tb_str = '\n```\n' + trimmed_format_exc() + '\n```\n'
            self.child.send(f'[Local Message] Newbing request failed，Error message as follows. If it is related to network issues，Recommend changing the proxy protocol（Recommend http）Or proxy node {tb_str}.')
            self.child.send('[Fail]')
            self.child.send('[Finish]')
        
    def stream_chat(self, **kwargs):
        """
        This function runs in the main process
        """
        self.threadLock.acquire()   # Acquire thread lock
        self.parent.send(kwargs)    # Requesting subprocess
        while True:
            res = self.parent.recv()                            # Waiting for the fragment of newbing reply
            if res == '[Finish]': break                         # End
            elif res == '[Fail]': self.success = False; break   # Failure
            else: yield res                                     # Fragment of newbing reply
        self.threadLock.release()   # Release thread lock


"""
========================================================================
Part III：The main process calls the function interface uniformly
========================================================================
"""
global newbingfree_handle
newbingfree_handle = None

def predict_no_ui_long_connection(inputs, llm_kwargs, history=[], sys_prompt="", observe_window=[], console_slience=False):
    """
        Multithreading method
        For function details, please see request_llms/bridge_all.py
    """
    global newbingfree_handle
    if (newbingfree_handle is None) or (not newbingfree_handle.success):
        newbingfree_handle = NewBingHandle()
        if len(observe_window) >= 1: observe_window[0] = load_message + "\n\n" + newbingfree_handle.info
        if not newbingfree_handle.success: 
            error = newbingfree_handle.info
            newbingfree_handle = None
            raise RuntimeError(error)

    # No sys_prompt interface，Therefore, add prompt to history
    history_feedin = []
    for i in range(len(history)//2):
        history_feedin.append([history[2*i], history[2*i+1]] )

    watch_dog_patience = 5 # Watchdog (watchdog) Patience, Set 5 seconds
    response = ""
    if len(observe_window) >= 1: observe_window[0] = "[Local Message] Waiting for NewBing response ..."
    for response in newbingfree_handle.stream_chat(query=inputs, history=history_feedin, system_prompt=sys_prompt, max_length=llm_kwargs['max_length'], top_p=llm_kwargs['top_p'], temperature=llm_kwargs['temperature']):
        if len(observe_window) >= 1:  observe_window[0] = preprocess_newbing_out_simple(response)
        if len(observe_window) >= 2:  
            if (time.time()-observe_window[1]) > watch_dog_patience:
                raise RuntimeError("Program terminated。")
    return preprocess_newbing_out_simple(response)

def predict(inputs, llm_kwargs, plugin_kwargs, chatbot, history=[], system_prompt='', stream = True, additional_fn=None):
    """
        Single-threaded method
        For function details, please see request_llms/bridge_all.py
    """
    chatbot.append((inputs, "[Local Message] Waiting for NewBing response ..."))

    global newbingfree_handle
    if (newbingfree_handle is None) or (not newbingfree_handle.success):
        newbingfree_handle = NewBingHandle()
        chatbot[-1] = (inputs, load_message + "\n\n" + newbingfree_handle.info)
        yield from update_ui(chatbot=chatbot, history=[])
        if not newbingfree_handle.success: 
            newbingfree_handle = None
            return

    if additional_fn is not None:
        from void_terminal.core_functional import handle_core_functionality
        inputs, history = handle_core_functionality(additional_fn, inputs, history, chatbot)

    history_feedin = []
    for i in range(len(history)//2):
        history_feedin.append([history[2*i], history[2*i+1]] )

    chatbot[-1] = (inputs, "[Local Message] Waiting for NewBing response ...")
    response = "[Local Message] Waiting for NewBing response ..."
    yield from update_ui(chatbot=chatbot, history=history, msg="NewBing response is slow，Not all responses have been completed yet，Please be patient and submit a new question after completing all responses。")
    for response in newbingfree_handle.stream_chat(query=inputs, history=history_feedin, system_prompt=system_prompt, max_length=llm_kwargs['max_length'], top_p=llm_kwargs['top_p'], temperature=llm_kwargs['temperature']):
        chatbot[-1] = (inputs, preprocess_newbing_out(response))
        yield from update_ui(chatbot=chatbot, history=history, msg="NewBing response is slow，Not all responses have been completed yet，Please be patient and submit a new question after completing all responses。")
    if response == "[Local Message] Waiting for NewBing response ...": response = "[Local Message] NewBing response is abnormal，Please refresh the page and try again ..."
    history.extend([inputs, response])
    logging.info(f'[raw_input] {inputs}')
    logging.info(f'[response] {response}')
    yield from update_ui(chatbot=chatbot, history=history, msg="All responses have been completed，Please submit a new question。")

