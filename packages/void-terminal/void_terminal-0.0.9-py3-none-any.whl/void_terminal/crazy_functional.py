from void_terminal.toolbox import HotReload  # HotReload means hot update，After modifying the function plugin，No need to restart the program，The code takes effect directly


def get_crazy_functions():
    from void_terminal.crazy_functions.ReadArticleWriteSummary import ReadArticleWriteSummary
    from void_terminal.crazy_functions.GenerateFunctionComments import BatchGenerateFunctionComments
    from void_terminal.crazy_functions.ParseProjectSourceCode import ParseProjectItself
    from void_terminal.crazy_functions.ParseProjectSourceCode import ParsePythonProject
    from void_terminal.crazy_functions.ParseProjectSourceCode import AnalyzeAMatlabProject
    from void_terminal.crazy_functions.ParseProjectSourceCode import ParseCProjectHeaderFiles
    from void_terminal.crazy_functions.ParseProjectSourceCode import ParseCProject
    from void_terminal.crazy_functions.ParseProjectSourceCode import ParseGolangProject
    from void_terminal.crazy_functions.ParseProjectSourceCode import ParseRustProject
    from void_terminal.crazy_functions.ParseProjectSourceCode import ParseJavaProject
    from void_terminal.crazy_functions.ParseProjectSourceCode import ParseFrontendProject
    from void_terminal.crazy_functions.AdvancedFunctionTemplate import HighOrderFunctionTemplateFunctions
    from void_terminal.crazy_functions.FullTextProofreadingForLatex import EnglishProofreadingForLatex
    from void_terminal.crazy_functions.InquiryMultipleLargeLanguageModels import SimultaneousInquiry
    from void_terminal.crazy_functions.ParseProjectSourceCode import ParsingLuaProject
    from void_terminal.crazy_functions.ParseProjectSourceCode import ParsingCSharpProject
    from void_terminal.crazy_functions.SummarizingWordDocuments import SummarizingWordDocuments
    from void_terminal.crazy_functions.ParsingJupyterNotebook import ParsingIpynbFiles
    from void_terminal.crazy_functions.ConversationHistoryArchive import ConversationHistoryArchive
    from void_terminal.crazy_functions.ConversationHistoryArchive import LoadConversationHistoryArchive
    from void_terminal.crazy_functions.ConversationHistoryArchive import DeleteAllLocalConversationHistoryRecords
    from void_terminal.crazy_functions.Accessibility import ClearCache
    from void_terminal.crazy_functions.BatchTranslateMarkdown import TranslateMarkdownFromEnglishToChinese
    from void_terminal.crazy_functions.BatchSummarizePDFDocuments import BatchSummarizePDFDocuments
    from void_terminal.crazy_functions.BatchTranslatePDFDocuments_MultiThreaded import BatchTranslatePDFDocuments
    from void_terminal.crazy_functions.GoogleSearchAssistant import GoogleSearchAssistant
    from void_terminal.crazy_functions.UnderstandPdfDocumentContent import UnderstandPdfDocumentContentStandardFileInput
    from void_terminal.crazy_functions.FullTextProofreadingForLatex import LatexChineseProofreading
    from void_terminal.crazy_functions.FullTextProofreadingForLatex import LatexEnglishCorrection
    from void_terminal.crazy_functions.LatexFullTextTranslation import LatexChineseToEnglish
    from void_terminal.crazy_functions.LatexFullTextTranslation import LatexEnglishToChinese
    from void_terminal.crazy_functions.BatchTranslateMarkdown import MarkdownChineseToEnglish
    from void_terminal.crazy_functions.VoidTerminal import VoidTerminal


    function_plugins = {
        "VoidTerminal": {
            "Group": "Dialogue|Programming|Academic|Intelligent agent",
            "Color": "stop",
            "AsButton": True,
            "Function": HotReload(VoidTerminal)
        },
        "Parse the entire Python project": {
            "Group": "programming",
            "Color": "stop",
            "AsButton": True,
            "Info": "All source files of ParsePythonProject(.py) | Input parameter is the path",
            "Function": HotReload(ParsePythonProject)
        },
        "LoadConversationHistoryArchive（Upload archive or enter path first）": {
            "Group": "Conversation",
            "Color": "stop",
            "AsButton": False,
            "Info": "LoadConversationHistoryArchive | Input parameter is a path",
            "Function": HotReload(LoadConversationHistoryArchive)
        },
        "DeleteAllLocalConversationHistoryRecords（Handle with caution）": {
            "Group": "Conversation",
            "AsButton": False,
            "Info": "DeleteAllLocalConversationHistoryRecords，Handle with caution | No input parameters required",
            "Function": HotReload(DeleteAllLocalConversationHistoryRecords)
        },
        "Clear all cache files（Handle with caution）": {
            "Group": "Conversation",
            "Color": "stop",
            "AsButton": False,  # Add to the drop-down menu
            "Info": "Clear all cache files，Handle with caution | No input parameters required",
            "Function": HotReload(ClearCache)
        },
        "Batch summarize Word documents": {
            "Group": "Academic",
            "Color": "stop",
            "AsButton": True,
            "Info": "Batch SummarizingWordDocuments | Input parameter is the path",
            "Function": HotReload(SummarizingWordDocuments)
        },
        "Parse the entire Matlab project": {
            "Group": "programming",
            "Color": "stop",
            "AsButton": False,
            "Info": "All source files of AnalyzeAMatlabProject(.m) | Input parameter is the path",
            "Function": HotReload(AnalyzeAMatlabProject)
        },
        "Parse the entire C++ project header file": {
            "Group": "programming",
            "Color": "stop",
            "AsButton": False,  # Add to the drop-down menu
            "Info": "Parse all header files of a C++ project(.h/.hpp) | Input parameter is the path",
            "Function": HotReload(ParseCProjectHeaderFiles)
        },
        "Parse the entire C++ project（.cpp/.hpp/.c/.h）": {
            "Group": "programming",
            "Color": "stop",
            "AsButton": False,  # Add to the drop-down menu
            "Info": "Parse all source files of a C++ project（.cpp/.hpp/.c/.h）| Input parameter is the path",
            "Function": HotReload(ParseCProject)
        },
        "Parse the entire Go project": {
            "Group": "programming",
            "Color": "stop",
            "AsButton": False,  # Add to the drop-down menu
            "Info": "Parse all source files of a Go project | Input parameter is path",
            "Function": HotReload(ParseGolangProject)
        },
        "Parse the entire Go project": {
            "Group": "programming",
            "Color": "stop",
            "AsButton": False,  # Add to the drop-down menu
            "Info": "All source files of ParseRustProject | Input parameter is path",
            "Function": HotReload(ParseRustProject)
        },
        "Parse the entire Java project": {
            "Group": "programming",
            "Color": "stop",
            "AsButton": False,  # Add to the drop-down menu
            "Info": "All source files of ParseJavaProject | Input parameter is path",
            "Function": HotReload(ParseJavaProject)
        },
        "Parse the entire front-end project（js,ts,CSS, etc.）": {
            "Group": "programming",
            "Color": "stop",
            "AsButton": False,  # Add to the drop-down menu
            "Info": "Parse all source files of ParseFrontendProject（js,ts,CSS, etc.） | Input parameter is the path",
            "Function": HotReload(ParseFrontendProject)
        },
        "Parse the entire Lua project": {
            "Group": "programming",
            "Color": "stop",
            "AsButton": False,  # Add to the drop-down menu
            "Info": "All source files of ParsingLuaProject | Input parameter is path",
            "Function": HotReload(ParsingLuaProject)
        },
        "Parse the entire C# project": {
            "Group": "programming",
            "Color": "stop",
            "AsButton": False,  # Add to the drop-down menu
            "Info": "ParsingCSharpProject`s all source files | Input parameter is a path",
            "Function": HotReload(ParsingCSharpProject)
        },
        "Parse Jupyter Notebook files": {
            "Group": "programming",
            "Color": "stop",
            "AsButton": False,
            "Info": "Parse Jupyter Notebook file | Input parameter is path",
            "Function": HotReload(ParsingIpynbFiles),
            "AdvancedArgs": True,  # When calling，Invoke the advanced parameter input area（Default is False）
            "ArgsReminder": "If 0 is entered，Do not parse Markdown blocks in the notebook",  # Display prompt in the advanced parameter input area
        },
        "Read Tex paper and write abstract": {
            "Group": "Academic",
            "Color": "stop",
            "AsButton": False,
            "Info": "Read Tex paper and write abstract | Input parameter is the path",
            "Function": HotReload(ReadArticleWriteSummary)
        },
        "Translate README or MD": {
            "Group": "programming",
            "Color": "stop",
            "AsButton": True,
            "Info": "Translate Markdown to Chinese | Input parameters are path or URL",
            "Function": HotReload(TranslateMarkdownFromEnglishToChinese)
        },
        "Translate Markdown or README（Support Github links）": {
            "Group": "programming",
            "Color": "stop",
            "AsButton": False,
            "Info": "Translate Markdown or README to Chinese | Input parameters are path or URL",
            "Function": HotReload(TranslateMarkdownFromEnglishToChinese)
        },
        "BatchGenerateFunctionComments": {
            "Group": "programming",
            "Color": "stop",
            "AsButton": False,  # Add to the drop-down menu
            "Info": "Batch generate function comments | Input parameter is the path",
            "Function": HotReload(BatchGenerateFunctionComments)
        },
        "Save the current conversation": {
            "Group": "Conversation",
            "AsButton": True,
            "Info": "Save current conversation | No input parameters required",
            "Function": HotReload(ConversationHistoryArchive)
        },
        "[Multithreading demo]Parse this project itself（Translate the source code）": {
            "Group": "Conversation|Programming",
            "AsButton": False,  # Add to the drop-down menu
            "Info": "Parse and translate the source code of this project in multi-threading | No input parameters required",
            "Function": HotReload(ParseProjectItself)
        },
        "Today in history": {
            "Group": "Conversation",
            "AsButton": True,
            "Info": "View events from history (This is a plugin demo for developers) | No input parameters required",
            "Function": HotReload(HighOrderFunctionTemplateFunctions)
        },
        "Accurate translation of PDF paper": {
            "Group": "Academic",
            "Color": "stop",
            "AsButton": True,  
            "Info": "Translate PDF papers accurately into Chinese | Input parameter is the path",
            "Function": HotReload(BatchTranslatePDFDocuments)
        },
        "Inquire multiple GPT models": {
            "Group": "Conversation",
            "Color": "stop",
            "AsButton": True,
            "Function": HotReload(SimultaneousInquiry)
        },
        "BatchSummarizePDFDocuments": {
            "Group": "Academic",
            "Color": "stop",
            "AsButton": False,  # Add to the drop-down menu
            "Info": "Content of BatchSummarizePDFDocuments | Input parameter is a path",
            "Function": HotReload(BatchSummarizePDFDocuments)
        },
        "Google Scholar search assistant（Enter the URL of Google Scholar search page）": {
            "Group": "Academic",
            "Color": "stop",
            "AsButton": False,  # Add to the drop-down menu
            "Info": "Use Google Scholar search assistant to search for results of a specific URL | Input parameter is the URL of Google Scholar search page",
            "Function": HotReload(GoogleSearchAssistant)
        },
        "UnderstandPdfDocumentContent （Imitate ChatPDF）": {
            "Group": "Academic",
            "Color": "stop",
            "AsButton": False,  # Add to the drop-down menu
            "Info": "Understand the content of the PDF document and answer | Input parameter is path",
            "Function": HotReload(UnderstandPdfDocumentContentStandardFileInput)
        },
        "English Latex project full text proofreading（Input path or upload compressed package）": {
            "Group": "Academic",
            "Color": "stop",
            "AsButton": False,  # Add to the drop-down menu
            "Info": "Polish the full text of English Latex projects | Input parameters are paths or uploaded compressed packages",
            "Function": HotReload(EnglishProofreadingForLatex)
        },
        "Full-text correction of English Latex projects（Input path or upload compressed package）": {
            "Group": "Academic",
            "Color": "stop",
            "AsButton": False,  # Add to the drop-down menu
            "Info": "Correct the entire English Latex project | Input parameter is the path or upload compressed package",
            "Function": HotReload(LatexEnglishCorrection)
        },
        "Chinese Latex project full text proofreading（Input path or upload compressed package）": {
            "Group": "Academic",
            "Color": "stop",
            "AsButton": False,  # Add to the drop-down menu
            "Info": "Polish the entire text of a Chinese Latex project | Input parameter is path or upload compressed package",
            "Function": HotReload(LatexChineseProofreading)
        },

        # Has been replaced by a new plugin
        # "Latex project full text translation from Chinese to English（Input path or upload compressed package）": {
        #     "Group": "Academic",
        #     "Color": "stop",
        #     "AsButton": False,  # Add to the drop-down menu
        #     "Info": "Translate the full text of Latex projects from Chinese to English | Input parameter is the path or upload a compressed package",
        #     "Function": HotReload(LatexChineseToEnglish)
        # },

        # Has been replaced by a new plugin
        # "Latex project full text translation from English to Chinese（Input path or upload compressed package）": {
        #     "Group": "Academic",
        #     "Color": "stop",
        #     "AsButton": False,  # Add to the drop-down menu
        #     "Info": "Translate the entire text of Latex project from English to Chinese | Input parameters are path or uploaded compressed package",
        #     "Function": HotReload(LatexEnglishToChinese)
        # },
        
        "Batch Markdown Chinese to English（Input path or upload compressed package）": {
            "Group": "programming",
            "Color": "stop",
            "AsButton": False,  # Add to the drop-down menu
            "Info": "Batch translate Chinese to English in Markdown files | Input parameter is a path or upload a compressed package",
            "Function": HotReload(MarkdownChineseToEnglish)
        },
    }

    # -=--=- Experimental plugins that have not been fully tested & plugins that require additional dependencies -=--=-
    try:
        from void_terminal.crazy_functions.DownloadArxivPaperTranslateAbstract import DownloadArxivPaperAndTranslateAbstract
        function_plugins.update({
            "One-click Download Arxiv Paper and Translate Abstract（Enter the number in input first，e.g. 1812.10695）": {
                "Group": "Academic",
                "Color": "stop",
                "AsButton": False,  # Add to the drop-down menu
                # "Info": "DownloadArxivPaperAndTranslateAbstract | InputParameters为arxiv编号e.g. 1812.10695",
                "Function": HotReload(DownloadArxivPaperAndTranslateAbstract)
            }
        })
    except:
        print('Load function plugin failed')

    try:
        from void_terminal.crazy_functions.ChatGPTConnectedToNetwork import ConnectToNetworkToAnswerQuestions
        function_plugins.update({
            "ConnectToNetworkToAnswerQuestions（Click the plugin after entering the question，Access to Google is required）": {
                "Group": "Conversation",
                "Color": "stop",
                "AsButton": False,  # Add to the drop-down menu
                # "Info": "ConnectToNetworkToAnswerQuestions（Access to Google is required）| Input parameter is a question",
                "Function": HotReload(ConnectToNetworkToAnswerQuestions)
            }
        })
        from void_terminal.crazy_functions.OnlineChatGPT_BingEdition import ConnectBingSearchAnswerQuestion
        function_plugins.update({
            "ConnectToNetworkToAnswerQuestions（Chinese Bing version，Click the plugin after entering the question）": {
                "Group": "Conversation",
                "Color": "stop",
                "AsButton": False,  # Add to the drop-down menu
                "Info": "ConnectToNetworkToAnswerQuestions（Need to access Chinese Bing）| Input parameter is a question",
                "Function": HotReload(ConnectBingSearchAnswerQuestion)
            }
        })
    except:
        print('Load function plugin failed')

    try:
        from void_terminal.crazy_functions.ParseProjectSourceCode import ParseAnyCodeProject
        function_plugins.update({
            "ParseProjectSourceCode（Manually specify and filter the source code file type）": {
                "Group": "programming",
                "Color": "stop",
                "AsButton": False,
                "AdvancedArgs": True,  # When calling，Invoke the advanced parameter input area（Default is False）
                "ArgsReminder": "Separate with commas when entering, * stands for wildcard, Adding ^ means not matching; Not entering means matching all。For example: \"*.c, ^*.cpp, config.toml, ^*.toml\"",  # Display prompt in the advanced parameter input area
                "Function": HotReload(ParseAnyCodeProject)
            },
        })
    except:
        print('Load function plugin failed')

    try:
        from void_terminal.crazy_functions.InquiryMultipleLargeLanguageModels import InquireSimultaneously_SpecifiedModel
        function_plugins.update({
            "Inquire multiple GPT models（Manually specify which models to ask）": {
                "Group": "Conversation",
                "Color": "stop",
                "AsButton": False,
                "AdvancedArgs": True,  # When calling，Invoke the advanced parameter input area（Default is False）
                "ArgsReminder": "Support any number of llm interfaces，Separate with & symbol。e.g. chatglm&gpt-3.5-turbo&api2d-gpt-4",  # Display prompt in the advanced parameter input area
                "Function": HotReload(InquireSimultaneously_SpecifiedModel)
            },
        })
    except:
        print('Load function plugin failed')

    try:
        from void_terminal.crazy_functions.ImageGeneration import ImageGeneration
        function_plugins.update({
            "ImageGeneration（Switch the model to openai or api2d first）": {
                "Group": "Conversation",
                "Color": "stop",
                "AsButton": False,
                "AdvancedArgs": True,  # When calling，Invoke the advanced parameter input area（Default is False）
                "ArgsReminder": "Enter the resolution here, e.g. 256x256（Default）",  # Display prompt in the advanced parameter input area
                "Info": "ImageGeneration | Input parameter string，Provide the content of the image",
                "Function": HotReload(ImageGeneration)
            },
        })
    except:
        print('Load function plugin failed')

    try:
        from void_terminal.crazy_functions.SummaryAudioVideo import SummaryAudioVideo
        function_plugins.update({
            "Batch Summary Audio Video（Input path or upload compressed package）": {
                "Group": "Conversation",
                "Color": "stop",
                "AsButton": False,
                "AdvancedArgs": True,
                "ArgsReminder": "Call openai api to use whisper-1 model, Supported formats at present:mp4, m4a, wav, mpga, mpeg, mp3。Parsing tips can be entered here，For example：Parse to Simplified Chinese（Default）。",
                "Info": "Batch summarize audio or video | Input parameter is path",
                "Function": HotReload(SummaryAudioVideo)
            }
        })
    except:
        print('Load function plugin failed')

    try:
        from void_terminal.crazy_functions.MathematicalAnimationGenerationManim import AnimationGeneration
        function_plugins.update({
            "Mathematical Animation Generation（Manim）": {
                "Group": "Conversation",
                "Color": "stop",
                "AsButton": False,
                "Info": "Generate an animation based on natural language description | Input parameter is a sentence",
                "Function": HotReload(AnimationGeneration)
            }
        })
    except:
        print('Load function plugin failed')

    try:
        from void_terminal.crazy_functions.BatchTranslateMarkdown import TranslateMarkdownToSpecifiedLanguage
        function_plugins.update({
            "Markdown translation（Specify the language to translate into）": {
                "Group": "programming",
                "Color": "stop",
                "AsButton": False,
                "AdvancedArgs": True,
                "ArgsReminder": "Please enter which language to translate into，Default is Chinese。",
                "Function": HotReload(TranslateMarkdownToSpecifiedLanguage)
            }
        })
    except:
        print('Load function plugin failed')

    try:
        from void_terminal.crazy_functions.LangchainKnowledgeBase import UpdateKnowledgeArchive
        function_plugins.update({
            "Building knowledge base（Upload file materials first,Run this plugin again）": {
                "Group": "Conversation",
                "Color": "stop",
                "AsButton": False,
                "AdvancedArgs": True,
                "ArgsReminder": "The knowledge base name ID to be injected here, Default is `default`。Files can be saved for a long time after entering the knowledge base。You can use this plugin again by calling it，Append more documents to the knowledge base。",
                "Function": HotReload(UpdateKnowledgeArchive)
            }
        })
    except:
        print('Load function plugin failed')

    try:
        from void_terminal.crazy_functions.LangchainKnowledgeBase import ReadKnowledgeArchiveAnswerQuestions
        function_plugins.update({
            "UpdateKnowledgeArchive（After building the knowledge base,Run this plugin again）": {
                "Group": "Conversation",
                "Color": "stop",
                "AsButton": False,
                "AdvancedArgs": True,
                "ArgsReminder": "Knowledge base name ID to be extracted, Default is `default`, You need to build the knowledge base before running this plugin。",
                "Function": HotReload(ReadKnowledgeArchiveAnswerQuestions)
            }
        })
    except:
        print('Load function plugin failed')

    try:
        from void_terminal.crazy_functions.InteractiveFunctionFunctionTemplate import InteractiveFunctionTemplateFunction
        function_plugins.update({
            "Interactive function template Demo function（Search for wallpapers on wallhaven.cc）": {
                "Group": "Conversation",
                "Color": "stop",
                "AsButton": False,
                "Function": HotReload(InteractiveFunctionTemplateFunction)
            }
        })
    except:
        print('Load function plugin failed')

    try:
        from void_terminal.crazy_functions.OutputPDFFromLatex import CorrectEnglishInLatexWithPDFComparison
        function_plugins.update({
            "Latex English correction + highlight correction position [Requires Latex]": {
                "Group": "Academic",
                "Color": "stop",
                "AsButton": False,
                "AdvancedArgs": True,
                "ArgsReminder": "If necessary, Please append more detailed correction instructions here（Use English）。",
                "Function": HotReload(CorrectEnglishInLatexWithPDFComparison)
            }
        })
        from void_terminal.crazy_functions.OutputPDFFromLatex import TranslateChineseToEnglishInLatexAndRecompilePDF
        function_plugins.update({
            "Fine translation of Arixv paper（Enter arxivID）[Requires Latex]": {
                "Group": "Academic",
                "Color": "stop",
                "AsButton": False,
                "AdvancedArgs": True,
                "ArgsReminder":
                    "If necessary, Please provide custom translation command here, Resolve the issue of inaccurate translation for some terms。 " +
                    "For example当单词'agent'Translation不准确When, Please try copying the following instructions to the advanced parameters section: " +
                    'If the term "agent" is used in this section, it should be translated to "Intelligent agent". ',
                "Info": "Fine translation of Arixv paper | Input parameter is the ID of arxiv paper，For example, 1812.10695",
                "Function": HotReload(TranslateChineseToEnglishInLatexAndRecompilePDF)
            }
        })
        function_plugins.update({
            "Local Latex paper fine translation（Upload Latex project）[Requires Latex]": {
                "Group": "Academic",
                "Color": "stop",
                "AsButton": False,
                "AdvancedArgs": True,
                "ArgsReminder":
                    "If necessary, Please provide custom translation command here, Resolve the issue of inaccurate translation for some terms。 " +
                    "For example当单词'agent'Translation不准确When, Please try copying the following instructions to the advanced parameters section: " +
                    'If the term "agent" is used in this section, it should be translated to "Intelligent agent". ',
                "Info": "Locally translate Latex papers with fine-grained translation | Input parameter is the path",
                "Function": HotReload(TranslateChineseToEnglishInLatexAndRecompilePDF)
            }
        })
    except:
        print('Load function plugin failed')

    try:
        from void_terminal.toolbox import get_conf
        ENABLE_AUDIO = get_conf('ENABLE_AUDIO')
        if ENABLE_AUDIO:
            from void_terminal.crazy_functions.VoiceAssistant import VoiceAssistant
            function_plugins.update({
                "Real-time voice conversation": {
                    "Group": "Conversation",
                    "Color": "stop",
                    "AsButton": True,
                    "Info": "This is a voice conversation assistant that is always listening | No input parameters",
                    "Function": HotReload(VoiceAssistant)
                }
            })
    except:
        print('Load function plugin failed')

    try:
        from void_terminal.crazy_functions.BatchTranslatePDFDocuments_NOUGAT import BatchTranslatePDFDocuments
        function_plugins.update({
            "Accurate translation of PDF documents（NOUGAT）": {
                "Group": "Academic",
                "Color": "stop",
                "AsButton": False,
                "Function": HotReload(BatchTranslatePDFDocuments)
            }
        })
    except:
        print('Load function plugin failed')

    try:
        from void_terminal.crazy_functions.DynamicFunctionGeneration import DynamicFunctionGeneration
        function_plugins.update({
            "Dynamic code interpreter（CodeInterpreter）": {
                "Group": "Intelligent agent",
                "Color": "stop",
                "AsButton": False,
                "Function": HotReload(DynamicFunctionGeneration)
            }
        })
    except:
        print('Load function plugin failed')

    # try:
    #     from crazy_functions.MultiAgent import MultiAgentTerminal
    #     function_plugins.update({
    #         "MultiAgentTerminal（Microsoft AutoGen）": {
    #             "Group": "Intelligent agent",
    #             "Color": "stop",
    #             "AsButton": True,
    #             "Function": HotReload(MultiAgentTerminal)
    #         }
    #     })
    # except:
    #     print('Load function plugin failed')

    # try:
    #     from crazy_functions.chatglm fine-tuning tool import fine-tuning dataset generation
    #     function_plugins.update({
    #         "黑盒模型学习: FineTuneDatasetGeneration (Upload dataset first)": {
    #             "Color": "stop",
    #             "AsButton": False,
    #             "AdvancedArgs": True,
    #             "ArgsReminder": "针对数据集Input（E.g. green hat * dark blue shirt * black sports pants）Give instructions，For example, you can copy the following command below: --llm_to_learn=azure-gpt-3.5 --prompt_prefix='根据下面的服装类型prompt，Imagine a wearer，Describe the appearance, environment, inner world, and past experiences of this person。Requirement：Within 100 words，Use the second person。' --system_prompt=''",
    #             "Function": HotReload(FineTuneDatasetGeneration)
    #         }
    #     })
    # except:
    #     print('Load function plugin failed')



    """
    Set default value:
    - Default Group = Conversation
    - Default AsButton = True
    - Default AdvancedArgs = False
    - Default Color = secondary
    """
    for name, function_meta in function_plugins.items():
        if "Group" not in function_meta:
            function_plugins[name]["Group"] = 'Conversation'
        if "AsButton" not in function_meta:
            function_plugins[name]["AsButton"] = True
        if "AdvancedArgs" not in function_meta:
            function_plugins[name]["AdvancedArgs"] = False
        if "Color" not in function_meta:
            function_plugins[name]["Color"] = 'secondary'

    return function_plugins
