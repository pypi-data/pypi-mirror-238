from void_terminal.toolbox import update_ui
from void_terminal.toolbox import CatchException, get_conf, markdown_convertion
from void_terminal.crazy_functions.crazy_utils import input_clipping
from void_terminal.crazy_functions.agent_fns.watchdog import WatchDog
from void_terminal.request_llms.bridge_all import predict_no_ui_long_connection
import threading, time
import numpy as np
from void_terminal.crazy_functions.live_audio.aliyunASR import AliyunASR
import json
import re


def chatbot2history(chatbot):
    history = []
    for c in chatbot:
        for q in c:
            if q in ["[ Please speak ]", "[ Waiting for GPT response ]", "[ Waiting for you to finish the question ]"]:
                continue
            elif q.startswith("[ Waiting for you to finish the question ]"):
                continue
            else:
                history.append(q.strip('<div class="markdown-body">').strip('</div>').strip('<p>').strip('</p>'))
    return history

def visualize_audio(chatbot, audio_shape):
    if len(chatbot) == 0: chatbot.append(["[ Please speak ]", "[ Waiting for you to finish the question ]"])
    chatbot[-1] = list(chatbot[-1])
    p1 = '「'
    p2 = '」'
    chatbot[-1][-1] = re.sub(p1+r'(.*)'+p2, '', chatbot[-1][-1])
    chatbot[-1][-1] += (p1+f"`{audio_shape}`"+p2)

class AsyncGptTask():
    def __init__(self) -> None:
        self.observe_future = []
        self.observe_future_chatbot_index = []

    def gpt_thread_worker(self, i_say, llm_kwargs, history, sys_prompt, observe_window, index):
        try:
            MAX_TOKEN_ALLO = 2560
            i_say, history = input_clipping(i_say, history, max_token_limit=MAX_TOKEN_ALLO)
            gpt_say_partial = predict_no_ui_long_connection(inputs=i_say, llm_kwargs=llm_kwargs, history=history, sys_prompt=sys_prompt, 
                                                            observe_window=observe_window[index], console_slience=True)
        except ConnectionAbortedError as token_exceed_err:
            print('At least one thread task fails due to token overflow', e)
        except Exception as e:
            print('At least one thread task fails unexpectedly', e)

    def add_async_gpt_task(self, i_say, chatbot_index, llm_kwargs, history, system_prompt):
        self.observe_future.append([""])
        self.observe_future_chatbot_index.append(chatbot_index)
        cur_index = len(self.observe_future)-1
        th_new = threading.Thread(target=self.gpt_thread_worker, args=(i_say, llm_kwargs, history, system_prompt, self.observe_future, cur_index))
        th_new.daemon = True
        th_new.start()

    def update_chatbot(self, chatbot):
        for of, ofci in zip(self.observe_future, self.observe_future_chatbot_index):
            try:
                chatbot[ofci] = list(chatbot[ofci])
                chatbot[ofci][1] = markdown_convertion(of[0])
            except:
                self.observe_future = []
                self.observe_future_chatbot_index = []
        return chatbot

class InterviewAssistant(AliyunASR):
    def __init__(self):
        self.capture_interval = 0.5 # second
        self.stop = False
        self.parsed_text = ""   # The part that has already been said in the next sentence, By test_on_result_chg() Write
        self.parsed_sentence = ""   # The whole sentence of a paragraph, By test_on_sentence_end() Write
        self.buffered_sentence = ""    #
        self.audio_shape = ""   # Visual representation of audio, By audio_convertion_thread() Write
        self.event_on_result_chg = threading.Event()
        self.event_on_entence_end = threading.Event()
        self.event_on_commit_question = threading.Event()

    def __del__(self):
        self.stop = True
        self.stop_msg = ""
        self.commit_wd.kill_dog = True
        self.plugin_wd.kill_dog = True

    def init(self, chatbot):
        # Initialize audio capture thread
        self.captured_audio = np.array([])
        self.keep_latest_n_second = 10
        self.commit_after_pause_n_second = 2.0
        self.ready_audio_flagment = None
        self.stop = False
        self.plugin_wd = WatchDog(timeout=5, bark_fn=self.__del__, msg="Program terminated")
        self.aut = threading.Thread(target=self.audio_convertion_thread, args=(chatbot._cookies['uuid'],))
        self.aut.daemon = True
        self.aut.start()
        # th2 = threading.Thread(target=self.audio2txt_thread, args=(chatbot._cookies['uuid'],))
        # th2.daemon = True
        # th2.start()

    def no_audio_for_a_while(self):
        if len(self.buffered_sentence) < 7: # If a sentence is less than 7 words，Do not submit for now
            self.commit_wd.begin_watch()
        else:
            self.event_on_commit_question.set()

    def begin(self, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt):
        # main plugin function
        self.init(chatbot)
        chatbot.append(["[ Please speak ]", "[ Waiting for you to finish the question ]"])
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        self.plugin_wd.begin_watch()
        self.agt = AsyncGptTask()
        self.commit_wd = WatchDog(timeout=self.commit_after_pause_n_second, bark_fn=self.no_audio_for_a_while, interval=0.2)
        self.commit_wd.begin_watch()

        while not self.stop:
            self.event_on_result_chg.wait(timeout=0.25)  # run once every 0.25 second
            chatbot = self.agt.update_chatbot(chatbot)   # Write the GPT result of the sub-thread into the chatbot
            history = chatbot2history(chatbot)
            yield from update_ui(chatbot=chatbot, history=history)      # Refresh the page
            self.plugin_wd.feed()

            if self.event_on_result_chg.is_set(): 
                # called when some words have finished
                self.event_on_result_chg.clear()
                chatbot[-1] = list(chatbot[-1])
                chatbot[-1][0] = self.buffered_sentence + self.parsed_text
                history = chatbot2history(chatbot)
                yield from update_ui(chatbot=chatbot, history=history)  # Refresh the page
                self.commit_wd.feed()

            if self.event_on_entence_end.is_set():
                # called when a sentence has ended
                self.event_on_entence_end.clear()
                self.parsed_text = self.parsed_sentence
                self.buffered_sentence += self.parsed_text
                chatbot[-1] = list(chatbot[-1])
                chatbot[-1][0] = self.buffered_sentence
                history = chatbot2history(chatbot)
                yield from update_ui(chatbot=chatbot, history=history)  # Refresh the page

            if self.event_on_commit_question.is_set():
                # called when a question should be commited
                self.event_on_commit_question.clear()
                if len(self.buffered_sentence) == 0: raise RuntimeError

                self.commit_wd.begin_watch()
                chatbot[-1] = list(chatbot[-1])
                chatbot[-1] = [self.buffered_sentence, "[ Waiting for GPT response ]"]
                yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
                # Add GPT task, create sub-thread to request GPT，Avoid thread blocking
                history = chatbot2history(chatbot)
                self.agt.add_async_gpt_task(self.buffered_sentence, len(chatbot)-1, llm_kwargs, history, system_prompt)
                
                self.buffered_sentence = ""
                chatbot.append(["[ Please speak ]", "[ Waiting for you to finish the question ]"])
                yield from update_ui(chatbot=chatbot, history=history) # Refresh the page

            if not self.event_on_result_chg.is_set() and not self.event_on_entence_end.is_set() and not self.event_on_commit_question.is_set():
                visualize_audio(chatbot, self.audio_shape)
                yield from update_ui(chatbot=chatbot, history=history) # Refresh the page

        if len(self.stop_msg) != 0:
            raise RuntimeError(self.stop_msg)



@CatchException
def VoiceAssistant(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    # pip install -U openai-whisper
    chatbot.append(["Chat assistant function plugin：When using，Take your hands off the mouse and keyboard", "Audio assistant, Listening to you（Click the `Stop` button to terminate the program）..."])
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page

    # Attempt to import dependencies，If dependencies are missing，Give installation suggestions
    try:
        import nls
        from scipy import io
    except:
        chatbot.append(["Failed to import dependencies", "Using this module requires additional dependencies, Installation method:```pip install --upgrade aliyun-python-sdk-core==2.13.3 pyOpenSSL webrtcvad scipy git+https://github.com/aliyun/alibabacloud-nls-python-sdk.git```"])
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return

    APPKEY = get_conf('ALIYUN_APPKEY')
    if APPKEY == "":
        chatbot.append(["Failed to import dependencies", "No Aliyun voice recognition APPKEY and TOKEN, See details at https://help.aliyun.com/document_detail/450255.html"])
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return

    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
    ia = InterviewAssistant()
    yield from ia.begin(llm_kwargs, plugin_kwargs, chatbot, history, system_prompt)

