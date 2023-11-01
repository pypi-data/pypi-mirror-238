# In this source code, ⭐ = Key step
"""
Test：
    - Crop image，Keep the lower half
    - Swap blue channel and red channel of the image
    - Convert the image to grayscale
    - Convert CSV file to Excel table

Testing: 
    - Crop the image, keeping the bottom half. 
    - Swap the blue channel and red channel of the image. 
    - Convert the image to grayscale. 
    - Convert the CSV file to an Excel spreadsheet.
"""


from void_terminal.toolbox import CatchException, update_ui, gen_time_str, trimmed_format_exc, is_the_upload_folder
from void_terminal.toolbox import promote_file_to_downloadzone, get_log_folder, update_ui_lastest_msg
from void_terminal.crazy_functions.crazy_utils import request_gpt_model_in_new_thread_with_ui_alive, get_plugin_arg
from void_terminal.crazy_functions.crazy_utils import input_clipping, try_install_deps
from void_terminal.crazy_functions.gen_fns.gen_fns_shared import is_function_successfully_generated
from void_terminal.crazy_functions.gen_fns.gen_fns_shared import get_class_name
from void_terminal.crazy_functions.gen_fns.gen_fns_shared import subprocess_worker
from void_terminal.crazy_functions.gen_fns.gen_fns_shared import try_make_module
import os
import time
import glob
import multiprocessing

templete = """
```python
import ...  # Put dependencies here, e.g. import numpy as np. 

class TerminalFunction(object): # Do not change the name of the class, The name of the class must be `TerminalFunction`

    def run(self, path):    # The name of the function must be `run`, it takes only a positional argument.
        # rewrite the function you have just written here 
        ...
        return generated_file_path
```
"""

def inspect_dependency(chatbot, history):
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
    return True

def get_code_block(reply):
    import re
    pattern = r"```([\s\S]*?)```" # regex pattern to match code blocks
    matches = re.findall(pattern, reply) # find all code blocks in text
    if len(matches) == 1: 
        return matches[0].strip('python') #  code block
    for match in matches:
        if 'class TerminalFunction' in match:
            return match.strip('python') #  code block
    raise RuntimeError("GPT is not generating proper code.")

def gpt_interact_multi_step(txt, file_type, llm_kwargs, chatbot, history):
    # Input
    prompt_compose = [
        f'Your job:\n'
        f'1. write a single Python function, which takes a path of a `{file_type}` file as the only argument and returns a `string` containing the result of analysis or the path of generated files. \n',
        f"2. You should write this function to perform following task: " + txt + "\n",
        f"3. Wrap the output python function with markdown codeblock."
    ]
    i_say = "".join(prompt_compose)
    demo = []

    # Step one
    gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
        inputs=i_say, inputs_show_user=i_say, 
        llm_kwargs=llm_kwargs, chatbot=chatbot, history=demo, 
        sys_prompt= r"You are a world-class programmer."
    )
    history.extend([i_say, gpt_say])
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page # UI update

    # Step two
    prompt_compose = [
        "If previous stage is successful, rewrite the function you have just written to satisfy following templete: \n",
        templete
    ]
    i_say = "".join(prompt_compose); inputs_show_user = "If previous stage is successful, rewrite the function you have just written to satisfy executable templete. "
    gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
        inputs=i_say, inputs_show_user=inputs_show_user, 
        llm_kwargs=llm_kwargs, chatbot=chatbot, history=history, 
        sys_prompt= r"You are a programmer. You need to replace `...` with valid packages, do not give `...` in your answer!"
    )
    code_to_return = gpt_say
    history.extend([i_say, gpt_say])
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page # UI update
    
    # # Step three
    # i_say = "Please list to packages to install to run the code above. Then show me how to use `try_install_deps` function to install them."
    # i_say += 'For instance. `try_install_deps(["opencv-python", "scipy", "numpy"])`'
    # installation_advance = yield from request_gpt_model_in_new_thread_with_ui_alive(
    #     inputs=i_say, inputs_show_user=inputs_show_user, 
    #     llm_kwargs=llm_kwargs, chatbot=chatbot, history=history, 
    #     sys_prompt= r"You are a programmer."
    # )

    # # # Step three  
    # i_say = "Show me how to use `pip` to install packages to run the code above. "
    # i_say += 'For instance. `pip install -r opencv-python scipy numpy`'
    # installation_advance = yield from request_gpt_model_in_new_thread_with_ui_alive(
    #     inputs=i_say, inputs_show_user=i_say, 
    #     llm_kwargs=llm_kwargs, chatbot=chatbot, history=history, 
    #     sys_prompt= r"You are a programmer."
    # )
    installation_advance = ""
    
    return code_to_return, installation_advance, txt, file_type, llm_kwargs, chatbot, history




def for_immediate_show_off_when_possible(file_type, fp, chatbot):
    if file_type in ['png', 'jpg']:
        image_path = os.path.abspath(fp)
        chatbot.append(['This is an image, Display as follows:',  
            f'Local file address: <br/>`{image_path}`<br/>'+
            f'Local file preview: <br/><div align="center"><img src="file={image_path}"></div>'
        ])
    return chatbot



def have_any_recent_upload_files(chatbot):
    _5min = 5 * 60
    if not chatbot: return False    # chatbot is None
    most_recent_uploaded = chatbot._cookies.get("most_recent_uploaded", None)
    if not most_recent_uploaded: return False   # most_recent_uploaded is None
    if time.time() - most_recent_uploaded["time"] < _5min: return True # most_recent_uploaded is new
    else: return False  # most_recent_uploaded is too old

def get_recent_file_prompt_support(chatbot):
    most_recent_uploaded = chatbot._cookies.get("most_recent_uploaded", None)
    path = most_recent_uploaded['path']
    return path

@CatchException
def DynamicFunctionGeneration(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    """
    txt             Text entered by the user in the input field，For example, a paragraph that needs to be translated，For example, a file path that contains files to be processed
    llm_kwargs      GPT model parameters，Such as temperature and top_p，Generally pass it on as is
    plugin_kwargs   Plugin model parameters，No use for the time being
    chatbot         Chat display box handle，Displayed to the user
    history         Chat history，Context summary
    system_prompt   Silent reminder to GPT
    web_port        Current software running port number
    """

    # Clear history
    history = []

    # Basic information：Function, contributor
    chatbot.append(["Starting: Dynamic generation of plugins", "Dynamic generation of plugins, Execution starts, Author Binary-Husky."])
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page

    # ⭐ Is there anything in the file upload area
    # 1. If there is a file: As a function parameter
    # 2. If there is no file：Need to extract parameters using GPT （Too lazy，Write it later，VoidTerminal has already implemented similar code）
    file_list = []
    if get_plugin_arg(plugin_kwargs, key="file_path_arg", default=False):
        file_path = get_plugin_arg(plugin_kwargs, key="file_path_arg", default=None)
        file_list.append(file_path)
        yield from update_ui_lastest_msg(f"Current file: {file_path}", chatbot, history, 1)
    elif have_any_recent_upload_files(chatbot):
        file_dir = get_recent_file_prompt_support(chatbot)
        file_list = glob.glob(os.path.join(file_dir, '**/*'), recursive=True)
        yield from update_ui_lastest_msg(f"Current file processing list: {file_list}", chatbot, history, 1)
    else:
        chatbot.append(["File retrieval", "No recent uploaded files found。"])
        yield from update_ui_lastest_msg("No recent uploaded files found。", chatbot, history, 1)
        return  # 2. If there is no file
    if len(file_list) == 0:
        chatbot.append(["File retrieval", "No recent uploaded files found。"])
        yield from update_ui_lastest_msg("No recent uploaded files found。", chatbot, history, 1)
        return  # 2. If there is no file
    
    # Read the file
    file_type = file_list[0].split('.')[-1]

    # Careful check
    if is_the_upload_folder(txt):
        yield from update_ui_lastest_msg(f"Please fill in the requirements in the input box, Then click the plugin again! As for your file，don`t worry, File path {txt} Already memorized. ", chatbot, history, 1)
        return
    
    # Start doing real work
    MAX_TRY = 3
    for j in range(MAX_TRY):  # Retry up to 5 times
        traceback = ""
        try:
            # ⭐ Let`s start!
            code, installation_advance, txt, file_type, llm_kwargs, chatbot, history = \
                yield from gpt_interact_multi_step(txt, file_type, llm_kwargs, chatbot, history)
            chatbot.append(["Code generation phase completed", ""])
            yield from update_ui_lastest_msg(f"Validating the above code ...", chatbot, history, 1)
            # ⭐ Separating code blocks
            code = get_code_block(code)
            # ⭐ Check module
            ok, traceback = try_make_module(code, chatbot)
            # Code generation is done
            if ok: break
        except Exception as e:
            if not traceback: traceback = trimmed_format_exc()
        # Handle exception
        if not traceback: traceback = trimmed_format_exc()
        yield from update_ui_lastest_msg(f"The {j+1}/{MAX_TRY} Attempt to generate code, Failed~ Don`t worry, Let`s try again in 5 seconds... \n\nThis time our error tracking is\n```\n{traceback}\n```\n", chatbot, history, 5)

    # Code generation ends, Start executing
    TIME_LIMIT = 15
    yield from update_ui_lastest_msg(f"Start creating a new process and executing the code! Time limit {TIME_LIMIT} Wait for the task to complete... ", chatbot, history, 1)
    manager = multiprocessing.Manager()
    return_dict = manager.dict()

    # ⭐ Reached the final step，Start processing files one by one
    for file_path in file_list:
        if os.path.exists(file_path):
            chatbot.append([f"Processing file: {file_path}", f"Please wait..."])
            chatbot = for_immediate_show_off_when_possible(file_type, file_path, chatbot)
            yield from update_ui(chatbot=chatbot, history=history) # Refresh the page # UI update
        else:
            continue

        # ⭐⭐⭐ subprocess_worker ⭐⭐⭐
        p = multiprocessing.Process(target=subprocess_worker, args=(code, file_path, return_dict))
        # ⭐ Start execution，Time limit TIME_LIMIT
        p.start(); p.join(timeout=TIME_LIMIT)
        if p.is_alive(): p.terminate(); p.join()
        p.close()
        res = return_dict['result']
        success = return_dict['success']
        traceback = return_dict['traceback']
        if not success:
            if not traceback: traceback = trimmed_format_exc()
            chatbot.append(["Execution failed", f"Error tracking\n```\n{trimmed_format_exc()}\n```\n"])
            # chatbot.append(["If it is缺乏依赖，请参考以下Suggestion", installation_advance])
            yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
            return
        
        # Completed smoothly，Wrap up
        res = str(res)
        if os.path.exists(res):
            chatbot.append(["Execution succeeded，The result is a valid file", "Result：" + res])
            new_file_path = promote_file_to_downloadzone(res, chatbot=chatbot)
            chatbot = for_immediate_show_off_when_possible(file_type, new_file_path, chatbot)
            yield from update_ui(chatbot=chatbot, history=history) # Refresh the page # UI update
        else:
            chatbot.append(["Execution succeeded，The result is a string", "Result：" + res])
            yield from update_ui(chatbot=chatbot, history=history) # Refresh the page # UI update   

