import gradio as gr
import os
import json

from llama_func import *
from utils import *
from presets import *

if os.path.exists("args.json"):
    with open("args.json", "r") as f:
        args = json.load(f)
else:
    args = {}
    args["api-key"] = ""
    args["host"] = "127.0.0.1"
    args["port"] = 7860
    args["share"] = False
    

with gr.Blocks() as demo:
    chat_context = gr.State([])
    new_google_chat_context = gr.State([])
    
    with gr.Row():
        with gr.Column(scale=1):
            with gr.Box():
                gr.Markdown("**OpenAI API-Key**")
                api_key = gr.Textbox(show_label=False, placeholder="请在这里输入你的API-key", value=args["api-key"], type="password").style(container=False)
        with gr.Column(scale=3):
            with gr.Box():
                gr.Markdown("**选择索引**")
                with gr.Row():
                    with gr.Column(scale=12):
                        index_select = gr.Dropdown(choices=refresh_json_list(plain=True), value="请选择索引文件", show_label=False, multiselect=False).style(container=False)
                    with gr.Column(min_width=30, scale=1):
                        index_refresh_btn = gr.Button("🔄").style()
        
        
    with gr.Tab("对话"):
        with gr.Row():
            with gr.Column(scale=1):
                chat_tone = gr.Radio(["创意", "平衡", "精确"], label="语气", type="index", value="平衡")
            with gr.Column(scale=3):
                search_options_checkbox = gr.CheckboxGroup(label="搜索选项（需清空索引）", choices=["🔍 New Google", "🔍 New Baidu", "🔍 手动输入"])
        chatbot = gr.Chatbot()
        with gr.Row():
            with gr.Column(min_width=50, scale=1):
                chat_empty_btn = gr.Button("🧹", variant="secondary")
            with gr.Column(scale=12):
                chat_input = gr.Textbox(show_label=False, placeholder="在此输入...").style(container=False)
            with gr.Column(min_width=50, scale=1):
                chat_submit_btn = gr.Button("🚀", variant="primary")


    with gr.Tab("对话设置"):
        with gr.Row():
            sim_k = gr.Slider(1, 10, 1, step=1, label="优化次数", interactive=True, show_label=True)
            tempurature = gr.Slider(0, 2, 0.5, step=0.1, label="回答灵活性", interactive=True, show_label=True)
        with gr.Row():
            with gr.Column():
                tmpl_select = gr.Radio(list(prompt_tmpl_dict.keys()), value="New Default", label="Prompt模板", interactive=True)
                prompt_tmpl = gr.Textbox(value=prompt_tmpl_dict["New Default"] ,lines=10, max_lines=40 ,show_label=False)
            with gr.Column():
                refine_select = gr.Radio(list(refine_tmpl_dict.keys()), value="Default", label="Refine模板", interactive=True)
                refine_tmpl = gr.Textbox(value=refine_tmpl_dict["Default"] ,lines=10, max_lines=40 ,show_label=False)


    with gr.Tab("构建索引"):
        with gr.Row():
            with gr.Column():
                index_type = gr.Dropdown(choices=["GPTSimpleVectorIndex", "GPTTreeIndex", "GPTKeywordTableIndex", "GPTListIndex"], label="索引类型", value="GPTSimpleVectorIndex")
                upload_file = gr.Files(label="上传文件(支持 .txt, .pdf, .epub, .docx等)")
                new_index_name = gr.Textbox(placeholder="新索引名称：", show_label=False).style(container=False)
                construct_btn = gr.Button("⚒️ 构建", variant="primary")
            with gr.Row():
                with gr.Column():
                    with gr.Row():
                        max_input_size = gr.Slider(256, 4096, 4096, step=1, label="每次输入tokens限制", interactive=True, show_label=True)
                        num_outputs = gr.Slider(256, 4096, 512, step=1, label="输出tokens限制", interactive=True, show_label=True)
                    with gr.Row():
                        max_chunk_overlap = gr.Slider(0, 100, 20, step=1, label="选段重复度", interactive=True, show_label=True)
                        chunk_size_limit = gr.Slider(0, 4096, 0, step=1, label="选段长度限制（0为自动）", interactive=True, show_label=True)
                    with gr.Row():
                        embedding_limit = gr.Slider(0, 100, 0, step=1, label="Embedding限制（0为自动）", interactive=True, show_label=True)
                        separator = gr.Textbox(show_label=False, label="分隔符", placeholder="分隔符，默认为空格", value="", interactive=True)
                    with gr.Row():
                        num_children = gr.Slider(2, 100, 10, step=1, label="子节点数量（当前索引类型不可用）", interactive=False, show_label=True)
                        max_keywords_per_chunk = gr.Slider(1, 100, 10, step=1, label="每段关键词数量（当前索引类型不可用）", interactive=False, show_label=True)

               
    index_refresh_btn.click(refresh_json_list, None, [index_select])
               
    chat_input.submit(chat_ai, [api_key, index_select, chat_input, prompt_tmpl, refine_tmpl, sim_k, chat_tone, chat_context, chatbot, search_options_checkbox], [chat_context, chatbot])
    chat_input.submit(reset_textbox, [], [chat_input])
    chat_submit_btn.click(chat_ai, [api_key, index_select, chat_input, prompt_tmpl, refine_tmpl, sim_k, chat_tone, chat_context, chatbot, search_options_checkbox], [chat_context, chatbot])
    chat_submit_btn.click(reset_textbox, [], [chat_input])
    chat_empty_btn.click(lambda: ([], []), None, [chat_context, chatbot])
    
    tmpl_select.change(change_prompt_tmpl, [tmpl_select], [prompt_tmpl])
    refine_select.change(change_refine_tmpl, [refine_select], [refine_tmpl])

    index_type.change(lock_params, [index_type], [num_children, max_keywords_per_chunk])
    construct_btn.click(construct_index, [api_key, upload_file, new_index_name, index_type, max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit, embedding_limit, separator, num_children], [index_select])
    

if __name__ == "__main__":
    demo.title = "Llama Do it for You!"
    demo.queue().launch(server_name=args["host"], server_port=args["port"], share=args["share"])
