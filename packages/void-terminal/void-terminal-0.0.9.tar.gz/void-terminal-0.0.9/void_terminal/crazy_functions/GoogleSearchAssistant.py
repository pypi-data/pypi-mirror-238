from void_terminal.crazy_functions.crazy_utils import request_gpt_model_in_new_thread_with_ui_alive
from void_terminal.toolbox import CatchException, report_execption, promote_file_to_downloadzone
from void_terminal.toolbox import update_ui, update_ui_lastest_msg, disable_auto_promotion, write_history_to_file
import logging
import requests
import time
import random

ENABLE_ALL_VERSION_SEARCH = True

def get_meta_information(url, chatbot, history):
    import arxiv
    import difflib
    import re
    from bs4 import BeautifulSoup
    from void_terminal.toolbox import get_conf
    from urllib.parse import urlparse
    session = requests.session()

    proxies = get_conf('proxies')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, br', 
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Cache-Control':'max-age=0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 
        'Connection': 'keep-alive'
    }
    try:
        session.proxies.update(proxies)
    except:
        report_execption(chatbot, history,
                    a=f"Failed to get proxy. It is very likely that you will not be able to access OpenAI family models and Google Scholar without a proxy. It is recommended：Check if the USE_PROXY option has been modified。",
                    b=f"Try to connect directly")
        yield from update_ui(chatbot=chatbot, history=history)  # Refresh the page
    session.headers.update(headers)

    response = session.get(url)
    # Parsing webpage content
    soup = BeautifulSoup(response.text, "html.parser")

    def string_similar(s1, s2):
        return difflib.SequenceMatcher(None, s1, s2).quick_ratio()

    if ENABLE_ALL_VERSION_SEARCH:
        def search_all_version(url):
            time.sleep(random.randint(1,5)) # Sleep for a while to prevent triggering Google anti-crawler
            response = session.get(url)
            soup = BeautifulSoup(response.text, "html.parser")

            for result in soup.select(".gs_ri"):
                try:
                    url = result.select_one(".gs_rt").a['href']
                except:
                    continue
                arxiv_id = extract_arxiv_id(url)
                if not arxiv_id:
                    continue
                search = arxiv.Search(
                    id_list=[arxiv_id],
                    max_results=1,
                    sort_by=arxiv.SortCriterion.Relevance,
                )
                try: paper = next(search.results())
                except: paper = None
                return paper

            return None

        def extract_arxiv_id(url):
            # Return the arxiv_id parsed from the given URL，Return None if the URL does not match successfully
            pattern = r'arxiv.org/abs/([^/]+)'
            match = re.search(pattern, url)
            if match:
                return match.group(1)
            else:
                return None

    profile = []
    # Getting titles and authors of all articles
    for result in soup.select(".gs_ri"):
        title = result.a.text.replace('\n', ' ').replace('  ', ' ')
        author = result.select_one(".gs_a").text
        try:
            citation = result.select_one(".gs_fl > a[href*='cites']").text  # The number of citations is in the link text，Take it out directly
        except:
            citation = 'cited by 0'
        abstract = result.select_one(".gs_rs").text.strip()  # The summary is in the .gs_rs text，Need to remove leading and trailing spaces

        # First search on arxiv，Get article summary
        search = arxiv.Search(
            query = title,
            max_results = 1,
            sort_by = arxiv.SortCriterion.Relevance,
        )
        try: paper = next(search.results())
        except: paper = None
        
        is_match = paper is not None and string_similar(title, paper.title) > 0.90

        # If the match fails on Arxiv，Retrieve the titles of historical versions of the article
        if not is_match and ENABLE_ALL_VERSION_SEARCH:
            other_versions_page_url = [tag['href'] for tag in result.select_one('.gs_flb').select('.gs_nph') if 'cluster' in tag['href']]
            if len(other_versions_page_url) > 0:
                other_versions_page_url = other_versions_page_url[0]
                paper = search_all_version('http://' + urlparse(url).netloc + other_versions_page_url)
                is_match = paper is not None and string_similar(title, paper.title) > 0.90

        if is_match:
            # same paper
            abstract = paper.summary.replace('\n', ' ')
            is_paper_in_arxiv = True
        else:
            # different paper
            abstract = abstract
            is_paper_in_arxiv = False

        logging.info('[title]:' + title)
        logging.info('[author]:' + author)
        logging.info('[citation]:' + citation)

        profile.append({
            'title': title,
            'author': author,
            'citation': citation,
            'abstract': abstract,
            'is_paper_in_arxiv': is_paper_in_arxiv,
        })

        chatbot[-1] = [chatbot[-1][0], title + f'\n\nIs it in arxiv?（Cannot get complete summary if it is not in arxiv）:{is_paper_in_arxiv}\n\n' + abstract]
        yield from update_ui(chatbot=chatbot, history=[]) # Refresh the page
    return profile

@CatchException
def GoogleSearchAssistant(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    disable_auto_promotion(chatbot=chatbot)
    # Basic information：Function, contributor
    chatbot.append([
        "Function plugin feature？",
        "Analyzing Google Scholar provided by the user（google scholar）In the search page，All articles that appear: binary-husky，Plugin initializing..."])
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page

    # Attempt to import dependencies，If dependencies are missing，Give installation suggestions
    try:
        import arxiv
        import math
        from bs4 import BeautifulSoup
    except:
        report_execption(chatbot, history, 
            a = f"Parsing project: {txt}", 
            b = f"Failed to import software dependencies。Using this module requires additional dependencies，Installation method```pip install --upgrade beautifulsoup4 arxiv```。")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return

    # Clear history，To avoid input overflow
    history = []
    meta_paper_info_list = yield from get_meta_information(txt, chatbot, history)
    if len(meta_paper_info_list) == 0:
        yield from update_ui_lastest_msg(lastmsg='Failed to retrieve literature，May have triggered Google anti-crawler mechanism。',chatbot=chatbot, history=history, delay=0)
        return
    batchsize = 5
    for batch in range(math.ceil(len(meta_paper_info_list)/batchsize)):
        if len(meta_paper_info_list[:batchsize]) > 0:
            i_say = "Below are some academic literature data，Extract the following content：" + \
            "1. English title; 2. Translation of Chinese title; 3. Author; 4. arxiv open access（is_paper_in_arxiv）Number of Citations（cite）Translation of Chinese Abstract。" + \
            f"Here are the Information Sources：{str(meta_paper_info_list[:batchsize])}" 

            inputs_show_user = f"Please Analyze all the Articles Appearing on this Page：{txt}，This is Batch Number{batch+1}"
            gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
                inputs=i_say, inputs_show_user=inputs_show_user,
                llm_kwargs=llm_kwargs, chatbot=chatbot, history=[],
                sys_prompt="You are an Academic Translator，Please Extract Information from the Data。You Must Use Markdown Tables。You Must Process Each Document One by One。"
            )

            history.extend([ f"The{batch+1}", gpt_say ])
            meta_paper_info_list = meta_paper_info_list[batchsize:]

    chatbot.append(["Status？", 
        "All Completed，You Can Try to Let AI Write a Related Works，For example您可以继续InputWrite a \"Related Works\" section about \"你搜索的研究领域\" for me."])
    msg = 'Normal'
    yield from update_ui(chatbot=chatbot, history=history, msg=msg) # Refresh the page
    path = write_history_to_file(history)
    promote_file_to_downloadzone(path, chatbot=chatbot)
    chatbot.append(("Are you done?？", path)); 
    yield from update_ui(chatbot=chatbot, history=history, msg=msg) # Refresh the page
