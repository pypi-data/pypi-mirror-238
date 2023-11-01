from void_terminal.toolbox import update_ui, trimmed_format_exc, get_conf, get_log_folder, promote_file_to_downloadzone
from void_terminal.toolbox import CatchException, report_execption, update_ui_lastest_msg, zip_result, gen_time_str
from functools import partial
import glob, os, requests, time
pj = os.path.join
ARXIV_CACHE_DIR = os.path.expanduser(f"~/arxiv_cache/")

# =================================== Utility functions ===============================================
# ProfessionalTerminologyDeclaration  = 'If the term "agent" is used in this section, it should be translated to "Intelligent agent". '
def switch_prompt(pfg, mode, more_requirement):
    """
    Generate prompts and system prompts based on the mode for proofreading or translating.
    Args:
    - pfg: Proofreader or Translator instance.
    - mode: A string specifying the mode, either 'proofread' or 'translate_zh'.

    Returns:
    - inputs_array: A list of strings containing prompts for users to respond to.
    - sys_prompt_array: A list of strings containing prompts for system prompts.
    """
    n_split = len(pfg.sp_file_contents)
    if mode == 'proofread_en':
        inputs_array = [r"Below is a section from an academic paper, proofread this section." + 
                        r"Do not modify any latex command such as \section, \cite, \begin, \item and equations. " + more_requirement +
                        r"Answer me only with the revised text:" + 
                        f"\n\n{frag}" for frag in pfg.sp_file_contents]
        sys_prompt_array = ["You are a professional academic paper writer." for _ in range(n_split)]
    elif mode == 'translate_zh':
        inputs_array = [r"Below is a section from an English academic paper, translate it into Chinese. " + more_requirement + 
                        r"Do not modify any latex command such as \section, \cite, \begin, \item and equations. " + 
                        r"Answer me only with the translated text:" + 
                        f"\n\n{frag}" for frag in pfg.sp_file_contents]
        sys_prompt_array = ["You are a professional translator." for _ in range(n_split)]
    else:
        assert False, "Unknown command"
    return inputs_array, sys_prompt_array

def desend_to_extracted_folder_if_exist(project_folder):
    """ 
    Descend into the extracted folder if it exists, otherwise return the original folder.

    Args:
    - project_folder: A string specifying the folder path.

    Returns:
    - A string specifying the path to the extracted folder, or the original folder if there is no extracted folder.
    """
    maybe_dir = [f for f in glob.glob(f'{project_folder}/*') if os.path.isdir(f)]
    if len(maybe_dir) == 0: return project_folder
    if maybe_dir[0].endswith('.extract'): return maybe_dir[0]
    return project_folder

def move_project(project_folder, arxiv_id=None):
    """ 
    Create a new work folder and copy the project folder to it.

    Args:
    - project_folder: A string specifying the folder path of the project.

    Returns:
    - A string specifying the path to the new work folder.
    """
    import shutil, time
    time.sleep(2)   # avoid time string conflict
    if arxiv_id is not None:
        new_workfolder = pj(ARXIV_CACHE_DIR, arxiv_id, 'workfolder')
    else:
        new_workfolder = f'{get_log_folder()}/{gen_time_str()}'
    try:
        shutil.rmtree(new_workfolder)
    except:
        pass

    # align subfolder if there is a folder wrapper
    items = glob.glob(pj(project_folder,'*'))
    if len(glob.glob(pj(project_folder,'*.tex'))) == 0 and len(items) == 1:
        if os.path.isdir(items[0]): project_folder = items[0]

    shutil.copytree(src=project_folder, dst=new_workfolder)
    return new_workfolder

def arxiv_download(chatbot, history, txt, allow_cache=True):
    def check_cached_translation_pdf(arxiv_id):
        translation_dir = pj(ARXIV_CACHE_DIR, arxiv_id, 'translation')
        if not os.path.exists(translation_dir):
            os.makedirs(translation_dir)
        target_file = pj(translation_dir, 'translate_zh.pdf')
        if os.path.exists(target_file):
            promote_file_to_downloadzone(target_file, rename_file=None, chatbot=chatbot)
            return target_file
        return False
    def is_float(s):
        try:
            float(s)
            return True
        except ValueError:
            return False
    if ('.' in txt) and ('/' not in txt) and is_float(txt): # is arxiv ID
        txt = 'https://arxiv.org/abs/' + txt.strip()
    if ('.' in txt) and ('/' not in txt) and is_float(txt[:10]): # is arxiv ID
        txt = 'https://arxiv.org/abs/' + txt[:10]
    if not txt.startswith('https://arxiv.org'): 
        return txt, None
    
    # <-------------- inspect format ------------->
    chatbot.append([f"Detected arXiv document link", 'Attempting to download ...']) 
    yield from update_ui(chatbot=chatbot, history=history)
    time.sleep(1) # Refresh the page

    url_ = txt   # https://arxiv.org/abs/1707.06690
    if not txt.startswith('https://arxiv.org/abs/'): 
        msg = f"Failed to parse arXiv URL, Expected format, for example: https://arxiv.org/abs/1707.06690。Obtained format in reality: {url_}。"
        yield from update_ui_lastest_msg(msg, chatbot=chatbot, history=history) # Refresh the page
        return msg, None
    # <-------------- set format ------------->
    arxiv_id = url_.split('/abs/')[-1]
    if 'v' in arxiv_id: arxiv_id = arxiv_id[:10]
    cached_translation_pdf = check_cached_translation_pdf(arxiv_id)
    if cached_translation_pdf and allow_cache: return cached_translation_pdf, arxiv_id

    url_tar = url_.replace('/abs/', '/e-print/')
    translation_dir = pj(ARXIV_CACHE_DIR, arxiv_id, 'e-print')
    extract_dst = pj(ARXIV_CACHE_DIR, arxiv_id, 'extract')
    os.makedirs(translation_dir, exist_ok=True)
    
    # <-------------- download arxiv source file ------------->
    dst = pj(translation_dir, arxiv_id+'.tar')
    if os.path.exists(dst):
        yield from update_ui_lastest_msg("Calling cache", chatbot=chatbot, history=history)  # Refresh the page
    else:
        yield from update_ui_lastest_msg("Start downloading", chatbot=chatbot, history=history)  # Refresh the page
        proxies = get_conf('proxies')
        r = requests.get(url_tar, proxies=proxies)
        with open(dst, 'wb+') as f:
            f.write(r.content)
    # <-------------- extract file ------------->
    yield from update_ui_lastest_msg("Download complete", chatbot=chatbot, history=history)  # Refresh the page
    from void_terminal.toolbox import extract_archive
    extract_archive(file_path=dst, dest_dir=extract_dst)
    return extract_dst, arxiv_id
# ========================================= Plugin Main Program 1 =====================================================    


@CatchException
def CorrectEnglishInLatexWithPDFComparison(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    # <-------------- information about this plugin ------------->
    chatbot.append([ "Function plugin feature？",
        "Correcting the entire Latex project, Compile to PDF using LaTeX and highlight the corrections。Function plugin contributor: Binary-Husky。Notes: Currently only supports GPT3.5/GPT4，Unknown conversion effect of other models。Currently, the best conversion effect for machine learning literature，Unknown conversion effect for other types of literature。Tested only on Windows system，Unknown performance on other operating systems。"])
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
    
    # <-------------- more requirements ------------->
    if ("advanced_arg" in plugin_kwargs) and (plugin_kwargs["advanced_arg"] == ""): plugin_kwargs.pop("advanced_arg")
    more_req = plugin_kwargs.get("advanced_arg", "")
    _switch_prompt_ = partial(switch_prompt, more_requirement=more_req)

    # <-------------- check deps ------------->
    try:
        import glob, os, time, subprocess
        subprocess.Popen(['pdflatex', '-version'])
        from void_terminal.crazy_functions.latex_fns.latex_actions import DecomposeAndConvertLatex, CompileLatex
    except Exception as e:
        chatbot.append([ f"Parsing project: {txt}",
            f"Failed to execute the LaTeX command。Latex is not installed, Or not in the environment variable PATH。Installation method: https://tug.org/texlive/。Error message\n\n```\n\n{trimmed_format_exc()}\n\n```\n\n"])
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return
    

    # <-------------- clear history and read input ------------->
    history = []
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
    

    # <-------------- if is a zip/tar file ------------->
    project_folder = desend_to_extracted_folder_if_exist(project_folder)


    # <-------------- move latex project away from temp folder ------------->
    project_folder = move_project(project_folder, arxiv_id=None)


    # <-------------- if merge_translate_zh is already generated, skip gpt req ------------->
    if not os.path.exists(project_folder + '/merge_proofread_en.tex'):
        yield from DecomposeAndConvertLatex(file_manifest, project_folder, llm_kwargs, plugin_kwargs, 
                                chatbot, history, system_prompt, mode='proofread_en', switch_prompt=_switch_prompt_)


    # <-------------- compile PDF ------------->
    success = yield from CompileLatex(chatbot, history, main_file_original='merge', main_file_modified='merge_proofread_en', 
                             work_folder_original=project_folder, work_folder_modified=project_folder, work_folder=project_folder)
    

    # <-------------- zip PDF ------------->
    zip_res = zip_result(project_folder)
    if success:
        chatbot.append((f"Success!", 'Please check the results（Compressed file）...'))
        yield from update_ui(chatbot=chatbot, history=history); time.sleep(1) # Refresh the page
        promote_file_to_downloadzone(file=zip_res, chatbot=chatbot)
    else:
        chatbot.append((f"Failed", 'Although PDF generation failed, But please check the results（Compressed file）, Contains a Tex document that has been translated, It is also readable, You can go to the Github Issue area, Provide feedback using the compressed package + ConversationHistoryArchive ...'))
        yield from update_ui(chatbot=chatbot, history=history); time.sleep(1) # Refresh the page
        promote_file_to_downloadzone(file=zip_res, chatbot=chatbot)

    # <-------------- we are done ------------->
    return success


# ========================================= Plugin Main Program 2 =====================================================    

@CatchException
def TranslateChineseToEnglishInLatexAndRecompilePDF(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    # <-------------- information about this plugin ------------->
    chatbot.append([
        "Function plugin feature？",
        "Translate the entire Latex project, Generate Chinese PDF。Function plugin contributor: Binary-Husky。Notes: This plugin has best support for Windows，Must install using Docker on Linux，See the main README.md of the project for details。Currently only supports GPT3.5/GPT4，Unknown conversion effect of other models。Currently, the best conversion effect for machine learning literature，Unknown conversion effect for other types of literature。"])
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page

    # <-------------- more requirements ------------->
    if ("advanced_arg" in plugin_kwargs) and (plugin_kwargs["advanced_arg"] == ""): plugin_kwargs.pop("advanced_arg")
    more_req = plugin_kwargs.get("advanced_arg", "")
    no_cache = more_req.startswith("--no-cache")
    if no_cache: more_req.lstrip("--no-cache")
    allow_cache = not no_cache
    _switch_prompt_ = partial(switch_prompt, more_requirement=more_req)

    # <-------------- check deps ------------->
    try:
        import glob, os, time, subprocess
        subprocess.Popen(['pdflatex', '-version'])
        from void_terminal.crazy_functions.latex_fns.latex_actions import DecomposeAndConvertLatex, CompileLatex
    except Exception as e:
        chatbot.append([ f"Parsing project: {txt}",
            f"Failed to execute the LaTeX command。Latex is not installed, Or not in the environment variable PATH。Installation method: https://tug.org/texlive/。Error message\n\n```\n\n{trimmed_format_exc()}\n\n```\n\n"])
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return
    

    # <-------------- clear history and read input ------------->
    history = []
    txt, arxiv_id = yield from arxiv_download(chatbot, history, txt, allow_cache)
    if txt.endswith('.pdf'):
        report_execption(chatbot, history, a = f"Parsing project: {txt}", b = f"Found an already translated PDF document")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return
    

    if os.path.exists(txt):
        project_folder = txt
    else:
        if txt == "": txt = 'Empty input field'
        report_execption(chatbot, history, a = f"Parsing project: {txt}", b = f"Unable to find local project or unable to process: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return
    
    file_manifest = [f for f in glob.glob(f'{project_folder}/**/*.tex', recursive=True)]
    if len(file_manifest) == 0:
        report_execption(chatbot, history, a = f"Parsing project: {txt}", b = f"Cannot find any .tex files: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return
    

    # <-------------- if is a zip/tar file ------------->
    project_folder = desend_to_extracted_folder_if_exist(project_folder)


    # <-------------- move latex project away from temp folder ------------->
    project_folder = move_project(project_folder, arxiv_id)


    # <-------------- if merge_translate_zh is already generated, skip gpt req ------------->
    if not os.path.exists(project_folder + '/merge_translate_zh.tex'):
        yield from DecomposeAndConvertLatex(file_manifest, project_folder, llm_kwargs, plugin_kwargs, 
                                chatbot, history, system_prompt, mode='translate_zh', switch_prompt=_switch_prompt_)


    # <-------------- compile PDF ------------->
    success = yield from CompileLatex(chatbot, history, main_file_original='merge', main_file_modified='merge_translate_zh', mode='translate_zh', 
                             work_folder_original=project_folder, work_folder_modified=project_folder, work_folder=project_folder)

    # <-------------- zip PDF ------------->
    zip_res = zip_result(project_folder)
    if success:
        chatbot.append((f"Success!", 'Please check the results（Compressed file）...'))
        yield from update_ui(chatbot=chatbot, history=history); time.sleep(1) # Refresh the page
        promote_file_to_downloadzone(file=zip_res, chatbot=chatbot)
    else:
        chatbot.append((f"Failed", 'Although PDF generation failed, But please check the results（Compressed file）, Contains a Tex document that has been translated, You can go to the Github Issue area, Use this compressed package for feedback。If the system is Linux，Please check system fonts（See Github wiki） ...'))
        yield from update_ui(chatbot=chatbot, history=history); time.sleep(1) # Refresh the page
        promote_file_to_downloadzone(file=zip_res, chatbot=chatbot)


    # <-------------- we are done ------------->
    return success
