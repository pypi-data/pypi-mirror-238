from pydantic import BaseModel, Field
from typing import List
from void_terminal.toolbox import update_ui_lastest_msg, get_conf
from void_terminal.request_llms.bridge_all import predict_no_ui_long_connection
from void_terminal.crazy_functions.json_fns.pydantic_io import GptJsonIO
import copy, json, pickle, os, sys


def modify_configuration_hot(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_intention):
    ALLOW_RESET_CONFIG = get_conf('ALLOW_RESET_CONFIG')
    if not ALLOW_RESET_CONFIG:
        yield from update_ui_lastest_msg(
            lastmsg=f"The current configuration does not allow modification! To activate this feature，Please set ALLOW_RESET_CONFIG=True in config.py and restart the software。", 
            chatbot=chatbot, history=history, delay=2
        )
        return

    # ⭐ ⭐ ⭐ Read configurable project entries
    names = {}
    from enum import Enum
    import config
    for k, v in config.__dict__.items():
        if k.startswith('__'): continue
        names.update({k:k})
        # if len(names) > 20: break   # Limit up to 10 configuration items，If there are too many, it will cause GPT to be unable to understand

    ConfigOptions = Enum('ConfigOptions', names)
    class ModifyConfigurationIntention(BaseModel):
        which_config_to_modify: ConfigOptions = Field(description="the name of the configuration to modify, you must choose from one of the ConfigOptions enum.", default=None)
        new_option_value: str = Field(description="the new value of the option", default=None)

    # ⭐ ⭐ ⭐ Analyze user intent
    yield from update_ui_lastest_msg(lastmsg=f"Executing task: {txt}\n\nReading new configuration", chatbot=chatbot, history=history, delay=0)
    gpt_json_io = GptJsonIO(ModifyConfigurationIntention)
    inputs = "Analyze how to change configuration according to following user input, answer me with json: \n\n" + \
             ">> " + txt.rstrip('\n').replace('\n','\n>> ') + '\n\n' + \
             gpt_json_io.format_instructions
    
    run_gpt_fn = lambda inputs, sys_prompt: predict_no_ui_long_connection(
        inputs=inputs, llm_kwargs=llm_kwargs, history=[], sys_prompt=sys_prompt, observe_window=[])
    user_intention = gpt_json_io.generate_output_auto_repair(run_gpt_fn(inputs, ""), run_gpt_fn)

    explicit_conf = user_intention.which_config_to_modify.value

    ok = (explicit_conf in txt)
    if ok:
        yield from update_ui_lastest_msg(
            lastmsg=f"Executing task: {txt}\n\nNew configuration{explicit_conf}={user_intention.new_option_value}", 
            chatbot=chatbot, history=history, delay=1
        )
        yield from update_ui_lastest_msg(
            lastmsg=f"Executing task: {txt}\n\nNew configuration{explicit_conf}={user_intention.new_option_value}\n\nModifying configuration", 
            chatbot=chatbot, history=history, delay=2
        )

        # ⭐ ⭐ ⭐ Apply configuration immediately
        from void_terminal.toolbox import set_conf
        set_conf(explicit_conf, user_intention.new_option_value)

        yield from update_ui_lastest_msg(
            lastmsg=f"Executing task: {txt}\n\nConfiguration modification completed，Refresh the page to take effect。", chatbot=chatbot, history=history, delay=1
        )
    else:
        yield from update_ui_lastest_msg(
            lastmsg=f"Failure，If configuration is needed{explicit_conf}，You need to specify and mention it in the command。", chatbot=chatbot, history=history, delay=5
        )

def modify_configuration_reboot(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_intention):
    ALLOW_RESET_CONFIG = get_conf('ALLOW_RESET_CONFIG')
    if not ALLOW_RESET_CONFIG:
        yield from update_ui_lastest_msg(
            lastmsg=f"The current configuration does not allow modification! To activate this feature，Please set ALLOW_RESET_CONFIG=True in config.py and restart the software。", 
            chatbot=chatbot, history=history, delay=2
        )
        return

    yield from modify_configuration_hot(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_intention)
    yield from update_ui_lastest_msg(
        lastmsg=f"Executing task: {txt}\n\nConfiguration modification completed，Restarting in five seconds! Please ignore if there is an error。", chatbot=chatbot, history=history, delay=5
    )
    os.execl(sys.executable, sys.executable, *sys.argv)
