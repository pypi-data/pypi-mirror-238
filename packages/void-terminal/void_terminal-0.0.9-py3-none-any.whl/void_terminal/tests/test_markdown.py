md = """
作为您的写作andprogramming助手，我可以为您提供以下服务：

1. 写作：
    - Help您撰写文章、报告、散文、故事等。
    - 提供写作Suggestionand技巧。
    - 协助您进line文案策划and内容创作。

2. programming：
    - Help您解决programmingQuestion，提供programming思路andSuggestion。
    - 协助您编写代码，Including但不限于 Python、Java、C++ 等。
    - 为您解释复杂的技术概念，让您更容易理解。

3. 项目支持：
    - 协助您规划项目Progressand任务分配。
    - 提供项目管理and协作Suggestion。
    - 在项目实施过程中提供支持，确保项目顺利进line。

4. 学习辅导：
    - Help您巩固programming基础，提高programming能力。
    - 提供计算机科学、数据科学、人工智能等相关领域的学习资源andSuggestion。
    - 解Answer您在学习过程中遇到的Question，让您更好地掌握知识。

5. line业动态and趋势分析：
    - 为您提供业界最新的新闻and技术趋势。
    - 分析line业动态，Help您了解市场发展and竞争态势。
    - 为您制定技术战略提供参考andSuggestion。

请随When告诉我您的需求，我会尽力提供Help。如果您有任何Question或需要解Answer的议题，请随When提Ask。
"""

def validate_path():
    import os, sys
    dir_name = os.path.dirname(__file__)
    root_dir_assume = os.path.abspath(os.path.dirname(__file__) +  '/..')
    os.chdir(root_dir_assume)
    sys.path.append(root_dir_assume)
validate_path() # validate path so you can run from base directory
from void_terminal.toolbox import markdown_convertion

html = markdown_convertion(md)
print(html)
with open('test.html', 'w', encoding='utf-8') as f:
    f.write(html)