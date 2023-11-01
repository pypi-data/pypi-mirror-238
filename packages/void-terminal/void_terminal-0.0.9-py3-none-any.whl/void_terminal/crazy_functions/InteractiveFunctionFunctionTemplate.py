from void_terminal.toolbox import CatchException, update_ui
from void_terminal.crazy_functions.crazy_utils import request_gpt_model_in_new_thread_with_ui_alive


@CatchException
def InteractiveFunctionTemplateFunction(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    """
    txt             Text entered by the user in the input field，For example, a paragraph that needs to be translated，For example, a file path that contains files to be processed
    llm_kwargs      GPT model parameters, Such as temperature and top_p, Generally pass it on as is
    plugin_kwargs   Plugin model parameters, Such as temperature and top_p, Generally pass it on as is
    chatbot         Chat display box handle，Displayed to the user
    history         Chat history，Context summary
    system_prompt   Silent reminder to GPT
    web_port        Current software running port number
    """
    history = []    # Clear history，To avoid input overflow
    chatbot.append(("What is this function？", "InteractiveFunctionFunctionTemplate。After execution is complete, You can store your own status in cookies, Waiting for the user to call again。"))
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page

    state = chatbot._cookies.get('plugin_state_0001', None) # Initializing plugin status

    if state is None:
        chatbot._cookies['lock_plugin'] = 'crazy_functions.InteractiveFunctionFunctionTemplate->InteractiveFunctionTemplateFunction'      # Assign plugin lock, lock plugin callback path，When the next user submits，Will directly jump to the function
        chatbot._cookies['plugin_state_0001'] = 'wait_user_keyword'                              # Assign plugin status

        chatbot.append(("First call：", "Please enter a keyword., I will search for related wallpapers for you, Suggest using English words, Plugin is locked，Submit directly。"))
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return

    if state == 'wait_user_keyword':
        chatbot._cookies['lock_plugin'] = None          # Unlock plugin，Avoid forgetting to cause deadlock
        chatbot._cookies['plugin_state_0001'] = None    # Release plugin status，Avoid forgetting to cause deadlock

        # Unlock plugin
        chatbot.append((f"Get keywords：{txt}", ""))
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        page_return = get_image_page_by_keyword(txt)
        inputs=inputs_show_user=f"Extract all image urls in this html page, pick the first 5 images and show them with markdown format: \n\n {page_return}"
        gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
            inputs=inputs, inputs_show_user=inputs_show_user,
            llm_kwargs=llm_kwargs, chatbot=chatbot, history=[], 
            sys_prompt="When you want to show an image, use markdown format. e.g. ![image_description](image_url). If there are no image url provided, answer 'no image url provided'"
        )
        chatbot[-1] = [chatbot[-1][0], gpt_say]
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return



# ---------------------------------------------------------------------------------

def get_image_page_by_keyword(keyword):
    import requests
    from bs4 import BeautifulSoup
    response = requests.get(f'https://wallhaven.cc/search?q={keyword}', timeout=2)
    res = "image urls: \n"
    for image_element in BeautifulSoup(response.content, 'html.parser').findAll("img"):
        try:
            res += image_element["data-src"]
            res += "\n"
        except:
            pass
    return res
