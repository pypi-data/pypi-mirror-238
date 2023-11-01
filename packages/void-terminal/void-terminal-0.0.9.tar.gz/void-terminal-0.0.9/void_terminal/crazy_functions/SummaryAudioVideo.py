from void_terminal.toolbox import CatchException, report_execption, select_api_key, update_ui, get_conf
from void_terminal.crazy_functions.crazy_utils import request_gpt_model_in_new_thread_with_ui_alive
from void_terminal.toolbox import write_history_to_file, promote_file_to_downloadzone, get_log_folder

def split_audio_file(filename, split_duration=1000):
    """
    Cut the audio file into multiple segments according to the given cutting duration。

    Args:
        filename (str): Name of audio file to be cut。
        split_duration (int, optional): The duration of each cut audio segment（In seconds）。Default value is 1000。

    Returns:
        filelist (list): A list containing the file paths of all segmented audio clips。

    """
    from moviepy.editor import AudioFileClip
    import os
    os.makedirs(f"{get_log_folder(plugin_name='audio')}/mp3/cut/", exist_ok=True)  # Create folder to store segmented audio

    # Reading audio files
    audio = AudioFileClip(filename)

    # Calculate total duration and cutting points of the file
    total_duration = audio.duration
    split_points = list(range(0, int(total_duration), split_duration))
    split_points.append(int(total_duration))
    filelist = []

    # Cut audio file
    for i in range(len(split_points) - 1):
        start_time = split_points[i]
        end_time = split_points[i + 1]
        split_audio = audio.subclip(start_time, end_time)
        split_audio.write_audiofile(f"{get_log_folder(plugin_name='audio')}/mp3/cut/{filename[0]}_{i}.mp3")
        filelist.append(f"{get_log_folder(plugin_name='audio')}/mp3/cut/{filename[0]}_{i}.mp3")

    audio.close()
    return filelist

def AnalyAudio(parse_prompt, file_manifest, llm_kwargs, chatbot, history):
    import os, requests
    from moviepy.editor import AudioFileClip
    from void_terminal.request_llms.bridge_all import model_info

    # Set OpenAI key and model
    api_key = select_api_key(llm_kwargs['api_key'], llm_kwargs['llm_model'])
    chat_endpoint = model_info[llm_kwargs['llm_model']]['endpoint']

    whisper_endpoint = chat_endpoint.replace('chat/completions', 'audio/transcriptions')
    url = whisper_endpoint
    headers = {
        'Authorization': f"Bearer {api_key}"
    }

    os.makedirs(f"{get_log_folder(plugin_name='audio')}/mp3/", exist_ok=True)
    for index, fp in enumerate(file_manifest):
        audio_history = []
        # Extract the file extension
        ext = os.path.splitext(fp)[1]
        # Extract audio from video
        if ext not in [".mp3", ".wav", ".m4a", ".mpga"]:
            audio_clip = AudioFileClip(fp)
            audio_clip.write_audiofile(f"{get_log_folder(plugin_name='audio')}/mp3/output{index}.mp3")
            fp = f"{get_log_folder(plugin_name='audio')}/mp3/output{index}.mp3"
        # Call whisper model to convert audio to text
        voice = split_audio_file(fp)
        for j, i in enumerate(voice):
            with open(i, 'rb') as f:
                file_content = f.read()  # Read file content into memory
                files = {
                    'file': (os.path.basename(i), file_content),
                }
                data = {
                    "model": "whisper-1",
                    "prompt": parse_prompt,
                    'response_format': "text"
                }

            chatbot.append([f"Convert {i} Send to openai audio parsing terminal (whisper)，Current parameters：{parse_prompt}", "Processing ..."])
            yield from update_ui(chatbot=chatbot, history=history)  # Refresh the page
            proxies = get_conf('proxies')
            response = requests.post(url, headers=headers, files=files, data=data, proxies=proxies).text

            chatbot.append(["Audio parsing result", response])
            history.extend(["Audio parsing result", response])
            yield from update_ui(chatbot=chatbot, history=history)  # Refresh the page

            i_say = f'Please summarize the following audio clip，The content of the audio is ```{response}```'
            i_say_show_user = f'The{index + 1}The{j + 1} / {len(voice)}Segment。'
            gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
                inputs=i_say,
                inputs_show_user=i_say_show_user,
                llm_kwargs=llm_kwargs,
                chatbot=chatbot,
                history=[],
                sys_prompt=f"Summarize audio。Audio file name{fp}"
            )

            chatbot[-1] = (i_say_show_user, gpt_say)
            history.extend([i_say_show_user, gpt_say])
            audio_history.extend([i_say_show_user, gpt_say])

        # All segments of the article have been summarized，If the article is cut into pieces
        result = "".join(audio_history)
        if len(audio_history) > 1:
            i_say = f"According to the above dialogue，Use Chinese to summarize audio{result}The main content of 。"
            i_say_show_user = f'The{index + 1}The main content of the segment audio is：'
            gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
                inputs=i_say,
                inputs_show_user=i_say_show_user,
                llm_kwargs=llm_kwargs,
                chatbot=chatbot,
                history=audio_history,
                sys_prompt="Summarize the article。"
            )
            history.extend([i_say, gpt_say])
            audio_history.extend([i_say, gpt_say])

        res = write_history_to_file(history)
        promote_file_to_downloadzone(res, chatbot=chatbot)
        chatbot.append((f"The{index + 1}Is the segment audio completed?？", res))
        yield from update_ui(chatbot=chatbot, history=history)  # Refresh the page

    # Delete intermediate folder
    import shutil
    shutil.rmtree(f"{get_log_folder(plugin_name='audio')}/mp3")
    res = write_history_to_file(history)
    promote_file_to_downloadzone(res, chatbot=chatbot)
    chatbot.append(("Are all audio summaries completed?？", res))
    yield from update_ui(chatbot=chatbot, history=history)


@CatchException
def SummaryAudioVideo(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, WEB_PORT):
    import glob, os

    # Basic information：Function, contributor
    chatbot.append([
        "Function plugin feature？",
        "SummaryAudioVideo content，Function plugin contributor: dalvqw & BinaryHusky"])
    yield from update_ui(chatbot=chatbot, history=history)  # Refresh the page

    try:
        from moviepy.editor import AudioFileClip
    except:
        report_execption(chatbot, history,
                         a=f"Parsing project: {txt}",
                         b=f"Failed to import software dependencies。Using this module requires additional dependencies，Installation method```pip install --upgrade moviepy```。")
        yield from update_ui(chatbot=chatbot, history=history)  # Refresh the page
        return

    # Clear history，To avoid input overflow
    history = []

    # Checking input parameters，If no input parameters are given，Exit directly
    if os.path.exists(txt):
        project_folder = txt
    else:
        if txt == "": txt = 'Empty input field'
        report_execption(chatbot, history, a=f"Parsing project: {txt}", b=f"Cannot find local project or do not have access: {txt}")
        yield from update_ui(chatbot=chatbot, history=history)  # Refresh the page
        return

    # Search for the list of files to be processed
    extensions = ['.mp4', '.m4a', '.wav', '.mpga', '.mpeg', '.mp3', '.avi', '.mkv', '.flac', '.aac']

    if txt.endswith(tuple(extensions)):
        file_manifest = [txt]
    else:
        file_manifest = []
        for extension in extensions:
            file_manifest.extend(glob.glob(f'{project_folder}/**/*{extension}', recursive=True))

    # If no files are found
    if len(file_manifest) == 0:
        report_execption(chatbot, history, a=f"Parsing project: {txt}", b=f"Cannot find any audio or video files: {txt}")
        yield from update_ui(chatbot=chatbot, history=history)  # Refresh the page
        return

    # Start executing the task formally
    if ("advanced_arg" in plugin_kwargs) and (plugin_kwargs["advanced_arg"] == ""): plugin_kwargs.pop("advanced_arg")
    parse_prompt = plugin_kwargs.get("advanced_arg", 'Parse audio into Simplified Chinese')
    yield from AnalyAudio(parse_prompt, file_manifest, llm_kwargs, chatbot, history)

    yield from update_ui(chatbot=chatbot, history=history)  # Refresh the page
