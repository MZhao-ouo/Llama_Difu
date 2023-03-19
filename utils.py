import os
import gradio as gr
from zipfile import ZipFile
import re
from presets import *

def save_index(index, index_name, exist_ok=False):
    file_path = f"./index/{index_name}.json"

    if not os.path.exists(file_path) or exist_ok:
        index.save_to_disk(file_path)
        print(f'Saved file "{file_path}".')
    else:
        i = 1
        while True:
            new_file_path = f'{os.path.splitext(file_path)[0]}_{i}{os.path.splitext(file_path)[1]}'
            if not os.path.exists(new_file_path):
                index.save_to_disk(new_file_path)
                print(f'Saved file "{new_file_path}".')
                break
            i += 1

def refresh_json_list(plain=False):
    json_list = []
    for root, dirs, files in os.walk("./index"):
        for file in files:
            if os.path.splitext(file)[1] == '.json':
                json_list.append(os.path.splitext(file)[0])
    if plain:
        return json_list
    return gr.Dropdown.update(choices=json_list)

def upload_file(file_obj):
    files = []
    with ZipFile(file_obj.name) as zfile:
        for zinfo in zfile.infolist():
            files.append(
                {
                    "name": zinfo.filename,
                }
            )
    return files

def reset_textbox():
    return gr.update(value='')

def change_prompt_tmpl(tmpl_select):
    new_tmpl = prompt_tmpl_dict[tmpl_select]
    return gr.update(value=new_tmpl)

def change_refine_tmpl(refine_select):
    new_tmpl = refine_tmpl_dict[refine_select]
    return gr.update(value=new_tmpl)

def lock_params(index_type):
    if index_type == "GPTSimpleVectorIndex" or index_type == "GPTListIndex":
        return gr.Slider.update(interactive=False, label="子节点数量（当前索引类型不可用）"), gr.Slider.update(interactive=False, label="每段关键词数量（当前索引类型不可用）")
    elif index_type == "GPTTreeIndex":
        return gr.Slider.update(interactive=True, label="子节点数量"), gr.Slider.update(interactive=False, label="每段关键词数量（当前索引类型不可用）")
    elif index_type == "GPTKeywordTableIndex":
        return gr.Slider.update(interactive=False, label="子节点数量（当前索引类型不可用）"), gr.Slider.update(interactive=True, label="每段关键词数量")

def add_space(text):
    punctuations = {'，': '， ', '。': '。 ', '？': '？ ', '！': '！ ', '：': '： ', '；': '； '}
    for cn_punc, en_punc in punctuations.items():
        text = text.replace(cn_punc, en_punc)
    return text

def parse_text(text):
    lines = text.split("\n")
    lines = [line for line in lines if line != ""]
    count = 0
    for i, line in enumerate(lines):
        if "```" in line:
            count += 1
            items = line.split('`')
            if count % 2 == 1:
                lines[i] = f'<pre><code class="language-{items[-1]}">'
            else:
                lines[i] = f'<br></code></pre>'
        else:
            if i > 0:
                if count % 2 == 1:
                    line = line.replace("`", "\`")
                    line = line.replace("<", "&lt;")
                    line = line.replace(">", "&gt;")
                    line = line.replace(" ", "&nbsp;")
                    line = line.replace("*", "&ast;")
                    line = line.replace("_", "&lowbar;")
                    line = line.replace("-", "&#45;")
                    line = line.replace(".", "&#46;")
                    line = line.replace("!", "&#33;")
                    line = line.replace("(", "&#40;")
                    line = line.replace(")", "&#41;")
                    line = line.replace("$", "&#36;")
                lines[i] = "<br>"+line
    text = "".join(lines)
    return text

def parse_law_text(law_text):
    law_dict = {}

    # 获取法律名称
    law_name = re.search(r'中华人民共和国(.*?)\n', law_text).group(1).strip()
    law_dict['name'] = "中华人民共和国" + law_name

    # 获取章节标题
    catalog = re.findall(r'第[一二三四五六七八九十百千]+章\s+(.*?)\n', law_text)
    law_dict['catalog'] = catalog[len(catalog)//2:]

    # 获取法律内容
    law_content = []
    chapters = re.split(r'第[一二三四五六七八九十百千]+章\s+', law_text)[1:]
    chapters = chapters[len(chapters)//2:]
    for i, chapter in enumerate(chapters):
        sections = re.split(r'第[一二三四五六七八九十百千]+节\s+', chapter)[1:]

        if len(sections) > 1:
            for j, section in enumerate(sections):
                articles = re.findall(r'　{2}第([一二三四五六七八九十百千]+)条(.*?)\n', section)
                lines = section.splitlines()
                for index, article in enumerate(articles):
                    article_content = article[1].strip()
                    append_flag = False
                    for line in lines:
                        if article_content in line.strip():
                            append_flag = True
                            continue
                        if index + 1 < len(articles):
                            if articles[index + 1][1].strip() in line.strip():
                                append_flag = False
                        if append_flag:
                            article_content += ("\n" + line.strip())
                    law_content.append(
                        [article_content.strip(), f'{law_name}，第{i + 1}章 {catalog[i]}，第{j + 1}节 {section.split()[0]}，第{article[0]}条'])
        else:
            articles = re.findall(r'　{2}第([一二三四五六七八九十百千]+)条(.*?)\n', chapter)
            lines = chapter.splitlines()
            for index, article in enumerate(articles):
                article_content = article[1].strip()
                append_flag = False
                for line in lines:
                    if line == "":
                        continue
                    if article_content in line.strip():
                        append_flag = True
                        continue
                    if index + 1 < len(articles):
                        if articles[index + 1][1].strip() in line.strip():
                            append_flag = False
                    if append_flag:
                        article_content += ("\n" + line.strip())
                law_content.append(
                    [article_content.strip(), f'{law_name}，第{i + 1}章 {catalog[i]}，第{article[0]}条'])

    law_dict['content'] = law_content

    return law_dict
