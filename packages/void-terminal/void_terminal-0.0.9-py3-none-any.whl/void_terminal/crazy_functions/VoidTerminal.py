"""
Explanation of the Void Terminal Plugin:

Please describe in natural language what you want to do.

1. You can open the plugin's dropdown menu to explore various capabilities of this project, and then describe your needs in natural language, for example:
- "Please call the plugin to translate a PDF paper for me. I just uploaded the paper to the upload area."
- "Please use the plugin to translate a PDF paper, with the address being https://www.nature.com/articles/s41586-019-1724-z.pdf."
- "Generate an image with blooming flowers and lush green grass using the plugin."
- "Translate the README using the plugin. The GitHub URL is https://github.com/facebookresearch/co-tracker."
- "Translate an Arxiv paper for me. The Arxiv ID is 1812.10695. Remember to use the plugin and don't do it manually!"
- "I don't like the current interface color. Modify the configuration and change the theme to THEME="High-Contrast"."
- "Could you please explain the structure of the Transformer network?"

2. If you use keywords like "call the plugin xxx", "modify the configuration xxx", "please", etc., your intention can be recognized more accurately.

3. Your intention can be recognized more accurately when using powerful models like GPT4. This plugin is relatively new, so please feel free to provide feedback on GitHub.

4. Now, if you need to process a file, please upload the file (drag the file to the file upload area) or describe the path to the file.

5. If you don't need to upload a file, you can simply repeat your command again.
"""
explain_msg = """
## VoidTerminal plugin description:

1. Please describe what you need to do in **natural language**。For example：
    - Please call the plugin，Translate PDF papers for me，I just put the paper in the upload area
    - Please call the plugin to translate the PDF paper，The address is https://openreview.net/pdf?id=rJl0r3R9KX」
    - Translate Arxiv papers into Chinese PDF，The ID of the arxiv paper is 1812.10695，Remember to use the plugin!
    - Generate an image，Flowers blooming in the picture，Green grass，Implemented with a plugin
    - Translate README with plugins，The Github URL is https://github.com/facebookresearch/co-tracker」
    - I don`t like the current interface color，Modify configuration，把主题THEME更换为THEME="High-Contrast"」
    - Please call the plugin，Parsing Python source code project，I just packed the code and dragged it to the upload area
    - What is the structure of the Transformer network?？」

2. You can open the plugin dropdown menu to learn about various capabilities of this project。    

3. If you use keywords such as `call plugin xxx`, `modify configuration xxx`, `please`, etc.，Your intent can be recognized more accurately。

4. It is recommended to use GPT3.5 or a stronger model，Weak model may not understand your ideas。This plugin has not been around for long，Welcome to go to Github to provide feedback。

5. Now，If file processing is required，Please upload the file（Drag and drop the file to the file upload area），Or the path of the description file。

6. If file upload is not needed，Now you just need to repeat your command again。
"""

from pydantic import BaseModel, Field
from typing import List
from void_terminal.toolbox import CatchException, update_ui, is_the_upload_folder
from void_terminal.toolbox import update_ui_lastest_msg, disable_auto_promotion
from void_terminal.request_llms.bridge_all import predict_no_ui_long_connection
from void_terminal.crazy_functions.crazy_utils import request_gpt_model_in_new_thread_with_ui_alive
from void_terminal.crazy_functions.crazy_utils import input_clipping
from void_terminal.crazy_functions.json_fns.pydantic_io import GptJsonIO, JsonStringError
from void_terminal.crazy_functions.vt_fns.vt_state import VoidTerminalState
from void_terminal.crazy_functions.vt_fns.vt_modify_config import modify_configuration_hot
from void_terminal.crazy_functions.vt_fns.vt_modify_config import modify_configuration_reboot
from void_terminal.crazy_functions.vt_fns.vt_call_plugin import execute_plugin

class UserIntention(BaseModel):
    user_prompt: str = Field(description="the content of user input", default="")
    intention_type: str = Field(description="the type of user intention, choose from ['ModifyConfiguration', 'ExecutePlugin', 'Chat']", default="ExecutePlugin")
    user_provide_file: bool = Field(description="whether the user provides a path to a file", default=False)
    user_provide_url: bool = Field(description="whether the user provides a url", default=False)


def chat(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_intention):
    gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
        inputs=txt, inputs_show_user=txt,
        llm_kwargs=llm_kwargs, chatbot=chatbot, history=[], 
        sys_prompt=system_prompt
    )
    chatbot[-1] = [txt, gpt_say]
    history.extend([txt, gpt_say])
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
    pass


explain_intention_to_user = {
    'Chat': "Chat conversation",
    'ExecutePlugin': "Invoke plugin",
    'ModifyConfiguration': "Modify configuration",
}


def analyze_intention_with_simple_rules(txt):
    user_intention = UserIntention()
    user_intention.user_prompt = txt
    is_certain = False

    if 'May I ask' in txt:
        is_certain = True
        user_intention.intention_type = 'Chat'

    if 'Use Plugin' in txt:
        is_certain = True
        user_intention.intention_type = 'ExecutePlugin'

    if 'Modify configuration' in txt:
        is_certain = True
        user_intention.intention_type = 'ModifyConfiguration'

    return is_certain, user_intention


@CatchException
def VoidTerminal(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    disable_auto_promotion(chatbot=chatbot)
    # Get the current VoidTerminal status
    state = VoidTerminalState.get_state(chatbot)
    appendix_msg = ""

    # Detect user intention with simple keywords
    is_certain, _ = analyze_intention_with_simple_rules(txt)
    if is_the_upload_folder(txt):
        state.set_state(chatbot=chatbot, key='has_provided_explaination', value=False)
        appendix_msg = "\n\n**Very good，You have uploaded the file **，Now please describe your requirements。"
        
    if is_certain or (state.has_provided_explaination):
        # If the intention is clear，Skip prompt section
        state.set_state(chatbot=chatbot, key='has_provided_explaination', value=True)
        state.unlock_plugin(chatbot=chatbot)
        yield from update_ui(chatbot=chatbot, history=history)
        yield from VoidTerminalMainRoute(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port)
        return
    else:
        # If the intent is ambiguous，prompt
        state.set_state(chatbot=chatbot, key='has_provided_explaination', value=True)
        state.lock_plugin(chatbot=chatbot)
        chatbot.append(("VoidTerminal status:", explain_msg+appendix_msg))
        yield from update_ui(chatbot=chatbot, history=history)
        return



def VoidTerminalMainRoute(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    history = []
    chatbot.append(("VoidTerminal status: ", f"Executing task: {txt}"))
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page

    # ⭐ ⭐ ⭐ Analyze user intent
    is_certain, user_intention = analyze_intention_with_simple_rules(txt)
    if not is_certain:
        yield from update_ui_lastest_msg(
            lastmsg=f"Executing task: {txt}\n\nAnalyzing user intent", chatbot=chatbot, history=history, delay=0)
        gpt_json_io = GptJsonIO(UserIntention)
        rf_req = "\nchoose from ['ModifyConfiguration', 'ExecutePlugin', 'Chat']"
        inputs = "Analyze the intention of the user according to following user input: \n\n" + \
            ">> " + (txt+rf_req).rstrip('\n').replace('\n','\n>> ') + '\n\n' + gpt_json_io.format_instructions
        run_gpt_fn = lambda inputs, sys_prompt: predict_no_ui_long_connection(
            inputs=inputs, llm_kwargs=llm_kwargs, history=[], sys_prompt=sys_prompt, observe_window=[])
        analyze_res = run_gpt_fn(inputs, "")
        try:
            user_intention = gpt_json_io.generate_output_auto_repair(analyze_res, run_gpt_fn)
            lastmsg=f"Executing task: {txt}\n\nUser intent understanding: Intent ={explain_intention_to_user[user_intention.intention_type]}", 
        except JsonStringError as e:
            yield from update_ui_lastest_msg(
                lastmsg=f"Executing task: {txt}\n\nUser intent understanding: Failed current language model（{llm_kwargs['llm_model']}）Cannot understand your intention", chatbot=chatbot, history=history, delay=0)
            return
    else:
        pass

    yield from update_ui_lastest_msg(
        lastmsg=f"Executing task: {txt}\n\nUser intent understanding: Intent ={explain_intention_to_user[user_intention.intention_type]}", 
        chatbot=chatbot, history=history, delay=0)

    # User intent: Modify the configuration of this project
    if user_intention.intention_type == 'ModifyConfiguration':
        yield from modify_configuration_reboot(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_intention)

    # User intent: Scheduling plugin
    if user_intention.intention_type == 'ExecutePlugin':
        yield from execute_plugin(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_intention)

    # User intent: Chat
    if user_intention.intention_type == 'Chat':
        yield from chat(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_intention)

    return

