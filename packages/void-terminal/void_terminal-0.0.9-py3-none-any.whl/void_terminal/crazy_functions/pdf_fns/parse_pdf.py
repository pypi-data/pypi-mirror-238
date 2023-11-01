from functools import lru_cache
from void_terminal.toolbox import gen_time_str
from void_terminal.toolbox import promote_file_to_downloadzone
from void_terminal.toolbox import write_history_to_file, promote_file_to_downloadzone
from void_terminal.toolbox import get_conf
from void_terminal.toolbox import ProxyNetworkActivate
from void_terminal.colorful import *
import requests
import random
import copy
import os
import math

class GROBID_OFFLINE_EXCEPTION(Exception): pass

def get_avail_grobid_url():
    GROBID_URLS = get_conf('GROBID_URLS')
    if len(GROBID_URLS) == 0: return None
    try:
        _grobid_url = random.choice(GROBID_URLS) # Random load balancing
        if _grobid_url.endswith('/'): _grobid_url = _grobid_url.rstrip('/')
        with ProxyNetworkActivate('Connect_Grobid'):
            res = requests.get(_grobid_url+'/api/isalive')
        if res.text=='true': return _grobid_url
        else: return None
    except:
        return None

@lru_cache(maxsize=32)
def parse_pdf(pdf_path, grobid_url):
    import scipdf   # pip install scipdf_parser
    if grobid_url.endswith('/'): grobid_url = grobid_url.rstrip('/')
    try:
        with ProxyNetworkActivate('Connect_Grobid'):
            article_dict = scipdf.parse_pdf_to_dict(pdf_path, grobid_url=grobid_url)
    except GROBID_OFFLINE_EXCEPTION:
        raise GROBID_OFFLINE_EXCEPTION("GROBID service is unavailable，Please modify GROBID_URL in the config，Can modify to local GROBID service。")
    except:
        raise RuntimeError("ParsePDF failed，Please check if the PDF is damaged。")
    return article_dict


def produce_report_markdown(gpt_response_collection, meta, paper_meta_info, chatbot, fp, generated_conclusion_files):
    # -=-=-=-=-=-=-=-= Write the first file：Mixed translation before and after -=-=-=-=-=-=-=-=
    res_path = write_history_to_file(meta +  ["# Meta Translation" , paper_meta_info] + gpt_response_collection, file_basename=f"{gen_time_str()}translated_and_original.md", file_fullname=None)
    promote_file_to_downloadzone(res_path, rename_file=os.path.basename(res_path)+'.md', chatbot=chatbot)
    generated_conclusion_files.append(res_path)

    # Write the second file：Translated text only -=-=-=-=-=-=-=-=
    translated_res_array = []
    # Record the current chapter title：
    last_section_name = ""
    for index, value in enumerate(gpt_response_collection):
        # First select even serial numbers：
        if index % 2 != 0:
            # First extract the current English title：
            cur_section_name = gpt_response_collection[index-1].split('\n')[0].split(" Part")[0]
            # If the index is 1，Then directly use the first section name：
            if cur_section_name != last_section_name:
                cur_value = cur_section_name + '\n'
                last_section_name = copy.deepcopy(cur_section_name)
            else:
                cur_value = ""
            # Make another small modification：Modify the title of the current part again，Default to English
            cur_value += value
            translated_res_array.append(cur_value)
    res_path = write_history_to_file(meta +  ["# Meta Translation" , paper_meta_info] + translated_res_array, 
                                     file_basename = f"{gen_time_str()}-translated_only.md", 
                                     file_fullname = None,
                                     auto_caption = False)
    promote_file_to_downloadzone(res_path, rename_file=os.path.basename(res_path)+'.md', chatbot=chatbot)
    generated_conclusion_files.append(res_path)
    return res_path

def translate_pdf(article_dict, llm_kwargs, chatbot, fp, generated_conclusion_files, TOKEN_LIMIT_PER_FRAGMENT, DST_LANG):
    from void_terminal.crazy_functions.pdf_fns.report_gen_html import construct_html
    from void_terminal.crazy_functions.crazy_utils import breakdown_txt_to_satisfy_token_limit_for_pdf
    from void_terminal.crazy_functions.crazy_utils import request_gpt_model_in_new_thread_with_ui_alive
    from void_terminal.crazy_functions.crazy_utils import request_gpt_model_multi_threads_with_very_awesome_ui_and_high_efficiency

    prompt = "The following is the basic information of an academic paper:\n"
    # title
    title = article_dict.get('title', 'Unable to get title'); prompt += f'title:{title}\n\n'
    # authors
    authors = article_dict.get('authors', 'Unable to retrieve authors'); prompt += f'authors:{authors}\n\n'
    # abstract
    abstract = article_dict.get('abstract', 'Unable to retrieve abstract'); prompt += f'abstract:{abstract}\n\n'
    # command
    prompt += f"Translate the title and abstract{DST_LANG}。"
    meta = [f'# Title:\n\n', title, f'# Abstract:\n\n', abstract ]

    # Single line，Get article meta information
    paper_meta_info = yield from request_gpt_model_in_new_thread_with_ui_alive(
        inputs=prompt,
        inputs_show_user=prompt,
        llm_kwargs=llm_kwargs,
        chatbot=chatbot, history=[],
        sys_prompt="You are an academic paper reader。",
    )

    # Multi-threaded，Translation
    inputs_array = []
    inputs_show_user_array = []

    # get_token_num
    from void_terminal.request_llms.bridge_all import model_info
    enc = model_info[llm_kwargs['llm_model']]['tokenizer']
    def get_token_num(txt): return len(enc.encode(txt, disallowed_special=()))

    def break_down(txt):
        raw_token_num = get_token_num(txt)
        if raw_token_num <= TOKEN_LIMIT_PER_FRAGMENT:
            return [txt]
        else:
            # raw_token_num > TOKEN_LIMIT_PER_FRAGMENT
            # find a smooth token limit to achieve even seperation
            count = int(math.ceil(raw_token_num / TOKEN_LIMIT_PER_FRAGMENT))
            token_limit_smooth = raw_token_num // count + count
            return breakdown_txt_to_satisfy_token_limit_for_pdf(txt, get_token_fn=get_token_num, limit=token_limit_smooth)

    for section in article_dict.get('sections'):
        if len(section['text']) == 0: continue
        section_frags = break_down(section['text'])
        for i, fragment in enumerate(section_frags):
            heading = section['heading']
            if len(section_frags) > 1: heading += f' Part-{i+1}'
            inputs_array.append(
                f"You need to translate{heading}Chapter，The content is as follows: \n\n{fragment}"
            )
            inputs_show_user_array.append(
                f"# {heading}\n\n{fragment}"
            )

    gpt_response_collection = yield from request_gpt_model_multi_threads_with_very_awesome_ui_and_high_efficiency(
        inputs_array=inputs_array,
        inputs_show_user_array=inputs_show_user_array,
        llm_kwargs=llm_kwargs,
        chatbot=chatbot,
        history_array=[meta for _ in inputs_array],
        sys_prompt_array=[
            "As an academic translator, please，be responsible for accurately translating academic papers into Chinese。Please translate every sentence in the article。" for _ in inputs_array],
    )
    # -=-=-=-=-=-=-=-= Write out Markdown file
    produce_report_markdown(gpt_response_collection, meta, paper_meta_info, chatbot, fp, generated_conclusion_files)

    # -=-=-=-=-=-=-=-= Write out HTML file -=-=-=-=-=-=-=-=
    ch = construct_html() 
    orig = ""
    trans = ""
    gpt_response_collection_html = copy.deepcopy(gpt_response_collection)
    for i,k in enumerate(gpt_response_collection_html): 
        if i%2==0:
            gpt_response_collection_html[i] = inputs_show_user_array[i//2]
        else:
            # First extract the current English title：
            cur_section_name = gpt_response_collection[i-1].split('\n')[0].split(" Part")[0]
            cur_value = cur_section_name + "\n" + gpt_response_collection_html[i]
            gpt_response_collection_html[i] = cur_value

    final = ["", "", "I. Overview of the paper",  "", "Abstract", paper_meta_info,  "II. Translation of the paper",  ""]
    final.extend(gpt_response_collection_html)
    for i, k in enumerate(final): 
        if i%2==0:
            orig = k
        if i%2==1:
            trans = k
            ch.add_row(a=orig, b=trans)
    create_report_file_name = f"{os.path.basename(fp)}.trans.html"
    html_file = ch.save_file(create_report_file_name)
    generated_conclusion_files.append(html_file)
    promote_file_to_downloadzone(html_file, rename_file=os.path.basename(html_file), chatbot=chatbot)
