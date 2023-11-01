sample = """
[1]: https://baike.baidu.com/item/%E8%B4%A8%E8%83%BD%E6%96%B9%E7%A8%8B/1884527 "质能方程（Mass-energy equivalence equation）_百度百科"
[2]: https://www.zhihu.com/question/348249281 "如何理解质能方程 E＝mc²？ - Zhihu"
[3]: https://zhuanlan.zhihu.com/p/32597385 "质能方程的推导与理解 - Zhihu - Zhihu专栏"

Hello，This is Bing。The mass-energy equivalence equation describes the equivalent relationship between mass and energy[^1^][1]。In tex format，The mass-energy equivalence equation can be written as $$E=mc^2$$，Where $E$ is energy，$m$ is mass，$c$ is the speed of light[^2^][2] [^3^][3]。
"""
import re

def preprocess_newbing_out(s):
    pattern = r'\^(\d+)\^' # Match ^number^
    pattern2 = r'\[(\d+)\]' # Match ^number^
    sub = lambda m: '\['+m.group(1)+'\]' # Replace the matched number as the replacement value
    result = re.sub(pattern, sub, s) # Replacement operation
    if '[1]' in result:
        result += '<br/><hr style="border-top: dotted 1px #44ac5c;"><br/><small>' + "<br/>".join([re.sub(pattern2, sub, r) for r in result.split('\n') if r.startswith('[')]) + '</small>'
    return result


def close_up_code_segment_during_stream(gpt_reply):
    """
    In the middle of outputting code with GPT（Output the front part```，But haven`t output the back part yet```），Complete the back part```

    Args:
        gpt_reply (str): Reply string returned by GPT model。

    Returns:
        str: Return a new string，Append the back part of output code snippet```to it。

    """
    if '```' not in gpt_reply:
        return gpt_reply
    if gpt_reply.endswith('```'):
        return gpt_reply

    # Exclude the above two cases，We
    segments = gpt_reply.split('```')
    n_mark = len(segments) - 1
    if n_mark % 2 == 1:
        # print('Output代码Segment中！')
        return gpt_reply+'\n```'
    else:
        return gpt_reply
    
import markdown
from latex2mathml.converter import convert as tex2mathml
from functools import wraps, lru_cache
def markdown_convertion(txt):
    """
    Convert Markdown format text to HTML format。If it contains mathematical formulas，Convert the formula to HTML format first。
    """
    pre = '<div class="markdown-body">'
    suf = '</div>'
    if txt.startswith(pre) and txt.endswith(suf):
        # print('Warning，Input a string that has already been converted，二次转化可能出Question')
        return txt # Has already been converted，No need to convert again
    
    markdown_extension_configs = {
        'mdx_math': {
            'enable_dollar_delimiter': True,
            'use_gitlab_delimiters': False,
        },
    }
    find_equation_pattern = r'<script type="math/tex(?:.*?)>(.*?)</script>'

    def tex2mathml_catch_exception(content, *args, **kwargs):
        try:
            content = tex2mathml(content, *args, **kwargs)
        except:
            content = content
        return content

    def replace_math_no_render(match):
        content = match.group(1)
        if 'mode=display' in match.group(0):
            content = content.replace('\n', '</br>')
            return f"<font color=\"#00FF00\">$$</font><font color=\"#FF00FF\">{content}</font><font color=\"#00FF00\">$$</font>"
        else:
            return f"<font color=\"#00FF00\">$</font><font color=\"#FF00FF\">{content}</font><font color=\"#00FF00\">$</font>"

    def replace_math_render(match):
        content = match.group(1)
        if 'mode=display' in match.group(0):
            if '\\begin{aligned}' in content:
                content = content.replace('\\begin{aligned}', '\\begin{array}')
                content = content.replace('\\end{aligned}', '\\end{array}')
                content = content.replace('&', ' ')
            content = tex2mathml_catch_exception(content, display="block")
            return content
        else:
            return tex2mathml_catch_exception(content)

    def markdown_bug_hunt(content):
        """
        Fix a bug in mdx_math（Redundant when wrapping begin command with single $<script>）
        """
        content = content.replace('<script type="math/tex">\n<script type="math/tex; mode=display">', '<script type="math/tex; mode=display">')
        content = content.replace('</script>\n</script>', '</script>')
        return content


    if ('$' in txt) and ('```' not in txt):  # Formula symbol with $ sign，And there is no code section```Identifier of
        # convert everything to html format
        split = markdown.markdown(text='---')
        convert_stage_1 = markdown.markdown(text=txt, extensions=['mdx_math', 'fenced_code', 'tables', 'sane_lists'], extension_configs=markdown_extension_configs)
        convert_stage_1 = markdown_bug_hunt(convert_stage_1)
        # re.DOTALL: Make the '.' special character match any character at all, including a newline; without this flag, '.' will match anything except a newline. Corresponds to the inline flag (?s).
        # 1. convert to easy-to-copy tex (do not render math)
        convert_stage_2_1, n = re.subn(find_equation_pattern, replace_math_no_render, convert_stage_1, flags=re.DOTALL)
        # 2. convert to rendered equation
        convert_stage_2_2, n = re.subn(find_equation_pattern, replace_math_render, convert_stage_1, flags=re.DOTALL)
        # cat them together
        return pre + convert_stage_2_1 + f'{split}' + convert_stage_2_2 + suf
    else:
        return pre + markdown.markdown(txt, extensions=['fenced_code', 'codehilite', 'tables', 'sane_lists']) + suf


sample = preprocess_newbing_out(sample)
sample = close_up_code_segment_during_stream(sample)
sample = markdown_convertion(sample)
with open('tmp.html', 'w', encoding='utf8') as f:
    f.write("""

<head>
    <title>My Website</title>
    <link rel="stylesheet" type="text/css" href="style.css">
</head>

    """)
    f.write(sample)
