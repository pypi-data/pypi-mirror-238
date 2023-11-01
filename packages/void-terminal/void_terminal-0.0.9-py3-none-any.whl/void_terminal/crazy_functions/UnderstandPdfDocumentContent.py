from void_terminal.toolbox import update_ui
from void_terminal.toolbox import CatchException, report_execption
from void_terminal.crazy_functions.crazy_utils import read_and_clean_pdf_text
from void_terminal.crazy_functions.crazy_utils import request_gpt_model_in_new_thread_with_ui_alive
fast_debug = False


def ParsePDF(file_name, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt):
    import tiktoken
    print('begin analysis on:', file_name)

    ############################## <Step 0，Split PDF> ##################################
    # Recursively split the PDF file，Each block（Try to use a complete section，such as introduction，experiment, etc.，cut if necessary）
    # its length must be less than 2500 tokens
    file_content, page_one = read_and_clean_pdf_text(file_name) # （try）cut PDF by sections
    file_content = file_content.encode('utf-8', 'ignore').decode()   # avoid reading non-utf8 chars
    page_one = str(page_one).encode('utf-8', 'ignore').decode()  # avoid reading non-utf8 chars
    
    TOKEN_LIMIT_PER_FRAGMENT = 2500

    from void_terminal.crazy_functions.crazy_utils import breakdown_txt_to_satisfy_token_limit_for_pdf
    from void_terminal.request_llms.bridge_all import model_info
    enc = model_info["gpt-3.5-turbo"]['tokenizer']
    def get_token_num(txt): return len(enc.encode(txt, disallowed_special=()))
    paper_fragments = breakdown_txt_to_satisfy_token_limit_for_pdf(
        txt=file_content,  get_token_fn=get_token_num, limit=TOKEN_LIMIT_PER_FRAGMENT)
    page_one_fragments = breakdown_txt_to_satisfy_token_limit_for_pdf(
        txt=str(page_one), get_token_fn=get_token_num, limit=TOKEN_LIMIT_PER_FRAGMENT//4)
    # For better results，We strip the part after Introduction（If there is）
    paper_meta = page_one_fragments[0].split('introduction')[0].split('Introduction')[0].split('INTRODUCTION')[0]
    
    ############################## <Step 1，extract high-value information from the abstract，put it in history> ##################################
    final_results = []
    final_results.append(paper_meta)

    ############################## <Step 2，iterate through the entire article，extract concise information> ##################################
    i_say_show_user = f'First, read the entire paper in an English context。'; gpt_say = "[Local Message] Received。"           # user prompt
    chatbot.append([i_say_show_user, gpt_say]); yield from update_ui(chatbot=chatbot, history=[])    # Update UI

    iteration_results = []
    last_iteration_result = paper_meta  # initial value is the abstract
    MAX_WORD_TOTAL = 4096
    n_fragment = len(paper_fragments)
    if n_fragment >= 20: print('Article is too long，Cannot achieve expected results')
    for i in range(n_fragment):
        NUM_OF_WORD = MAX_WORD_TOTAL // n_fragment
        i_say = f"Read this section, recapitulate the content of this section with less than {NUM_OF_WORD} words: {paper_fragments[i]}"
        i_say_show_user = f"[{i+1}/{n_fragment}] Read this section, recapitulate the content of this section with less than {NUM_OF_WORD} words: {paper_fragments[i][:200]}"
        gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(i_say, i_say_show_user,  # i_say=questions actually asked to chatgpt， i_say_show_user=questions shown to the user
                                                                           llm_kwargs, chatbot, 
                                                                           history=["The main idea of the previous section is?", last_iteration_result], # iterate over the previous result
                                                                           sys_prompt="Extract the main idea of this section."  # prompt
                                                                        ) 
        iteration_results.append(gpt_say)
        last_iteration_result = gpt_say

    ############################## <Step 3，organize history> ##################################
    final_results.extend(iteration_results)
    final_results.append(f'Next，You are a professional academic professor，Utilize the above information，Answer my questions in Chinese。')
    # the next two sentences are only displayed on the interface，do not have an actual effect
    i_say_show_user = f'Next，You are a professional academic professor，Utilize the above information，Answer my questions in Chinese。'; gpt_say = "[Local Message] Received。"
    chatbot.append([i_say_show_user, gpt_say])

    ############################## <Step 4，set a token limit，prevent token overflow when answering> ##################################
    from void_terminal.crazy_functions.crazy_utils import input_clipping
    _, final_results = input_clipping("", final_results, max_token_limit=3200)
    yield from update_ui(chatbot=chatbot, history=final_results) # note that the history record here has been replaced


@CatchException
def UnderstandPdfDocumentContentStandardFileInput(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    import glob, os

    # Basic information：Function, contributor
    chatbot.append([
        "Function plugin feature？",
        "Understand the content of a PDF paper，And will combine with the context，Provide academic answers。Function plugin contributor: Hanzoe, binary-husky"])
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page

    # Attempt to import dependencies，If dependencies are missing，Give installation suggestions
    try:
        import fitz
    except:
        report_execption(chatbot, history, 
            a = f"Parsing project: {txt}", 
            b = f"Failed to import software dependencies。Using this module requires additional dependencies，Installation method```pip install --upgrade pymupdf```。")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return

    # Clear history，To avoid input overflow
    history = []

    # Checking input parameters，If no input parameters are given，Exit directly
    if os.path.exists(txt):
        project_folder = txt
    else:
        if txt == "":
            txt = 'Empty input field'
        report_execption(chatbot, history,
                         a=f"Parsing project: {txt}", b=f"Cannot find local project or do not have access: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return

    # Search for the list of files to be processed
    file_manifest = [f for f in glob.glob(f'{project_folder}/**/*.pdf', recursive=True)]
    # If no files are found
    if len(file_manifest) == 0:
        report_execption(chatbot, history,
                         a=f"Parsing project: {txt}", b=f"Cannot find any .tex or .pdf files: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return
    txt = file_manifest[0]
    # Start executing the task formally
    yield from ParsePDF(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt)
