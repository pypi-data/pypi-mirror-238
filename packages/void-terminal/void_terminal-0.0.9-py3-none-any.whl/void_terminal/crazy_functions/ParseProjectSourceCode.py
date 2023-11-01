from void_terminal.toolbox import update_ui, promote_file_to_downloadzone, disable_auto_promotion
from void_terminal.toolbox import CatchException, report_execption, write_history_to_file
from void_terminal.crazy_functions.crazy_utils import input_clipping

def ParsingSourceCodeNew(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt):
    import os, copy
    from void_terminal.crazy_functions.crazy_utils import request_gpt_model_multi_threads_with_very_awesome_ui_and_high_efficiency
    from void_terminal.crazy_functions.crazy_utils import request_gpt_model_in_new_thread_with_ui_alive
    disable_auto_promotion(chatbot=chatbot)

    summary_batch_isolation = True
    inputs_array = []
    inputs_show_user_array = []
    history_array = []
    sys_prompt_array = []
    report_part_1 = []

    assert len(file_manifest) <= 512, "Too many source files（Exceeds 512）, Please reduce the number of input files。Or，You can also choose to delete this line of warning，And modify the code to split the file_manifest list，To achieve batch processing。"
    ############################## <Step one，Analyze each file，Multithreading> ##################################
    for index, fp in enumerate(file_manifest):
        # Read the file
        with open(fp, 'r', encoding='utf-8', errors='replace') as f:
            file_content = f.read()
        prefix = "Next, please analyze the following project file by file" if index==0 else ""
        i_say = prefix + f'Please give an overview of the following program files, the file name is{os.path.relpath(fp, project_folder)}，The file code is ```{file_content}```'
        i_say_show_user = prefix + f'[{index}/{len(file_manifest)}] Please provide an overview of the program file below: {fp}'
        # Load the request content
        inputs_array.append(i_say)
        inputs_show_user_array.append(i_say_show_user)
        history_array.append([])
        sys_prompt_array.append("You are a program architecture analyst，Analyzing a source code project。Your answer must be concise and clear。")

    # File reading completed，For each source code file，Generate a request thread，Send to chatgpt for analysis
    gpt_response_collection = yield from request_gpt_model_multi_threads_with_very_awesome_ui_and_high_efficiency(
        inputs_array = inputs_array,
        inputs_show_user_array = inputs_show_user_array,
        history_array = history_array,
        sys_prompt_array = sys_prompt_array,
        llm_kwargs = llm_kwargs,
        chatbot = chatbot,
        show_user_at_complete = True
    )

    # All files parsed，Write results to file，Prepare to summarize and analyze project source code
    report_part_1 = copy.deepcopy(gpt_response_collection)
    history_to_return = report_part_1
    res = write_history_to_file(report_part_1)
    promote_file_to_downloadzone(res, chatbot=chatbot)
    chatbot.append(("Completed？", "Analysis of each file has been completed。" + res + "\n\nStarting to summarize。"))
    yield from update_ui(chatbot=chatbot, history=history_to_return) # Refresh the page

    ############################## <Step two，Synthesis，Single thread，Grouping + iterative processing> ##################################
    batchsize = 16  # 10 files per group
    report_part_2 = []
    previous_iteration_files = []
    last_iteration_result = ""
    while True:
        if len(file_manifest) == 0: break
        this_iteration_file_manifest = file_manifest[:batchsize]
        this_iteration_gpt_response_collection = gpt_response_collection[:batchsize*2]
        file_rel_path = [os.path.relpath(fp, project_folder) for index, fp in enumerate(this_iteration_file_manifest)]
        # 把“Please provide an overview of the program file below” 替换成 精简的 "文件名：{all_file[index]}"
        for index, content in enumerate(this_iteration_gpt_response_collection):
            if index%2==0: this_iteration_gpt_response_collection[index] = f"{file_rel_path[index//2]}" # Keep only file names to save tokens
        this_iteration_files = [os.path.relpath(fp, project_folder) for index, fp in enumerate(this_iteration_file_manifest)]
        previous_iteration_files.extend(this_iteration_files)
        previous_iteration_files_string = ', '.join(previous_iteration_files)
        current_iteration_focus = ', '.join(this_iteration_files)
        if summary_batch_isolation: focus = current_iteration_focus
        else:                       focus = previous_iteration_files_string
        i_say = f'Briefly describe the functions of the following files in a Markdown table：{focus}。Based on the above analysis，Summarize the overall function of the program in one sentence。'
        if last_iteration_result != "":
            sys_prompt_additional = "It is known that the local effect of some code is:" + last_iteration_result + "\nPlease continue to analyze other source code，So as to have a more comprehensive understanding of the overall function of the project。"
        else:
            sys_prompt_additional = ""
        inputs_show_user = f'Based on the above analysis，Redescribe the overall function and architecture of the program，Due to input length limitations，Group processing may be required，This group of files is {current_iteration_focus} + Files group already summarized。'
        this_iteration_history = copy.deepcopy(this_iteration_gpt_response_collection)
        this_iteration_history.append(last_iteration_result)
        # Trim input
        inputs, this_iteration_history_feed = input_clipping(inputs=i_say, history=this_iteration_history, max_token_limit=2560)
        result = yield from request_gpt_model_in_new_thread_with_ui_alive(
            inputs=inputs, inputs_show_user=inputs_show_user, llm_kwargs=llm_kwargs, chatbot=chatbot,
            history=this_iteration_history_feed,   # Analysis before iteration
            sys_prompt="You are a program architecture analyst，Analyzing source code of a project。" + sys_prompt_additional)
        
        summary = "Please summarize the overall function of these files in one sentence"
        summary_result = yield from request_gpt_model_in_new_thread_with_ui_alive(
            inputs=summary, 
            inputs_show_user=summary, 
            llm_kwargs=llm_kwargs, 
            chatbot=chatbot,
            history=[i_say, result],   # Analysis before iteration
            sys_prompt="You are a program architecture analyst，Analyzing source code of a project。" + sys_prompt_additional)

        report_part_2.extend([i_say, result])
        last_iteration_result = summary_result
        file_manifest = file_manifest[batchsize:]
        gpt_response_collection = gpt_response_collection[batchsize*2:]

    ############################## <END> ##################################
    history_to_return.extend(report_part_2)
    res = write_history_to_file(history_to_return)
    promote_file_to_downloadzone(res, chatbot=chatbot)
    chatbot.append(("Are you done?？", res))
    yield from update_ui(chatbot=chatbot, history=history_to_return) # Refresh the page


@CatchException
def ParseProjectItself(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    history = []    # Clear history，To avoid input overflow
    import glob
    file_manifest = [f for f in glob.glob('./*.py')] + \
                    [f for f in glob.glob('./*/*.py')]
    project_folder = './'
    if len(file_manifest) == 0:
        report_execption(chatbot, history, a = f"Parsing project: {txt}", b = f"No Python files found: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return
    yield from ParsingSourceCodeNew(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt)

@CatchException
def ParsePythonProject(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    history = []    # Clear history，To avoid input overflow
    import glob, os
    if os.path.exists(txt):
        project_folder = txt
    else:
        if txt == "": txt = 'Empty input field'
        report_execption(chatbot, history, a = f"Parsing project: {txt}", b = f"Cannot find local project or do not have access: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return
    file_manifest = [f for f in glob.glob(f'{project_folder}/**/*.py', recursive=True)]
    if len(file_manifest) == 0:
        report_execption(chatbot, history, a = f"Parsing project: {txt}", b = f"No Python files found: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return
    yield from ParsingSourceCodeNew(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt)

@CatchException
def AnalyzeAMatlabProject(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    history = []    # Clear history，To avoid input overflow
    import glob, os
    if os.path.exists(txt):
        project_folder = txt
    else:
        if txt == "": txt = 'Empty input field'
        report_execption(chatbot, history, a = f"Parse Matlab project: {txt}", b = f"Cannot find local project or do not have access: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return
    file_manifest = [f for f in glob.glob(f'{project_folder}/**/*.m', recursive=True)]
    if len(file_manifest) == 0:
        report_execption(chatbot, history, a = f"Parse Matlab project: {txt}", b = f"Unable to find any`.m`Source file: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return
    yield from ParsingSourceCodeNew(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt)

@CatchException
def ParseCProjectHeaderFiles(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    history = []    # Clear history，To avoid input overflow
    import glob, os
    if os.path.exists(txt):
        project_folder = txt
    else:
        if txt == "": txt = 'Empty input field'
        report_execption(chatbot, history, a = f"Parsing project: {txt}", b = f"Cannot find local project or do not have access: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return
    file_manifest = [f for f in glob.glob(f'{project_folder}/**/*.h', recursive=True)]  + \
                    [f for f in glob.glob(f'{project_folder}/**/*.hpp', recursive=True)] #+ \
                    # [f for f in glob.glob(f'{project_folder}/**/*.c', recursive=True)]
    if len(file_manifest) == 0:
        report_execption(chatbot, history, a = f"Parsing project: {txt}", b = f"No .h header files found: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return
    yield from ParsingSourceCodeNew(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt)

@CatchException
def ParseCProject(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    history = []    # Clear history，To avoid input overflow
    import glob, os
    if os.path.exists(txt):
        project_folder = txt
    else:
        if txt == "": txt = 'Empty input field'
        report_execption(chatbot, history, a = f"Parsing project: {txt}", b = f"Cannot find local project or do not have access: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return
    file_manifest = [f for f in glob.glob(f'{project_folder}/**/*.h', recursive=True)]  + \
                    [f for f in glob.glob(f'{project_folder}/**/*.cpp', recursive=True)] + \
                    [f for f in glob.glob(f'{project_folder}/**/*.hpp', recursive=True)] + \
                    [f for f in glob.glob(f'{project_folder}/**/*.c', recursive=True)]
    if len(file_manifest) == 0:
        report_execption(chatbot, history, a = f"Parsing project: {txt}", b = f"No .h header files found: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return
    yield from ParsingSourceCodeNew(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt)


@CatchException
def ParseJavaProject(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    history = []  # Clear history，To avoid input overflow
    import glob, os
    if os.path.exists(txt):
        project_folder = txt
    else:
        if txt == "": txt = 'Empty input field'
        report_execption(chatbot, history, a=f"Parsing project: {txt}", b=f"Cannot find local project or do not have access: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return
    file_manifest = [f for f in glob.glob(f'{project_folder}/**/*.java', recursive=True)] + \
                    [f for f in glob.glob(f'{project_folder}/**/*.jar', recursive=True)] + \
                    [f for f in glob.glob(f'{project_folder}/**/*.xml', recursive=True)] + \
                    [f for f in glob.glob(f'{project_folder}/**/*.sh', recursive=True)]
    if len(file_manifest) == 0:
        report_execption(chatbot, history, a=f"Parsing project: {txt}", b=f"No Java files found: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return
    yield from ParsingSourceCodeNew(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt)


@CatchException
def ParseFrontendProject(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    history = []  # Clear history，To avoid input overflow
    import glob, os
    if os.path.exists(txt):
        project_folder = txt
    else:
        if txt == "": txt = 'Empty input field'
        report_execption(chatbot, history, a=f"Parsing project: {txt}", b=f"Cannot find local project or do not have access: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return
    file_manifest = [f for f in glob.glob(f'{project_folder}/**/*.ts', recursive=True)] + \
                    [f for f in glob.glob(f'{project_folder}/**/*.tsx', recursive=True)] + \
                    [f for f in glob.glob(f'{project_folder}/**/*.json', recursive=True)] + \
                    [f for f in glob.glob(f'{project_folder}/**/*.js', recursive=True)] + \
                    [f for f in glob.glob(f'{project_folder}/**/*.vue', recursive=True)] + \
                    [f for f in glob.glob(f'{project_folder}/**/*.less', recursive=True)] + \
                    [f for f in glob.glob(f'{project_folder}/**/*.sass', recursive=True)] + \
                    [f for f in glob.glob(f'{project_folder}/**/*.wxml', recursive=True)] + \
                    [f for f in glob.glob(f'{project_folder}/**/*.wxss', recursive=True)] + \
                    [f for f in glob.glob(f'{project_folder}/**/*.css', recursive=True)] + \
                    [f for f in glob.glob(f'{project_folder}/**/*.jsx', recursive=True)]
    if len(file_manifest) == 0:
        report_execption(chatbot, history, a=f"Parsing project: {txt}", b=f"No front-end related files found: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return
    yield from ParsingSourceCodeNew(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt)


@CatchException
def ParseGolangProject(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    history = []  # Clear history，To avoid input overflow
    import glob, os
    if os.path.exists(txt):
        project_folder = txt
    else:
        if txt == "": txt = 'Empty input field'
        report_execption(chatbot, history, a=f"Parsing project: {txt}", b=f"Cannot find local project or do not have access: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return
    file_manifest = [f for f in glob.glob(f'{project_folder}/**/*.go', recursive=True)] + \
                    [f for f in glob.glob(f'{project_folder}/**/go.mod', recursive=True)] + \
                    [f for f in glob.glob(f'{project_folder}/**/go.sum', recursive=True)] + \
                    [f for f in glob.glob(f'{project_folder}/**/go.work', recursive=True)]
    if len(file_manifest) == 0:
        report_execption(chatbot, history, a=f"Parsing project: {txt}", b=f"No Golang files found: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return
    yield from ParsingSourceCodeNew(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt)

@CatchException
def ParseRustProject(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    history = []  # Clear history，To avoid input overflow
    import glob, os
    if os.path.exists(txt):
        project_folder = txt
    else:
        if txt == "": txt = 'Empty input field'
        report_execption(chatbot, history, a=f"Parsing project: {txt}", b=f"Cannot find local project or do not have access: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return
    file_manifest = [f for f in glob.glob(f'{project_folder}/**/*.rs', recursive=True)] + \
                    [f for f in glob.glob(f'{project_folder}/**/*.toml', recursive=True)] + \
                    [f for f in glob.glob(f'{project_folder}/**/*.lock', recursive=True)]
    if len(file_manifest) == 0:
        report_execption(chatbot, history, a=f"Parsing project: {txt}", b=f"No Golang files found: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return
    yield from ParsingSourceCodeNew(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt)

@CatchException
def ParsingLuaProject(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    history = []    # Clear history，To avoid input overflow
    import glob, os
    if os.path.exists(txt):
        project_folder = txt
    else:
        if txt == "": txt = 'Empty input field'
        report_execption(chatbot, history, a = f"Parsing project: {txt}", b = f"Cannot find local project or do not have access: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return
    file_manifest = [f for f in glob.glob(f'{project_folder}/**/*.lua', recursive=True)] + \
                    [f for f in glob.glob(f'{project_folder}/**/*.xml', recursive=True)] + \
                    [f for f in glob.glob(f'{project_folder}/**/*.json', recursive=True)] + \
                    [f for f in glob.glob(f'{project_folder}/**/*.toml', recursive=True)]
    if len(file_manifest) == 0:
        report_execption(chatbot, history, a = f"Parsing project: {txt}", b = f"No Lua files found: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return
    yield from ParsingSourceCodeNew(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt)


@CatchException
def ParsingCSharpProject(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    history = []    # Clear history，To avoid input overflow
    import glob, os
    if os.path.exists(txt):
        project_folder = txt
    else:
        if txt == "": txt = 'Empty input field'
        report_execption(chatbot, history, a = f"Parsing project: {txt}", b = f"Cannot find local project or do not have access: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return
    file_manifest = [f for f in glob.glob(f'{project_folder}/**/*.cs', recursive=True)] + \
                    [f for f in glob.glob(f'{project_folder}/**/*.csproj', recursive=True)]
    if len(file_manifest) == 0:
        report_execption(chatbot, history, a = f"Parsing project: {txt}", b = f"No CSharp files found: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return
    yield from ParsingSourceCodeNew(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt)


@CatchException
def ParseAnyCodeProject(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    txt_pattern = plugin_kwargs.get("advanced_arg")
    txt_pattern = txt_pattern.replace("，", ",")
    # Pattern to match(For example: *.c, *.cpp, *.py, config.toml)
    pattern_include = [_.lstrip(" ,").rstrip(" ,") for _ in txt_pattern.split(",") if _ != "" and not _.strip().startswith("^")]
    if not pattern_include: pattern_include = ["*"] # Match all if not input
    # File suffixes to ignore in matching(For example: ^*.c, ^*.cpp, ^*.py)
    pattern_except_suffix = [_.lstrip(" ^*.,").rstrip(" ,") for _ in txt_pattern.split(" ") if _ != "" and _.strip().startswith("^*.")]
    pattern_except_suffix += ['zip', 'rar', '7z', 'tar', 'gz'] # Avoid parsing compressed files
    # File names to ignore in matching(For example: ^README.md)
    pattern_except_name = [_.lstrip(" ^*,").rstrip(" ,").replace(".", "\.") for _ in txt_pattern.split(" ") if _ != "" and _.strip().startswith("^") and not _.strip().startswith("^*.")]
    # Generate regular expression
    pattern_except = '/[^/]+\.(' + "|".join(pattern_except_suffix) + ')$'
    pattern_except += '|/(' + "|".join(pattern_except_name) + ')$' if pattern_except_name != [] else ''

    history.clear()
    import glob, os, re
    if os.path.exists(txt):
        project_folder = txt
    else:
        if txt == "": txt = 'Empty input field'
        report_execption(chatbot, history, a = f"Parsing project: {txt}", b = f"Cannot find local project or do not have access: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return
    # If uploading compressed files, First find the path of the decompressed folder, Thus avoid parsing compressed files
    maybe_dir = [f for f in glob.glob(f'{project_folder}/*') if os.path.isdir(f)]
    if len(maybe_dir)>0 and maybe_dir[0].endswith('.extract'):
        extract_folder_path = maybe_dir[0]
    else:
        extract_folder_path = project_folder
    # Find uncompressed and decompressed files uploaded according to the input matching pattern
    file_manifest = [f for pattern in pattern_include for f in glob.glob(f'{extract_folder_path}/**/{pattern}', recursive=True) if "" != extract_folder_path and \
                      os.path.isfile(f) and (not re.search(pattern_except, f) or pattern.endswith('.' + re.search(pattern_except, f).group().split('.')[-1]))]
    if len(file_manifest) == 0:
        report_execption(chatbot, history, a = f"Parsing project: {txt}", b = f"No files found: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return
    yield from ParsingSourceCodeNew(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt)