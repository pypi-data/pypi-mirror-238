from void_terminal.toolbox import update_ui
from void_terminal.toolbox import CatchException, report_execption
from void_terminal.toolbox import write_history_to_file, promote_file_to_downloadzone
from void_terminal.crazy_functions.crazy_utils import request_gpt_model_in_new_thread_with_ui_alive
fast_debug = False


def ParseDocx(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt):
    import time, os
    # pip install python-docx for docx format，Cross-platform
    # pip install pywin32 for doc format，Only supports Win platform
    for index, fp in enumerate(file_manifest):
        if fp.split(".")[-1] == "docx":
            from docx import Document
            doc = Document(fp)
            file_content = "\n".join([para.text for para in doc.paragraphs])
        else:
            try:
                import win32com.client
                word = win32com.client.Dispatch("Word.Application")
                word.visible = False
                # Open file
                doc = word.Documents.Open(os.getcwd() + '/' + fp)
                # file_content = doc.Content.Text
                doc = word.ActiveDocument
                file_content = doc.Range().Text
                doc.Close()
                word.Quit()
            except:
                raise RuntimeError('Please convert .doc documents to .docx documents first。')

        print(file_content)
        # The file name inside private_upload is prone to garbled characters after unzipping（RAR and 7z formats are normal），So you can only analyze the content of the article，Do not enter the file name
        from void_terminal.crazy_functions.crazy_utils import breakdown_txt_to_satisfy_token_limit_for_pdf
        from void_terminal.request_llms.bridge_all import model_info
        max_token = model_info[llm_kwargs['llm_model']]['max_token']
        TOKEN_LIMIT_PER_FRAGMENT = max_token * 3 // 4
        paper_fragments = breakdown_txt_to_satisfy_token_limit_for_pdf(
            txt=file_content,  
            get_token_fn=model_info[llm_kwargs['llm_model']]['token_cnt'], 
            limit=TOKEN_LIMIT_PER_FRAGMENT
        )
        this_paper_history = []
        for i, paper_frag in enumerate(paper_fragments):
            i_say = f'Please summarize the following article fragment in Chinese，The file name is{os.path.relpath(fp, project_folder)}，The content of the article is ```{paper_frag}```'
            i_say_show_user = f'Please summarize the following article fragment: {os.path.abspath(fp)}The{i+1}/{len(paper_fragments)}fragment。'
            gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
                inputs=i_say, 
                inputs_show_user=i_say_show_user, 
                llm_kwargs=llm_kwargs,
                chatbot=chatbot, 
                history=[],
                sys_prompt="Summarize the article。"
            )

            chatbot[-1] = (i_say_show_user, gpt_say)
            history.extend([i_say_show_user,gpt_say])
            this_paper_history.extend([i_say_show_user,gpt_say])

        # All segments of the article have been summarized，If the article is cut into pieces，
        if len(paper_fragments) > 1:
            i_say = f"According to the above dialogue，Summarize the article{os.path.abspath(fp)}The main content of。"
            gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
                inputs=i_say, 
                inputs_show_user=i_say, 
                llm_kwargs=llm_kwargs,
                chatbot=chatbot, 
                history=this_paper_history,
                sys_prompt="Summarize the article。"
            )

            history.extend([i_say,gpt_say])
            this_paper_history.extend([i_say,gpt_say])

        res = write_history_to_file(history)
        promote_file_to_downloadzone(res, chatbot=chatbot)
        chatbot.append(("Are you done?？", res))
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page

    res = write_history_to_file(history)
    promote_file_to_downloadzone(res, chatbot=chatbot)
    chatbot.append(("Are all files summarized?？", res))
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page


@CatchException
def SummarizingWordDocuments(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    import glob, os

    # Basic information：Function, contributor
    chatbot.append([
        "Function plugin feature？",
        "Batch summarize Word documents。Function plugin contributor: JasonGuo1。Attention, If it is a .doc file, Please convert it to .docx format first。"])
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page

    # Attempt to import dependencies，If dependencies are missing，Give installation suggestions
    try:
        from docx import Document
    except:
        report_execption(chatbot, history,
                         a=f"Parsing project: {txt}",
                         b=f"Failed to import software dependencies。Using this module requires additional dependencies，Installation method```pip install --upgrade python-docx pywin32```。")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return

    # Clear history，To avoid input overflow
    history = []

    # Checking input parameters，If no input parameters are given，Exit directly
    if os.path.exists(txt):
        project_folder = txt
    else:
        if txt == "": txt = 'Empty input field'
        report_execption(chatbot, history, a=f"Parsing project: {txt}", b=f"Cannot find local project or do not have access: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return

    # Search for the list of files to be processed
    if txt.endswith('.docx') or txt.endswith('.doc'):
        file_manifest = [txt]
    else:
        file_manifest = [f for f in glob.glob(f'{project_folder}/**/*.docx', recursive=True)] + \
                        [f for f in glob.glob(f'{project_folder}/**/*.doc', recursive=True)]

    # If no files are found
    if len(file_manifest) == 0:
        report_execption(chatbot, history, a=f"Parsing project: {txt}", b=f"Cannot find any .docx or .doc files: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return

    # Start executing the task formally
    yield from ParseDocx(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt)
