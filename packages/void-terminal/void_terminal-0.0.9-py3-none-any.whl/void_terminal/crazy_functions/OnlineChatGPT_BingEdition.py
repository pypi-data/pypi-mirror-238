from void_terminal.toolbox import CatchException, update_ui
from void_terminal.crazy_functions.crazy_utils import request_gpt_model_in_new_thread_with_ui_alive, input_clipping
import requests
from bs4 import BeautifulSoup
from void_terminal.request_llms.bridge_all import model_info


def bing_search(query, proxies=None):
    query = query
    url = f"https://cn.bing.com/search?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}
    response = requests.get(url, headers=headers, proxies=proxies)
    soup = BeautifulSoup(response.content, 'html.parser')
    results = []
    for g in soup.find_all('li', class_='b_algo'):
        anchors = g.find_all('a')
        if anchors:
            link = anchors[0]['href']
            if not link.startswith('http'):
                continue
            title = g.find('h2').text
            item = {'title': title, 'link': link}
            results.append(item)

    for r in results:
        print(r['link'])
    return results


def scrape_text(url, proxies) -> str:
    """Scrape text from a webpage

    Args:
        url (str): The URL to scrape text from

    Returns:
        str: The scraped text
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
        'Content-Type': 'text/plain',
    }
    try:
        response = requests.get(url, headers=headers, proxies=proxies, timeout=8)
        if response.encoding == "ISO-8859-1": response.encoding = response.apparent_encoding
    except:
        return "Cannot connect to the webpage"
    soup = BeautifulSoup(response.text, "html.parser")
    for script in soup(["script", "style"]):
        script.extract()
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = "\n".join(chunk for chunk in chunks if chunk)
    return text

@CatchException
def ConnectBingSearchAnswerQuestion(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    """
    txt             Text entered by the user in the input field，For example, a paragraph that needs to be translated，For example, a file path that contains files to be processed
    llm_kwargs      GPT model parameters，Such as temperature and top_p，Generally pass it on as is
    plugin_kwargs   Plugin model parameters，No use for the time being
    chatbot         Chat display box handle，Displayed to the user
    history         Chat history，Context summary
    system_prompt   Silent reminder to GPT
    web_port        Current software running port number
    """
    history = []    # Clear history，To avoid input overflow
    chatbot.append((f"Please answer the following questions based on internet information：{txt}",
                    "[Local Message] Please note，You are calling a[function plugin]template，This template can achieve ChatGPT network information integration。This function is aimed at developers who want to implement more interesting features，It can be used as a template for creating new feature functions。If you want to share new feature modules，Please don`t hesitate to PR!"))
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page # As requesting GPT takes some time，Let`s do a UI update in time

    # ------------- < Step 1：Crawl the results of search engines > -------------
    from void_terminal.toolbox import get_conf
    proxies = get_conf('proxies')
    urls = bing_search(txt, proxies)
    history = []
    if len(urls) == 0:
        chatbot.append((f"Conclusion：{txt}",
                        "[Local Message] Restricted by Bing，Unable to retrieve information from Bing!"))
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page # As requesting GPT takes some time，Let`s do a UI update in time
        return
    # ------------- < Step 2：Visit web pages in order > -------------
    max_search_result = 8   # Include results from how many web pages at most
    for index, url in enumerate(urls[:max_search_result]):
        res = scrape_text(url['link'], proxies)
        history.extend([f"The{index}search results：", res])
        chatbot.append([f"The{index}search results：", res[:500]+"......"])
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page # As requesting GPT takes some time，Let`s do a UI update in time

    # ------------- < Step 3：ChatGPT synthesis > -------------
    i_say = f"Extract information from the above search results，Then answer the question：{txt}"
    i_say, history = input_clipping(    # Trim the input，Start trimming from the longest entry，Prevent token explosion
        inputs=i_say,
        history=history,
        max_token_limit=model_info[llm_kwargs['llm_model']]['max_token']*3//4
    )
    gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
        inputs=i_say, inputs_show_user=i_say,
        llm_kwargs=llm_kwargs, chatbot=chatbot, history=history,
        sys_prompt="Please extract information from the given search results，Summarize the two most relevant search results，Then answer the question。"
    )
    chatbot[-1] = (i_say, gpt_say)
    history.append(i_say);history.append(gpt_say)
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page # UI update

