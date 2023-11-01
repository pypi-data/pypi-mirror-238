from void_terminal.toolbox import CatchException, update_ui, promote_file_to_downloadzone, get_log_folder
from void_terminal.crazy_functions.crazy_utils import request_gpt_model_in_new_thread_with_ui_alive
import re

def write_chat_to_file(chatbot, history=None, file_name=None):
    """
    Write the conversation record history to a file in Markdown format。If no file name is specified，Generate a file name using the current time。
    """
    import os
    import time
    if file_name is None:
        file_name = 'ChatGPT conversation history' + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + '.html'
    fp = os.path.join(get_log_folder(), file_name)
    with open(fp, 'w', encoding='utf8') as f:
        from void_terminal.themes.theme import advanced_css
        f.write(f'<!DOCTYPE html><head><meta charset="utf-8"><title>Conversation history</title><style>{advanced_css}</style></head>')
        for i, contents in enumerate(chatbot):
            for j, content in enumerate(contents):
                try:    # The trigger condition for this bug has not been found，Temporarily handle it this way
                    if type(content) != str: content = str(content)
                except:
                    continue
                f.write(content)
                if j == 0:
                    f.write('<hr style="border-top: dotted 3px #ccc;">')
            f.write('<hr color="red"> \n\n')
        f.write('<hr color="blue"> \n\n raw chat context:\n')
        f.write('<code>')
        for h in history:
            f.write("\n>>>" + h)
        f.write('</code>')
    promote_file_to_downloadzone(fp, rename_file=file_name, chatbot=chatbot)
    return 'Conversation history written：' + fp

def gen_file_preview(file_name):
    try:
        with open(file_name, 'r', encoding='utf8') as f:
            file_content = f.read()
        # pattern to match the text between <head> and </head>
        pattern = re.compile(r'<head>.*?</head>', flags=re.DOTALL)
        file_content = re.sub(pattern, '', file_content)
        html, history = file_content.split('<hr color="blue"> \n\n raw chat context:\n')
        history = history.strip('<code>')
        history = history.strip('</code>')
        history = history.split("\n>>>")
        return list(filter(lambda x:x!="", history))[0][:100]
    except:
        return ""

def read_file_to_chat(chatbot, history, file_name):
    with open(file_name, 'r', encoding='utf8') as f:
        file_content = f.read()
    # pattern to match the text between <head> and </head>
    pattern = re.compile(r'<head>.*?</head>', flags=re.DOTALL)
    file_content = re.sub(pattern, '', file_content)
    html, history = file_content.split('<hr color="blue"> \n\n raw chat context:\n')
    history = history.strip('<code>')
    history = history.strip('</code>')
    history = history.split("\n>>>")
    history = list(filter(lambda x:x!="", history))
    html = html.split('<hr color="red"> \n\n')
    html = list(filter(lambda x:x!="", html))
    chatbot.clear()
    for i, h in enumerate(html):
        i_say, gpt_say = h.split('<hr style="border-top: dotted 3px #ccc;">')
        chatbot.append([i_say, gpt_say])
    chatbot.append([f"Archive file details？", f"[Local Message] Load conversation{len(html)}条，Context{len(history)}条。"])
    return chatbot, history    

@CatchException
def ConversationHistoryArchive(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    """
    txt             Text entered by the user in the input field，For example, a paragraph that needs to be translated，For example, a file path that contains files to be processed
    llm_kwargs      GPT model parameters，Such as temperature and top_p，Generally pass it on as is
    plugin_kwargs   Plugin model parameters，No use for the time being
    chatbot         Chat display box handle，Displayed to the user
    history         Chat history，Context summary
    system_prompt   Silent reminder to GPT
    web_port        Current software running port number
    """

    chatbot.append(("Save current conversation", 
        f"[Local Message] {write_chat_to_file(chatbot, history)}，You can call `LoadConversationHistoryArchive` to restore the current conversation。\nWarning! The saved conversation history can be viewed by anyone using this system。"))
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page # As requesting GPT takes some time，Let`s do a UI update in time

def hide_cwd(str):
    import os
    current_path = os.getcwd()
    replace_path = "."
    return str.replace(current_path, replace_path)

@CatchException
def LoadConversationHistoryArchive(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    """
    txt             Text entered by the user in the input field，For example, a paragraph that needs to be translated，For example, a file path that contains files to be processed
    llm_kwargs      GPT model parameters，Such as temperature and top_p，Generally pass it on as is
    plugin_kwargs   Plugin model parameters，No use for the time being
    chatbot         Chat display box handle，Displayed to the user
    history         Chat history，Context summary
    system_prompt   Silent reminder to GPT
    web_port        Current software running port number
    """
    from void_terminal.crazy_functions.crazy_utils import get_files_from_everything
    success, file_manifest, _ = get_files_from_everything(txt, type='.html')

    if not success:
        if txt == "": txt = 'Empty input field'
        import glob
        local_history = "<br/>".join(["`"+hide_cwd(f)+f" ({gen_file_preview(f)})"+"`" for f in glob.glob(f'{get_log_folder()}/**/chatGPT conversation history*.html', recursive=True)])
        chatbot.append([f"Looking for conversation history file（HTML format）: {txt}", f"No HTML files found: {txt}。But the following history files are stored locally，You can paste any file path into the input area，and try again：<br/>{local_history}"])
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return

    try:
        chatbot, history = read_file_to_chat(chatbot, history, file_manifest[0])
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
    except:
        chatbot.append([f"Load conversation history file", f"Conversation history file is corrupted!"])
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return

@CatchException
def DeleteAllLocalConversationHistoryRecords(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    """
    txt             Text entered by the user in the input field，For example, a paragraph that needs to be translated，For example, a file path that contains files to be processed
    llm_kwargs      GPT model parameters，Such as temperature and top_p，Generally pass it on as is
    plugin_kwargs   Plugin model parameters，No use for the time being
    chatbot         Chat display box handle，Displayed to the user
    history         Chat history，Context summary
    system_prompt   Silent reminder to GPT
    web_port        Current software running port number
    """

    import glob, os
    local_history = "<br/>".join(["`"+hide_cwd(f)+"`" for f in glob.glob(f'{get_log_folder()}/**/chatGPT conversation history*.html', recursive=True)])
    for f in glob.glob(f'{get_log_folder()}/**/chatGPT conversation history*.html', recursive=True):
        os.remove(f)
    chatbot.append([f"Delete all history conversation files", f"Deleted<br/>{local_history}"])
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
    return


