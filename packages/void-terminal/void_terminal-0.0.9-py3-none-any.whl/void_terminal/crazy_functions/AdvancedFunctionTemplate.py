from void_terminal.toolbox import CatchException, update_ui
from void_terminal.crazy_functions.crazy_utils import request_gpt_model_in_new_thread_with_ui_alive
import datetime
@CatchException
def HighOrderFunctionTemplateFunctions(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
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
    chatbot.append(("What is this function？", "[Local Message] Please note，You are calling a[function plugin]template，This function is aimed at developers who want to implement more interesting features，It can be used as a template for creating new feature functions（This Function Has Only 20+ Lines of Code）。In addition, we also provide a multi-threaded demo that can process a large number of files synchronously for your reference。If you want to share new feature modules，Please don`t hesitate to PR!"))
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page # As requesting GPT takes some time，Let`s do a UI update in time
    for i in range(5):
        currentMonth = (datetime.date.today() + datetime.timedelta(days=i)).month
        currentDay = (datetime.date.today() + datetime.timedelta(days=i)).day
        i_say = f'Which Events Happened in History on{currentMonth}Month{currentDay}Day？List Two and Send Relevant Pictures。When Sending Pictures，Please Use Markdown，Replace PUT_YOUR_QUERY_HERE in the Unsplash API with the Most Important Word Describing the Event。'
        gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
            inputs=i_say, inputs_show_user=i_say, 
            llm_kwargs=llm_kwargs, chatbot=chatbot, history=[], 
            sys_prompt="When you want to send a photo，Please Use Markdown, And do not use backslashes, Do not use code blocks。Use Unsplash API (https://source.unsplash.com/1280x720/? < PUT_YOUR_QUERY_HERE >)。"
        )
        chatbot[-1] = (i_say, gpt_say)
        history.append(i_say);history.append(gpt_say)
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page # UI update