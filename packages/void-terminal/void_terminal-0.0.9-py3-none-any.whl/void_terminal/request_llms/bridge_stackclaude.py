from void_terminal.request_llms.bridge_newbingfree import preprocess_newbing_out, preprocess_newbing_out_simple
from multiprocessing import Process, Pipe
from void_terminal.toolbox import update_ui, get_conf, trimmed_format_exc
import threading
import importlib
import logging
import time
from void_terminal.toolbox import get_conf
import asyncio
load_message = "Loading Claude component，Please wait..."

try:
    """
    ========================================================================
    First part：Slack API Client
    https://github.com/yokonsan/claude-in-slack-api
    ========================================================================
    """

    from slack_sdk.errors import SlackApiError
    from slack_sdk.web.async_client import AsyncWebClient

    class SlackClient(AsyncWebClient):
        """The SlackClient class is used to interact with the Slack API，Implement message sending, receiving and other functions。

            Attribute：
            - CHANNEL_ID：str type，Representing channel ID。

            Method：
            - open_channel()：Asynchronous method。Open a channel by calling the conversations_open method，And save the returned channel ID in the property CHANNEL_ID。
            - chat(text: str)：Asynchronous method。Send a text message to the opened channel。
            - get_slack_messages()：Asynchronous method。Get the latest messages from the opened channel and return a list of messages，Historical message queries are currently not supported。
            - get_reply()：Asynchronous method。Loop to listen to messages in an open channel，如果Received"Typing…_"结尾的消息Say明Claude还在继续Output，Otherwise end the loop。

        """
        CHANNEL_ID = None

        async def open_channel(self):
            response = await self.conversations_open(users=get_conf('SLACK_CLAUDE_BOT_ID'))
            self.CHANNEL_ID = response["channel"]["id"]

        async def chat(self, text):
            if not self.CHANNEL_ID:
                raise Exception("Channel not found.")

            resp = await self.chat_postMessage(channel=self.CHANNEL_ID, text=text)
            self.LAST_TS = resp["ts"]

        async def get_slack_messages(self):
            try:
                # TODO：Historical messages are not supported temporarily，Because there is a problem of historical message penetration when multiple people use it in the same channel
                resp = await self.conversations_history(channel=self.CHANNEL_ID, oldest=self.LAST_TS, limit=1)
                msg = [msg for msg in resp["messages"]
                    if msg.get("user") == get_conf('SLACK_CLAUDE_BOT_ID')]
                return msg
            except (SlackApiError, KeyError) as e:
                raise RuntimeError(f"Failed to get Slack message。")
        
        async def get_reply(self):
            while True:
                slack_msgs = await self.get_slack_messages()
                if len(slack_msgs) == 0:
                    await asyncio.sleep(0.5)
                    continue
                
                msg = slack_msgs[-1]
                if msg["text"].endswith("Typing…_"):
                    yield False, msg["text"]
                else:
                    yield True, msg["text"]
                    break
except:
    pass

"""
========================================================================
Second part：Child process Worker（Call subject）
========================================================================
"""


class ClaudeHandle(Process):
    def __init__(self):
        super().__init__(daemon=True)
        self.parent, self.child = Pipe()
        self.claude_model = None
        self.info = ""
        self.success = True
        self.local_history = []
        self.check_dependency()
        if self.success: 
            self.start()
            self.threadLock = threading.Lock()

    def check_dependency(self):
        try:
            self.success = False
            import slack_sdk
            self.info = "Dependency check passed，Waiting for Claude`s response。Note that multiple people cannot currently call the Claude interface at the same time（There is a thread lock），Otherwise, everyone`s Claude inquiry history will be mutually infiltrated。When calling Claude，the configured proxy will be automatically used。"
            self.success = True
        except:
            self.info = "Missing dependencies，If you want to use Claude，In addition to the basic pip dependencies，You also need to run`pip install -r request_llms/requirements_slackclaude.txt`Install Claude`s dependencies，Then restart the program。"
            self.success = False

    def ready(self):
        return self.claude_model is not None    
    
    async def async_run(self):
        await self.claude_model.open_channel()
        while True:
            # Waiting
            kwargs = self.child.recv()
            question = kwargs['query']
            history = kwargs['history']

            # Start asking questions
            prompt = ""

            # Question
            prompt += question
            print('question:', prompt)

            # Submit
            await self.claude_model.chat(prompt)
            
            # Get reply
            async for final, response in self.claude_model.get_reply():                
                if not final:
                    print(response)
                    self.child.send(str(response))
                else:
                    # Prevent the last message from being lost
                    slack_msgs = await self.claude_model.get_slack_messages()
                    last_msg = slack_msgs[-1]["text"] if slack_msgs and len(slack_msgs) > 0 else ""
                    if last_msg:
                        self.child.send(last_msg)
                    print('-------- receive final ---------')
                    self.child.send('[Finish]')
                    
    def run(self):
        """
        This function runs in a child process
        """
        # First run，Load parameters
        self.success = False
        self.local_history = []
        if (self.claude_model is None) or (not self.success):
            # Proxy settings
            proxies = get_conf('proxies')
            if proxies is None:
                self.proxies_https = None
            else:
                self.proxies_https = proxies['https']

            try:
                SLACK_CLAUDE_USER_TOKEN = get_conf('SLACK_CLAUDE_USER_TOKEN')
                self.claude_model = SlackClient(token=SLACK_CLAUDE_USER_TOKEN, proxy=self.proxies_https)
                print('Claude component initialized successfully。')
            except:
                self.success = False
                tb_str = '\n```\n' + trimmed_format_exc() + '\n```\n'
                self.child.send(f'[Local Message] Cannot load Claude component。{tb_str}')
                self.child.send('[Fail]')
                self.child.send('[Finish]')
                raise RuntimeError(f"Cannot load Claude component。")

        self.success = True
        try:
            # Enter task waiting state
            asyncio.run(self.async_run())
        except Exception:
            tb_str = '\n```\n' + trimmed_format_exc() + '\n```\n'
            self.child.send(f'[Local Message] Claude failed {tb_str}.')
            self.child.send('[Fail]')
            self.child.send('[Finish]')

    def stream_chat(self, **kwargs):
        """
        This function runs in the main process
        """
        self.threadLock.acquire()
        self.parent.send(kwargs)    # Send request to child process
        while True:
            res = self.parent.recv()    # Wait for the segment replied by Claude
            if res == '[Finish]':
                break       # End
            elif res == '[Fail]':
                self.success = False
                break
            else:
                yield res   # Fragment replied by Claude
        self.threadLock.release()


"""
========================================================================
Part III：The main process calls the function interface uniformly
========================================================================
"""
global claude_handle
claude_handle = None


def predict_no_ui_long_connection(inputs, llm_kwargs, history=[], sys_prompt="", observe_window=None, console_slience=False):
    """
        Multithreading method
        For function details, please see request_llms/bridge_all.py
    """
    global claude_handle
    if (claude_handle is None) or (not claude_handle.success):
        claude_handle = ClaudeHandle()
        observe_window[0] = load_message + "\n\n" + claude_handle.info
        if not claude_handle.success:
            error = claude_handle.info
            claude_handle = None
            raise RuntimeError(error)

    # No sys_prompt interface，Therefore, add prompt to history
    history_feedin = []
    for i in range(len(history)//2):
        history_feedin.append([history[2*i], history[2*i+1]])

    watch_dog_patience = 5  # Watchdog (watchdog) Patience, Set 5 seconds
    response = ""
    observe_window[0] = "[Local Message] Waiting for Claude`s response ..."
    for response in claude_handle.stream_chat(query=inputs, history=history_feedin, system_prompt=sys_prompt, max_length=llm_kwargs['max_length'], top_p=llm_kwargs['top_p'], temperature=llm_kwargs['temperature']):
        observe_window[0] = preprocess_newbing_out_simple(response)
        if len(observe_window) >= 2:
            if (time.time()-observe_window[1]) > watch_dog_patience:
                raise RuntimeError("Program terminated。")
    return preprocess_newbing_out_simple(response)


def predict(inputs, llm_kwargs, plugin_kwargs, chatbot, history=[], system_prompt='', stream=True, additional_fn=None):
    """
        Single-threaded method
        For function details, please see request_llms/bridge_all.py
    """
    chatbot.append((inputs, "[Local Message] Waiting for Claude`s response ..."))

    global claude_handle
    if (claude_handle is None) or (not claude_handle.success):
        claude_handle = ClaudeHandle()
        chatbot[-1] = (inputs, load_message + "\n\n" + claude_handle.info)
        yield from update_ui(chatbot=chatbot, history=[])
        if not claude_handle.success:
            claude_handle = None
            return

    if additional_fn is not None:
        from void_terminal.core_functional import handle_core_functionality
        inputs, history = handle_core_functionality(additional_fn, inputs, history, chatbot)

    history_feedin = []
    for i in range(len(history)//2):
        history_feedin.append([history[2*i], history[2*i+1]])

    chatbot[-1] = (inputs, "[Local Message] Waiting for Claude`s response ...")
    response = "[Local Message] Waiting for Claude`s response ..."
    yield from update_ui(chatbot=chatbot, history=history, msg="Claude responds slowly，Not all responses have been completed yet，Please be patient and submit a new question after completing all responses。")
    for response in claude_handle.stream_chat(query=inputs, history=history_feedin, system_prompt=system_prompt):
        chatbot[-1] = (inputs, preprocess_newbing_out(response))
        yield from update_ui(chatbot=chatbot, history=history, msg="Claude responds slowly，Not all responses have been completed yet，Please be patient and submit a new question after completing all responses。")
    if response == "[Local Message] Waiting for Claude`s response ...":
        response = "[Local Message] Claude responds abnormally，Please refresh the page and try again ..."
    history.extend([inputs, response])
    logging.info(f'[raw_input] {inputs}')
    logging.info(f'[response] {response}')
    yield from update_ui(chatbot=chatbot, history=history, msg="All responses have been completed，Please submit a new question。")
