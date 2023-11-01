from void_terminal.toolbox import CatchException, update_ui, gen_time_str, trimmed_format_exc, ProxyNetworkActivate
from void_terminal.toolbox import report_execption, get_log_folder, update_ui_lastest_msg, Singleton
from void_terminal.crazy_functions.agent_fns.pipe import PluginMultiprocessManager, PipeCom
import time


class AutoGenGeneral(PluginMultiprocessManager):

    def gpt_academic_print_override(self, user_proxy, message, sender):
        # ⭐⭐ Subprocess execution
        self.child_conn.send(PipeCom("show", sender.name + '\n\n---\n\n' + message['content']))

    def gpt_academic_get_human_input(self, user_proxy, message):
        # ⭐⭐ Subprocess execution
        patience = 300
        begin_waiting_time = time.time()
        self.child_conn.send(PipeCom("interact", message))
        while True:
            time.sleep(0.5)
            if self.child_conn.poll(): 
                wait_success = True
                break
            if time.time() - begin_waiting_time > patience:
                self.child_conn.send(PipeCom("done", ""))
                wait_success = False
                break
        if wait_success:
            return self.child_conn.recv().content
        else:
            raise TimeoutError("Wait for user input timeout")

    def define_agents(self):
        raise NotImplementedError

    def do_audogen(self, input):
        # ⭐⭐ Subprocess execution
        input = input.content
        with ProxyNetworkActivate("AutoGen"):
            config_list = self.get_config_list()
            code_execution_config={"work_dir": self.autogen_work_dir, "use_docker":self.use_docker}
            agents = self.define_agents()
            user_proxy = None
            assistant = None
            for agent_kwargs in agents:
                agent_cls = agent_kwargs.pop('cls')
                kwargs = {
                    'llm_config':{
                        "config_list": config_list,
                    },
                    'code_execution_config':code_execution_config
                }
                kwargs.update(agent_kwargs)
                agent_handle = agent_cls(**kwargs)
                agent_handle._print_received_message = lambda a,b: self.gpt_academic_print_override(agent_kwargs, a, b)
                if agent_kwargs['name'] == 'user_proxy':
                    agent_handle.get_human_input = lambda a: self.gpt_academic_get_human_input(user_proxy, a)
                    user_proxy = agent_handle
                if agent_kwargs['name'] == 'assistant': assistant = agent_handle
            try:
                if user_proxy is None or assistant is None: raise Exception("User agent or assistant agent is not defined")
                user_proxy.initiate_chat(assistant, message=input)
            except Exception as e:
                tb_str = '```\n' + trimmed_format_exc() + '```'
                self.child_conn.send(PipeCom("done", "AutoGen execution failed: \n\n" + tb_str))

    def get_config_list(self):
        model = self.llm_kwargs['llm_model']
        api_base = None
        if self.llm_kwargs['llm_model'].startswith('api2d-'):
            model = self.llm_kwargs['llm_model'][len('api2d-'):]
            api_base = "https://openai.api2d.net/v1"
        config_list = [{
                'model': model, 
                'api_key': self.llm_kwargs['api_key'],
            },]
        if api_base is not None:
            config_list[0]['api_base'] = api_base
        return config_list

    def subprocess_worker(self, child_conn):
        # ⭐⭐ Subprocess execution
        self.child_conn = child_conn
        while True:
            msg = self.child_conn.recv() # PipeCom
            self.do_audogen(msg)
