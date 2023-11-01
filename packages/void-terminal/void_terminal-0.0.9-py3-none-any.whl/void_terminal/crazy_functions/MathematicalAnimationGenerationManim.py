from void_terminal.toolbox import CatchException, update_ui, gen_time_str
from void_terminal.crazy_functions.crazy_utils import request_gpt_model_in_new_thread_with_ui_alive
from void_terminal.crazy_functions.crazy_utils import input_clipping

def inspect_dependency(chatbot, history):
    # Attempt to import dependencies，If dependencies are missing，Give installation suggestions
    try:
        import manim
        return True
    except:
        chatbot.append(["Failed to import dependencies", "Using this module requires additional dependencies，Installation method:```pip install manim manimgl```"])
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return False

def eval_manim(code):
    import subprocess, sys, os, shutil

    with open('gpt_log/MyAnimation.py', 'w', encoding='utf8') as f:
        f.write(code)

    def get_class_name(class_string):
        import re
        # Use regex to extract the class name
        class_name = re.search(r'class (\w+)\(', class_string).group(1)
        return class_name

    class_name = get_class_name(code)

    try: 
        subprocess.check_output([sys.executable, '-c', f"from gpt_log.MyAnimation import {class_name}; {class_name}().render()"])
        shutil.move('media/videos/1080p60/{class_name}.mp4', f'gpt_log/{class_name}-{gen_time_str()}.mp4')
        return f'gpt_log/{gen_time_str()}.mp4'
    except subprocess.CalledProcessError as e:
        output = e.output.decode()
        print(f"Command returned non-zero exit status {e.returncode}: {output}.")
        return f"Evaluating python script failed: {e.output}."
    except: 
        print('generating mp4 failed')
        return "Generating mp4 failed."


def get_code_block(reply):
    import re
    pattern = r"```([\s\S]*?)```" # regex pattern to match code blocks
    matches = re.findall(pattern, reply) # find all code blocks in text
    if len(matches) != 1: 
        raise RuntimeError("GPT is not generating proper code.")
    return matches[0].strip('python') #  code block

@CatchException
def AnimationGeneration(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    """
    txt             Text entered by the user in the input field，For example, a paragraph that needs to be translated，For example, a file path that contains files to be processed
    llm_kwargs      GPT model parameters，Such as temperature and top_p，Generally pass it on as is
    plugin_kwargs   Plugin model parameters，No use for the time being
    chatbot         Chat display box handle，Displayed to the user
    history         Chat history，Context summary
    system_prompt   Silent reminder to GPT
    web_port        Current software running port number
    """
    # Clear history，To avoid input overflow
    history = []    

    # Basic information：Function, contributor
    chatbot.append([
        "Function plugin feature？",
        "Generate mathematical animations, This plugin is in the development stage, It is recommended not to use it temporarily, Author: binary-husky, Plugin initializing ..."
    ])
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page

    # Attempt to import dependencies, If dependencies are missing, Give installation suggestions
    dep_ok = yield from inspect_dependency(chatbot=chatbot, history=history) # Refresh the page
    if not dep_ok: return
    
    # Input
    i_say = f'Generate a animation to show: ' + txt
    demo = ["Here is some examples of manim", examples_of_manim()]
    _, demo = input_clipping(inputs="", history=demo, max_token_limit=2560)
    # Start
    gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
        inputs=i_say, inputs_show_user=i_say, 
        llm_kwargs=llm_kwargs, chatbot=chatbot, history=demo, 
        sys_prompt=
        r"Write a animation script with 3blue1brown's manim. "+
        r"Please begin with `from manim import *`. " + 
        r"Answer me with a code block wrapped by ```."
    )
    chatbot.append(["Start generating animation", "..."])
    history.extend([i_say, gpt_say])
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page # UI update
    
    # Convert code to animation
    code = get_code_block(gpt_say)
    res = eval_manim(code)

    chatbot.append(("Generated video file path", res))
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page # UI update

# Put some demos collected online here，Assist GPT in generating code
def examples_of_manim():
    return r"""


```

class MovingGroupToDestination(Scene):
    def construct(self):
        group = VGroup(Dot(LEFT), Dot(ORIGIN), Dot(RIGHT, color=RED), Dot(2 * RIGHT)).scale(1.4)
        dest = Dot([4, 3, 0], color=YELLOW)
        self.add(group, dest)
        self.play(group.animate.shift(dest.get_center() - group[2].get_center()))
        self.wait(0.5)

```


```

class LatexWithMovingFramebox(Scene):
    def construct(self):
        text=MathTex(
            "\\frac{d}{dx}f(x)g(x)=","f(x)\\frac{d}{dx}g(x)","+",
            "g(x)\\frac{d}{dx}f(x)"
        )
        self.play(Write(text))
        framebox1 = SurroundingRectangle(text[1], buff = .1)
        framebox2 = SurroundingRectangle(text[3], buff = .1)
        self.play(
            Create(framebox1),
        )
        self.wait()
        self.play(
            ReplacementTransform(framebox1,framebox2),
        )
        self.wait()

```



```

class PointWithTrace(Scene):
    def construct(self):
        path = VMobject()
        dot = Dot()
        path.set_points_as_corners([dot.get_center(), dot.get_center()])
        def update_path(path):
            previous_path = path.copy()
            previous_path.add_points_as_corners([dot.get_center()])
            path.become(previous_path)
        path.add_updater(update_path)
        self.add(path, dot)
        self.play(Rotating(dot, radians=PI, about_point=RIGHT, run_time=2))
        self.wait()
        self.play(dot.animate.shift(UP))
        self.play(dot.animate.shift(LEFT))
        self.wait()

```

```

# do not use get_graph, this funciton is deprecated

class ExampleFunctionGraph(Scene):
    def construct(self):
        cos_func = FunctionGraph(
            lambda t: np.cos(t) + 0.5 * np.cos(7 * t) + (1 / 7) * np.cos(14 * t),
            color=RED,
        )

        sin_func_1 = FunctionGraph(
            lambda t: np.sin(t) + 0.5 * np.sin(7 * t) + (1 / 7) * np.sin(14 * t),
            color=BLUE,
        )

        sin_func_2 = FunctionGraph(
            lambda t: np.sin(t) + 0.5 * np.sin(7 * t) + (1 / 7) * np.sin(14 * t),
            x_range=[-4, 4],
            color=GREEN,
        ).move_to([0, 1, 0])

        self.add(cos_func, sin_func_1, sin_func_2)

```
"""