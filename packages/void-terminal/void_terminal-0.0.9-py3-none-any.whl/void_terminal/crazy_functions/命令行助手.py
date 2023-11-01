from void_terminal.toolbox import CatchException, update_ui, gen_time_str
from void_terminal.crazy_functions.crazy_utils import request_gpt_model_in_new_thread_with_ui_alive
from void_terminal.crazy_functions.crazy_utils import input_clipping
import copy, json

@CatchException
def 命令line助手(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    """
    txt             Text entered by the user in the input field, For example, a paragraph that needs to be translated, For example, a file path that contains files to be processed
    llm_kwargs      GPT model parameters, Such as temperature and top_p, Generally pass it on as is
    plugin_kwargs   Plugin model parameters, No use for the time being
    chatbot         Chat display box handle, Displayed to the user
    history         Chat history, Context summary
    system_prompt   Silent reminder to GPT
    web_port        Current software running port number
    """
    # Clear history, To avoid input overflow
    history = []

    # Input
    i_say = "Please write a bash command to implement the following function：" + txt
    # Start
    gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
        inputs=i_say, inputs_show_user=txt, 
        llm_kwargs=llm_kwargs, chatbot=chatbot, history=[], 
        sys_prompt="You are a Linux master-level user。Attention，When I ask you to write a bash command，Try to solve my request using only one command。"
    )
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page # UI update



