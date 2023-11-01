from void_terminal.toolbox import update_ui, get_conf, trimmed_format_exc, get_log_folder
import threading
import os
import logging

def input_clipping(inputs, history, max_token_limit):
    import numpy as np
    from void_terminal.request_llms.bridge_all import model_info
    enc = model_info["gpt-3.5-turbo"]['tokenizer']
    def get_token_num(txt): return len(enc.encode(txt, disallowed_special=()))

    mode = 'input-and-history'
    # When the proportion of tokens in the input part is less than half of the entire text，Trim only history
    input_token_num = get_token_num(inputs)
    if input_token_num < max_token_limit//2: 
        mode = 'only-history'
        max_token_limit = max_token_limit - input_token_num

    everything = [inputs] if mode == 'input-and-history' else ['']
    everything.extend(history)
    n_token = get_token_num('\n'.join(everything))
    everything_token = [get_token_num(e) for e in everything]
    delta = max(everything_token) // 16 # Granularity when truncating
        
    while n_token > max_token_limit:
        where = np.argmax(everything_token)
        encoded = enc.encode(everything[where], disallowed_special=())
        clipped_encoded = encoded[:len(encoded)-delta]
        everything[where] = enc.decode(clipped_encoded)[:-1]    # -1 to remove the may-be illegal char
        everything_token[where] = get_token_num(everything[where])
        n_token = get_token_num('\n'.join(everything))

    if mode == 'input-and-history':
        inputs = everything[0]
    else:
        pass
    history = everything[1:]
    return inputs, history

def request_gpt_model_in_new_thread_with_ui_alive(
        inputs, inputs_show_user, llm_kwargs, 
        chatbot, history, sys_prompt, refresh_interval=0.2,
        handle_token_exceed=True, 
        retry_times_at_unknown_error=2,
        ):
    """
    Request GPT model，Request GPT model while keeping the user interface active。

    Input parameter Args （Input variables ending in _array are all lists，The length of the list is the number of sub-tasks，When executing，The list will be broken down，And executed separately in each sub-thread）:
        inputs (string): List of inputs （Input）
        inputs_show_user (string): List of inputs to show user（Input displayed in the report，With the help of this parameter，Hide verbose real input in the summary report，Enhance the readability of the report）
        top_p (float): Top p value for sampling from model distribution （GPT parameters，Floating point number）
        temperature (float): Temperature value for sampling from model distribution（GPT parameters，Floating point number）
        chatbot: chatbot inputs and outputs （Handle of the user interface dialog window，Used for data flow visualization）
        history (list): List of chat history （History，List of conversation history）
        sys_prompt (string): List of system prompts （System input，List，Prompt for input to GPT，For example, if you are a translator, how to...）
        refresh_interval (float, optional): Refresh interval for UI (default: 0.2) （Refresh time interval frequency，Suggested to be less than 1，Cannot be higher than 3，Only serves for visual effects）
        handle_token_exceed：Whether to automatically handle token overflow，If selected to handle automatically，It will be forcefully truncated when overflow occurs，Default enabled
        retry_times_at_unknown_error：Number of retries when failed

    Output Returns:
        future: Output，Result returned by GPT
    """
    import time
    from concurrent.futures import ThreadPoolExecutor
    from void_terminal.request_llms.bridge_all import predict_no_ui_long_connection
    # User feedback
    chatbot.append([inputs_show_user, ""])
    yield from update_ui(chatbot=chatbot, history=[]) # Refresh the page
    executor = ThreadPoolExecutor(max_workers=16)
    mutable = ["", time.time(), ""]
    # Watchdog patience
    watch_dog_patience = 5
    # Request Task
    def _req_gpt(inputs, history, sys_prompt):
        retry_op = retry_times_at_unknown_error
        exceeded_cnt = 0
        while True:
            # watchdog error
            if len(mutable) >= 2 and (time.time()-mutable[1]) > watch_dog_patience: 
                raise RuntimeError("Program termination detected。")
            try:
                # 【First scenario】：Completed smoothly
                result = predict_no_ui_long_connection(
                    inputs=inputs, llm_kwargs=llm_kwargs,
                    history=history, sys_prompt=sys_prompt, observe_window=mutable)
                return result
            except ConnectionAbortedError as token_exceeded_error:
                # 【Second scenario】：Token overflow
                if handle_token_exceed:
                    exceeded_cnt += 1
                    # 【Choose processing】 Attempt to calculate ratio，Retain text as much as possible
                    from void_terminal.toolbox import get_reduce_token_percent
                    p_ratio, n_exceed = get_reduce_token_percent(str(token_exceeded_error))
                    MAX_TOKEN = 4096
                    EXCEED_ALLO = 512 + 512 * exceeded_cnt
                    inputs, history = input_clipping(inputs, history, max_token_limit=MAX_TOKEN-EXCEED_ALLO)
                    mutable[0] += f'[Local Message] Warning，Text will be truncated if too long，Token overflow count：{n_exceed}。\n\n'
                    continue # Return and retry
                else:
                    # 【Choose to give up】
                    tb_str = '```\n' + trimmed_format_exc() + '```'
                    mutable[0] += f"[Local Message] Warning，Encountered a problem during execution, Traceback：\n\n{tb_str}\n\n"
                    return mutable[0] # Give up
            except:
                # 【Third scenario】：Other errors：Retry several times
                tb_str = '```\n' + trimmed_format_exc() + '```'
                print(tb_str)
                mutable[0] += f"[Local Message] Warning，Encountered a problem during execution, Traceback：\n\n{tb_str}\n\n"
                if retry_op > 0:
                    retry_op -= 1
                    mutable[0] += f"[Local Message] Retrying，Please wait {retry_times_at_unknown_error-retry_op}/{retry_times_at_unknown_error}：\n\n"
                    if ("Rate limit reached" in tb_str) or ("Too Many Requests" in tb_str):
                        time.sleep(30)
                    time.sleep(5)
                    continue # Return and retry
                else:
                    time.sleep(5)
                    return mutable[0] # Give up

    # Submit task
    future = executor.submit(_req_gpt, inputs, history, sys_prompt)
    while True:
        # Yield once to refresh the front-end page
        time.sleep(refresh_interval)
        # Feed the dog（Watchdog）
        mutable[1] = time.time()
        if future.done():
            break
        chatbot[-1] = [chatbot[-1][0], mutable[0]]
        yield from update_ui(chatbot=chatbot, history=[]) # Refresh the page

    final_result = future.result()
    chatbot[-1] = [chatbot[-1][0], final_result]
    yield from update_ui(chatbot=chatbot, history=[]) # If successful in the end，Delete error message
    return final_result

def can_multi_process(llm):
    if llm.startswith('gpt-'): return True
    if llm.startswith('api2d-'): return True
    if llm.startswith('azure-'): return True
    return False

def request_gpt_model_multi_threads_with_very_awesome_ui_and_high_efficiency(
        inputs_array, inputs_show_user_array, llm_kwargs, 
        chatbot, history_array, sys_prompt_array, 
        refresh_interval=0.2, max_workers=-1, scroller_max_len=30,
        handle_token_exceed=True, show_user_at_complete=False,
        retry_times_at_unknown_error=2,
        ):
    """
    Request GPT model using multiple threads with UI and high efficiency
    Requesting GPT model[Multithreading]version。
    Features include：
        Real-time feedback of remote data streams on UI
        Using thread pool，The size of the thread pool can be adjusted to avoid openai traffic limit errors
        Handling mid-process interruptions
        When there are network issues，Traceback and received data will be outputted

    Input parameter Args （Input variables ending in _array are all lists，The length of the list is the number of sub-tasks，When executing，The list will be broken down，And executed separately in each sub-thread）:
        inputs_array (list): List of inputs （Input for each subtask）
        inputs_show_user_array (list): List of inputs to show user（Input displayed in the report for each subtask，With the help of this parameter，Hide verbose real input in the summary report，Enhance the readability of the report）
        llm_kwargs: llm_kwargs parameter
        chatbot: chatbot （Handle of the user interface dialog window，Used for data flow visualization）
        history_array (list): List of chat history （Historical conversation input，Double-layer list，The first layer of the list is the decomposition of subtasks，The second layer of the list is the conversation history）
        sys_prompt_array (list): List of system prompts （System input，List，Prompt for input to GPT，For example, if you are a translator, how to...）
        refresh_interval (float, optional): Refresh interval for UI (default: 0.2) （Refresh time interval frequency，Suggested to be less than 1，Cannot be higher than 3，Only serves for visual effects）
        max_workers (int, optional): Maximum number of threads (default: see config.py) （Maximum number of threads，If there are many subtasks，Use this option to prevent frequent requests to OpenAI that may cause errors）
        scroller_max_len (int, optional): Maximum length for scroller (default: 30)（Display the last few characters received in the data stream，Only serves for visual effects）
        handle_token_exceed (bool, optional): （Automatically truncate text when input is too long，Automatically shorten the text）
        handle_token_exceed：Whether to automatically handle token overflow，If selected to handle automatically，It will be forcefully truncated when overflow occurs，Default enabled
        show_user_at_complete (bool, optional): (At the end，Display the complete input-output results in the chat box)
        retry_times_at_unknown_error：Number of retries when a subtask fails

    Output Returns:
        list: List of GPT model responses （Summary of output for each subtask，If a subtask encounters an error，Traceback error information will be included in the response，Facilitate debugging and problem locating。）
    """
    import time, random
    from concurrent.futures import ThreadPoolExecutor
    from void_terminal.request_llms.bridge_all import predict_no_ui_long_connection
    assert len(inputs_array) == len(history_array)
    assert len(inputs_array) == len(sys_prompt_array)
    if max_workers == -1: # Read configuration file
        try: max_workers = get_conf('DEFAULT_WORKER_NUM')
        except: max_workers = 8
        if max_workers <= 0: max_workers = 3
    # Disable chatglm`s multi-threading，May cause serious lag
    if not can_multi_process(llm_kwargs['llm_model']):
        max_workers = 1
        
    executor = ThreadPoolExecutor(max_workers=max_workers)
    n_frag = len(inputs_array)
    # User feedback
    chatbot.append(["Please start multi-threaded operation。", ""])
    yield from update_ui(chatbot=chatbot, history=[]) # Refresh the page
    # Cross-thread communication
    mutable = [["", time.time(), "Waiting"] for _ in range(n_frag)]

    # Watchdog patience
    watch_dog_patience = 5

    # Sub-thread task
    def _req_gpt(index, inputs, history, sys_prompt):
        gpt_say = ""
        retry_op = retry_times_at_unknown_error
        exceeded_cnt = 0
        mutable[index][2] = "Executing"
        while True:
            # watchdog error
            if len(mutable[index]) >= 2 and (time.time()-mutable[index][1]) > watch_dog_patience: 
                raise RuntimeError("Program termination detected。")
            try:
                # 【First scenario】：Completed smoothly
                # time.sleep(10); raise RuntimeError("Test")
                gpt_say = predict_no_ui_long_connection(
                    inputs=inputs, llm_kwargs=llm_kwargs, history=history, 
                    sys_prompt=sys_prompt, observe_window=mutable[index], console_slience=True
                )
                mutable[index][2] = "Successful"
                return gpt_say
            except ConnectionAbortedError as token_exceeded_error:
                # 【Second scenario】：Token overflow，
                if handle_token_exceed:
                    exceeded_cnt += 1
                    # 【Choose processing】 Attempt to calculate ratio，Retain text as much as possible
                    from void_terminal.toolbox import get_reduce_token_percent
                    p_ratio, n_exceed = get_reduce_token_percent(str(token_exceeded_error))
                    MAX_TOKEN = 4096
                    EXCEED_ALLO = 512 + 512 * exceeded_cnt
                    inputs, history = input_clipping(inputs, history, max_token_limit=MAX_TOKEN-EXCEED_ALLO)
                    gpt_say += f'[Local Message] Warning，Text will be truncated if too long，Token overflow count：{n_exceed}。\n\n'
                    mutable[index][2] = f"Truncated retry"
                    continue # Return and retry
                else:
                    # 【Choose to give up】
                    tb_str = '```\n' + trimmed_format_exc() + '```'
                    gpt_say += f"[Local Message] Warning，Thread{index}Encountered a problem during execution, Traceback：\n\n{tb_str}\n\n"
                    if len(mutable[index][0]) > 0: gpt_say += "Answer received by this thread before failure：\n\n" + mutable[index][0]
                    mutable[index][2] = "Input is too long and has been abandoned"
                    return gpt_say # Give up
            except:
                # 【Third scenario】：Other errors
                tb_str = '```\n' + trimmed_format_exc() + '```'
                print(tb_str)
                gpt_say += f"[Local Message] Warning，Thread{index}Encountered a problem during execution, Traceback：\n\n{tb_str}\n\n"
                if len(mutable[index][0]) > 0: gpt_say += "Answer received by this thread before failure：\n\n" + mutable[index][0]
                if retry_op > 0: 
                    retry_op -= 1
                    wait = random.randint(5, 20)
                    if ("Rate limit reached" in tb_str) or ("Too Many Requests" in tb_str):
                        wait = wait * 3
                        fail_info = "Binding a credit card to OpenAI can remove frequency restrictions "
                    else:
                        fail_info = ""
                    # Perhaps after waiting for more than ten seconds，The situation will improve
                    for i in range(wait):
                        mutable[index][2] = f"{fail_info}Waiting for retry {wait-i}"; time.sleep(1)
                    # Start retrying
                    mutable[index][2] = f"Retrying {retry_times_at_unknown_error-retry_op}/{retry_times_at_unknown_error}"
                    continue # Return and retry
                else:
                    mutable[index][2] = "Failed"
                    wait = 5
                    time.sleep(5)
                    return gpt_say # Give up

    # Asynchronous task starts
    futures = [executor.submit(_req_gpt, index, inputs, history, sys_prompt) for index, inputs, history, sys_prompt in zip(
        range(len(inputs_array)), inputs_array, history_array, sys_prompt_array)]
    cnt = 0
    while True:
        # Yield once to refresh the front-end page
        time.sleep(refresh_interval)
        cnt += 1
        worker_done = [h.done() for h in futures]
        # Better UI visual effects
        observe_win = []
        # Each thread needs to `feed the dog`（Watchdog）
        for thread_index, _ in enumerate(worker_done):
            mutable[thread_index][1] = time.time()
        # Print some fun things in the front end
        for thread_index, _ in enumerate(worker_done):
            print_something_really_funny = "[ ...`"+mutable[thread_index][0][-scroller_max_len:].\
                replace('\n', '').replace('`', '.').replace(
                    ' ', '.').replace('<br/>', '.....').replace('$', '.')+"`... ]"
            observe_win.append(print_something_really_funny)
        # Print some fun things in the front end
        stat_str = ''.join([f'`{mutable[thread_index][2]}`: {obs}\n\n' 
                            if not done else f'`{mutable[thread_index][2]}`\n\n' 
                            for thread_index, done, obs in zip(range(len(worker_done)), worker_done, observe_win)])
        # Print some fun things in the front end
        chatbot[-1] = [chatbot[-1][0], f'Multi-threaded operation has started，Completion status: \n\n{stat_str}' + ''.join(['.']*(cnt % 10+1))]
        yield from update_ui(chatbot=chatbot, history=[]) # Refresh the page
        if all(worker_done):
            executor.shutdown()
            break

    # Asynchronous task ends
    gpt_response_collection = []
    for inputs_show_user, f in zip(inputs_show_user_array, futures):
        gpt_res = f.result()
        gpt_response_collection.extend([inputs_show_user, gpt_res])
    
    # Whether to display the result on the interface when ending，Display the result on the interface
    if show_user_at_complete:
        for inputs_show_user, f in zip(inputs_show_user_array, futures):
            gpt_res = f.result()
            chatbot.append([inputs_show_user, gpt_res])
            yield from update_ui(chatbot=chatbot, history=[]) # Refresh the page
            time.sleep(0.5)
    return gpt_response_collection


def breakdown_txt_to_satisfy_token_limit(txt, get_token_fn, limit):
    def cut(txt_tocut, must_break_at_empty_line):  # Recursion
        if get_token_fn(txt_tocut) <= limit:
            return [txt_tocut]
        else:
            lines = txt_tocut.split('\n')
            estimated_line_cut = limit / get_token_fn(txt_tocut) * len(lines)
            estimated_line_cut = int(estimated_line_cut)
            for cnt in reversed(range(estimated_line_cut)):
                if must_break_at_empty_line:
                    if lines[cnt] != "":
                        continue
                print(cnt)
                prev = "\n".join(lines[:cnt])
                post = "\n".join(lines[cnt:])
                if get_token_fn(prev) < limit:
                    break
            if cnt == 0:
                raise RuntimeError("There is an extremely long line of text!")
            # print(len(post))
            # List recursion chaining
            result = [prev]
            result.extend(cut(post, must_break_at_empty_line))
            return result
    try:
        return cut(txt, must_break_at_empty_line=True)
    except RuntimeError:
        return cut(txt, must_break_at_empty_line=False)


def force_breakdown(txt, limit, get_token_fn):
    """
    When punctuation and blank lines cannot be used for separation，We use the most brutal method to cut
    """
    for i in reversed(range(len(txt))):
        if get_token_fn(txt[:i]) < limit:
            return txt[:i], txt[i:]
    return "Tiktok unknown error", "Tiktok unknown error"

def breakdown_txt_to_satisfy_token_limit_for_pdf(txt, get_token_fn, limit):
    # Recursion
    def cut(txt_tocut, must_break_at_empty_line, break_anyway=False):  
        if get_token_fn(txt_tocut) <= limit:
            return [txt_tocut]
        else:
            lines = txt_tocut.split('\n')
            estimated_line_cut = limit / get_token_fn(txt_tocut) * len(lines)
            estimated_line_cut = int(estimated_line_cut)
            cnt = 0
            for cnt in reversed(range(estimated_line_cut)):
                if must_break_at_empty_line:
                    if lines[cnt] != "":
                        continue
                prev = "\n".join(lines[:cnt])
                post = "\n".join(lines[cnt:])
                if get_token_fn(prev) < limit:
                    break
            if cnt == 0:
                if break_anyway:
                    prev, post = force_breakdown(txt_tocut, limit, get_token_fn)
                else:
                    raise RuntimeError(f"There is an extremely long line of text!{txt_tocut}")
            # print(len(post))
            # List recursion chaining
            result = [prev]
            result.extend(cut(post, must_break_at_empty_line, break_anyway=break_anyway))
            return result
    try:
        # 1st attempt，Use double blank lines as splitting points（\n\n）As a splitting point
        return cut(txt, must_break_at_empty_line=True)
    except RuntimeError:
        try:
            # 2nd attempt，Use single blank lines（\n）As a splitting point
            return cut(txt, must_break_at_empty_line=False)
        except RuntimeError:
            try:
                # 3rd attempt，Use English periods（.）As a splitting point
                res = cut(txt.replace('.', '。\n'), must_break_at_empty_line=False) # This Chinese period is intentional，Exists as an identifier
                return [r.replace('。\n', '.') for r in res]
            except RuntimeError as e:
                try:
                    # 4th attempt，Chinese period（。）As a splitting point
                    res = cut(txt.replace('。', '。。\n'), must_break_at_empty_line=False)
                    return [r.replace('。。\n', '。') for r in res]
                except RuntimeError as e:
                    # 5th attempt，No other way，Cut it randomly and perfunctorily
                    return cut(txt, must_break_at_empty_line=False, break_anyway=True)



def read_and_clean_pdf_text(fp):
    """
    This function is used to split PDF，Used a lot of tricks，The logic is messy，The effect is very good

    **Input Parameter Description**
    - `fp`：The path of the PDF file that needs to be read and cleaned

    **Output Parameter Description**
    - `meta_txt`：Cleaned text content string
    - `page_one_meta`：List of cleaned text content on the first page

    **Functionality**
    Read the PDF file and clean its text content，Cleaning rules include：
    - Extract text information from all block elements，And merge into one string
    - Remove short blocks（Character count is less than 100）And replace with a carriage return
    - CleanUpExcessBlankLines
    - Merge paragraph blocks that start with lowercase letters and replace with spaces
    - Remove duplicate line breaks
    - Replace each line break with two line breaks，Separate each paragraph with two line breaks
    """
    import fitz, copy
    import re
    import numpy as np
    from void_terminal.colorful import PrintBrightYellow, PrintBrightGreen
    fc = 0  # Index 0 Text
    fs = 1  # Index 1 Font
    fb = 2  # Index 2 Box
    REMOVE_FOOT_NOTE = True # Whether to discard non-main text content （Smaller than main text font，Such as references, footnotes, captions, etc.）
    REMOVE_FOOT_FFSIZE_PERCENT = 0.95 # Less than main text？When，Determined as non-main text（In some articles, the font size of the main text is not 100% consistent，Small changes invisible to the naked eye）
    def primary_ffsize(l):
        """
        Main font of extracted text block
        """
        fsize_statiscs = {}
        for wtf in l['spans']:
            if wtf['size'] not in fsize_statiscs: fsize_statiscs[wtf['size']] = 0
            fsize_statiscs[wtf['size']] += len(wtf['text'])
        return max(fsize_statiscs, key=fsize_statiscs.get)
        
    def ffsize_same(a,b):
        """
        Whether the font sizes of extracted text are approximately equal
        """
        return abs((a-b)/max(a,b)) < 0.02

    with fitz.open(fp) as doc:
        meta_txt = []
        meta_font = []

        meta_line = []
        meta_span = []
        ############################## <Step 1，Collect initial information> ##################################
        for index, page in enumerate(doc):
            # file_content += page.get_text()
            text_areas = page.get_text("dict")  # Get text information on the page
            for t in text_areas['blocks']:
                if 'lines' in t:
                    pf = 998
                    for l in t['lines']:
                        txt_line = "".join([wtf['text'] for wtf in l['spans']])
                        if len(txt_line) == 0: continue
                        pf = primary_ffsize(l)
                        meta_line.append([txt_line, pf, l['bbox'], l])
                        for wtf in l['spans']: # for l in t['lines']:
                            meta_span.append([wtf['text'], wtf['size'], len(wtf['text'])])
                    # meta_line.append(["NEW_BLOCK", pf])
            # Block element extraction                           for each word segment with in line                       for each line         cross-line words                          for each block
            meta_txt.extend([" ".join(["".join([wtf['text'] for wtf in l['spans']]) for l in t['lines']]).replace(
                '- ', '') for t in text_areas['blocks'] if 'lines' in t])
            meta_font.extend([np.mean([np.mean([wtf['size'] for wtf in l['spans']])
                             for l in t['lines']]) for t in text_areas['blocks'] if 'lines' in t])
            if index == 0:
                page_one_meta = [" ".join(["".join([wtf['text'] for wtf in l['spans']]) for l in t['lines']]).replace(
                    '- ', '') for t in text_areas['blocks'] if 'lines' in t]
                
        ############################## <Step 2，Get main text font> ##################################
        try:
            fsize_statiscs = {}
            for span in meta_span:
                if span[1] not in fsize_statiscs: fsize_statiscs[span[1]] = 0
                fsize_statiscs[span[1]] += span[2]
            main_fsize = max(fsize_statiscs, key=fsize_statiscs.get)
            if REMOVE_FOOT_NOTE:
                give_up_fize_threshold = main_fsize * REMOVE_FOOT_FFSIZE_PERCENT
        except:
            raise RuntimeError(f'Sorry, We are temporarily unable to parse this PDF document: {fp}。')
        ############################## <Step 3，Split and reassemble> ##################################
        mega_sec = []
        sec = []
        for index, line in enumerate(meta_line):
            if index == 0: 
                sec.append(line[fc])
                continue
            if REMOVE_FOOT_NOTE:
                if meta_line[index][fs] <= give_up_fize_threshold:
                    continue
            if ffsize_same(meta_line[index][fs], meta_line[index-1][fs]):
                # Attempt to identify paragraphs
                if meta_line[index][fc].endswith('.') and\
                    (meta_line[index-1][fc] != 'NEW_BLOCK') and \
                    (meta_line[index][fb][2] - meta_line[index][fb][0]) < (meta_line[index-1][fb][2] - meta_line[index-1][fb][0]) * 0.7:
                    sec[-1] += line[fc]
                    sec[-1] += "\n\n"
                else:
                    sec[-1] += " "
                    sec[-1] += line[fc]
            else:
                if (index+1 < len(meta_line)) and \
                    meta_line[index][fs] > main_fsize:
                    # Single line + Large font
                    mega_sec.append(copy.deepcopy(sec))
                    sec = []
                    sec.append("# " + line[fc])
                else:
                    # Attempt to recognize section
                    if meta_line[index-1][fs] > meta_line[index][fs]:
                        sec.append("\n" + line[fc])
                    else:
                        sec.append(line[fc])
        mega_sec.append(copy.deepcopy(sec))

        finals = []
        for ms in mega_sec:
            final = " ".join(ms)
            final = final.replace('- ', ' ')
            finals.append(final)
        meta_txt = finals

        ############################## <Step 4，Messy post-processing> ##################################
        def ClearBlocksWithTooFewCharactersToNewline(meta_txt):
            for index, block_txt in enumerate(meta_txt):
                if len(block_txt) < 100:
                    meta_txt[index] = '\n'
            return meta_txt
        meta_txt = ClearBlocksWithTooFewCharactersToNewline(meta_txt)

        def CleanUpExcessBlankLines(meta_txt):
            for index in reversed(range(1, len(meta_txt))):
                if meta_txt[index] == '\n' and meta_txt[index-1] == '\n':
                    meta_txt.pop(index)
            return meta_txt
        meta_txt = CleanUpExcessBlankLines(meta_txt)

        def MergeLowercaseStartingParagraphBlocks(meta_txt):
            def starts_with_lowercase_word(s):
                pattern = r"^[a-z]+"
                match = re.match(pattern, s)
                if match:
                    return True
                else:
                    return False
            for _ in range(100):
                for index, block_txt in enumerate(meta_txt):
                    if starts_with_lowercase_word(block_txt):
                        if meta_txt[index-1] != '\n':
                            meta_txt[index-1] += ' '
                        else:
                            meta_txt[index-1] = ''
                        meta_txt[index-1] += meta_txt[index]
                        meta_txt[index] = '\n'
            return meta_txt
        meta_txt = MergeLowercaseStartingParagraphBlocks(meta_txt)
        meta_txt = CleanUpExcessBlankLines(meta_txt)

        meta_txt = '\n'.join(meta_txt)
        # Remove duplicate line breaks
        for _ in range(5):
            meta_txt = meta_txt.replace('\n\n', '\n')

        # Line break -> Double line break
        meta_txt = meta_txt.replace('\n', '\n\n')

        ############################## <Step 5，Display segmentation effect> ##################################
        # for f in finals:
        #    PrintBrightYellow(f)
        #    PrintBrightGreen('***************************')

    return meta_txt, page_one_meta


def get_files_from_everything(txt, type): # type='.md'
    """
    This function is used to get all files of a specified type in a specified directory（such as .md）files，and for files on the internet，it can also be obtained。
    Below are explanations for each parameter and return value：
    Parameters 
    - txt: Path or URL，Indicates the file or folder path to be searched or the file on the internet。 
    - type: String，Indicates the file type to be searched。default is .md。
    Return value 
    - success: Boolean value，Indicates whether the function is executed successfully。 
    - file_manifest: List of file paths，Contains the absolute paths of all files with the specified type as the suffix。 
    - project_folder: String，Indicates the folder path where the file is located。If it is a file on the internet，it is the path of the temporary folder。
    Detailed comments for this function have been added，Please confirm if it meets your needs。
    """
    import glob, os

    success = True
    if txt.startswith('http'):
        # Remote file on the network
        import requests
        from void_terminal.toolbox import get_conf
        from void_terminal.toolbox import get_log_folder, gen_time_str
        proxies = get_conf('proxies')
        try:
            r = requests.get(txt, proxies=proxies)
        except:
            raise ConnectionRefusedError(f"Unable to download resources{txt}，Please check。")
        path = os.path.join(get_log_folder(plugin_name='web_download'), gen_time_str()+type)
        with open(path, 'wb+') as f: f.write(r.content)
        project_folder = get_log_folder(plugin_name='web_download')
        file_manifest = [path]
    elif txt.endswith(type):
        # Directly given file
        file_manifest = [txt]
        project_folder = os.path.dirname(txt)
    elif os.path.exists(txt):
        # Local path，Recursive search
        project_folder = txt
        file_manifest = [f for f in glob.glob(f'{project_folder}/**/*'+type, recursive=True)]
        if len(file_manifest) == 0:
            success = False
    else:
        project_folder = None
        file_manifest = []
        success = False

    return success, file_manifest, project_folder




def Singleton(cls):
    _instance = {}
 
    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]
 
    return _singleton


@Singleton
class knowledge_archive_interface():
    def __init__(self) -> None:
        self.threadLock = threading.Lock()
        self.current_id = ""
        self.kai_path = None
        self.qa_handle = None
        self.text2vec_large_chinese = None

    def get_chinese_text2vec(self):
        if self.text2vec_large_chinese is None:
            # < ------------------- Preheating text vectorization module--------------- >
            from void_terminal.toolbox import ProxyNetworkActivate
            print('Checking Text2vec ...')
            from langchain.embeddings.huggingface import HuggingFaceEmbeddings
            with ProxyNetworkActivate('Download_LLM'):    # Temporarily activate proxy network
                self.text2vec_large_chinese = HuggingFaceEmbeddings(model_name="GanymedeNil/text2vec-large-chinese")

        return self.text2vec_large_chinese


    def feed_archive(self, file_manifest, id="default"):
        self.threadLock.acquire()
        # import uuid
        self.current_id = id
        from zh_langchain import construct_vector_store
        self.qa_handle, self.kai_path = construct_vector_store(   
            vs_id=self.current_id, 
            files=file_manifest, 
            sentence_size=100,
            history=[],
            one_conent="",
            one_content_segmentation="",
            text2vec = self.get_chinese_text2vec(),
        )
        self.threadLock.release()

    def get_current_archive_id(self):
        return self.current_id
    
    def get_loaded_file(self):
        return self.qa_handle.get_loaded_file()

    def answer_with_archive_by_id(self, txt, id):
        self.threadLock.acquire()
        if not self.current_id == id:
            self.current_id = id
            from zh_langchain import construct_vector_store
            self.qa_handle, self.kai_path = construct_vector_store(   
                vs_id=self.current_id, 
                files=[], 
                sentence_size=100,
                history=[],
                one_conent="",
                one_content_segmentation="",
                text2vec = self.get_chinese_text2vec(),
            )
        VECTOR_SEARCH_SCORE_THRESHOLD = 0
        VECTOR_SEARCH_TOP_K = 4
        CHUNK_SIZE = 512
        resp, prompt = self.qa_handle.get_knowledge_based_conent_test(
            query = txt,
            vs_path = self.kai_path,
            score_threshold=VECTOR_SEARCH_SCORE_THRESHOLD,
            vector_search_top_k=VECTOR_SEARCH_TOP_K, 
            chunk_conent=True,
            chunk_size=CHUNK_SIZE,
            text2vec = self.get_chinese_text2vec(),
        )
        self.threadLock.release()
        return resp, prompt
    
@Singleton
class nougat_interface():
    def __init__(self):
        self.threadLock = threading.Lock()

    def nougat_with_timeout(self, command, cwd, timeout=3600):
        import subprocess
        from void_terminal.toolbox import ProxyNetworkActivate
        logging.info(f'Executing command {command}')
        with ProxyNetworkActivate("Nougat_Download"):
            process = subprocess.Popen(command, shell=True, cwd=cwd, env=os.environ)
        try:
            stdout, stderr = process.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            process.kill()
            stdout, stderr = process.communicate()
            print("Process timed out!")
            return False
        return True


    def NOUGAT_parse_pdf(self, fp, chatbot, history):
        from void_terminal.toolbox import update_ui_lastest_msg

        yield from update_ui_lastest_msg("Analyzing the paper, Please wait。Progress：In queue, Waiting for thread lock...", 
                                         chatbot=chatbot, history=history, delay=0)
        self.threadLock.acquire()
        import glob, threading, os
        from void_terminal.toolbox import get_log_folder, gen_time_str
        dst = os.path.join(get_log_folder(plugin_name='nougat'), gen_time_str())
        os.makedirs(dst)

        yield from update_ui_lastest_msg("Analyzing the paper, Please wait。Progress：Loading NOUGAT... （prompt：The first run takes a long time to download NOUGAT parameters）", 
                                         chatbot=chatbot, history=history, delay=0)
        self.nougat_with_timeout(f'nougat --out "{os.path.abspath(dst)}" "{os.path.abspath(fp)}"', os.getcwd(), timeout=3600)
        res = glob.glob(os.path.join(dst,'*.mmd'))
        if len(res) == 0:
            self.threadLock.release()
            raise RuntimeError("Nougat failed to parse the paper。")
        self.threadLock.release()
        return res[0]




def try_install_deps(deps, reload_m=[]):
    import subprocess, sys, importlib
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--user', dep])
    import site
    importlib.reload(site)
    for m in reload_m:
        importlib.reload(__import__(m))


def get_plugin_arg(plugin_kwargs, key, default):
    # If the parameter is empty
    if (key in plugin_kwargs) and (plugin_kwargs[key] == ""): plugin_kwargs.pop(key)
    # Normal situation
    return plugin_kwargs.get(key, default)
