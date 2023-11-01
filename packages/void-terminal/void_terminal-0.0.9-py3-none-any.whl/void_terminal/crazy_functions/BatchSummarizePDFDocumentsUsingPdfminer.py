from void_terminal.toolbox import update_ui
from void_terminal.toolbox import CatchException, report_execption
from void_terminal.crazy_functions.crazy_utils import request_gpt_model_in_new_thread_with_ui_alive
from void_terminal.toolbox import write_history_to_file, promote_file_to_downloadzone

fast_debug = False

def readPdf(pdfPath):
    """
    Read the pdf file，Return the text content
    """
    import pdfminer
    from pdfminer.pdfparser import PDFParser
    from pdfminer.pdfdocument import PDFDocument
    from pdfminer.pdfpage import PDFPage, PDFTextExtractionNotAllowed
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.pdfdevice import PDFDevice
    from pdfminer.layout import LAParams
    from pdfminer.converter import PDFPageAggregator

    fp = open(pdfPath, 'rb')

    # Create a PDF parser object associated with the file object
    parser = PDFParser(fp)

    # Create a PDF document object that stores the document structure.
    # Password for initialization as 2nd parameter
    document = PDFDocument(parser)
    # Check if the document allows text extraction. If not, abort.
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed

    # Create a PDF resource manager object that stores shared resources.
    rsrcmgr = PDFResourceManager()

    # Create a PDF device object.
    # device = PDFDevice(rsrcmgr)

    # BEGIN LAYOUT ANALYSIS.
    # Set parameters for analysis.
    laparams = LAParams(
        char_margin=10.0,
        line_margin=0.2,
        boxes_flow=0.2,
        all_texts=False,
    )
    # Create a PDF page aggregator object.
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # loop over all pages in the document
    outTextList = []
    for page in PDFPage.create_pages(document):
        # read the page into a layout object
        interpreter.process_page(page)
        layout = device.get_result()
        for obj in layout._objs:
            if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
                # print(obj.get_text())
                outTextList.append(obj.get_text())

    return outTextList


def ParsePaper(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt):
    import time, glob, os
    from bs4 import BeautifulSoup
    print('begin analysis on:', file_manifest)
    for index, fp in enumerate(file_manifest):
        if ".tex" in fp:
            with open(fp, 'r', encoding='utf-8', errors='replace') as f:
                file_content = f.read()
        if ".pdf" in fp.lower():
            file_content = readPdf(fp)
            file_content = BeautifulSoup(''.join(file_content), features="lxml").body.text.encode('gbk', 'ignore').decode('gbk')

        prefix = "Next, please analyze the following paper files one by one，Summarize its content" if index==0 else ""
        i_say = prefix + f'Please summarize the following article in Chinese，The file name is{os.path.relpath(fp, project_folder)}，The content of the article is ```{file_content}```'
        i_say_show_user = prefix + f'[{index}/{len(file_manifest)}] Please summarize the following article: {os.path.abspath(fp)}'
        chatbot.append((i_say_show_user, "[Local Message] waiting gpt response."))
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page

        if not fast_debug:
            msg = 'Normal'
            # ** gpt request **
            gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
                inputs=i_say, 
                inputs_show_user=i_say_show_user, 
                llm_kwargs=llm_kwargs,
                chatbot=chatbot, 
                history=[],
                sys_prompt="Summarize the article。"
            )  # With timeout countdown
            chatbot[-1] = (i_say_show_user, gpt_say)
            history.append(i_say_show_user); history.append(gpt_say)
            yield from update_ui(chatbot=chatbot, history=history, msg=msg) # Refresh the page
            if not fast_debug: time.sleep(2)

    all_file = ', '.join([os.path.relpath(fp, project_folder) for index, fp in enumerate(file_manifest)])
    i_say = f'According to your own analysis above，Summarize the entire text，Write a Chinese abstract in academic language，Then write an English abstract（Including{all_file}）。'
    chatbot.append((i_say, "[Local Message] waiting gpt response."))
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page

    if not fast_debug:
        msg = 'Normal'
        # ** gpt request **
        gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
            inputs=i_say, 
            inputs_show_user=i_say, 
            llm_kwargs=llm_kwargs,
            chatbot=chatbot, 
            history=history,
            sys_prompt="Summarize the article。"
        )  # With timeout countdown
        chatbot[-1] = (i_say, gpt_say)
        history.append(i_say); history.append(gpt_say)
        yield from update_ui(chatbot=chatbot, history=history, msg=msg) # Refresh the page
        res = write_history_to_file(history)
        promote_file_to_downloadzone(res, chatbot=chatbot)
        chatbot.append(("Are you done?？", res))
        yield from update_ui(chatbot=chatbot, history=history, msg=msg) # Refresh the page



@CatchException
def BatchSummarizePDFDocumentspdfminer(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    history = []    # Clear history，To avoid input overflow
    import glob, os

    # Basic information：Function, contributor
    chatbot.append([
        "Function plugin feature？",
        "BatchSummarizePDFDocuments，This version uses the pdfminer plugin，With token reduction function。Function plugin contributor: Euclid-Jie。"])
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page

    # Attempt to import dependencies，If dependencies are missing，Give installation suggestions
    try:
        import pdfminer, bs4
    except:
        report_execption(chatbot, history, 
            a = f"Parsing project: {txt}", 
            b = f"Failed to import software dependencies。Using this module requires additional dependencies，Installation method```pip install --upgrade pdfminer beautifulsoup4```。")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return
    if os.path.exists(txt):
        project_folder = txt
    else:
        if txt == "": txt = 'Empty input field'
        report_execption(chatbot, history, a = f"Parsing project: {txt}", b = f"Cannot find local project or do not have access: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return
    file_manifest = [f for f in glob.glob(f'{project_folder}/**/*.tex', recursive=True)] + \
                    [f for f in glob.glob(f'{project_folder}/**/*.pdf', recursive=True)] # + \
                    # [f for f in glob.glob(f'{project_folder}/**/*.cpp', recursive=True)] + \
                    # [f for f in glob.glob(f'{project_folder}/**/*.c', recursive=True)]
    if len(file_manifest) == 0:
        report_execption(chatbot, history, a = f"Parsing project: {txt}", b = f"Cannot find any .tex or .pdf files: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return
    yield from ParsePaper(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt)

