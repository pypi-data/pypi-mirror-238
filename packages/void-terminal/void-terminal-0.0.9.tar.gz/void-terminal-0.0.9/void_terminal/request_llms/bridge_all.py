
"""
    There are mainly 2 functions in this file，It is a common interface for all LLMs，They will continue to call lower-level LLM models，Handling details such as multi-model parallelism

    Functions without multi-threading capability：Used in normal conversation，Fully interactive，Not multi-threaded
    1. predict(...)

    Functions with multi-threading capability：Called in function plugins，Flexible and concise
    2. predict_no_ui_long_connection(...)
"""
import tiktoken
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor
from void_terminal.toolbox import get_conf, trimmed_format_exc

from void_terminal.request_llms.bridge_chatgpt import predict_no_ui_long_connection as chatgpt_noui
from void_terminal.request_llms.bridge_chatgpt import predict as chatgpt_ui

from void_terminal.request_llms.bridge_chatglm import predict_no_ui_long_connection as chatglm_noui
from void_terminal.request_llms.bridge_chatglm import predict as chatglm_ui

from void_terminal.request_llms.bridge_chatglm3 import predict_no_ui_long_connection as chatglm3_noui
from void_terminal.request_llms.bridge_chatglm3 import predict as chatglm3_ui

from void_terminal.request_llms.bridge_qianfan import predict_no_ui_long_connection as qianfan_noui
from void_terminal.request_llms.bridge_qianfan import predict as qianfan_ui

colors = ['#FF00FF', '#00FFFF', '#FF0000', '#990099', '#009999', '#990044']

class LazyloadTiktoken(object):
    def __init__(self, model):
        self.model = model

    @staticmethod
    @lru_cache(maxsize=128)
    def get_encoder(model):
        print('Loading tokenizer，If it is the first time running，It may take some time to download parameters')
        tmp = tiktoken.encoding_for_model(model)
        print('Loading tokenizer completed')
        return tmp
    
    def encode(self, *args, **kwargs):
        encoder = self.get_encoder(self.model) 
        return encoder.encode(*args, **kwargs)
    
    def decode(self, *args, **kwargs):
        encoder = self.get_encoder(self.model) 
        return encoder.decode(*args, **kwargs)

# Endpoint redirection
API_URL_REDIRECT, AZURE_ENDPOINT, AZURE_ENGINE = get_conf("API_URL_REDIRECT", "AZURE_ENDPOINT", "AZURE_ENGINE")
openai_endpoint = "https://api.openai.com/v1/chat/completions"
api2d_endpoint = "https://openai.api2d.net/v1/chat/completions"
newbing_endpoint = "wss://sydney.bing.com/sydney/ChatHub"
if not AZURE_ENDPOINT.endswith('/'): AZURE_ENDPOINT += '/'
azure_endpoint = AZURE_ENDPOINT + f'openai/deployments/{AZURE_ENGINE}/chat/completions?api-version=2023-05-15'
# Compatible with old version configuration
try:
    API_URL = get_conf("API_URL")
    if API_URL != "https://api.openai.com/v1/chat/completions": 
        openai_endpoint = API_URL
        print("Warning! The API_URL configuration option will be deprecated，Please replace it with the API_URL_REDIRECT configuration")
except:
    pass
# New version configuration
if openai_endpoint in API_URL_REDIRECT: openai_endpoint = API_URL_REDIRECT[openai_endpoint]
if api2d_endpoint in API_URL_REDIRECT: api2d_endpoint = API_URL_REDIRECT[api2d_endpoint]
if newbing_endpoint in API_URL_REDIRECT: newbing_endpoint = API_URL_REDIRECT[newbing_endpoint]


# Get tokenizer
tokenizer_gpt35 = LazyloadTiktoken("gpt-3.5-turbo")
tokenizer_gpt4 = LazyloadTiktoken("gpt-4")
get_token_num_gpt35 = lambda txt: len(tokenizer_gpt35.encode(txt, disallowed_special=()))
get_token_num_gpt4 = lambda txt: len(tokenizer_gpt4.encode(txt, disallowed_special=()))


# Start initializing model
AVAIL_LLM_MODELS, LLM_MODEL = get_conf("AVAIL_LLM_MODELS", "LLM_MODEL")
AVAIL_LLM_MODELS = AVAIL_LLM_MODELS + [LLM_MODEL]
# -=-=-=-=-=-=- The following section is the earliest and most stable model added
model_info = {
    # openai
    "gpt-3.5-turbo": {
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": openai_endpoint,
        "max_token": 4096,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },
    
    "gpt-3.5-turbo-16k": {
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": openai_endpoint,
        "max_token": 1024*16,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },

    "gpt-3.5-turbo-0613": {
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": openai_endpoint,
        "max_token": 4096,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },

    "gpt-3.5-turbo-16k-0613": {
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": openai_endpoint,
        "max_token": 1024 * 16,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },

    "gpt-4": {
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": openai_endpoint,
        "max_token": 8192,
        "tokenizer": tokenizer_gpt4,
        "token_cnt": get_token_num_gpt4,
    },

    "gpt-4-32k": {
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": openai_endpoint,
        "max_token": 32768,
        "tokenizer": tokenizer_gpt4,
        "token_cnt": get_token_num_gpt4,
    },

    "gpt-3.5-random": {
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": openai_endpoint,
        "max_token": 4096,
        "tokenizer": tokenizer_gpt4,
        "token_cnt": get_token_num_gpt4,
    },
    
    # azure openai
    "azure-gpt-3.5":{
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": azure_endpoint,
        "max_token": 4096,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },

    "azure-gpt-4":{
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": azure_endpoint,
        "max_token": 8192,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },

    # api_2d
    "api2d-gpt-3.5-turbo": {
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": api2d_endpoint,
        "max_token": 4096,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },

    "api2d-gpt-4": {
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": api2d_endpoint,
        "max_token": 8192,
        "tokenizer": tokenizer_gpt4,
        "token_cnt": get_token_num_gpt4,
    },

    "api2d-gpt-3.5-turbo-16k": {
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": api2d_endpoint,
        "max_token": 1024*16,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },

    # Align chatglm directly to chatglm2
    "chatglm": {
        "fn_with_ui": chatglm_ui,
        "fn_without_ui": chatglm_noui,
        "endpoint": None,
        "max_token": 1024,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },
    "chatglm2": {
        "fn_with_ui": chatglm_ui,
        "fn_without_ui": chatglm_noui,
        "endpoint": None,
        "max_token": 1024,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },
    "chatglm3": {
        "fn_with_ui": chatglm3_ui,
        "fn_without_ui": chatglm3_noui,
        "endpoint": None,
        "max_token": 8192,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },
    "qianfan": {
        "fn_with_ui": qianfan_ui,
        "fn_without_ui": qianfan_noui,
        "endpoint": None,
        "max_token": 2000,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },
}

# -=-=-=-=-=-=- The following section is the newly added model，May come with additional dependencies -=-=-=-=-=-=-
if "claude-1-100k" in AVAIL_LLM_MODELS or "claude-2" in AVAIL_LLM_MODELS:
    from void_terminal.request_llms.bridge_claude import predict_no_ui_long_connection as claude_noui
    from void_terminal.request_llms.bridge_claude import predict as claude_ui
    model_info.update({
        "claude-1-100k": {
            "fn_with_ui": claude_ui,
            "fn_without_ui": claude_noui,
            "endpoint": None,
            "max_token": 8196,
            "tokenizer": tokenizer_gpt35,
            "token_cnt": get_token_num_gpt35,
        },
    })
    model_info.update({
        "claude-2": {
            "fn_with_ui": claude_ui,
            "fn_without_ui": claude_noui,
            "endpoint": None,
            "max_token": 8196,
            "tokenizer": tokenizer_gpt35,
            "token_cnt": get_token_num_gpt35,
        },
    })
if "jittorllms_rwkv" in AVAIL_LLM_MODELS:
    from void_terminal.request_llms.bridge_jittorllms_rwkv import predict_no_ui_long_connection as rwkv_noui
    from void_terminal.request_llms.bridge_jittorllms_rwkv import predict as rwkv_ui
    model_info.update({
        "jittorllms_rwkv": {
            "fn_with_ui": rwkv_ui,
            "fn_without_ui": rwkv_noui,
            "endpoint": None,
            "max_token": 1024,
            "tokenizer": tokenizer_gpt35,
            "token_cnt": get_token_num_gpt35,
        },
    })
if "jittorllms_llama" in AVAIL_LLM_MODELS:
    from void_terminal.request_llms.bridge_jittorllms_llama import predict_no_ui_long_connection as llama_noui
    from void_terminal.request_llms.bridge_jittorllms_llama import predict as llama_ui
    model_info.update({
        "jittorllms_llama": {
            "fn_with_ui": llama_ui,
            "fn_without_ui": llama_noui,
            "endpoint": None,
            "max_token": 1024,
            "tokenizer": tokenizer_gpt35,
            "token_cnt": get_token_num_gpt35,
        },
    })
if "jittorllms_pangualpha" in AVAIL_LLM_MODELS:
    from void_terminal.request_llms.bridge_jittorllms_pangualpha import predict_no_ui_long_connection as pangualpha_noui
    from void_terminal.request_llms.bridge_jittorllms_pangualpha import predict as pangualpha_ui
    model_info.update({
        "jittorllms_pangualpha": {
            "fn_with_ui": pangualpha_ui,
            "fn_without_ui": pangualpha_noui,
            "endpoint": None,
            "max_token": 1024,
            "tokenizer": tokenizer_gpt35,
            "token_cnt": get_token_num_gpt35,
        },
    })
if "moss" in AVAIL_LLM_MODELS:
    from void_terminal.request_llms.bridge_moss import predict_no_ui_long_connection as moss_noui
    from void_terminal.request_llms.bridge_moss import predict as moss_ui
    model_info.update({
        "moss": {
            "fn_with_ui": moss_ui,
            "fn_without_ui": moss_noui,
            "endpoint": None,
            "max_token": 1024,
            "tokenizer": tokenizer_gpt35,
            "token_cnt": get_token_num_gpt35,
        },
    })
if "stack-claude" in AVAIL_LLM_MODELS:
    from void_terminal.request_llms.bridge_stackclaude import predict_no_ui_long_connection as claude_noui
    from void_terminal.request_llms.bridge_stackclaude import predict as claude_ui
    model_info.update({
        "stack-claude": {
            "fn_with_ui": claude_ui,
            "fn_without_ui": claude_noui,
            "endpoint": None,
            "max_token": 8192,
            "tokenizer": tokenizer_gpt35,
            "token_cnt": get_token_num_gpt35,
        }
    })
if "newbing-free" in AVAIL_LLM_MODELS:
    try:
        from void_terminal.request_llms.bridge_newbingfree import predict_no_ui_long_connection as newbingfree_noui
        from void_terminal.request_llms.bridge_newbingfree import predict as newbingfree_ui
        model_info.update({
            "newbing-free": {
                "fn_with_ui": newbingfree_ui,
                "fn_without_ui": newbingfree_noui,
                "endpoint": newbing_endpoint,
                "max_token": 4096,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            }
        })
    except:
        print(trimmed_format_exc())
if "newbing" in AVAIL_LLM_MODELS:   # same with newbing-free
    try:
        from void_terminal.request_llms.bridge_newbingfree import predict_no_ui_long_connection as newbingfree_noui
        from void_terminal.request_llms.bridge_newbingfree import predict as newbingfree_ui
        model_info.update({
            "newbing": {
                "fn_with_ui": newbingfree_ui,
                "fn_without_ui": newbingfree_noui,
                "endpoint": newbing_endpoint,
                "max_token": 4096,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            }
        })
    except:
        print(trimmed_format_exc())
if "chatglmft" in AVAIL_LLM_MODELS:   # same with newbing-free
    try:
        from void_terminal.request_llms.bridge_chatglmft import predict_no_ui_long_connection as chatglmft_noui
        from void_terminal.request_llms.bridge_chatglmft import predict as chatglmft_ui
        model_info.update({
            "chatglmft": {
                "fn_with_ui": chatglmft_ui,
                "fn_without_ui": chatglmft_noui,
                "endpoint": None,
                "max_token": 4096,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            }
        })
    except:
        print(trimmed_format_exc())
if "internlm" in AVAIL_LLM_MODELS:
    try:
        from void_terminal.request_llms.bridge_internlm import predict_no_ui_long_connection as internlm_noui
        from void_terminal.request_llms.bridge_internlm import predict as internlm_ui
        model_info.update({
            "internlm": {
                "fn_with_ui": internlm_ui,
                "fn_without_ui": internlm_noui,
                "endpoint": None,
                "max_token": 4096,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            }
        })
    except:
        print(trimmed_format_exc())
if "chatglm_onnx" in AVAIL_LLM_MODELS:
    try:
        from void_terminal.request_llms.bridge_chatglmonnx import predict_no_ui_long_connection as chatglm_onnx_noui
        from void_terminal.request_llms.bridge_chatglmonnx import predict as chatglm_onnx_ui
        model_info.update({
            "chatglm_onnx": {
                "fn_with_ui": chatglm_onnx_ui,
                "fn_without_ui": chatglm_onnx_noui,
                "endpoint": None,
                "max_token": 4096,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            }
        })
    except:
        print(trimmed_format_exc())
if "qwen" in AVAIL_LLM_MODELS:
    try:
        from void_terminal.request_llms.bridge_qwen import predict_no_ui_long_connection as qwen_noui
        from void_terminal.request_llms.bridge_qwen import predict as qwen_ui
        model_info.update({
            "qwen": {
                "fn_with_ui": qwen_ui,
                "fn_without_ui": qwen_noui,
                "endpoint": None,
                "max_token": 4096,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            }
        })
    except:
        print(trimmed_format_exc())
if "chatgpt_website" in AVAIL_LLM_MODELS:   # Access some reverse engineering https://github.com/acheong08/ChatGPT-to-API/
    try:
        from void_terminal.request_llms.bridge_chatgpt_website import predict_no_ui_long_connection as chatgpt_website_noui
        from void_terminal.request_llms.bridge_chatgpt_website import predict as chatgpt_website_ui
        model_info.update({
            "chatgpt_website": {
                "fn_with_ui": chatgpt_website_ui,
                "fn_without_ui": chatgpt_website_noui,
                "endpoint": openai_endpoint,
                "max_token": 4096,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            }
        })
    except:
        print(trimmed_format_exc())
if "spark" in AVAIL_LLM_MODELS:   # Xunfei Xinghuo cognitive model
    try:
        from void_terminal.request_llms.bridge_spark import predict_no_ui_long_connection as spark_noui
        from void_terminal.request_llms.bridge_spark import predict as spark_ui
        model_info.update({
            "spark": {
                "fn_with_ui": spark_ui,
                "fn_without_ui": spark_noui,
                "endpoint": None,
                "max_token": 4096,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            }
        })
    except:
        print(trimmed_format_exc())
if "sparkv2" in AVAIL_LLM_MODELS:   # Xunfei Xinghuo cognitive model
    try:
        from void_terminal.request_llms.bridge_spark import predict_no_ui_long_connection as spark_noui
        from void_terminal.request_llms.bridge_spark import predict as spark_ui
        model_info.update({
            "sparkv2": {
                "fn_with_ui": spark_ui,
                "fn_without_ui": spark_noui,
                "endpoint": None,
                "max_token": 4096,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            }
        })
    except:
        print(trimmed_format_exc())
if "sparkv3" in AVAIL_LLM_MODELS:   # Xunfei Xinghuo cognitive model
    try:
        from void_terminal.request_llms.bridge_spark import predict_no_ui_long_connection as spark_noui
        from void_terminal.request_llms.bridge_spark import predict as spark_ui
        model_info.update({
            "sparkv3": {
                "fn_with_ui": spark_ui,
                "fn_without_ui": spark_noui,
                "endpoint": None,
                "max_token": 4096,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            }
        })
    except:
        print(trimmed_format_exc())
if "llama2" in AVAIL_LLM_MODELS:   # llama2
    try:
        from void_terminal.request_llms.bridge_llama2 import predict_no_ui_long_connection as llama2_noui
        from void_terminal.request_llms.bridge_llama2 import predict as llama2_ui
        model_info.update({
            "llama2": {
                "fn_with_ui": llama2_ui,
                "fn_without_ui": llama2_noui,
                "endpoint": None,
                "max_token": 4096,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            }
        })
    except:
        print(trimmed_format_exc())
if "zhipuai" in AVAIL_LLM_MODELS:   # zhipuai
    try:
        from void_terminal.request_llms.bridge_zhipu import predict_no_ui_long_connection as zhipu_noui
        from void_terminal.request_llms.bridge_zhipu import predict as zhipu_ui
        model_info.update({
            "zhipuai": {
                "fn_with_ui": zhipu_ui,
                "fn_without_ui": zhipu_noui,
                "endpoint": None,
                "max_token": 4096,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            }
        })
    except:
        print(trimmed_format_exc())

# <-- 用于定义and切换多itemsazure模型 -->
AZURE_CFG_ARRAY = get_conf("AZURE_CFG_ARRAY")
if len(AZURE_CFG_ARRAY) > 0:
    for azure_model_name, azure_cfg_dict in AZURE_CFG_ARRAY.items():
        # 可能会覆盖之前Configuration，但这是意料之中的
        if not azure_model_name.startswith('azure'): 
            raise ValueError("AZURE_CFG_ARRAY中配置的模型必须以azure开头")
        endpoint_ = azure_cfg_dict["AZURE_ENDPOINT"] + \
            f'openai/deployments/{azure_cfg_dict["AZURE_ENGINE"]}/chat/completions?api-version=2023-05-15'
        model_info.update({
            azure_model_name: {
                "fn_with_ui": chatgpt_ui,
                "fn_without_ui": chatgpt_noui,
                "endpoint": endpoint_,
                "azure_api_key": azure_cfg_dict["AZURE_API_KEY"],
                "max_token": azure_cfg_dict["AZURE_MODEL_MAX_TOKEN"],
                "tokenizer": tokenizer_gpt35,   # tokenizer只用于粗估token数量
                "token_cnt": get_token_num_gpt35,
            }
        })
        if azure_model_name not in AVAIL_LLM_MODELS:
            AVAIL_LLM_MODELS += [azure_model_name]




def LLM_CATCH_EXCEPTION(f):
    """
    Decorator function，Display errors
    """
    def decorated(inputs, llm_kwargs, history, sys_prompt, observe_window, console_slience):
        try:
            return f(inputs, llm_kwargs, history, sys_prompt, observe_window, console_slience)
        except Exception as e:
            tb_str = '\n```\n' + trimmed_format_exc() + '\n```\n'
            observe_window[0] = tb_str
            return tb_str
    return decorated


def predict_no_ui_long_connection(inputs, llm_kwargs, history, sys_prompt, observe_window, console_slience=False):
    """
    Send to LLM，Waiting for reply，Completed in one go，Do not display intermediate processes。But internally use the stream method to avoid the network being cut off midway。
    inputs：
        This is the input of this inquiry
    sys_prompt:
        System silent prompt
    llm_kwargs：
        LLM`s internal tuning parameters
    history：
        history is the list of previous conversations
    observe_window = None：
        Used to transfer the already output part across threads，Most of the time it`s just for fancy visual effects，Leave it blank。observe_window[0]：Observation window。observe_window[1]：Watchdog
    """
    import threading, time, copy

    model = llm_kwargs['llm_model']
    n_model = 1
    if '&' not in model:
        assert not model.startswith("tgui"), "TGUI does not support the implementation of function plugins"

        # If only one large language model is queried：
        method = model_info[model]["fn_without_ui"]
        return method(inputs, llm_kwargs, history, sys_prompt, observe_window, console_slience)
    else:

        # If InquiryMultipleLargeLanguageModels is queried at the same time，This is a bit verbose，But the idea is the same，You don`t have to read this else branch
        executor = ThreadPoolExecutor(max_workers=4)
        models = model.split('&')
        n_model = len(models)
        
        window_len = len(observe_window)
        assert window_len==3
        window_mutex = [["", time.time(), ""] for _ in range(n_model)] + [True]

        futures = []
        for i in range(n_model):
            model = models[i]
            method = model_info[model]["fn_without_ui"]
            llm_kwargs_feedin = copy.deepcopy(llm_kwargs)
            llm_kwargs_feedin['llm_model'] = model
            future = executor.submit(LLM_CATCH_EXCEPTION(method), inputs, llm_kwargs_feedin, history, sys_prompt, window_mutex[i], console_slience)
            futures.append(future)

        def mutex_manager(window_mutex, observe_window):
            while True:
                time.sleep(0.25)
                if not window_mutex[-1]: break
                # Watchdog（watchdog）
                for i in range(n_model): 
                    window_mutex[i][1] = observe_window[1]
                # Observation window（window）
                chat_string = []
                for i in range(n_model):
                    chat_string.append( f"【{str(models[i])} Say】: <font color=\"{colors[i]}\"> {window_mutex[i][0]} </font>" )
                res = '<br/><br/>\n\n---\n\n'.join(chat_string)
                # # # # # # # # # # #
                observe_window[0] = res

        t_model = threading.Thread(target=mutex_manager, args=(window_mutex, observe_window), daemon=True)
        t_model.start()

        return_string_collect = []
        while True:
            worker_done = [h.done() for h in futures]
            if all(worker_done):
                executor.shutdown()
                break
            time.sleep(1)

        for i, future in enumerate(futures):  # wait and get
            return_string_collect.append( f"【{str(models[i])} Say】: <font color=\"{colors[i]}\"> {future.result()} </font>" )

        window_mutex[-1] = False # stop mutex thread
        res = '<br/><br/>\n\n---\n\n'.join(return_string_collect)
        return res


def predict(inputs, llm_kwargs, *args, **kwargs):
    """
    Send to LLM，Get output in a streaming way。
    Used for basic conversation functions。
    inputs are the inputs for this inquiry
    top_p, Temperature is an internal tuning parameter of LLM
    history is the list of previous conversations（Note that both inputs and history，An error of token overflow will be triggered if the content is too long）
    chatbot is the conversation list displayed in WebUI，Modify it，Then yield it out，You can directly modify the conversation interface content
    additional_fn represents which button is clicked，See functional.py for buttons
    """

    method = model_info[llm_kwargs['llm_model']]["fn_with_ui"]  # If there is an error here，Check the AVAIL_LLM_MODELS option in config
    yield from method(inputs, llm_kwargs, *args, **kwargs)

