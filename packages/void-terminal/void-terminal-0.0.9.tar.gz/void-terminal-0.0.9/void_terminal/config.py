"""
    All the following configurations can also be overridden using environment variables，See docker-compose.yml for the format of environment variable configuration。
    Read priority：Environment variable > config_private.py > config.py
    --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
    All the following configurations also support using environment variables to override, 
    and the environment variable configuration format can be seen in docker-compose.yml. 
    Configuration reading priority: environment variable > config_private.py > config.py
"""

# [step 1]>> API_KEY = "sk-123456789xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx123456789"。In very few cases，You also need to fill in the organization（In the format of org-123456789abcdefghijklmno），Please scroll down，Find API_ORG setting item
API_KEY = "Fill in the API key here"    # Multiple API-KEYs can be filled in at the same time，Separated by commas，For exampleAPI_KEY = "sk-openaikey1,sk-openaikey2,fkxxxx-api2dkey3,azure-apikey4"


# [step 2]>> Change to True to apply proxy，If deployed directly on overseas servers，Do not modify here; if using local or region-unrestricted large models，No modification is needed here
USE_PROXY = False
if USE_PROXY:
    """
    Format for filling in is [Protocol]://  [Address] :[Port]，Don`t forget to change USE_PROXY to True before filling in，If deployed directly on overseas servers，Do not modify here
            <Configuration tutorial & video tutorial> https://github.com/binary-husky/gpt_academic/issues/1>
    [Protocol] Common protocols are nothing but socks5h/http; For example, the default local protocol for v2**y and ss* is socks5h; While the default local protocol for cl**h is http
    [Address] Those who understand, understand，If you don`t understand, just fill in localhost or 127.0.0.1 and you won`t go wrong（localhost means that the proxy software is installed on the local machine）
    [Port] Look for it in the settings of the proxy software。Although the interface of different proxy software is different，But the port number should be in the most prominent position
    """
    # Address of the proxy network，Open your *learning* software to view the proxy protocol(socks5h / http)and address(localhost)and port(11284)
    proxies = {
        #          [Protocol]://  [Address]  :[Port]
        "http":  "socks5h://localhost:11284",  # 再For example  "http":  "http://127.0.0.1:7890",
        "https": "socks5h://localhost:11284",  # 再For example  "https": "http://127.0.0.1:7890",
    }
else:
    proxies = None

# ------------------------------------ The following configurations can optimize the experience, However, it does not need to be modified in most cases ------------------------------------

# Redirect URL，Realize the function of changing API_URL（High-risk setting! Do not modify under normal circumstances! Modify this setting，You will completely expose your API-KEY and conversation privacy to the middleman you set!）
# Format: API_URL_REDIRECT = {"https://api.openai.com/v1/chat/completions": "在这里填写重定To的api.openai.com的URL"} 
# For example: API_URL_REDIRECT = {"https://api.openai.com/v1/chat/completions": "https://reverse-proxy-url/v1/chat/completions"}
API_URL_REDIRECT = {}


# In the multi-threaded function plugin，How many threads are allowed to access OpenAI at the same time by default。The limit for free trial users is 3 times per minute，The limit for Pay-as-you-go users is 3500 times per minute
# In short：Free（5 dollars）User fills in 3，Users who have bound their credit card to OpenAI can fill in 16 or higher。Please check for higher limits：https://platform.openai.com/docs/guides/rate-limits/overview
DEFAULT_WORKER_NUM = 3


# Color theme, Optional ["Default", "Chuanhu-Small-and-Beautiful", "High-Contrast"]
# More themes, Please refer to the Gradio theme store: https://huggingface.co/spaces/gradio/theme-gallery optional ["Gstaff/Xkcd", "NoCrypt/Miku", ...]
THEME = "Default"
AVAIL_THEMES = ["Default", "Chuanhu-Small-and-Beautiful", "High-Contrast", "Gstaff/Xkcd", "NoCrypt/Miku"]


# Default的系统prompt词（system prompt）
INIT_SYS_PROMPT = "Serve me as a writing and programming assistant."


# Height of the Dialogue Window （仅在LAYOUT="TOP-DOWN"When生效）
CHATBOT_HEIGHT = 1115


# Code Highlighting
CODE_HIGHLIGHT = True


# Window Layout
LAYOUT = "LEFT-RIGHT"   # "LEFT-RIGHT"（Horizontal Layout） # "TOP-DOWN"（Vertical Layout）


# Dark mode / Light mode
DARK_MODE = True        


# After sending the request to OpenAI，Timeout Threshold
TIMEOUT_SECONDS = 30


# Web Port, -1 represents random port
WEB_PORT = -1


# If OpenAI does not respond（Network Lag, Proxy Failure, KEY Invalid），Retry Limit
MAX_RETRY = 2


# Default options for plugin classification
DEFAULT_FN_GROUPS = ['Conversation', 'programming', 'Academic', 'Intelligent agent']


# Model selection is (Attention: LLM_MODEL is the default selected model, It *must* be included in the AVAIL_LLM_MODELS list )
LLM_MODEL = "gpt-3.5-turbo" # Optional ↓↓↓
AVAIL_LLM_MODELS = ["gpt-3.5-turbo-16k", "gpt-3.5-turbo", "azure-gpt-3.5",
                    "api2d-gpt-3.5-turbo", 'api2d-gpt-3.5-turbo-16k', 
                    "gpt-4", "gpt-4-32k", "azure-gpt-4", "api2d-gpt-4", 
                    "chatglm", "moss", "newbing", "claude-2"]
# P.S. Other available models include ["zhipuai", "qianfan", "llama2", "qwen", "gpt-3.5-turbo-0613", "gpt-3.5-turbo-16k-0613",  "gpt-3.5-random"
# "spark", "sparkv2", "sparkv3", "chatglm_onnx", "claude-1-100k", "claude-2", "internlm", "jittorllms_pangualpha", "jittorllms_llama"]


# Baidu Qianfan（LLM_MODEL="qianfan"）
BAIDU_CLOUD_API_KEY = ''
BAIDU_CLOUD_SECRET_KEY = ''
BAIDU_CLOUD_QIANFAN_MODEL = 'ERNIE-Bot'    # Optional "ERNIE-Bot"(Original text), "ERNIE-Bot-turbo", "BLOOMZ-7B", "Llama-2-70B-Chat", "Llama-2-13B-Chat", "Llama-2-7B-Chat"


# If using ChatGLM2 fine-tuning model，请把 LLM_MODEL="chatglmft"，And specify the model path here
CHATGLM_PTUNING_CHECKPOINT = "" # For example"/home/hmp/ChatGLM2-6B/ptuning/output/6b-pt-128-1e-2/checkpoint-100"


# Execution mode of local LLM models such as ChatGLM CPU/GPU
LOCAL_MODEL_DEVICE = "cpu" # Optional "cuda"
LOCAL_MODEL_QUANT = "FP16" # Default "FP16" "INT4" 启用量化INT4version本 "INT8" 启用量化INT8version本


# Set the number of parallel threads for Gradio（No modification is needed）
CONCURRENT_COUNT = 100


# Whether to automatically clear the input box upon submission
AUTO_CLEAR_TXT = False


# Add a Live2D decoration
ADD_WAIFU = False


# Set username and password（No modification is needed）（Related functions are unstable，Related to gradio version and network，Not recommended to add this for local use）
# [("username", "password"), ("username2", "password2"), ...]
AUTHENTICATION = []


# If you need to run under the second-level path（Under normal circumstances，Do not modify!!）（Need to be modified in conjunction with main.py to take effect!）
CUSTOM_PATH = "/"


# HTTPS Key and Certificate（No modification is needed）
SSL_KEYFILE = ""
SSL_CERTFILE = ""


# In very few cases，Openai`s official KEY needs to be accompanied by organizational code（Format like org-xxxxxxxxxxxxxxxxxxxxxxxx）Use
API_ORG = ""


# If you need to use Slack Claude，See request_llms/README.md for detailed usage instructions
SLACK_CLAUDE_BOT_ID = ''   
SLACK_CLAUDE_USER_TOKEN = ''


# 如果需要UseAZURE（Method一：单itemsazure模型部署）详情请见额外文档 docs\use_azure.md
AZURE_ENDPOINT = "https://你亲手写的api名称.openai.azure.com/"
AZURE_API_KEY = "Fill in the Azure OpenAI API key"    # It is recommended to fill in directly at API_KEY.，This option will be deprecated soon
AZURE_ENGINE = "Fill in the deployment name you wrote by yourself"            # Read docs\use_azure.md


# 如果需要UseAZURE（Method二：多itemsazure模型部署+动态切换）详情请见额外文档 docs\use_azure.md
AZURE_CFG_ARRAY = {}


# Using Newbing (Not recommended for use，Will be deleted in the future)
NEWBING_STYLE = "creative"  # ["creative", "balanced", "precise"]
NEWBING_COOKIES = """
put your new bing cookies here
"""


# Aliyun real-time speech recognition has high configuration difficulty and is only recommended for advanced users. Refer to https://github.com/binary-husky/gpt_academic/blob/master/docs/use_audio.md
ENABLE_AUDIO = False
ALIYUN_TOKEN=""     # For example, f37f30e0f9934c34a992f6f64f7eba4f
ALIYUN_APPKEY=""    # For example, RoPlZrM88DnAFkZK
ALIYUN_ACCESSKEY="" # （No need to fill in）
ALIYUN_SECRET=""    # （No need to fill in）


# Access to Xunfei Xinghuo large model https://console.xfyun.cn/services/iat
XFYUN_APPID = "00000000"
XFYUN_API_SECRET = "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
XFYUN_API_KEY = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"


# 接入智谱大模型
ZHIPUAI_API_KEY = ""
ZHIPUAI_MODEL = "chatglm_turbo"


# Claude API KEY
ANTHROPIC_API_KEY = ""


# Customize API KEY format
CUSTOM_API_KEY_PATTERN = ""


# HUGGINGFACE`s TOKEN，Works when downloading LLAMA https://huggingface.co/docs/hub/security-tokens
HUGGINGFACE_ACCESS_TOKEN = "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"


# GROBID server address（Filling in multiple can balance the load），Used for high-quality reading of PDF documents
# Get method：Copy the following space https://huggingface.co/spaces/qingxu98/grobid，Set as public，然后GROBID_URL = "https://(Your hf username is qingxu98)-(Your filled space name such as grobid).hf.space"
GROBID_URLS = [
    "https://qingxu98-grobid.hf.space","https://qingxu98-grobid2.hf.space","https://qingxu98-grobid3.hf.space",
    "https://qingxu98-grobid4.hf.space","https://qingxu98-grobid5.hf.space", "https://qingxu98-grobid6.hf.space", 
    "https://qingxu98-grobid7.hf.space", "https://qingxu98-grobid8.hf.space", 
]


# Allow modifying the configuration of this page through natural language description，This feature has a certain level of danger，Default closed
ALLOW_RESET_CONFIG = False


# 在UseAutoGenPluginWhen，是否UseDocker容器运line代码
AUTOGEN_USE_DOCKER = True


# Temporary upload folder location，Please do not modify
PATH_PRIVATE_UPLOAD = "private_upload"


# Location of the log folder，Please do not modify
PATH_LOGGING = "gpt_log"


# In addition to connecting OpenAI，What other occasions allow the use of proxies，Please do not modify
WHEN_TO_USE_PROXY = ["Download_LLM", "Download_Gradio_Theme", "Connect_Grobid", 
                     "Warmup_Modules", "Nougat_Download", "AutoGen"]


# *实验性功能*: 自动检测并屏蔽失效的KEY，请勿Use
BLOCK_INVALID_APIKEY = False


# Maximum number limit for custom buttons
NUM_CUSTOM_BASIC_BTN = 4

"""
Online large model configuration relationship diagram
│
├── "gpt-3.5-turbo" 等openai模型
│   ├── API_KEY
│   ├── CUSTOM_API_KEY_PATTERN（Not commonly used）
│   ├── API_ORG（Not commonly used）
│   └── API_URL_REDIRECT（Not commonly used）
│
├── "azure-gpt-3.5" 等azure模型（单itemsazure模型，不需要动态切换）
│   ├── API_KEY
│   ├── AZURE_ENDPOINT
│   ├── AZURE_API_KEY
│   ├── AZURE_ENGINE
│   └── API_URL_REDIRECT
│
├── "azure-gpt-3.5" 等azure模型（多itemsazure模型，需要动态切换，高preferred级）
│   └── AZURE_CFG_ARRAY
│
├── "spark" Spark Cognitive Big Model spark & sparkv2
│   ├── XFYUN_APPID
│   ├── XFYUN_API_SECRET
│   └── XFYUN_API_KEY
│
├── "claude-1-100k" 等claude模型
│   └── ANTHROPIC_API_KEY
│
├── "stack-claude"
│   ├── SLACK_CLAUDE_BOT_ID
│   └── SLACK_CLAUDE_USER_TOKEN
│
├── "qianfan" Baidu Qianfan大模型库
│   ├── BAIDU_CLOUD_QIANFAN_MODEL
│   ├── BAIDU_CLOUD_API_KEY
│   └── BAIDU_CLOUD_SECRET_KEY
│
├── "newbing" Newbing接口不再稳定，Not recommended for use
    ├── NEWBING_STYLE
    └── NEWBING_COOKIES

    
Diagram of user interface layout dependencies
│
├── CHATBOT_HEIGHT Height of the chat window
├── CODE_HIGHLIGHT Code highlighting
├── LAYOUT window layout
├── DARK_MODE Dark mode / Light mode
├── DEFAULT_FN_GROUPS Plugin classification default options
├── THEME color theme
├── AUTO_CLEAR_TXT Whether to automatically clear the input box when submitting
├── ADD_WAIFU Add a live2d decoration
├── ALLOW_RESET_CONFIG Whether to allow modifying the configuration of this page through natural language description，This feature has a certain level of danger


Plugin online service configuration dependency diagram
│
├── Voice function
│   ├── ENABLE_AUDIO
│   ├── ALIYUN_TOKEN
│   ├── ALIYUN_APPKEY
│   ├── ALIYUN_ACCESSKEY
│   └── ALIYUN_SECRET
│
├── Accurate parsing of PDF documents
│   └── GROBID_URLS

"""
