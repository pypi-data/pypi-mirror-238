from void_terminal.toolbox import update_ui, get_log_folder
from void_terminal.toolbox import write_history_to_file, promote_file_to_downloadzone
from void_terminal.toolbox import CatchException, report_execption, get_conf
import re, requests, unicodedata, os
from void_terminal.crazy_functions.crazy_utils import request_gpt_model_in_new_thread_with_ui_alive
def download_arxiv_(url_pdf):
    if 'arxiv.org' not in url_pdf:
        if ('.' in url_pdf) and ('/' not in url_pdf):
            new_url = 'https://arxiv.org/abs/'+url_pdf
            print('Download number：', url_pdf, 'Auto-locating：', new_url)
            # download_arxiv_(new_url)
            return download_arxiv_(new_url)
        else:
            print('Unrecognized URL!')
            return None
    if 'abs' in url_pdf:
        url_pdf = url_pdf.replace('abs', 'pdf')
        url_pdf = url_pdf + '.pdf'

    url_abs = url_pdf.replace('.pdf', '').replace('pdf', 'abs')
    title, other_info = get_name(_url_=url_abs)

    paper_id = title.split()[0]  # '[1712.00559]'
    if '2' in other_info['year']:
        title = other_info['year'] + ' ' + title

    known_conf = ['NeurIPS', 'NIPS', 'Nature', 'Science', 'ICLR', 'AAAI']
    for k in known_conf:
        if k in other_info['comment']:
            title = k + ' ' + title

    download_dir = get_log_folder(plugin_name='arxiv')
    os.makedirs(download_dir, exist_ok=True)

    title_str = title.replace('?', '？')\
        .replace(':', '：')\
        .replace('\"', '“')\
        .replace('\n', '')\
        .replace('  ', ' ')\
        .replace('  ', ' ')

    requests_pdf_url = url_pdf
    file_path = download_dir+title_str

    print('Downloading')
    proxies = get_conf('proxies')
    r = requests.get(requests_pdf_url, proxies=proxies)
    with open(file_path, 'wb+') as f:
        f.write(r.content)
    print('Download complete')

    # print('Output下载命令：','aria2c -o \"%s\" %s'%(title_str,url_pdf))
    # subprocess.call('aria2c --all-proxy=\"172.18.116.150:11084\" -o \"%s\" %s'%(download_dir+title_str,url_pdf), shell=True)

    x = "%s  %s %s.bib" % (paper_id, other_info['year'], other_info['authors'])
    x = x.replace('?', '？')\
        .replace(':', '：')\
        .replace('\"', '“')\
        .replace('\n', '')\
        .replace('  ', ' ')\
        .replace('  ', ' ')
    return file_path, other_info


def get_name(_url_):
    import os
    from bs4 import BeautifulSoup
    print('Getting article name!')
    print(_url_)

    # arxiv_recall = {}
    # if os.path.exists('./arxiv_recall.pkl'):
    #     with open('./arxiv_recall.pkl', 'rb') as f:
    #         arxiv_recall = pickle.load(f)

    # if _url_ in arxiv_recall:
    #     print('在缓存中')
    #     return arxiv_recall[_url_]

    proxies = get_conf('proxies')
    res = requests.get(_url_, proxies=proxies)

    bs = BeautifulSoup(res.text, 'html.parser')
    other_details = {}

    # get year
    try:
        year = bs.find_all(class_='dateline')[0].text
        year = re.search(r'(\d{4})', year, re.M | re.I).group(1)
        other_details['year'] = year
        abstract = bs.find_all(class_='abstract mathjax')[0].text
        other_details['abstract'] = abstract
    except:
        other_details['year'] = ''
        print('Failed to get year')

    # get author
    try:
        authors = bs.find_all(class_='authors')[0].text
        authors = authors.split('Authors:')[1]
        other_details['authors'] = authors
    except:
        other_details['authors'] = ''
        print('Failed to get authors')

    # get comment
    try:
        comment = bs.find_all(class_='metatable')[0].text
        real_comment = None
        for item in comment.replace('\n', ' ').split('   '):
            if 'Comments' in item:
                real_comment = item
        if real_comment is not None:
            other_details['comment'] = real_comment
        else:
            other_details['comment'] = ''
    except:
        other_details['comment'] = ''
        print('Failed to get year')

    title_str = BeautifulSoup(
        res.text, 'html.parser').find('title').contents[0]
    print('Successfully retrieved：', title_str)
    # arxiv_recall[_url_] = (title_str+'.pdf', other_details)
    # with open('./arxiv_recall.pkl', 'wb') as f:
    #     pickle.dump(arxiv_recall, f)

    return title_str+'.pdf', other_details



@CatchException
def DownloadArxivPaperAndTranslateAbstract(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):

    CRAZY_FUNCTION_INFO = "DownloadArxivPaperAndTranslateAbstract，Function plugin author[binary-husky]。Extracting abstract and downloading PDF document..."
    import glob
    import os

    # Basic information：Function, contributor
    chatbot.append(["Function plugin feature？", CRAZY_FUNCTION_INFO])
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page

    # Attempt to import dependencies，If dependencies are missing，Give installation suggestions
    try:
        import bs4
    except:
        report_execption(chatbot, history, 
            a = f"Parsing project: {txt}", 
            b = f"Failed to import software dependencies。Using this module requires additional dependencies，Installation method```pip install --upgrade beautifulsoup4```。")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return

    # Clear history，To avoid input overflow
    history = []

    # Extract abstract，Download PDF document
    try:
        pdf_path, info = download_arxiv_(txt)
    except:
        report_execption(chatbot, history, 
            a = f"Parsing project: {txt}", 
            b = f"PDF file download unsuccessful")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return
    
    # Translate abstract, etc.
    i_say =            f"Please read the following academic paper related materials，Extract abstract，Translate to Chinese。Materials are as follows：{str(info)}"
    i_say_show_user =  f'Please read the following academic paper related materials，Extract abstract，Translate to Chinese。Paper：{pdf_path}'
    chatbot.append((i_say_show_user, "[Local Message] waiting gpt response."))
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
    msg = 'Normal'
    # ** gpt request **
    # Single line，Get article meta information
    gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
        inputs=i_say,
        inputs_show_user=i_say_show_user,
        llm_kwargs=llm_kwargs,
        chatbot=chatbot, history=[],
        sys_prompt="Your job is to collect information from materials and translate to Chinese。",
    )

    chatbot[-1] = (i_say_show_user, gpt_say)
    history.append(i_say_show_user); history.append(gpt_say)
    yield from update_ui(chatbot=chatbot, history=history, msg=msg) # Refresh the page
    res = write_history_to_file(history)
    promote_file_to_downloadzone(res, chatbot=chatbot)
    promote_file_to_downloadzone(pdf_path, chatbot=chatbot)

    chatbot.append(("Are you done?？", res + "\n\nPDF file has also been downloaded"))
    yield from update_ui(chatbot=chatbot, history=history, msg=msg) # Refresh the page

