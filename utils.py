import os
import gradio as gr
from zipfile import ZipFile
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
