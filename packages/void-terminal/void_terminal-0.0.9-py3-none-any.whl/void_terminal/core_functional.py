# 'primary' 颜色对应 theme.py 中的 primary_hue
# 'secondary' 颜色对应 theme.py 中的 neutral_hue
# 'stop' 颜色对应 theme.py 中的 color_er
import importlib
from void_terminal.toolbox import clear_line_break


def get_core_functions():
    return {
        "English academic polishing": {
            # Prefix，Will be added before your input。For example，Used to describe your requirements，such as translation, code interpretation, polishing, etc.
            "Prefix":   r"Below is a paragraph from an academic paper. Polish the writing to meet the academic style, " +
                        r"improve the spelling, grammar, clarity, concision and overall readability. When necessary, rewrite the whole sentence. " +
                        r"Firstly, you should provide the polished paragraph. "
                        r"Secondly, you should list all your modification and explain the reasons to do so in markdown table." + "\n\n",
            # Suffix，Will be added after your input。For example，With the prefix, you can enclose your input content in quotation marks
            "Suffix":   r"",
            # Button color (Default secondary)
            "Color":    r"secondary",
            # Is the button visible? (Default True，Visible immediately)
            "Visible": True,
            # Whether to clear history when triggered (Default False，That is, do not process previous conversation history)
            "AutoClearHistory": False
        },
        "Chinese academic polishing": {
            "Prefix":   r"As a Chinese academic paper writing improvement assistant，Your task is to improve the spelling, grammar, clarity, conciseness and overall readability of the provided text，" +
                        r"Also, break down long sentences，Reduce repetition，And provide improvement suggestions。Please only provide corrected versions of the text，Avoid including explanations。Please edit the following text" + "\n\n",
            "Suffix":   r"",
        },
        "Find syntax errors": {
            "Prefix":   r"Help me ensure that the grammar and the spelling is correct. "
                        r"Do not try to polish the text, if no mistake is found, tell me that this paragraph is good. "
                        r"If you find grammar or spelling mistakes, please list mistakes you find in a two-column markdown table, "
                        r"put the original text the first column, "
                        r"put the corrected text in the second column and highlight the key words you fixed. "
                        r"Finally, please provide the proofreaded text.""\n\n"
                        r"Example:""\n"
                        r"Paragraph: How is you? Do you knows what is it?""\n"
                        r"| Original sentence | Corrected sentence |""\n"
                        r"| :--- | :--- |""\n"
                        r"| How **is** you? | How **are** you? |""\n"
                        r"| Do you **knows** what **is** **it**? | Do you **know** what **it** **is** ? |""\n\n"
                        r"Below is a paragraph from an academic paper. "
                        r"You need to report all grammar and spelling mistakes as the example before."
                        + "\n\n",
            "Suffix":   r"",
            "PreProcess": clear_line_break,    # Preprocessing：Remove line breaks
        },
        "Chinese to English translation": {
            "Prefix":   r"Please translate following sentence to English:" + "\n\n",
            "Suffix":   r"",
        },
        "Academic Chinese-English Translation": {
            "Prefix":   r"I want you to act as a scientific English-Chinese translator, " +
                        r"I will provide you with some paragraphs in one language " +
                        r"and your task is to accurately and academically translate the paragraphs only into the other language. " +
                        r"Do not repeat the original provided paragraphs after translation. " +
                        r"You should use artificial intelligence tools, " +
                        r"such as natural language processing, and rhetorical knowledge " +
                        r"and experience about effective writing techniques to reply. " +
                        r"I'll give you my paragraphs as follows, tell me what language it is written in, and then translate:" + "\n\n",
            "Suffix": "",
            "Color": "secondary",
        },
        "English to Chinese translation": {
            "Prefix":   r"Translate into authentic Chinese：" + "\n\n",
            "Suffix":   r"",
            "Visible": False,
        },
        "Find image": {
            "Prefix":   r"I need you to find a web image。Use Unsplash API(https://source.unsplash.com/960x640/?<English keywords>)Get image URL，" +
                        r"Then please wrap it in Markdown format，And do not use backslashes，Do not use code blocks。Now，Please send me the image following the description below：" + "\n\n",
            "Suffix":   r"",
            "Visible": False,
        },
        "Explain code": {
            "Prefix":   r"Please explain the following code：" + "\n```\n",
            "Suffix":   "\n```\n",
        },
        "Convert reference to Bib": {
            "Prefix":   r"Here are some bibliography items, please transform them into bibtex style." +
                        r"Note that, reference styles maybe more than one kind, you should transform each item correctly." +
                        r"Items need to be transformed:",
            "Visible": False,
            "Suffix":   r"",
        }
    }


def handle_core_functionality(additional_fn, inputs, history, chatbot):
    import core_functional
    importlib.reload(core_functional)    # Hot update prompt
    core_functional = core_functional.get_core_functions()
    addition = chatbot._cookies['customize_fn_overwrite']
    if additional_fn in addition:
        # Custom Function
        inputs = addition[additional_fn]["Prefix"] + inputs + addition[additional_fn]["Suffix"]
        return inputs, history
    else:
        # Prefabricated Function
        if "PreProcess" in core_functional[additional_fn]: inputs = core_functional[additional_fn]["PreProcess"](inputs)  # Get preprocessing function（If any）
        inputs = core_functional[additional_fn]["Prefix"] + inputs + core_functional[additional_fn]["Suffix"]
        if core_functional[additional_fn].get("AutoClearHistory", False):
            history = []
        return inputs, history
