import markdown
import importlib
import time
import inspect
import re
import os
import gradio
import shutil
import glob
import math
from latex2mathml.converter import convert as tex2mathml
from functools import wraps, lru_cache
pj = os.path.join

"""
========================================================================
First part
Function plugin input and output docking area
    - ChatBotWithCookies:   Chatbot class with cookies，Laying the foundation for implementing more powerful functions
    - ArgsGeneralWrapper:   Decorator function，Used to restructure input parameters，Change the order and structure of input parameters
    - update_ui:            Refresh the interface using yield from update_ui(chatbot, history)
    - CatchException:       Display all questions from the plugin on the interface
    - HotReload:            Implement hot update of the plugin
    - trimmed_format_exc:   Print traceback，Hide absolute address for security reasons
========================================================================
"""

class ChatBotWithCookies(list):
    def __init__(self, cookie):
        """
        cookies = {
            'top_p': top_p,
            'temperature': temperature,
            'lock_plugin': bool,
            "files_to_promote": ["file1", "file2"],
            "most_recent_uploaded": {
                "path": "uploaded_path",
                "time": time.time(),
                "time_str": "timestr",
            }
        }
        """
        self._cookies = cookie

    def write_list(self, list):
        for t in list:
            self.append(t)

    def get_list(self):
        return [t for t in self]

    def get_cookies(self):
        return self._cookies


def ArgsGeneralWrapper(f):
    """
    Decorator function，Used to restructure input parameters，Change the order and structure of input parameters。
    """
    def decorated(request: gradio.Request, cookies, max_length, llm_model, txt, txt2, top_p, temperature, chatbot, history, system_prompt, plugin_advanced_arg, *args):
        txt_passon = txt
        if txt == "" and txt2 != "": txt_passon = txt2
        # Introduce a chatbot with cookies
        cookies.update({
            'top_p':top_p,
            'api_key': cookies['api_key'],
            'llm_model': llm_model,
            'temperature':temperature,
        })
        llm_kwargs = {
            'api_key': cookies['api_key'],
            'llm_model': llm_model,
            'top_p':top_p,
            'max_length': max_length,
            'temperature':temperature,
            'client_ip': request.client.host,
        }
        plugin_kwargs = {
            "advanced_arg": plugin_advanced_arg,
        }
        chatbot_with_cookie = ChatBotWithCookies(cookies)
        chatbot_with_cookie.write_list(chatbot)
        
        if cookies.get('lock_plugin', None) is None:
            # Normal state
            if len(args) == 0:  # Plugin channel
                yield from f(txt_passon, llm_kwargs, plugin_kwargs, chatbot_with_cookie, history, system_prompt, request)
            else:               # Conversation channel，Or the basic function channel
                yield from f(txt_passon, llm_kwargs, plugin_kwargs, chatbot_with_cookie, history, system_prompt, *args)
        else:
            # Handle the locked state of special plugins in a few cases
            module, fn_name = cookies['lock_plugin'].split('->')
            f_hot_reload = getattr(importlib.import_module(module, fn_name), fn_name)
            yield from f_hot_reload(txt_passon, llm_kwargs, plugin_kwargs, chatbot_with_cookie, history, system_prompt, request)
            # Check if the user entered through the dialogue channel by mistake，If it is，Then remind
            final_cookies = chatbot_with_cookie.get_cookies()
            # len(args) != 0 represents the `Submit` key dialogue channel，Or the basic function channel
            if len(args) != 0 and 'files_to_promote' in final_cookies and len(final_cookies['files_to_promote']) > 0:
                chatbot_with_cookie.append(["Detected **stuck cache document**，Please handle it in time。", "Please click `**Save Current Dialogue**` in time to obtain all cached documents。"])
                yield from update_ui(chatbot_with_cookie, final_cookies['history'], msg="Detected cached documents being left behind")
    return decorated


def update_ui(chatbot, history, msg='Normal', **kwargs):  # Refresh the page
    """
    Refresh the user interface
    """
    assert isinstance(chatbot, ChatBotWithCookies), "Do not discard it when passing the chatbot。If necessary, It can be cleared with clear if necessary, Then reassign with for+append loop。"
    cookies = chatbot.get_cookies()
    # Backup a copy of History as a record
    cookies.update({'history': history})
    # Solve the interface display problem when the plugin is locked
    if cookies.get('lock_plugin', None):
        label = cookies.get('llm_model', "") + " | " + "Locking plugin" + cookies.get('lock_plugin', None)
        chatbot_gr = gradio.update(value=chatbot, label=label)
        if cookies.get('label', "") != label: cookies['label'] = label   # Remember the current label.
    elif cookies.get('label', None):
        chatbot_gr = gradio.update(value=chatbot, label=cookies.get('llm_model', ""))
        cookies['label'] = None    # Clear label
    else:
        chatbot_gr = chatbot

    yield cookies, chatbot_gr, history, msg

def update_ui_lastest_msg(lastmsg, chatbot, history, delay=1):  # Refresh the page
    """
    Refresh the user interface
    """
    if len(chatbot) == 0: chatbot.append(["update_ui_last_msg", lastmsg])
    chatbot[-1] = list(chatbot[-1])
    chatbot[-1][-1] = lastmsg
    yield from update_ui(chatbot=chatbot, history=history)
    time.sleep(delay)


def trimmed_format_exc():
    import os, traceback
    str = traceback.format_exc()
    current_path = os.getcwd()
    replace_path = "."
    return str.replace(current_path, replace_path)

def CatchException(f):
    """
    Decorator function，Capture exceptions in function f and encapsulate them into a generator to return，And display it in the chat。
    """

    @wraps(f)
    def decorated(main_input, llm_kwargs, plugin_kwargs, chatbot_with_cookie, history, *args, **kwargs):
        try:
            yield from f(main_input, llm_kwargs, plugin_kwargs, chatbot_with_cookie, history, *args, **kwargs)
        except Exception as e:
            from void_terminal.check_proxy import check_proxy
            from void_terminal.toolbox import get_conf
            proxies = get_conf('proxies')
            tb_str = '```\n' + trimmed_format_exc() + '```'
            if len(chatbot_with_cookie) == 0:
                chatbot_with_cookie.clear()
                chatbot_with_cookie.append(["Plugin scheduling exception", "Exception reason"])
            chatbot_with_cookie[-1] = (chatbot_with_cookie[-1][0],
                           f"[Local Message] Experimental function call error: \n\n{tb_str} \n\nCurrent proxy availability: \n\n{check_proxy(proxies)}")
            yield from update_ui(chatbot=chatbot_with_cookie, history=history, msg=f'Exception {e}') # Refresh the page
    return decorated


def HotReload(f):
    """
    Decorator function of HotReload，Used to implement hot updates of Python function plugins。
    Function hot update refers to updating function code in real-time without stopping program execution，Update function code，To achieve real-time update function。
    Inside the decorator，Use wraps(f)Preserve the metadata of the function，and define an inner function named decorated。
    The inner function reloads and retrieves the function module by using the reload function of the importlib module and the getmodule function of the inspect module，
    Then it retrieves the function name using the getattr function，and reloads the function in the new module。
    Finally，it returns the reloaded function using the yield from statement，and executes it on the decorated function。
    Ultimately，the decorator function returns the inner function。which can update the original definition of the function to the latest version，and execute the new version of the function。
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        fn_name = f.__name__
        f_hot_reload = getattr(importlib.reload(inspect.getmodule(f)), fn_name)
        yield from f_hot_reload(*args, **kwargs)
    return decorated


"""
========================================================================
Second part
Other utilities:
    - write_history_to_file:    Write the results to a markdown file
    - regular_txt_to_markdown:  Convert plain text to Markdown formatted text。
    - report_execption:         Add simple unexpected error messages to the chatbot
    - text_divide_paragraph:    Split the text into paragraphs according to the paragraph separator，Generate HTML code with paragraph tags。
    - markdown_convertion:      Combine in various ways，Convert markdown to nice-looking HTML
    - format_io:                Take over the default markdown handling of gradio
    - on_file_uploaded:         Handle file uploads（Automatically decompress）
    - on_report_generated:      Automatically project the generated report to the file upload area
    - clip_history:             Automatically truncate when the historical context is too long，Automatic truncation
    - get_conf:                 Get settings
    - select_api_key:           According to the current model category，Extract available API keys
========================================================================
"""

def get_reduce_token_percent(text):
    """
        * This function will be deprecated in the future
    """
    try:
        # text = "maximum context length is 4097 tokens. However, your messages resulted in 4870 tokens"
        pattern = r"(\d+)\s+tokens\b"
        match = re.findall(pattern, text)
        EXCEED_ALLO = 500  # Leave a little room，Otherwise, there will be problems with insufficient space when replying
        max_limit = float(match[0]) - EXCEED_ALLO
        current_tokens = float(match[1])
        ratio = max_limit/current_tokens
        assert ratio > 0 and ratio < 1
        return ratio, str(int(current_tokens-max_limit))
    except:
        return 0.5, 'Unknown'


def write_history_to_file(history, file_basename=None, file_fullname=None, auto_caption=True):
    """
    Write the conversation record history to a file in Markdown format。If no file name is specified，Generate a file name using the current time。
    """
    import os
    import time
    if file_fullname is None:
        if file_basename is not None:
            file_fullname = pj(get_log_folder(), file_basename)
        else:
            file_fullname = pj(get_log_folder(), f'GPT-Academic-{gen_time_str()}.md')
    os.makedirs(os.path.dirname(file_fullname), exist_ok=True)
    with open(file_fullname, 'w', encoding='utf8') as f:
        f.write('# GPT-Academic Report\n')
        for i, content in enumerate(history):
            try:    
                if type(content) != str: content = str(content)
            except:
                continue
            if i % 2 == 0 and auto_caption:
                f.write('## ')
            try:
                f.write(content)
            except:
                # remove everything that cannot be handled by utf8
                f.write(content.encode('utf-8', 'ignore').decode())
            f.write('\n\n')
    res = os.path.abspath(file_fullname)
    return res


def regular_txt_to_markdown(text):
    """
    Convert plain text to Markdown formatted text。
    """
    text = text.replace('\n', '\n\n')
    text = text.replace('\n\n\n', '\n\n')
    text = text.replace('\n\n\n', '\n\n')
    return text




def report_execption(chatbot, history, a, b):
    """
    Add error information to the chatbot
    """
    chatbot.append((a, b))
    history.extend([a, b])


def text_divide_paragraph(text):
    """
    Split the text into paragraphs according to the paragraph separator，Generate HTML code with paragraph tags。
    """
    pre = '<div class="markdown-body">'
    suf = '</div>'
    if text.startswith(pre) and text.endswith(suf):
        return text
    
    if '```' in text:
        # careful input
        return pre + text + suf
    else:
        # wtf input
        lines = text.split("\n")
        for i, line in enumerate(lines):
            lines[i] = lines[i].replace(" ", "&nbsp;")
        text = "</br>".join(lines)
        return pre + text + suf


@lru_cache(maxsize=128) # Use LRU cache to speed up conversion
def markdown_convertion(txt):
    """
    Convert Markdown format text to HTML format。If it contains mathematical formulas，Convert the formula to HTML format first。
    """
    pre = '<div class="markdown-body">'
    suf = '</div>'
    if txt.startswith(pre) and txt.endswith(suf):
        # print('Warning，Input a string that has already been converted，二次转化可能出Question')
        return txt # Has already been converted，No need to convert again
    
    markdown_extension_configs = {
        'mdx_math': {
            'enable_dollar_delimiter': True,
            'use_gitlab_delimiters': False,
        },
    }
    find_equation_pattern = r'<script type="math/tex(?:.*?)>(.*?)</script>'

    def tex2mathml_catch_exception(content, *args, **kwargs):
        try:
            content = tex2mathml(content, *args, **kwargs)
        except:
            content = content
        return content

    def replace_math_no_render(match):
        content = match.group(1)
        if 'mode=display' in match.group(0):
            content = content.replace('\n', '</br>')
            return f"<font color=\"#00FF00\">$$</font><font color=\"#FF00FF\">{content}</font><font color=\"#00FF00\">$$</font>"
        else:
            return f"<font color=\"#00FF00\">$</font><font color=\"#FF00FF\">{content}</font><font color=\"#00FF00\">$</font>"

    def replace_math_render(match):
        content = match.group(1)
        if 'mode=display' in match.group(0):
            if '\\begin{aligned}' in content:
                content = content.replace('\\begin{aligned}', '\\begin{array}')
                content = content.replace('\\end{aligned}', '\\end{array}')
                content = content.replace('&', ' ')
            content = tex2mathml_catch_exception(content, display="block")
            return content
        else:
            return tex2mathml_catch_exception(content)

    def markdown_bug_hunt(content):
        """
        Fix a bug in mdx_math（Redundant when wrapping begin command with single $<script>）
        """
        content = content.replace('<script type="math/tex">\n<script type="math/tex; mode=display">', '<script type="math/tex; mode=display">')
        content = content.replace('</script>\n</script>', '</script>')
        return content

    def is_equation(txt):
        """
        Determine whether it is a formula | Test 1 write out the Lorentz law，Use the tex format formula to test 2 and give the Cauchy inequality，Write Maxwell`s equations using latex format for test 3
        """
        if '```' in txt and '```reference' not in txt: return False
        if '$' not in txt and '\\[' not in txt: return False
        mathpatterns = {
            r'(?<!\\|\$)(\$)([^\$]+)(\$)': {'allow_multi_lines': False},                            #  $...$
            r'(?<!\\)(\$\$)([^\$]+)(\$\$)': {'allow_multi_lines': True},                            # $$...$$
            r'(?<!\\)(\\\[)(.+?)(\\\])': {'allow_multi_lines': False},                              # \[...\]
            # r'(?<!\\)(\\\()(.+?)(\\\))': {'allow_multi_lines': False},                            # \(...\)
            # r'(?<!\\)(\\begin{([a-z]+?\*?)})(.+?)(\\end{\2})': {'allow_multi_lines': True},       # \begin...\end
            # r'(?<!\\)(\$`)([^`]+)(`\$)': {'allow_multi_lines': False},                            # $`...`$
        }
        matches = []
        for pattern, property in mathpatterns.items():
            flags = re.ASCII|re.DOTALL if property['allow_multi_lines'] else re.ASCII
            matches.extend(re.findall(pattern, txt, flags))
        if len(matches) == 0: return False
        contain_any_eq = False
        illegal_pattern = re.compile(r'[^\x00-\x7F]|echo')
        for match in matches:
            if len(match) != 3: return False
            eq_canidate = match[1]
            if illegal_pattern.search(eq_canidate): 
                return False
            else: 
                contain_any_eq = True
        return contain_any_eq

    def fix_markdown_indent(txt):
        # fix markdown indent
        if (' - ' not in txt) or ('. ' not in txt): 
            return txt # do not need to fix, fast escape
        # walk through the lines and fix non-standard indentation
        lines = txt.split("\n")
        pattern = re.compile(r'^\s+-')
        activated = False
        for i, line in enumerate(lines):
            if line.startswith('- ') or line.startswith('1. '):
                activated = True
            if activated and pattern.match(line):
                stripped_string = line.lstrip()
                num_spaces = len(line) - len(stripped_string)
                if (num_spaces % 4) == 3:
                    num_spaces_should_be = math.ceil(num_spaces/4) * 4
                    lines[i] = ' ' * num_spaces_should_be + stripped_string
        return '\n'.join(lines)

    txt = fix_markdown_indent(txt)
    if is_equation(txt):  # Formula symbol with $ sign，And there is no code section```Identifier of
        # convert everything to html format
        split = markdown.markdown(text='---')
        convert_stage_1 = markdown.markdown(text=txt, extensions=['sane_lists', 'tables', 'mdx_math', 'fenced_code'], extension_configs=markdown_extension_configs)
        convert_stage_1 = markdown_bug_hunt(convert_stage_1)
        # 1. convert to easy-to-copy tex (do not render math)
        convert_stage_2_1, n = re.subn(find_equation_pattern, replace_math_no_render, convert_stage_1, flags=re.DOTALL)
        # 2. convert to rendered equation
        convert_stage_2_2, n = re.subn(find_equation_pattern, replace_math_render, convert_stage_1, flags=re.DOTALL)
        # cat them together
        return pre + convert_stage_2_1 + f'{split}' + convert_stage_2_2 + suf
    else:
        return pre + markdown.markdown(txt, extensions=['sane_lists', 'tables', 'fenced_code', 'codehilite']) + suf


def close_up_code_segment_during_stream(gpt_reply):
    """
    In the middle of outputting code with GPT（Output the front part```，But haven`t output the back part yet```），Complete the back part```

    Args:
        gpt_reply (str): Reply string returned by GPT model。

    Returns:
        str: Return a new string，Append the back part of output code snippet```to it。

    """
    if '```' not in gpt_reply:
        return gpt_reply
    if gpt_reply.endswith('```'):
        return gpt_reply

    # Exclude the above two cases，We
    segments = gpt_reply.split('```')
    n_mark = len(segments) - 1
    if n_mark % 2 == 1:
        # print('Output代码Segment中！')
        return gpt_reply+'\n```'
    else:
        return gpt_reply


def format_io(self, y):
    """
    Parse input and output as HTML format。Paragraphize the input part of the last item in y，And convert the output part of Markdown and math formulas to HTML format。
    """
    if y is None or y == []:
        return []
    i_ask, gpt_reply = y[-1]
    # The input part is too free，Preprocess it
    if i_ask is not None: i_ask = text_divide_paragraph(i_ask)
    # When the code output is halfway，Try to fill in the latter```
    if gpt_reply is not None: gpt_reply = close_up_code_segment_during_stream(gpt_reply)
    # process
    y[-1] = (
        None if i_ask is None else markdown.markdown(i_ask, extensions=['fenced_code', 'tables']),
        None if gpt_reply is None else markdown_convertion(gpt_reply)
    )
    return y


def find_free_port():
    """
    Return an available unused port in the current system。
    """
    import socket
    from contextlib import closing
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


def extract_archive(file_path, dest_dir):
    import zipfile
    import tarfile
    import os
    # Get the file extension of the input file
    file_extension = os.path.splitext(file_path)[1]

    # Extract the archive based on its extension
    if file_extension == '.zip':
        with zipfile.ZipFile(file_path, 'r') as zipobj:
            zipobj.extractall(path=dest_dir)
            print("Successfully extracted zip archive to {}".format(dest_dir))

    elif file_extension in ['.tar', '.gz', '.bz2']:
        with tarfile.open(file_path, 'r:*') as tarobj:
            tarobj.extractall(path=dest_dir)
            print("Successfully extracted tar archive to {}".format(dest_dir))

    # Third-party library，Need to pip install rarfile in advance
    # In addition，WinRAR software needs to be installed on Windows，Configure its Path environment variable，如"C:\Program Files\WinRAR"才可以
    elif file_extension == '.rar':
        try:
            import rarfile
            with rarfile.RarFile(file_path) as rf:
                rf.extractall(path=dest_dir)
                print("Successfully extracted rar archive to {}".format(dest_dir))
        except:
            print("Rar format requires additional dependencies to install")
            return '\n\nDecompression failed! Install `pip install rarfile` to decompress rar files。Suggestion：Using zip compression format。'

    # Third-party library，Need to pip install py7zr in advance
    elif file_extension == '.7z':
        try:
            import py7zr
            with py7zr.SevenZipFile(file_path, mode='r') as f:
                f.extractall(path=dest_dir)
                print("Successfully extracted 7z archive to {}".format(dest_dir))
        except:
            print("7z format requires additional dependencies to install")
            return '\n\nDecompression failed! Install `pip install py7zr` to decompress 7z files'
    else:
        return ''
    return ''


def find_recent_files(directory):
    """
        me: find files that is created with in one minutes under a directory with python, write a function
        gpt: here it is!
    """
    import os
    import time
    current_time = time.time()
    one_minute_ago = current_time - 60
    recent_files = []
    if not os.path.exists(directory): 
        os.makedirs(directory, exist_ok=True)
    for filename in os.listdir(directory):
        file_path = pj(directory, filename)
        if file_path.endswith('.log'):
            continue
        created_time = os.path.getmtime(file_path)
        if created_time >= one_minute_ago:
            if os.path.isdir(file_path):
                continue
            recent_files.append(file_path)

    return recent_files

def promote_file_to_downloadzone(file, rename_file=None, chatbot=None):
    # Make a copy of the file in the download area
    import shutil
    if rename_file is None: rename_file = f'{gen_time_str()}-{os.path.basename(file)}'
    new_path = pj(get_log_folder(), rename_file)
    # If it already exists，Delete first
    if os.path.exists(new_path) and not os.path.samefile(new_path, file): os.remove(new_path)
    # Copy the file over
    if not os.path.exists(new_path): shutil.copyfile(file, new_path)
    # Add files to chatbot cookie，Avoid multiple user interference
    if chatbot is not None:
        if 'files_to_promote' in chatbot._cookies: current = chatbot._cookies['files_to_promote']
        else: current = []
        chatbot._cookies.update({'files_to_promote': [new_path] + current})
    return new_path

def disable_auto_promotion(chatbot):
    chatbot._cookies.update({'files_to_promote': []})
    return

def is_the_upload_folder(string):
    PATH_PRIVATE_UPLOAD = get_conf('PATH_PRIVATE_UPLOAD')
    pattern = r'^PATH_PRIVATE_UPLOAD/[A-Za-z0-9_-]+/\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}$'
    pattern = pattern.replace('PATH_PRIVATE_UPLOAD', PATH_PRIVATE_UPLOAD)
    if re.match(pattern, string): return True
    else: return False

def del_outdated_uploads(outdate_time_seconds):
    PATH_PRIVATE_UPLOAD = get_conf('PATH_PRIVATE_UPLOAD')
    current_time = time.time()
    one_hour_ago = current_time - outdate_time_seconds
    # Get a list of all subdirectories in the PATH_PRIVATE_UPLOAD folder
    # Remove subdirectories that are older than one hour
    for subdirectory in glob.glob(f'{PATH_PRIVATE_UPLOAD}/*/*'):
        subdirectory_time = os.path.getmtime(subdirectory)
        if subdirectory_time < one_hour_ago:
            try: shutil.rmtree(subdirectory)
            except: pass
    return

def on_file_uploaded(request: gradio.Request, files, chatbot, txt, txt2, checkboxes, cookies):
    """
    Callback function when a file is uploaded
    """
    if len(files) == 0:
        return chatbot, txt
    
    # Remove outdated old files to save space & protect privacy
    outdate_time_seconds = 60
    del_outdated_uploads(outdate_time_seconds)

    # Create a working directory
    user_name = "default" if not request.username else request.username
    time_tag = gen_time_str()
    PATH_PRIVATE_UPLOAD = get_conf('PATH_PRIVATE_UPLOAD')
    target_path_base = pj(PATH_PRIVATE_UPLOAD, user_name, time_tag)
    os.makedirs(target_path_base, exist_ok=True)

    # Move each file to the target path
    upload_msg = ''
    for file in files:
        file_origin_name = os.path.basename(file.orig_name)
        this_file_path = pj(target_path_base, file_origin_name)
        shutil.move(file.name, this_file_path)
        upload_msg += extract_archive(file_path=this_file_path, dest_dir=this_file_path+'.extract')
    
    # Organize file collection
    moved_files = [fp for fp in glob.glob(f'{target_path_base}/**/*', recursive=True)]
    if "Floating input area" in checkboxes: 
        txt, txt2 = "", target_path_base
    else:
        txt, txt2 = target_path_base, ""

    # Output message
    moved_files_str = '\t\n\n'.join(moved_files)
    chatbot.append(['I uploaded a file，Please check', 
                    f'[Local Message] Received the following files: \n\n{moved_files_str}' +
                    f'\n\nThe call path parameter has been automatically corrected to: \n\n{txt}' +
                    f'\n\nNow when you click on any function plugin，The above files will be used as input parameters'+upload_msg])
    
    # Record recent files
    cookies.update({
        'most_recent_uploaded': {
            'path': target_path_base,
            'time': time.time(),
            'time_str': time_tag
    }})
    return chatbot, txt, txt2, cookies


def on_report_generated(cookies, files, chatbot):
    from void_terminal.toolbox import find_recent_files
    PATH_LOGGING = get_conf('PATH_LOGGING')
    if 'files_to_promote' in cookies:
        report_files = cookies['files_to_promote']
        cookies.pop('files_to_promote')
    else:
        report_files = find_recent_files(PATH_LOGGING)
    if len(report_files) == 0:
        return cookies, None, chatbot
    # files.extend(report_files)
    file_links = ''
    for f in report_files: file_links += f'<br/><a href="file={os.path.abspath(f)}" target="_blank">{f}</a>'
    chatbot.append(['Report how to obtain remotely？', f'The report has been added to the `File Upload Area` on the right（It may be in a collapsed state），Please check。{file_links}'])
    return cookies, report_files, chatbot

def load_chat_cookies():
    API_KEY, LLM_MODEL, AZURE_API_KEY = get_conf('API_KEY', 'LLM_MODEL', 'AZURE_API_KEY')
    AZURE_CFG_ARRAY, NUM_CUSTOM_BASIC_BTN = get_conf('AZURE_CFG_ARRAY', 'NUM_CUSTOM_BASIC_BTN')

    # deal with azure openai key
    if is_any_api_key(AZURE_API_KEY):
        if is_any_api_key(API_KEY): API_KEY = API_KEY + ',' + AZURE_API_KEY
        else: API_KEY = AZURE_API_KEY
    if len(AZURE_CFG_ARRAY) > 0:
        for azure_model_name, azure_cfg_dict in AZURE_CFG_ARRAY.items():
            if not azure_model_name.startswith('azure'): 
                raise ValueError("AZURE_CFG_ARRAY中配置的模型必须以azure开头")
            AZURE_API_KEY_ = azure_cfg_dict["AZURE_API_KEY"]
            if is_any_api_key(AZURE_API_KEY_):
                if is_any_api_key(API_KEY): API_KEY = API_KEY + ',' + AZURE_API_KEY_
                else: API_KEY = AZURE_API_KEY_

    customize_fn_overwrite_ = {}
    for k in range(NUM_CUSTOM_BASIC_BTN):
        customize_fn_overwrite_.update({  
            "Custom button" + str(k+1):{
                "Title":    r"",
                "Prefix":   r"Please define the prefix of the prompt word in the custom menu.",
                "Suffix":   r"Please define the suffix of the prompt word in the custom menu",
            }
        })
    return {'api_key': API_KEY, 'llm_model': LLM_MODEL, 'customize_fn_overwrite': customize_fn_overwrite_}

def is_openai_api_key(key):
    CUSTOM_API_KEY_PATTERN = get_conf('CUSTOM_API_KEY_PATTERN')
    if len(CUSTOM_API_KEY_PATTERN) != 0:
        API_MATCH_ORIGINAL = re.match(CUSTOM_API_KEY_PATTERN, key)
    else:
        API_MATCH_ORIGINAL = re.match(r"sk-[a-zA-Z0-9]{48}$", key)
    return bool(API_MATCH_ORIGINAL)

def is_azure_api_key(key):
    API_MATCH_AZURE = re.match(r"[a-zA-Z0-9]{32}$", key)
    return bool(API_MATCH_AZURE)

def is_api2d_key(key):
    API_MATCH_API2D = re.match(r"fk[a-zA-Z0-9]{6}-[a-zA-Z0-9]{32}$", key)
    return bool(API_MATCH_API2D)

def is_any_api_key(key):
    if ',' in key:
        keys = key.split(',')
        for k in keys:
            if is_any_api_key(k): return True
        return False
    else:
        return is_openai_api_key(key) or is_api2d_key(key) or is_azure_api_key(key)

def what_keys(keys):
    avail_key_list = {'OpenAI Key':0, "Azure Key":0, "API2D Key":0}
    key_list = keys.split(',')

    for k in key_list:
        if is_openai_api_key(k): 
            avail_key_list['OpenAI Key'] += 1

    for k in key_list:
        if is_api2d_key(k): 
            avail_key_list['API2D Key'] += 1

    for k in key_list:
        if is_azure_api_key(k): 
            avail_key_list['Azure Key'] += 1

    return f"Detected： OpenAI Key {avail_key_list['OpenAI Key']} items, Azure Key {avail_key_list['Azure Key']} items, API2D Key {avail_key_list['API2D Key']} items"

def select_api_key(keys, llm_model):
    import random
    avail_key_list = []
    key_list = keys.split(',')

    if llm_model.startswith('gpt-'):
        for k in key_list:
            if is_openai_api_key(k): avail_key_list.append(k)

    if llm_model.startswith('api2d-'):
        for k in key_list:
            if is_api2d_key(k): avail_key_list.append(k)

    if llm_model.startswith('azure-'):
        for k in key_list:
            if is_azure_api_key(k): avail_key_list.append(k)

    if len(avail_key_list) == 0:
        raise RuntimeError(f"The api-key you provided does not meet the requirements，Does not contain any that can be used for{llm_model}api-key。You may have selected the wrong model or request source（OpenAI can be switched in the model menu in the lower right corner,azure,claude,api2d and other request sources）。")

    api_key = random.choice(avail_key_list) # Random load balancing
    return api_key

def read_env_variable(arg, default_value):
    """
    Environment variables can be `GPT_ACADEMIC_CONFIG`(preferred)，or can be directly`CONFIG`
    For example, in windows cmd，it can be written as：
        set USE_PROXY=True
        set API_KEY=sk-j7caBpkRoxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        set proxies={"http":"http://127.0.0.1:10085", "https":"http://127.0.0.1:10085",}
        set AVAIL_LLM_MODELS=["gpt-3.5-turbo", "chatglm"]
        set AUTHENTICATION=[("username", "password"), ("username2", "password2")]
    or as：
        set GPT_ACADEMIC_USE_PROXY=True
        set GPT_ACADEMIC_API_KEY=sk-j7caBpkRoxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        set GPT_ACADEMIC_proxies={"http":"http://127.0.0.1:10085", "https":"http://127.0.0.1:10085",}
        set GPT_ACADEMIC_AVAIL_LLM_MODELS=["gpt-3.5-turbo", "chatglm"]
        set GPT_ACADEMIC_AUTHENTICATION=[("username", "password"), ("username2", "password2")]
    """
    from void_terminal.colorful import PrintBrightRed, PrintBrightGreen
    arg_with_prefix = "GPT_ACADEMIC_" + arg 
    if arg_with_prefix in os.environ: 
        env_arg = os.environ[arg_with_prefix]
    elif arg in os.environ: 
        env_arg = os.environ[arg]
    else:
        raise KeyError
    print(f"[ENV_VAR] Attempting to load{arg}，Default value：{default_value} --> Corrected value：{env_arg}")
    try:
        if isinstance(default_value, bool):
            env_arg = env_arg.strip()
            if env_arg == 'True': r = True
            elif env_arg == 'False': r = False
            else: print('enter True or False, but have:', env_arg); r = default_value
        elif isinstance(default_value, int):
            r = int(env_arg)
        elif isinstance(default_value, float):
            r = float(env_arg)
        elif isinstance(default_value, str):
            r = env_arg.strip()
        elif isinstance(default_value, dict):
            r = eval(env_arg)
        elif isinstance(default_value, list):
            r = eval(env_arg)
        elif default_value is None:
            assert arg == "proxies"
            r = eval(env_arg)
        else:
            PrintBrightRed(f"[ENV_VAR] Environment variable{arg}Setting through environment variables is not supported! ")
            raise KeyError
    except:
        PrintBrightRed(f"[ENV_VAR] Environment variable{arg}Loading failed! ")
        raise KeyError(f"[ENV_VAR] Environment variable{arg}Loading failed! ")

    PrintBrightGreen(f"[ENV_VAR] Successfully read environment variables{arg}")
    return r

@lru_cache(maxsize=128)
def read_single_conf_with_lru_cache(arg):
    from void_terminal.colorful import PrintBrightRed, PrintBrightGreen, PrintBrightBlue
    try:
        # Priority 1. Get environment variables as configuration
        default_ref = getattr(importlib.import_module('void_terminal.config'), arg)   # Read the default value as a reference for data type conversion
        r = read_env_variable(arg, default_ref) 
    except:
        try:
            # Priority 2. Get the configuration in config_private
            r = getattr(importlib.import_module('void_terminal.config_private'), arg)
        except:
            # Priority 3. Get the configuration in config
            r = getattr(importlib.import_module('void_terminal.config'), arg)

    # When reading API_KEY，Check if you forgot to change the config
    if arg == 'API_KEY':
        PrintBrightBlue(f"[API_KEY] This project now supports OpenAI and Azure`s api-key。It also supports filling in multiple api-keys at the same time，如API_KEY=\"openai-key1,openai-key2,azure-key3\"")
        PrintBrightBlue(f"[API_KEY] You can modify the api-key in config.py(s)，You can also enter a temporary api-key in the question input area(s)，After submitting with the enter key, it will take effect。")
        if is_any_api_key(r):
            PrintBrightGreen(f"[API_KEY] Your API_KEY is: {r[:15]}*** API_KEY imported successfully")
        else:
            PrintBrightRed( "[API_KEY] Your API_KEY does not meet any known key format，Please modify the API key in the config file before running。")
    if arg == 'proxies':
        if not read_single_conf_with_lru_cache('USE_PROXY'): r = None   # Check USE_PROXY，Prevent proxies from working alone
        if r is None:
            PrintBrightRed('[PROXY] Network proxy status：Not configured。It is very likely that you cannot access OpenAI`s models without a proxy。Suggestion：Check if the USE_PROXY option has been modified。')
        else:
            PrintBrightGreen('[PROXY] Network proxy status：Configured。Configuration information is as follows：', r)
            assert isinstance(r, dict), 'Proxies format error，Please note the format of the proxies option，Do not miss the parentheses。'
    return r


@lru_cache(maxsize=128)
def get_conf(*args):
    # We suggest you to copy a config_private.py file to keep your secrets, such as API and proxy URLs, from being accidentally uploaded to Github and seen by others., Such as API and proxy URLs, Avoid being accidentally uploaded to Github and seen by others
    res = []
    for arg in args:
        r = read_single_conf_with_lru_cache(arg)
        res.append(r)
    if len(res) == 1: return res[0]
    return res


def clear_line_break(txt):
    txt = txt.replace('\n', ' ')
    txt = txt.replace('  ', ' ')
    txt = txt.replace('  ', ' ')
    return txt


class DummyWith():
    """
    This code defines an empty context manager named DummyWith，
    Its purpose is...um...to not do anything，That is, to replace other context managers without changing the code structure。
    Context managers are a type of Python object，Used in conjunction with the with statement，
    To ensure that some resources are properly initialized and cleaned up during code block execution。
    Context managers must implement two methods，They are __enter__()and __exit__()。
    At the beginning of the context execution，__enter__()The method is called before the code block is executed，
    While at the end of the context execution，__exit__()The method is called。
    """
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return

def run_gradio_in_subpath(demo, auth, port, custom_path):
    """
    Change the running address of Gradio to the specified secondary path
    """
    def is_path_legal(path: str)->bool:
        '''
        check path for sub url
        path: path to check
        return value: do sub url wrap
        '''
        if path == "/": return True
        if len(path) == 0:
            print("ilegal custom path: {}\npath must not be empty\ndeploy on root url".format(path))
            return False
        if path[0] == '/':
            if path[1] != '/':
                print("deploy on sub-path {}".format(path))
                return True
            return False
        print("ilegal custom path: {}\npath should begin with \'/\'\ndeploy on root url".format(path))
        return False

    if not is_path_legal(custom_path): raise RuntimeError('Ilegal custom path')
    import uvicorn
    import gradio as gr
    from fastapi import FastAPI
    app = FastAPI()
    if custom_path != "/":
        @app.get("/")
        def read_main(): 
            return {"message": f"Gradio is running at: {custom_path}"}
    app = gr.mount_gradio_app(app, demo, path=custom_path)
    uvicorn.run(app, host="0.0.0.0", port=port) # , auth=auth


def clip_history(inputs, history, tokenizer, max_token_limit):
    """
    reduce the length of history by clipping.
    this function search for the longest entries to clip, little by little,
    until the number of token of history is reduced under threshold.
    Shorten the length of the history by trimming。 
    This function gradually searches for the longest entry to clip，
    Until the number of history markers is reduced to below the threshold。
    """
    import numpy as np
    from void_terminal.request_llms.bridge_all import model_info
    def get_token_num(txt): 
        return len(tokenizer.encode(txt, disallowed_special=()))
    input_token_num = get_token_num(inputs)
    if input_token_num < max_token_limit * 3 / 4:
        # When the token proportion of the input part is less than 3/4 of the limit，When trimming
        # 1. Leave the surplus of input
        max_token_limit = max_token_limit - input_token_num
        # 2. Leave the surplus used for output
        max_token_limit = max_token_limit - 128
        # 3. If the surplus is too small，Clear the history directly
        if max_token_limit < 128:
            history = []
            return history
    else:
        # When the token proportion of the input part > is 3/4 of the limit，Clear the history directly
        history = []
        return history

    everything = ['']
    everything.extend(history)
    n_token = get_token_num('\n'.join(everything))
    everything_token = [get_token_num(e) for e in everything]

    # Granularity when truncating
    delta = max(everything_token) // 16

    while n_token > max_token_limit:
        where = np.argmax(everything_token)
        encoded = tokenizer.encode(everything[where], disallowed_special=())
        clipped_encoded = encoded[:len(encoded)-delta]
        everything[where] = tokenizer.decode(clipped_encoded)[:-1]    # -1 to remove the may-be illegal char
        everything_token[where] = get_token_num(everything[where])
        n_token = get_token_num('\n'.join(everything))

    history = everything[1:]
    return history

"""
========================================================================
Part III
Other utilities:
    - zip_folder:    Compress all files under a certain path，Then move to a specified path（Written by GPT）
    - gen_time_str:  Generate a timestamp
    - ProxyNetworkActivate: Temporarily start proxy network（If there is）
    - objdump/objload: Convenient debugging function
========================================================================
"""

def zip_folder(source_folder, dest_folder, zip_name):
    import zipfile
    import os
    # Make sure the source folder exists
    if not os.path.exists(source_folder):
        print(f"{source_folder} does not exist")
        return

    # Make sure the destination folder exists
    if not os.path.exists(dest_folder):
        print(f"{dest_folder} does not exist")
        return

    # Create the name for the zip file
    zip_file = pj(dest_folder, zip_name)

    # Create a ZipFile object
    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Walk through the source folder and add files to the zip file
        for foldername, subfolders, filenames in os.walk(source_folder):
            for filename in filenames:
                filepath = pj(foldername, filename)
                zipf.write(filepath, arcname=os.path.relpath(filepath, source_folder))

    # Move the zip file to the destination folder (if it wasn't already there)
    if os.path.dirname(zip_file) != dest_folder:
        os.rename(zip_file, pj(dest_folder, os.path.basename(zip_file)))
        zip_file = pj(dest_folder, os.path.basename(zip_file))

    print(f"Zip file created at {zip_file}")

def zip_result(folder):
    t = gen_time_str()
    zip_folder(folder, get_log_folder(), f'{t}-result.zip')
    return pj(get_log_folder(), f'{t}-result.zip')

def gen_time_str():
    import time
    return time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())

def get_log_folder(user='default', plugin_name='shared'):
    PATH_LOGGING = get_conf('PATH_LOGGING')
    _dir = pj(PATH_LOGGING, user, plugin_name)
    if not os.path.exists(_dir): os.makedirs(_dir)
    return _dir

class ProxyNetworkActivate():
    """
    This code defines an empty context manager named TempProxy, Used to proxy a small piece of code
    """
    def __init__(self, task=None) -> None:
        self.task = task
        if not task:
            # No task given, Then we default to proxy
            self.valid = True
        else:
            # Given a task, Let`s check
            from void_terminal.toolbox import get_conf
            WHEN_TO_USE_PROXY = get_conf('WHEN_TO_USE_PROXY')
            self.valid = (task in WHEN_TO_USE_PROXY)

    def __enter__(self):
        if not self.valid: return self
        from void_terminal.toolbox import get_conf
        proxies = get_conf('proxies')
        if 'no_proxy' in os.environ: os.environ.pop('no_proxy')
        if proxies is not None:
            if 'http' in proxies: os.environ['HTTP_PROXY'] = proxies['http']
            if 'https' in proxies: os.environ['HTTPS_PROXY'] = proxies['https']
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        os.environ['no_proxy'] = '*'
        if 'HTTP_PROXY' in os.environ: os.environ.pop('HTTP_PROXY')
        if 'HTTPS_PROXY' in os.environ: os.environ.pop('HTTPS_PROXY')
        return

def objdump(obj, file='objdump.tmp'):
    import pickle
    with open(file, 'wb+') as f:
        pickle.dump(obj, f)
    return

def objload(file='objdump.tmp'):
    import pickle, os
    if not os.path.exists(file): 
        return
    with open(file, 'rb') as f:
        return pickle.load(f)
    
def Singleton(cls):
    """
    Single instance decorator
    """
    _instance = {}
 
    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]
 
    return _singleton

"""
========================================================================
Part Four
接驳void-terminal:
    - set_conf:                     Dynamically modify configurations during runtime
    - set_multi_conf:               Dynamically modify multiple configurations during runtime
    - get_plugin_handle:            Get handle of plugin
    - get_plugin_default_kwargs:    Get default parameters of plugin
    - get_chat_handle:              Get handle of simple chat
    - get_chat_default_kwargs:      Get default parameters for simple chat
========================================================================
"""

def set_conf(key, value):
    from void_terminal.toolbox import read_single_conf_with_lru_cache, get_conf
    read_single_conf_with_lru_cache.cache_clear()
    get_conf.cache_clear()
    os.environ[key] = str(value)
    altered = get_conf(key)
    return altered

def set_multi_conf(dic):
    for k, v in dic.items(): set_conf(k, v)
    return

def get_plugin_handle(plugin_name):
    """
    e.g. plugin_name = 'crazy_functions.BatchTranslateMarkdown->TranslateMarkdownToSpecifiedLanguage'
    """
    import importlib
    assert '->' in plugin_name, \
        "Example of plugin_name: crazy_functions.BatchTranslateMarkdown->TranslateMarkdownToSpecifiedLanguage"
    module, fn_name = plugin_name.split('->')
    f_hot_reload = getattr(importlib.import_module(module, fn_name), fn_name)
    return f_hot_reload

def get_chat_handle():
    """
    """
    from void_terminal.request_llms.bridge_all import predict_no_ui_long_connection
    return predict_no_ui_long_connection

def get_plugin_default_kwargs():
    """
    """
    from void_terminal.toolbox import get_conf, ChatBotWithCookies

    WEB_PORT, LLM_MODEL, API_KEY = \
        get_conf('WEB_PORT', 'LLM_MODEL', 'API_KEY')

    llm_kwargs = {
        'api_key': API_KEY,
        'llm_model': LLM_MODEL,
        'top_p':1.0, 
        'max_length': None,
        'temperature':1.0,
    }
    chatbot = ChatBotWithCookies(llm_kwargs)

    # txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port
    DEFAULT_FN_GROUPS_kwargs = {
        "main_input": "./README.md",
        "llm_kwargs": llm_kwargs,
        "plugin_kwargs": {},
        "chatbot_with_cookie": chatbot,
        "history": [],
        "system_prompt": "You are a good AI.", 
        "web_port": WEB_PORT
    }
    return DEFAULT_FN_GROUPS_kwargs

def get_chat_default_kwargs():
    """
    """
    from void_terminal.toolbox import get_conf

    LLM_MODEL, API_KEY = get_conf('LLM_MODEL', 'API_KEY')

    llm_kwargs = {
        'api_key': API_KEY,
        'llm_model': LLM_MODEL,
        'top_p':1.0, 
        'max_length': None,
        'temperature':1.0,
    }

    default_chat_kwargs = {
        "inputs": "Hello there, are you ready?",
        "llm_kwargs": llm_kwargs,
        "history": [],
        "sys_prompt": "You are AI assistant",
        "observe_window": None,
        "console_slience": False,
    }

    return default_chat_kwargs

