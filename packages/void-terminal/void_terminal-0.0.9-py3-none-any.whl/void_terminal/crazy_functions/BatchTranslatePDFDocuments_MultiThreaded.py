from void_terminal.toolbox import CatchException, report_execption, get_log_folder, gen_time_str
from void_terminal.toolbox import update_ui, promote_file_to_downloadzone, update_ui_lastest_msg, disable_auto_promotion
from void_terminal.toolbox import write_history_to_file, promote_file_to_downloadzone
from void_terminal.crazy_functions.crazy_utils import request_gpt_model_in_new_thread_with_ui_alive
from void_terminal.crazy_functions.crazy_utils import request_gpt_model_multi_threads_with_very_awesome_ui_and_high_efficiency
from void_terminal.crazy_functions.crazy_utils import read_and_clean_pdf_text
from void_terminal.crazy_functions.pdf_fns.parse_pdf import parse_pdf, get_avail_grobid_url, translate_pdf
from void_terminal.colorful import *
import copy
import os
import math

@CatchException
def BatchTranslatePDFDocuments(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):

    disable_auto_promotion(chatbot)
    # Basic information：Function, contributor
    chatbot.append([
        "Function plugin feature？",
        "BatchTranslatePDFDocuments。Function plugin contributor: Binary-Husky"])
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page

    # Attempt to import dependencies，If dependencies are missing，Give installation suggestions
    try:
        import fitz
        import tiktoken
        import scipdf
    except:
        report_execption(chatbot, history,
                         a=f"Parsing project: {txt}",
                         b=f"Failed to import software dependencies。Using this module requires additional dependencies，Installation method```pip install --upgrade pymupdf tiktoken scipdf_parser```。")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return

    # Clear history，To avoid input overflow
    history = []

    from void_terminal.crazy_functions.crazy_utils import get_files_from_everything
    success, file_manifest, project_folder = get_files_from_everything(txt, type='.pdf')
    # Checking input parameters，If no input parameters are given，Exit directly
    if not success:
        if txt == "": txt = 'Empty input field'

    # If no files are found
    if len(file_manifest) == 0:
        report_execption(chatbot, history,
                         a=f"Parsing project: {txt}", b=f"Unable to find any.pdf拓展名files: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return

    # Start executing the task formally
    grobid_url = get_avail_grobid_url()
    if grobid_url is not None:
        yield from ParsePDF_BasedOnGROBID(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, grobid_url)
    else:
        yield from update_ui_lastest_msg("GROBID service is unavailable，Please check the GROBID_URL in the config。As an alternative，Now execute the older version code with slightly worse performance。", chatbot, history, delay=3)
        yield from ParsePDF(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt)


def ParsePDF_BasedOnGROBID(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, grobid_url):
    import copy, json
    TOKEN_LIMIT_PER_FRAGMENT = 1024
    generated_conclusion_files = []
    generated_html_files = []
    DST_LANG = "Chinese"
    from void_terminal.crazy_functions.pdf_fns.report_gen_html import construct_html
    for index, fp in enumerate(file_manifest):
        chatbot.append(["Current progress：", f"Connecting to GROBID service，Please wait: {grobid_url}\nIf the waiting time is too long，Please modify GROBID_URL in the config，Can modify to local GROBID service。"]); yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        article_dict = parse_pdf(fp, grobid_url)
        grobid_json_res = os.path.join(get_log_folder(), gen_time_str() + "grobid.json")
        with open(grobid_json_res, 'w+', encoding='utf8') as f:
            f.write(json.dumps(article_dict, indent=4, ensure_ascii=False))
        promote_file_to_downloadzone(grobid_json_res, chatbot=chatbot)
        
        if article_dict is None: raise RuntimeError("ParsePDF failed，Please check if the PDF is damaged。")
        yield from translate_pdf(article_dict, llm_kwargs, chatbot, fp, generated_conclusion_files, TOKEN_LIMIT_PER_FRAGMENT, DST_LANG)
    chatbot.append(("Provide a list of output files", str(generated_conclusion_files + generated_html_files)))
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page


def ParsePDF(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt):
    """
    This function has been deprecated
    """
    import copy
    TOKEN_LIMIT_PER_FRAGMENT = 1024
    generated_conclusion_files = []
    generated_html_files = []
    from void_terminal.crazy_functions.pdf_fns.report_gen_html import construct_html
    for index, fp in enumerate(file_manifest):
        # Read PDF file
        file_content, page_one = read_and_clean_pdf_text(fp)
        file_content = file_content.encode('utf-8', 'ignore').decode()   # avoid reading non-utf8 chars
        page_one = str(page_one).encode('utf-8', 'ignore').decode()      # avoid reading non-utf8 chars

        # Recursively split the PDF file
        from void_terminal.crazy_functions.crazy_utils import breakdown_txt_to_satisfy_token_limit_for_pdf
        from void_terminal.request_llms.bridge_all import model_info
        enc = model_info["gpt-3.5-turbo"]['tokenizer']
        def get_token_num(txt): return len(enc.encode(txt, disallowed_special=()))
        paper_fragments = breakdown_txt_to_satisfy_token_limit_for_pdf(
            txt=file_content,  get_token_fn=get_token_num, limit=TOKEN_LIMIT_PER_FRAGMENT)
        page_one_fragments = breakdown_txt_to_satisfy_token_limit_for_pdf(
            txt=page_one, get_token_fn=get_token_num, limit=TOKEN_LIMIT_PER_FRAGMENT//4)

        # For better results，We strip the part after Introduction（If there is）
        paper_meta = page_one_fragments[0].split('introduction')[0].split('Introduction')[0].split('INTRODUCTION')[0]
        
        # Single line，Get article meta information
        paper_meta_info = yield from request_gpt_model_in_new_thread_with_ui_alive(
            inputs=f"The following is the basic information of an academic paper，Please extract the following six parts: `Title`, `Conference or Journal`, `Author`, `Abstract`, `Number`, `Author`s Email`。Please output in markdown format，Finally, translate the abstract into Chinese。Please extract：{paper_meta}",
            inputs_show_user=f"Please extract from{fp}Please extract basic information such as `Title` and `Conference or Journal` from。",
            llm_kwargs=llm_kwargs,
            chatbot=chatbot, history=[],
            sys_prompt="Your job is to collect information from materials。",
        )

        # Multi-threaded，Translation
        gpt_response_collection = yield from request_gpt_model_multi_threads_with_very_awesome_ui_and_high_efficiency(
            inputs_array=[
                f"You need to translate the following content：\n{frag}" for frag in paper_fragments],
            inputs_show_user_array=[f"\n---\n Original text： \n\n {frag.replace('#', '')}  \n---\n Translation：\n " for frag in paper_fragments],
            llm_kwargs=llm_kwargs,
            chatbot=chatbot,
            history_array=[[paper_meta] for _ in paper_fragments],
            sys_prompt_array=[
                "As an academic translator, please，be responsible for accurately translating academic papers into Chinese。Please translate every sentence in the article。" for _ in paper_fragments],
            # max_workers=5  # Maximum parallel overload allowed by OpenAI
        )
        gpt_response_collection_md = copy.deepcopy(gpt_response_collection)
        # Organize the format of the report
        for i,k in enumerate(gpt_response_collection_md): 
            if i%2==0:
                gpt_response_collection_md[i] = f"\n\n---\n\n ## Original text[{i//2}/{len(gpt_response_collection_md)//2}]： \n\n {paper_fragments[i//2].replace('#', '')}  \n\n---\n\n ## Translation[{i//2}/{len(gpt_response_collection_md)//2}]：\n "
            else:
                gpt_response_collection_md[i] = gpt_response_collection_md[i]
        final = ["I. Overview of the paper\n\n---\n\n", paper_meta_info.replace('# ', '### ') + '\n\n---\n\n', "II. Translation of the paper", ""]
        final.extend(gpt_response_collection_md)
        create_report_file_name = f"{os.path.basename(fp)}.trans.md"
        res = write_history_to_file(final, create_report_file_name)
        promote_file_to_downloadzone(res, chatbot=chatbot)

        # Update UI
        generated_conclusion_files.append(f'{get_log_folder()}/{create_report_file_name}')
        chatbot.append((f"{fp}Are you done?？", res))
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page

        # write html
        try:
            ch = construct_html() 
            orig = ""
            trans = ""
            gpt_response_collection_html = copy.deepcopy(gpt_response_collection)
            for i,k in enumerate(gpt_response_collection_html): 
                if i%2==0:
                    gpt_response_collection_html[i] = paper_fragments[i//2].replace('#', '')
                else:
                    gpt_response_collection_html[i] = gpt_response_collection_html[i]
            final = ["Overview of the paper", paper_meta_info.replace('# ', '### '),  "II. Translation of the paper",  ""]
            final.extend(gpt_response_collection_html)
            for i, k in enumerate(final): 
                if i%2==0:
                    orig = k
                if i%2==1:
                    trans = k
                    ch.add_row(a=orig, b=trans)
            create_report_file_name = f"{os.path.basename(fp)}.trans.html"
            generated_html_files.append(ch.save_file(create_report_file_name))
        except:
            from void_terminal.toolbox import trimmed_format_exc
            print('writing html result failed:', trimmed_format_exc())

    # Prepare for file download
    for pdf_path in generated_conclusion_files:
        # Rename file
        rename_file = f'Translation -{os.path.basename(pdf_path)}'
        promote_file_to_downloadzone(pdf_path, rename_file=rename_file, chatbot=chatbot)
    for html_path in generated_html_files:
        # Rename file
        rename_file = f'Translation -{os.path.basename(html_path)}'
        promote_file_to_downloadzone(html_path, rename_file=rename_file, chatbot=chatbot)
    chatbot.append(("Provide a list of output files", str(generated_conclusion_files + generated_html_files)))
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page


