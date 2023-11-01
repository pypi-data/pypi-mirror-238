from void_terminal.toolbox import update_ui, promote_file_to_downloadzone
from void_terminal.toolbox import CatchException, report_execption, write_history_to_file
fast_debug = False

class PaperFileGroup():
    def __init__(self):
        self.file_paths = []
        self.file_contents = []
        self.sp_file_contents = []
        self.sp_file_index = []
        self.sp_file_tag = []

        # count_token
        from void_terminal.request_llms.bridge_all import model_info
        enc = model_info["gpt-3.5-turbo"]['tokenizer']
        def get_token_num(txt): return len(enc.encode(txt, disallowed_special=()))
        self.get_token_num = get_token_num

    def run_file_split(self, max_token_limit=1900):
        """
        Separate long text
        """
        for index, file_content in enumerate(self.file_contents):
            if self.get_token_num(file_content) < max_token_limit:
                self.sp_file_contents.append(file_content)
                self.sp_file_index.append(index)
                self.sp_file_tag.append(self.file_paths[index])
            else:
                from void_terminal.crazy_functions.crazy_utils import breakdown_txt_to_satisfy_token_limit_for_pdf
                segments = breakdown_txt_to_satisfy_token_limit_for_pdf(file_content, self.get_token_num, max_token_limit)
                for j, segment in enumerate(segments):
                    self.sp_file_contents.append(segment)
                    self.sp_file_index.append(index)
                    self.sp_file_tag.append(self.file_paths[index] + f".part-{j}.tex")

        print('Segmentation: done')

def TranslateMultipleFiles(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, language='en'):
    import time, os, re
    from void_terminal.crazy_functions.crazy_utils import request_gpt_model_multi_threads_with_very_awesome_ui_and_high_efficiency

    #  <-------- Read Latex file，Remove all comments from it ----------> 
    pfg = PaperFileGroup()

    for index, fp in enumerate(file_manifest):
        with open(fp, 'r', encoding='utf-8', errors='replace') as f:
            file_content = f.read()
            # Define the regular expression of comments
            comment_pattern = r'(?<!\\)%.*'
            # Use regular expressions to find comments，And replace them with an empty string
            clean_tex_content = re.sub(comment_pattern, '', file_content)
            # Record the text after removing comments
            pfg.file_paths.append(fp)
            pfg.file_contents.append(clean_tex_content)

    #  <-------- Split long latex files ----------> 
    pfg.run_file_split(max_token_limit=1024)
    n_split = len(pfg.sp_file_contents)

    #  <-------- Extract abstract ----------> 
    # if language == 'en':
    #     abs_extract_inputs = f"Please write an abstract for this paper"

    # # Single line，Get article meta information
    # paper_meta_info = yield from request_gpt_model_in_new_thread_with_ui_alive(
    #     inputs=abs_extract_inputs,
    #     inputs_show_user=f"正在Extract abstract信息。",
    #     llm_kwargs=llm_kwargs,
    #     chatbot=chatbot, history=[],
    #     sys_prompt="Your job is to collect information from materials。",
    # )

    #  <-------- Multithreading polishing begins ----------> 
    if language == 'en->zh':
        inputs_array = ["Below is a section from an English academic paper, translate it into Chinese, do not modify any latex command such as \section, \cite and equations:" + 
                        f"\n\n{frag}" for frag in pfg.sp_file_contents]
        inputs_show_user_array = [f"Translation {f}" for f in pfg.sp_file_tag]
        sys_prompt_array = ["You are a professional academic paper translator." for _ in range(n_split)]
    elif language == 'zh->en':
        inputs_array = [f"Below is a section from a Chinese academic paper, translate it into English, do not modify any latex command such as \section, \cite and equations:" + 
                        f"\n\n{frag}" for frag in pfg.sp_file_contents]
        inputs_show_user_array = [f"Translation {f}" for f in pfg.sp_file_tag]
        sys_prompt_array = ["You are a professional academic paper translator." for _ in range(n_split)]

    gpt_response_collection = yield from request_gpt_model_multi_threads_with_very_awesome_ui_and_high_efficiency(
        inputs_array=inputs_array,
        inputs_show_user_array=inputs_show_user_array,
        llm_kwargs=llm_kwargs,
        chatbot=chatbot,
        history_array=[[""] for _ in range(n_split)],
        sys_prompt_array=sys_prompt_array,
        # max_workers=5,  # Maximum parallel overload allowed by OpenAI
        scroller_max_len = 80
    )

    #  <-------- Organize the results，Exit ----------> 
    create_report_file_name = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + f"-chatgpt.polish.md"
    res = write_history_to_file(gpt_response_collection, create_report_file_name)
    promote_file_to_downloadzone(res, chatbot=chatbot)
    history = gpt_response_collection
    chatbot.append((f"{fp}Are you done?？", res))
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page





@CatchException
def LatexEnglishToChinese(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    # Basic information：Function, contributor
    chatbot.append([
        "Function plugin feature？",
        "Translate the entire Latex project。Function plugin contributor: Binary-Husky"])
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page

    # Attempt to import dependencies，If dependencies are missing，Give installation suggestions
    try:
        import tiktoken
    except:
        report_execption(chatbot, history,
                         a=f"Parsing project: {txt}",
                         b=f"Failed to import software dependencies。Using this module requires additional dependencies，Installation method```pip install --upgrade tiktoken```。")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return
    history = []    # Clear history，To avoid input overflow
    import glob, os
    if os.path.exists(txt):
        project_folder = txt
    else:
        if txt == "": txt = 'Empty input field'
        report_execption(chatbot, history, a = f"Parsing project: {txt}", b = f"Cannot find local project or do not have access: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return
    file_manifest = [f for f in glob.glob(f'{project_folder}/**/*.tex', recursive=True)]
    if len(file_manifest) == 0:
        report_execption(chatbot, history, a = f"Parsing project: {txt}", b = f"Cannot find any .tex files: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return
    yield from TranslateMultipleFiles(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, language='en->zh')





@CatchException
def LatexChineseToEnglish(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    # Basic information：Function, contributor
    chatbot.append([
        "Function plugin feature？",
        "Translate the entire Latex project。Function plugin contributor: Binary-Husky"])
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page

    # Attempt to import dependencies，If dependencies are missing，Give installation suggestions
    try:
        import tiktoken
    except:
        report_execption(chatbot, history,
                         a=f"Parsing project: {txt}",
                         b=f"Failed to import software dependencies。Using this module requires additional dependencies，Installation method```pip install --upgrade tiktoken```。")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return
    history = []    # Clear history，To avoid input overflow
    import glob, os
    if os.path.exists(txt):
        project_folder = txt
    else:
        if txt == "": txt = 'Empty input field'
        report_execption(chatbot, history, a = f"Parsing project: {txt}", b = f"Cannot find local project or do not have access: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return
    file_manifest = [f for f in glob.glob(f'{project_folder}/**/*.tex', recursive=True)]
    if len(file_manifest) == 0:
        report_execption(chatbot, history, a = f"Parsing project: {txt}", b = f"Cannot find any .tex files: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return
    yield from TranslateMultipleFiles(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, language='zh->en')