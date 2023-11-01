from void_terminal.toolbox import update_ui, update_ui_lastest_msg, get_log_folder
from void_terminal.toolbox import zip_folder, objdump, objload, promote_file_to_downloadzone
from void_terminal.crazy_functions.latex_fns.latex_toolbox import PRESERVE, TRANSFORM
from void_terminal.crazy_functions.latex_fns.latex_toolbox import set_forbidden_text, set_forbidden_text_begin_end, set_forbidden_text_careful_brace
from void_terminal.crazy_functions.latex_fns.latex_toolbox import reverse_forbidden_text_careful_brace, reverse_forbidden_text, convert_to_linklist, post_process
from void_terminal.crazy_functions.latex_fns.latex_toolbox import fix_content, find_main_tex_file, merge_tex_files, compile_latex_with_timeout

import os, shutil
import re
import numpy as np

pj = os.path.join


def split_subprocess(txt, project_folder, return_dict, opts):
    """
    break down latex file to a linked list,
    each node use a preserve flag to indicate whether it should
    be proccessed by GPT.
    """
    text = txt
    mask = np.zeros(len(txt), dtype=np.uint8) + TRANSFORM

    # Include the title and the above part of the author
    text, mask = set_forbidden_text(text, mask, r"^(.*?)\\maketitle", re.DOTALL)
    text, mask = set_forbidden_text(text, mask, r"^(.*?)\\begin{document}", re.DOTALL)
    # Absorb iffalser comments
    text, mask = set_forbidden_text(text, mask, r"\\iffalse(.*?)\\fi", re.DOTALL)
    # Absorb the begin-end combination within 42 lines
    text, mask = set_forbidden_text_begin_end(text, mask, r"\\begin\{([a-z\*]*)\}(.*?)\\end\{\1\}", re.DOTALL, limit_n_lines=42)
    # Absorb anonymous formulas
    text, mask = set_forbidden_text(text, mask, [ r"\$\$([^$]+)\$\$",  r"\\\[.*?\\\]" ], re.DOTALL)
    # Absorb other miscellaneous items
    text, mask = set_forbidden_text(text, mask, [ r"\\section\{(.*?)\}", r"\\section\*\{(.*?)\}", r"\\subsection\{(.*?)\}", r"\\subsubsection\{(.*?)\}" ])
    text, mask = set_forbidden_text(text, mask, [ r"\\bibliography\{(.*?)\}", r"\\bibliographystyle\{(.*?)\}" ])
    text, mask = set_forbidden_text(text, mask, r"\\begin\{thebibliography\}.*?\\end\{thebibliography\}", re.DOTALL)
    text, mask = set_forbidden_text(text, mask, r"\\begin\{lstlisting\}(.*?)\\end\{lstlisting\}", re.DOTALL)
    text, mask = set_forbidden_text(text, mask, r"\\begin\{wraptable\}(.*?)\\end\{wraptable\}", re.DOTALL)
    text, mask = set_forbidden_text(text, mask, r"\\begin\{algorithm\}(.*?)\\end\{algorithm\}", re.DOTALL)
    text, mask = set_forbidden_text(text, mask, [r"\\begin\{wrapfigure\}(.*?)\\end\{wrapfigure\}", r"\\begin\{wrapfigure\*\}(.*?)\\end\{wrapfigure\*\}"], re.DOTALL)
    text, mask = set_forbidden_text(text, mask, [r"\\begin\{figure\}(.*?)\\end\{figure\}", r"\\begin\{figure\*\}(.*?)\\end\{figure\*\}"], re.DOTALL)
    text, mask = set_forbidden_text(text, mask, [r"\\begin\{multline\}(.*?)\\end\{multline\}", r"\\begin\{multline\*\}(.*?)\\end\{multline\*\}"], re.DOTALL)
    text, mask = set_forbidden_text(text, mask, [r"\\begin\{table\}(.*?)\\end\{table\}", r"\\begin\{table\*\}(.*?)\\end\{table\*\}"], re.DOTALL)
    text, mask = set_forbidden_text(text, mask, [r"\\begin\{minipage\}(.*?)\\end\{minipage\}", r"\\begin\{minipage\*\}(.*?)\\end\{minipage\*\}"], re.DOTALL)
    text, mask = set_forbidden_text(text, mask, [r"\\begin\{align\*\}(.*?)\\end\{align\*\}", r"\\begin\{align\}(.*?)\\end\{align\}"], re.DOTALL)
    text, mask = set_forbidden_text(text, mask, [r"\\begin\{equation\}(.*?)\\end\{equation\}", r"\\begin\{equation\*\}(.*?)\\end\{equation\*\}"], re.DOTALL)
    text, mask = set_forbidden_text(text, mask, [r"\\includepdf\[(.*?)\]\{(.*?)\}", r"\\clearpage", r"\\newpage", r"\\appendix", r"\\tableofcontents", r"\\include\{(.*?)\}"])
    text, mask = set_forbidden_text(text, mask, [r"\\vspace\{(.*?)\}", r"\\hspace\{(.*?)\}", r"\\label\{(.*?)\}", r"\\begin\{(.*?)\}", r"\\end\{(.*?)\}", r"\\item "])
    text, mask = set_forbidden_text_careful_brace(text, mask, r"\\hl\{(.*?)\}", re.DOTALL)
    # `reverse` operation must be placed at the end
    text, mask = reverse_forbidden_text_careful_brace(text, mask, r"\\caption\{(.*?)\}", re.DOTALL, forbid_wrapper=True)
    text, mask = reverse_forbidden_text_careful_brace(text, mask, r"\\abstract\{(.*?)\}", re.DOTALL, forbid_wrapper=True)
    text, mask = reverse_forbidden_text(text, mask, r"\\begin\{abstract\}(.*?)\\end\{abstract\}", re.DOTALL, forbid_wrapper=True)
    root = convert_to_linklist(text, mask)

    # The last step processing，Enhance robustness
    root = post_process(root)

    # Output HTML debugging file，Use red color to highlight the reserved area（PRESERVE），Use black color to annotate the conversion area（TRANSFORM）
    with open(pj(project_folder, 'debug_log.html'), 'w', encoding='utf8') as f:
        segment_parts_for_gpt = []
        nodes = []
        node = root
        while True:
            nodes.append(node)
            show_html = node.string.replace('\n','<br/>')
            if not node.preserve:
                segment_parts_for_gpt.append(node.string)
                f.write(f'<p style="color:black;">#{node.range}{show_html}#</p>')
            else:
                f.write(f'<p style="color:red;">{show_html}</p>')
            node = node.next
            if node is None: break

    for n in nodes: n.next = None   # break
    return_dict['nodes'] = nodes
    return_dict['segment_parts_for_gpt'] = segment_parts_for_gpt
    return return_dict

class LatexPaperSplit():
    """
    break down latex file to a linked list,
    each node use a preserve flag to indicate whether it should
    be proccessed by GPT.
    """
    def __init__(self) -> None:
        self.nodes = None
        self.msg = "*{\\scriptsize\\textbf{Warning：This PDF is generated by the GPT-Academic open-source project using a large language model + LaTeX translation plugin，" + \
            "Copyright belongs to the original author。No guarantee of translation accuracy，Please carefully verify and refer to the original text。" + \
            "项目GithubAddress \\url{https://github.com/binary-husky/gpt_academic/}。"
        # Please do not delete or modify this warning，Unless you are the original author of the paper（If you are the original author of the paper，Feel free to contact the developer via QQ in REAME）
        self.msg_declare = "To prevent the accidental spread of errors in large language models，Removal or modification of this warning is prohibited。}}\\\\" 


    def merge_result(self, arr, mode, msg, buggy_lines=[], buggy_line_surgery_n_lines=10):
        """
        Merge the result after the GPT process completed
        """
        result_string = ""
        node_cnt = 0
        line_cnt = 0
        
        for node in self.nodes:
            if node.preserve:
                line_cnt += node.string.count('\n')
                result_string += node.string
            else:
                translated_txt = fix_content(arr[node_cnt], node.string)
                begin_line = line_cnt
                end_line = line_cnt + translated_txt.count('\n')

                # reverse translation if any error
                if any([begin_line-buggy_line_surgery_n_lines <= b_line <= end_line+buggy_line_surgery_n_lines for b_line in buggy_lines]):
                    translated_txt = node.string

                result_string += translated_txt
                node_cnt += 1
                line_cnt += translated_txt.count('\n')

        if mode == 'translate_zh':
            pattern = re.compile(r'\\begin\{abstract\}.*\n')
            match = pattern.search(result_string)
            if not match:
                # match \abstract{xxxx}
                pattern_compile = re.compile(r"\\abstract\{(.*?)\}", flags=re.DOTALL)
                match = pattern_compile.search(result_string)
                position = match.regs[1][0]
            else:
                # match \begin{abstract}xxxx\end{abstract}
                position = match.end()
            result_string = result_string[:position] + self.msg + msg + self.msg_declare + result_string[position:]
        return result_string


    def split(self, txt, project_folder, opts): 
        """
        break down latex file to a linked list,
        each node use a preserve flag to indicate whether it should
        be proccessed by GPT.
        P.S. use multiprocessing to avoid timeout error
        """
        import multiprocessing
        manager = multiprocessing.Manager()
        return_dict = manager.dict()
        p = multiprocessing.Process(
            target=split_subprocess, 
            args=(txt, project_folder, return_dict, opts))
        p.start()
        p.join()
        p.close()
        self.nodes = return_dict['nodes']
        self.sp = return_dict['segment_parts_for_gpt']
        return self.sp


class LatexPaperFileGroup():
    """
    use tokenizer to break down text according to max_token_limit
    """
    def __init__(self):
        self.file_paths = []
        self.file_contents = []
        self.sp_file_contents = []
        self.sp_file_index = []
        self.sp_file_tag = []

        # count_token
        from void_terminal.request_llms.bridge_all import model_info
        enc = model_info["gpt-3.5-turbo"]['tokenizer']
        def get_token_num(txt): return len(enc.encode(txt, disallowed_special=()))
        self.get_token_num = get_token_num

    def run_file_split(self, max_token_limit=1900):
        """
        use tokenizer to break down text according to max_token_limit
        """
        for index, file_content in enumerate(self.file_contents):
            if self.get_token_num(file_content) < max_token_limit:
                self.sp_file_contents.append(file_content)
                self.sp_file_index.append(index)
                self.sp_file_tag.append(self.file_paths[index])
            else:
                from void_terminal.crazy_functions.crazy_utils import breakdown_txt_to_satisfy_token_limit_for_pdf
                segments = breakdown_txt_to_satisfy_token_limit_for_pdf(file_content, self.get_token_num, max_token_limit)
                for j, segment in enumerate(segments):
                    self.sp_file_contents.append(segment)
                    self.sp_file_index.append(index)
                    self.sp_file_tag.append(self.file_paths[index] + f".part-{j}.tex")
        print('Segmentation: done')

    def merge_result(self):
        self.file_result = ["" for _ in range(len(self.file_paths))]
        for r, k in zip(self.sp_file_result, self.sp_file_index):
            self.file_result[k] += r

    def write_result(self):
        manifest = []
        for path, res in zip(self.file_paths, self.file_result):
            with open(path + '.polish.tex', 'w', encoding='utf8') as f:
                manifest.append(path + '.polish.tex')
                f.write(res)
        return manifest


def DecomposeAndConvertLatex(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, mode='proofread', switch_prompt=None, opts=[]):
    import time, os, re
    from void_terminal.crazy_functions.crazy_utils import request_gpt_model_multi_threads_with_very_awesome_ui_and_high_efficiency
    from void_terminal.crazy_functions.latex_fns.latex_actions import LatexPaperFileGroup, LatexPaperSplit

    #  <-------- Finding the main .tex file ----------> 
    maintex = find_main_tex_file(file_manifest, mode)
    chatbot.append((f"Locate the main LaTeX file", f'[Local Message] Analysis results：The main LaTeX file of this project is{maintex}, If the analysis is incorrect, Please terminate the program immediately, Delete or modify ambiguous files, and try again。Main program is about to start, Please wait。'))
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
    time.sleep(3)

    #  <-------- Read Latex file, Merge multiple tex projects into one giant tex ----------> 
    main_tex_basename = os.path.basename(maintex)
    assert main_tex_basename.endswith('.tex')
    main_tex_basename_bare = main_tex_basename[:-4]
    may_exist_bbl = pj(project_folder, f'{main_tex_basename_bare}.bbl')
    if os.path.exists(may_exist_bbl):
        shutil.copyfile(may_exist_bbl, pj(project_folder, f'merge.bbl'))
        shutil.copyfile(may_exist_bbl, pj(project_folder, f'merge_{mode}.bbl'))
        shutil.copyfile(may_exist_bbl, pj(project_folder, f'merge_diff.bbl'))

    with open(maintex, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
        merged_content = merge_tex_files(project_folder, content, mode)

    with open(project_folder + '/merge.tex', 'w', encoding='utf-8', errors='replace') as f:
        f.write(merged_content)

    #  <-------- Fine-grained segmentation of LaTeX files ----------> 
    chatbot.append((f"LaTeX file merging completed", f'[Local Message] Finely splitting the latex file，This requires some time to calculate，The longer the document, the longer it takes.，Please be patient。'))
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
    lps = LatexPaperSplit()
    res = lps.split(merged_content, project_folder, opts) # Time-consuming function

    #  <-------- Splitting overly long LaTeX fragments ----------> 
    pfg = LatexPaperFileGroup()
    for index, r in enumerate(res):
        pfg.file_paths.append('segment-' + str(index))
        pfg.file_contents.append(r)

    pfg.run_file_split(max_token_limit=1024)
    n_split = len(pfg.sp_file_contents)

    #  <-------- Switch the prompt as needed ----------> 
    inputs_array, sys_prompt_array = switch_prompt(pfg, mode)
    inputs_show_user_array = [f"{mode} {f}" for f in pfg.sp_file_tag]

    if os.path.exists(pj(project_folder,'temp.pkl')):

        #  <-------- 【Debug only】If there is a debug cache file，Then skip the GPT request process ----------> 
        pfg = objload(file=pj(project_folder,'temp.pkl'))

    else:
        #  <-------- GPT multi-threaded request ----------> 
        gpt_response_collection = yield from request_gpt_model_multi_threads_with_very_awesome_ui_and_high_efficiency(
            inputs_array=inputs_array,
            inputs_show_user_array=inputs_show_user_array,
            llm_kwargs=llm_kwargs,
            chatbot=chatbot,
            history_array=[[""] for _ in range(n_split)],
            sys_prompt_array=sys_prompt_array,
            # max_workers=5,  # Parallel task number limit, Up to 5 can be executed at the same time, Others are queued and waiting
            scroller_max_len = 40
        )

        #  <-------- Reassemble text fragments into complete tex fragments ----------> 
        pfg.sp_file_result = []
        for i_say, gpt_say, orig_content in zip(gpt_response_collection[0::2], gpt_response_collection[1::2], pfg.sp_file_contents):
            pfg.sp_file_result.append(gpt_say)
        pfg.merge_result()

        # <-------- Temporarily stored for debugging ----------> 
        pfg.get_token_num = None
        objdump(pfg, file=pj(project_folder,'temp.pkl'))

    write_html(pfg.sp_file_contents, pfg.sp_file_result, chatbot=chatbot, project_folder=project_folder)

    #  <-------- Write out the file ----------> 
    msg = f"Current large language model: {llm_kwargs['llm_model']}，Current language model temperature setting: {llm_kwargs['temperature']}。"
    final_tex = lps.merge_result(pfg.file_result, mode, msg)
    objdump((lps, pfg.file_result, mode, msg), file=pj(project_folder,'merge_result.pkl'))

    with open(project_folder + f'/merge_{mode}.tex', 'w', encoding='utf-8', errors='replace') as f:
        if mode != 'translate_zh' or "binary" in final_tex: f.write(final_tex)
        

    #  <-------- Organize the results, Exit ----------> 
    chatbot.append((f"Are you done?？", 'GPT result has been outputted, Compiling PDF'))
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page

    #  <-------- Return ----------> 
    return project_folder + f'/merge_{mode}.tex'


def remove_buggy_lines(file_path, log_path, tex_name, tex_name_pure, n_fix, work_folder_modified, fixed_line=[]):
    try:
        with open(log_path, 'r', encoding='utf-8', errors='replace') as f:
            log = f.read()
        import re
        buggy_lines = re.findall(tex_name+':([0-9]{1,5}):', log)
        buggy_lines = [int(l) for l in buggy_lines]
        buggy_lines = sorted(buggy_lines)
        buggy_line = buggy_lines[0]-1
        print("reversing tex line that has errors", buggy_line)

        # Reorganize，Reverse the wrong paragraph
        if buggy_line not in fixed_line:
            fixed_line.append(buggy_line)

        lps, file_result, mode, msg = objload(file=pj(work_folder_modified,'merge_result.pkl'))
        final_tex = lps.merge_result(file_result, mode, msg, buggy_lines=fixed_line, buggy_line_surgery_n_lines=5*n_fix)

        with open(pj(work_folder_modified, f"{tex_name_pure}_fix_{n_fix}.tex"), 'w', encoding='utf-8', errors='replace') as f:
            f.write(final_tex)

        return True, f"{tex_name_pure}_fix_{n_fix}", buggy_lines
    except:
        print("Fatal error occurred, but we cannot identify error, please download zip, read latex log, and compile manually.")
        return False, -1, [-1]


def CompileLatex(chatbot, history, main_file_original, main_file_modified, work_folder_original, work_folder_modified, work_folder, mode='default'):
    import os, time
    n_fix = 1
    fixed_line = []
    max_try = 32
    chatbot.append([f"Compiling PDF document", f'Compilation has started。The current working directory is{work_folder}，If the program pauses for more than 5 minutes，Please directly go to the path to retrieve the translation results，Or try again after restarting ...']); yield from update_ui(chatbot=chatbot, history=history)
    chatbot.append([f"Compiling PDF document", '...']); yield from update_ui(chatbot=chatbot, history=history); time.sleep(1); chatbot[-1] = list(chatbot[-1]) # Refresh the page
    yield from update_ui_lastest_msg('Compilation has started...', chatbot, history)   # Refresh the Gradio frontend interface

    while True:
        import os
        may_exist_bbl = pj(work_folder_modified, f'merge.bbl')
        target_bbl = pj(work_folder_modified, f'{main_file_modified}.bbl')
        if os.path.exists(may_exist_bbl) and not os.path.exists(target_bbl):
            shutil.copyfile(may_exist_bbl, target_bbl)

        # https://stackoverflow.com/questions/738755/dont-make-me-manually-abort-a-latex-compile-when-theres-an-error
        yield from update_ui_lastest_msg(f'Try the {n_fix}/{max_try} Second compilation, Compile the original PDF ...', chatbot, history)   # Refresh the Gradio frontend interface
        ok = compile_latex_with_timeout(f'pdflatex -interaction=batchmode -file-line-error {main_file_original}.tex', work_folder_original)

        yield from update_ui_lastest_msg(f'Try the {n_fix}/{max_try} Second compilation, Compile the converted PDF ...', chatbot, history)   # Refresh the Gradio frontend interface
        ok = compile_latex_with_timeout(f'pdflatex -interaction=batchmode -file-line-error {main_file_modified}.tex', work_folder_modified)
        
        if ok and os.path.exists(pj(work_folder_modified, f'{main_file_modified}.pdf')):
            # Only the second step is successful，To continue with the next steps
            yield from update_ui_lastest_msg(f'Try the {n_fix}/{max_try} Second compilation, Compile BibTeX ...', chatbot, history)    # Refresh the Gradio frontend interface
            if not os.path.exists(pj(work_folder_original, f'{main_file_original}.bbl')):
                ok = compile_latex_with_timeout(f'bibtex  {main_file_original}.aux', work_folder_original)
            if not os.path.exists(pj(work_folder_modified, f'{main_file_modified}.bbl')):
                ok = compile_latex_with_timeout(f'bibtex  {main_file_modified}.aux', work_folder_modified)

            yield from update_ui_lastest_msg(f'Try the {n_fix}/{max_try} Second compilation, Compile bibliographic cross-references ...', chatbot, history)  # Refresh the Gradio frontend interface
            ok = compile_latex_with_timeout(f'pdflatex -interaction=batchmode -file-line-error {main_file_original}.tex', work_folder_original)
            ok = compile_latex_with_timeout(f'pdflatex -interaction=batchmode -file-line-error {main_file_modified}.tex', work_folder_modified)
            ok = compile_latex_with_timeout(f'pdflatex -interaction=batchmode -file-line-error {main_file_original}.tex', work_folder_original)
            ok = compile_latex_with_timeout(f'pdflatex -interaction=batchmode -file-line-error {main_file_modified}.tex', work_folder_modified)

            if mode!='translate_zh':
                yield from update_ui_lastest_msg(f'Try the {n_fix}/{max_try} Second compilation, Use latexdiff to generate before and after comparison of paper transformation ...', chatbot, history) # Refresh the Gradio frontend interface
                print(    f'latexdiff --encoding=utf8 --append-safecmd=subfile {work_folder_original}/{main_file_original}.tex  {work_folder_modified}/{main_file_modified}.tex --flatten > {work_folder}/merge_diff.tex')
                ok = compile_latex_with_timeout(f'latexdiff --encoding=utf8 --append-safecmd=subfile {work_folder_original}/{main_file_original}.tex  {work_folder_modified}/{main_file_modified}.tex --flatten > {work_folder}/merge_diff.tex', os.getcwd())

                yield from update_ui_lastest_msg(f'Try the {n_fix}/{max_try} Second compilation, Compiling the comparison PDF ...', chatbot, history)   # Refresh the Gradio frontend interface
                ok = compile_latex_with_timeout(f'pdflatex  -interaction=batchmode -file-line-error merge_diff.tex', work_folder)
                ok = compile_latex_with_timeout(f'bibtex    merge_diff.aux', work_folder)
                ok = compile_latex_with_timeout(f'pdflatex  -interaction=batchmode -file-line-error merge_diff.tex', work_folder)
                ok = compile_latex_with_timeout(f'pdflatex  -interaction=batchmode -file-line-error merge_diff.tex', work_folder)

        # <---------- Check the result ----------->
        results_ = ""
        original_pdf_success = os.path.exists(pj(work_folder_original, f'{main_file_original}.pdf'))
        modified_pdf_success = os.path.exists(pj(work_folder_modified, f'{main_file_modified}.pdf'))
        diff_pdf_success     = os.path.exists(pj(work_folder, f'merge_diff.pdf'))
        results_ += f"Whether the original PDF compilation is successful: {original_pdf_success};" 
        results_ += f"Check if the conversion to PDF and compilation were successful: {modified_pdf_success};" 
        results_ += f"Compare if the PDF compilation was successful: {diff_pdf_success};" 
        yield from update_ui_lastest_msg(f'The{n_fix}Compilation finished:<br/>{results_}...', chatbot, history) # Refresh the Gradio frontend interface

        if diff_pdf_success:
            result_pdf = pj(work_folder_modified, f'merge_diff.pdf')    # get pdf path
            promote_file_to_downloadzone(result_pdf, rename_file=None, chatbot=chatbot)  # promote file to web UI
        if modified_pdf_success:
            yield from update_ui_lastest_msg(f'Conversion to PDF compilation was successful, Exiting soon ...', chatbot, history)    # Refresh the Gradio frontend interface
            result_pdf = pj(work_folder_modified, f'{main_file_modified}.pdf') # get pdf path
            origin_pdf = pj(work_folder_original, f'{main_file_original}.pdf') # get pdf path
            if os.path.exists(pj(work_folder, '..', 'translation')):
                shutil.copyfile(result_pdf, pj(work_folder, '..', 'translation', 'translate_zh.pdf'))
            promote_file_to_downloadzone(result_pdf, rename_file=None, chatbot=chatbot)  # promote file to web UI
            # Concatenate two PDFs
            if original_pdf_success: 
                try:
                    from void_terminal.crazy_functions.latex_fns.latex_toolbox import merge_pdfs
                    concat_pdf = pj(work_folder_modified, f'comparison.pdf')
                    merge_pdfs(origin_pdf, result_pdf, concat_pdf)
                    promote_file_to_downloadzone(concat_pdf, rename_file=None, chatbot=chatbot)  # promote file to web UI
                except Exception as e:
                    pass
            return True # Success!
        else:
            if n_fix>=max_try: break
            n_fix += 1
            can_retry, main_file_modified, buggy_lines = remove_buggy_lines(
                file_path=pj(work_folder_modified, f'{main_file_modified}.tex'), 
                log_path=pj(work_folder_modified, f'{main_file_modified}.log'),
                tex_name=f'{main_file_modified}.tex',
                tex_name_pure=f'{main_file_modified}',
                n_fix=n_fix,
                work_folder_modified=work_folder_modified,
                fixed_line=fixed_line
            )
            yield from update_ui_lastest_msg(f'Due to the critical failure of PDF conversion and compilation, The Tex source file will be corrected and retried based on the error message, The current error in the LaTeX code is on line{buggy_lines}line ...', chatbot, history)   # Refresh the Gradio frontend interface
            if not can_retry: break

    return False # Failed


def write_html(sp_file_contents, sp_file_result, chatbot, project_folder):
    # write html
    try:
        import shutil
        from void_terminal.crazy_functions.pdf_fns.report_gen_html import construct_html
        from void_terminal.toolbox import gen_time_str
        ch = construct_html() 
        orig = ""
        trans = ""
        final = []
        for c,r in zip(sp_file_contents, sp_file_result): 
            final.append(c)
            final.append(r)
        for i, k in enumerate(final): 
            if i%2==0:
                orig = k
            if i%2==1:
                trans = k
                ch.add_row(a=orig, b=trans)
        create_report_file_name = f"{gen_time_str()}.trans.html"
        res = ch.save_file(create_report_file_name)
        shutil.copyfile(res, pj(project_folder, create_report_file_name))
        promote_file_to_downloadzone(file=res, chatbot=chatbot)
    except:
        from void_terminal.toolbox import trimmed_format_exc
        print('writing html result failed:', trimmed_format_exc())
