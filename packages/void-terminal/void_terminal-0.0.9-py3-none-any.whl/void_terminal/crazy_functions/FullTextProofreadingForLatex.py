from void_terminal.toolbox import update_ui, trimmed_format_exc, promote_file_to_downloadzone, get_log_folder
from void_terminal.toolbox import CatchException, report_execption, write_history_to_file, zip_folder


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
    def merge_result(self):
        self.file_result = ["" for _ in range(len(self.file_paths))]
        for r, k in zip(self.sp_file_result, self.sp_file_index):
            self.file_result[k] += r

    def write_result(self):
        manifest = []
        for path, res in zip(self.file_paths, self.file_result):
            with open(path + '.polish.tex', 'w', encoding='utf8') as f:
                manifest.append(path + '.polish.tex')
                f.write(res)
        return manifest
    
    def zip_result(self):
        import os, time
        folder = os.path.dirname(self.file_paths[0])
        t = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
        zip_folder(folder, get_log_folder(), f'{t}-polished.zip')


def ProofreadMultipleFiles(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, language='en', mode='polish'):
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


    #  <-------- Multithreading polishing begins ----------> 
    if language == 'en':
        if mode == 'polish':
            inputs_array = ["Below is a section from an academic paper, polish this section to meet the academic standard, " + 
                            "improve the grammar, clarity and overall readability, do not modify any latex command such as \section, \cite and equations:" + 
                            f"\n\n{frag}" for frag in pfg.sp_file_contents]
        else:
            inputs_array = [r"Below is a section from an academic paper, proofread this section." + 
                            r"Do not modify any latex command such as \section, \cite, \begin, \item and equations. " + 
                            r"Answer me only with the revised text:" + 
                        f"\n\n{frag}" for frag in pfg.sp_file_contents]
        inputs_show_user_array = [f"Polish {f}" for f in pfg.sp_file_tag]
        sys_prompt_array = ["You are a professional academic paper writer." for _ in range(n_split)]
    elif language == 'zh':
        if mode == 'polish':
            inputs_array = [f"The following is a paragraph from an academic paper，Please polish this section to meet academic standards，Improve grammar, clarity, and overall readability，Do not modify any LaTeX commands，such as \section，\cite and equations：" + 
                            f"\n\n{frag}" for frag in pfg.sp_file_contents]
        else:
            inputs_array = [f"The following is a paragraph from an academic paper，Please correct the grammar of this part。Do not modify any LaTeX commands，such as \section，\cite and equations：" + 
                            f"\n\n{frag}" for frag in pfg.sp_file_contents] 
        inputs_show_user_array = [f"Polishing {f}" for f in pfg.sp_file_tag]
        sys_prompt_array=["You are a professional Chinese academic paper writer。" for _ in range(n_split)]


    gpt_response_collection = yield from request_gpt_model_multi_threads_with_very_awesome_ui_and_high_efficiency(
        inputs_array=inputs_array,
        inputs_show_user_array=inputs_show_user_array,
        llm_kwargs=llm_kwargs,
        chatbot=chatbot,
        history_array=[[""] for _ in range(n_split)],
        sys_prompt_array=sys_prompt_array,
        # max_workers=5,  # Parallel task number limit，Up to 5 can be executed at the same time，Others are queued and waiting
        scroller_max_len = 80
    )

    #  <-------- Reassemble text fragments into a complete tex file，Organize the results into a compressed package ----------> 
    try:
        pfg.sp_file_result = []
        for i_say, gpt_say in zip(gpt_response_collection[0::2], gpt_response_collection[1::2]):
            pfg.sp_file_result.append(gpt_say)
        pfg.merge_result()
        pfg.write_result()
        pfg.zip_result()
    except:
        print(trimmed_format_exc())

    #  <-------- Organize the results，Exit ----------> 
    create_report_file_name = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + f"-chatgpt.polish.md"
    res = write_history_to_file(gpt_response_collection, file_basename=create_report_file_name)
    promote_file_to_downloadzone(res, chatbot=chatbot)

    history = gpt_response_collection
    chatbot.append((f"{fp}Are you done?？", res))
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page


@CatchException
def EnglishProofreadingForLatex(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    # Basic information：Function, contributor
    chatbot.append([
        "Function plugin feature？",
        "Polish the entire Latex project。Function plugin contributor: Binary-Husky。（Attention，This plugin does not call Latex，If there is a Latex environment，Please use the `LatexEnglishCorrection+Highlight` plugin）"])
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
    yield from ProofreadMultipleFiles(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, language='en')






@CatchException
def LatexChineseProofreading(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    # Basic information：Function, contributor
    chatbot.append([
        "Function plugin feature？",
        "Polish the entire Latex project。Function plugin contributor: Binary-Husky"])
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
    yield from ProofreadMultipleFiles(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, language='zh')




@CatchException
def LatexEnglishCorrection(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    # Basic information：Function, contributor
    chatbot.append([
        "Function plugin feature？",
        "Correcting the entire Latex project。Function plugin contributor: Binary-Husky"])
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
    yield from ProofreadMultipleFiles(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, language='en', mode='proofread')



