
from transformers import AutoModel, AutoTokenizer
import time
import threading
import importlib
from void_terminal.toolbox import update_ui, get_conf
from multiprocessing import Process, Pipe

load_message = "jittorllms has not been loaded yet，Loading takes some time。Attention，Please avoid mixing multiple jittor models，Otherwise, it may cause a graphics memory overflow and cause stuttering，Depending on`config.py`Configuration，jittorllms consumes a lot of memory（CPU）Or video memory（GPU），May cause low-end computers to freeze..."

#################################################################################
class GetGLMHandle(Process):
    def __init__(self):
        super().__init__(daemon=True)
        self.parent, self.child = Pipe()
        self.jittorllms_model = None
        self.info = ""
        self.local_history = []
        self.success = True
        self.check_dependency()
        self.start()
        self.threadLock = threading.Lock()
        
    def check_dependency(self):
        try:
            import pandas
            self.info = "Dependency check passed"
            self.success = True
        except:
            from void_terminal.toolbox import trimmed_format_exc
            self.info = r"Missing dependencies for jittorllms，If you want to use jittorllms，In addition to the basic pip dependencies，You also need to run`pip install -r request_llms/requirements_jittorllms.txt -i https://pypi.jittor.org/simple -I`"+\
                        r"and`git clone https://gitlink.org.cn/jittor/JittorLLMs.git --depth 1 request_llms/jittorllms`Two commands to install jittorllms dependencies（Run these two commands in the project root directory）。" +\
                        r"Warning：Installing jittorllms dependencies will completely destroy the existing pytorch environment，It is recommended to use a docker environment!" + trimmed_format_exc()
            self.success = False

    def ready(self):
        return self.jittorllms_model is not None

    def run(self):
        # Subprocess execution
        # First run，Load parameters
        def validate_path():
            import os, sys
            dir_name = os.path.dirname(__file__)
            env = os.environ.get("PATH", "")
            os.environ["PATH"] = env.replace('/cuda/bin', '/x/bin')
            root_dir_assume = os.path.abspath(os.path.dirname(__file__) +  '/..')
            os.chdir(root_dir_assume + '/request_llms/jittorllms')
            sys.path.append(root_dir_assume + '/request_llms/jittorllms')
        validate_path() # validate path so you can run from base directory

        def load_model():
            import types
            try:
                if self.jittorllms_model is None:
                    device = get_conf('LOCAL_MODEL_DEVICE')
                    from void_terminal.request_llms.jittorllms.models import get_model
                    # availabel_models = ["chatglm", "pangualpha", "llama", "chatrwkv"]
                    args_dict = {'model': 'pangualpha'}
                    print('self.jittorllms_model = get_model(types.SimpleNamespace(**args_dict))')
                    self.jittorllms_model = get_model(types.SimpleNamespace(**args_dict))
                    print('done get model')
            except:
                self.child.send('[Local Message] Call jittorllms fail, cannot load jittorllms parameters normally。')
                raise RuntimeError("Cannot load jittorllms parameters normally!")
        print('load_model')
        load_model()

        # Enter task waiting state
        print('Enter task waiting state')
        while True:
            # Enter task waiting state
            kwargs = self.child.recv()
            query = kwargs['query']
            history = kwargs['history']
            # Whether to reset
            if len(self.local_history) > 0 and len(history)==0:
                print('Trigger reset')
                self.jittorllms_model.reset()
            self.local_history.append(query)

            print('Received message，Start requesting')
            try:
                for response in self.jittorllms_model.stream_chat(query, history):
                    print(response)
                    self.child.send(response)
            except:
                from void_terminal.toolbox import trimmed_format_exc
                print(trimmed_format_exc())
                self.child.send('[Local Message] Call jittorllms fail.')
            # Request processing ends，Start the next loop
            self.child.send('[Finish]')

    def stream_chat(self, **kwargs):
        # Main process execution
        self.threadLock.acquire()
        self.parent.send(kwargs)
        while True:
            res = self.parent.recv()
            if res != '[Finish]':
                yield res
            else:
                break
        self.threadLock.release()
    
global pangu_glm_handle
pangu_glm_handle = None
#################################################################################
def predict_no_ui_long_connection(inputs, llm_kwargs, history=[], sys_prompt="", observe_window=[], console_slience=False):
    """
        Multithreading method
        For function details, please see request_llms/bridge_all.py
    """
    global pangu_glm_handle
    if pangu_glm_handle is None:
        pangu_glm_handle = GetGLMHandle()
        if len(observe_window) >= 1: observe_window[0] = load_message + "\n\n" + pangu_glm_handle.info
        if not pangu_glm_handle.success: 
            error = pangu_glm_handle.info
            pangu_glm_handle = None
            raise RuntimeError(error)

    # jittorllms does not have a sys_prompt interface，Therefore, add prompt to history
    history_feedin = []
    for i in range(len(history)//2):
        history_feedin.append([history[2*i], history[2*i+1]] )

    watch_dog_patience = 5 # Watchdog (watchdog) Patience, Set 5 seconds
    response = ""
    for response in pangu_glm_handle.stream_chat(query=inputs, history=history_feedin, system_prompt=sys_prompt, max_length=llm_kwargs['max_length'], top_p=llm_kwargs['top_p'], temperature=llm_kwargs['temperature']):
        print(response)
        if len(observe_window) >= 1:  observe_window[0] = response
        if len(observe_window) >= 2:  
            if (time.time()-observe_window[1]) > watch_dog_patience:
                raise RuntimeError("Program terminated。")
    return response



def predict(inputs, llm_kwargs, plugin_kwargs, chatbot, history=[], system_prompt='', stream = True, additional_fn=None):
    """
        Single-threaded method
        For function details, please see request_llms/bridge_all.py
    """
    chatbot.append((inputs, ""))

    global pangu_glm_handle
    if pangu_glm_handle is None:
        pangu_glm_handle = GetGLMHandle()
        chatbot[-1] = (inputs, load_message + "\n\n" + pangu_glm_handle.info)
        yield from update_ui(chatbot=chatbot, history=[])
        if not pangu_glm_handle.success: 
            pangu_glm_handle = None
            return

    if additional_fn is not None:
        from void_terminal.core_functional import handle_core_functionality
        inputs, history = handle_core_functionality(additional_fn, inputs, history, chatbot)

    # Process historical information
    history_feedin = []
    for i in range(len(history)//2):
        history_feedin.append([history[2*i], history[2*i+1]] )

    # Start receiving jittorllms responses
    response = "[Local Message] Waiting for jittorllms response ..."
    for response in pangu_glm_handle.stream_chat(query=inputs, history=history_feedin, system_prompt=system_prompt, max_length=llm_kwargs['max_length'], top_p=llm_kwargs['top_p'], temperature=llm_kwargs['temperature']):
        chatbot[-1] = (inputs, response)
        yield from update_ui(chatbot=chatbot, history=history)

    # Summary output
    if response == "[Local Message] Waiting for jittorllms response ...":
        response = "[Local Message] Jittor LMS Response Exception ..."
    history.extend([inputs, response])
    yield from update_ui(chatbot=chatbot, history=history)
