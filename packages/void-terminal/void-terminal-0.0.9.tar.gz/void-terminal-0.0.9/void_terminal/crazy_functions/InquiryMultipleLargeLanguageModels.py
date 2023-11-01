from void_terminal.toolbox import CatchException, update_ui
from void_terminal.crazy_functions.crazy_utils import request_gpt_model_in_new_thread_with_ui_alive
import datetime
@CatchException
def SimultaneousInquiry(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    """
    txt             Text entered by the user in the input field，For example, a paragraph that needs to be translated，For example, a file path that contains files to be processed
    llm_kwargs      GPT model parameters，Such as temperature and top_p，Generally pass it on as is
    plugin_kwargs   Plugin model parameters，Various parameters used to flexibly adjust complex functions
    chatbot         Chat display box handle，Displayed to the user
    history         Chat history，Context summary
    system_prompt   Silent reminder to GPT
    web_port        Current software running port number
    """
    history = []    # Clear history，To avoid input overflow
    chatbot.append((txt, "Consulting ChatGPT and ChatGLM simultaneously..."))
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page # As requesting GPT takes some time，Let`s do a UI update in time

    # llm_kwargs['llm_model'] = 'chatglm&gpt-3.5-turbo&api2d-gpt-3.5-turbo' # Support any number of llm interfaces，Separate with & symbol
    llm_kwargs['llm_model'] = 'chatglm&gpt-3.5-turbo' # Support any number of llm interfaces，Separate with & symbol
    gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
        inputs=txt, inputs_show_user=txt, 
        llm_kwargs=llm_kwargs, chatbot=chatbot, history=history, 
        sys_prompt=system_prompt,
        retry_times_at_unknown_error=0
    )

    history.append(txt)
    history.append(gpt_say)
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page # UI update


@CatchException
def InquireSimultaneously_SpecifiedModel(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    """
    txt             Text entered by the user in the input field，For example, a paragraph that needs to be translated，For example, a file path that contains files to be processed
    llm_kwargs      GPT model parameters，Such as temperature and top_p，Generally pass it on as is
    plugin_kwargs   Plugin model parameters，Various parameters used to flexibly adjust complex functions
    chatbot         Chat display box handle，Displayed to the user
    history         Chat history，Context summary
    system_prompt   Silent reminder to GPT
    web_port        Current software running port number
    """
    history = []    # Clear history，To avoid input overflow

    if ("advanced_arg" in plugin_kwargs) and (plugin_kwargs["advanced_arg"] == ""): plugin_kwargs.pop("advanced_arg")
    # llm_kwargs['llm_model'] = 'chatglm&gpt-3.5-turbo&api2d-gpt-3.5-turbo' # Support any number of llm interfaces，Separate with & symbol
    llm_kwargs['llm_model'] = plugin_kwargs.get("advanced_arg", 'chatglm&gpt-3.5-turbo') # 'chatglm&gpt-3.5-turbo' # Support any number of llm interfaces，Separate with & symbol

    chatbot.append((txt, f"Consulting simultaneously{llm_kwargs['llm_model']}"))
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page # As requesting GPT takes some time，Let`s do a UI update in time

    gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
        inputs=txt, inputs_show_user=txt, 
        llm_kwargs=llm_kwargs, chatbot=chatbot, history=history, 
        sys_prompt=system_prompt,
        retry_times_at_unknown_error=0
    )

    history.append(txt)
    history.append(gpt_say)
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page # UI update