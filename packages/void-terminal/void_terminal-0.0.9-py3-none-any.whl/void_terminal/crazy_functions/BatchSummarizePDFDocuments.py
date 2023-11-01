from void_terminal.toolbox import update_ui, promote_file_to_downloadzone, gen_time_str
from void_terminal.toolbox import CatchException, report_execption
from void_terminal.toolbox import write_history_to_file, promote_file_to_downloadzone
from void_terminal.crazy_functions.crazy_utils import request_gpt_model_in_new_thread_with_ui_alive
from void_terminal.crazy_functions.crazy_utils import read_and_clean_pdf_text
from void_terminal.crazy_functions.crazy_utils import input_clipping



def ParsePDF(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt):
    file_write_buffer = []
    for file_name in file_manifest:
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
        i_say_show_user = f'First, read the entire paper in a Chinese context。'; gpt_say = "[Local Message] Received。"           # user prompt
        chatbot.append([i_say_show_user, gpt_say]); yield from update_ui(chatbot=chatbot, history=[])    # Update UI

        iteration_results = []
        last_iteration_result = paper_meta  # initial value is the abstract
        MAX_WORD_TOTAL = 4096 * 0.7
        n_fragment = len(paper_fragments)
        if n_fragment >= 20: print('Article is too long，Cannot achieve expected results')
        for i in range(n_fragment):
            NUM_OF_WORD = MAX_WORD_TOTAL // n_fragment
            i_say = f"Read this section, recapitulate the content of this section with less than {NUM_OF_WORD} Chinese characters: {paper_fragments[i]}"
            i_say_show_user = f"[{i+1}/{n_fragment}] Read this section, recapitulate the content of this section with less than {NUM_OF_WORD} Chinese characters: {paper_fragments[i][:200]}"
            gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(i_say, i_say_show_user,  # i_say=questions actually asked to chatgpt， i_say_show_user=questions shown to the user
                                                                                llm_kwargs, chatbot, 
                                                                                history=["The main idea of the previous section is?", last_iteration_result], # iterate over the previous result
                                                                                sys_prompt="Extract the main idea of this section with Chinese."  # prompt
                                                                                ) 
            iteration_results.append(gpt_say)
            last_iteration_result = gpt_say

        ############################## <Step 3，organize history，Extract summary> ##################################
        final_results.extend(iteration_results)
        final_results.append(f'Please conclude this paper discussed above。')
        # This prompt is from https://github.com/kaixindelele/ChatPaper/blob/main/chat_paper.py
        NUM_OF_WORD = 1000
        i_say = """
1. Mark the title of the paper (with Chinese translation)
2. list all the authors' names (use English)
3. mark the first author's affiliation (output Chinese translation only)
4. mark the keywords of this article (use English)
5. link to the paper, Github code link (if available, fill in Github:None if not)
6. summarize according to the following four points.Be sure to use Chinese answers (proper nouns need to be marked in English)
    - (1):What is the research background of this article?
    - (2):What are the past methods? What are the problems with them? Is the approach well motivated?
    - (3):What is the research methodology proposed in this paper?
    - (4):On what task and what performance is achieved by the methods in this paper? Can the performance support their goals?
Follow the format of the output that follows:                  
1. Title: xxx\n\n
2. Authors: xxx\n\n
3. Affiliation: xxx\n\n
4. Keywords: xxx\n\n
5. Urls: xxx or xxx , xxx \n\n
6. Summary: \n\n
    - (1):xxx;\n 
    - (2):xxx;\n 
    - (3):xxx;\n
    - (4):xxx.\n\n
Be sure to use Chinese answers (proper nouns need to be marked in English), statements as concise and academic as possible,
do not have too much repetitive information, numerical values using the original numbers.
        """
        # This prompt is from https://github.com/kaixindelele/ChatPaper/blob/main/chat_paper.py
        file_write_buffer.extend(final_results)
        i_say, final_results = input_clipping(i_say, final_results, max_token_limit=2000)
        gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
            inputs=i_say, inputs_show_user='Start final summary', 
            llm_kwargs=llm_kwargs, chatbot=chatbot, history=final_results, 
            sys_prompt= f"Extract the main idea of this paper with less than {NUM_OF_WORD} Chinese characters"
        )
        final_results.append(gpt_say)
        file_write_buffer.extend([i_say, gpt_say])
        ############################## <Step 4，set a token limit> ##################################
        _, final_results = input_clipping("", final_results, max_token_limit=3200)
        yield from update_ui(chatbot=chatbot, history=final_results) # note that the history record here has been replaced

    res = write_history_to_file(file_write_buffer)
    promote_file_to_downloadzone(res, chatbot=chatbot)
    yield from update_ui(chatbot=chatbot, history=final_results) # Refresh the page


@CatchException
def BatchSummarizePDFDocuments(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    import glob, os

    # Basic information：Function, contributor
    chatbot.append([
        "Function plugin feature？",
        "BatchSummarizePDFDocuments。Function plugin contributor: ValeriaWong，Eralien"])
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
        if txt == "": txt = 'Empty input field'
        report_execption(chatbot, history, a = f"Parsing project: {txt}", b = f"Cannot find local project or do not have access: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return

    # Search for the list of files to be processed
    file_manifest = [f for f in glob.glob(f'{project_folder}/**/*.pdf', recursive=True)]
    
    # If no files are found
    if len(file_manifest) == 0:
        report_execption(chatbot, history, a = f"Parsing project: {txt}", b = f"Cannot find any .tex or .pdf files: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return

    # Start executing the task formally
    yield from ParsePDF(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt)
