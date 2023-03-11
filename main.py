import gradio as gr
import os
import json

from llama_func import *
from utils import *
from presets import *

if os.path.exists("args.json"):
    with open("args.json", "r") as f:
        args = json.load(f)
    

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
                        index_select = gr.Dropdown(choices=refresh_json_list(plain=True), show_label=False).style(container=False)
                    with gr.Column(min_width=30, scale=1):
                        index_refresh_btn = gr.Button("🔄").style()
        
        
    with gr.Tab("对话"):
        with gr.Row():
            with gr.Column(scale=1):
                chat_tone = gr.Radio(["创意", "平衡", "精确"], label="语气", type="index", value="平衡")
            with gr.Column(scale=3):
                search_options_checkbox = gr.CheckboxGroup(label="搜索选项", choices=["🔍 New Google", "🔍 New Baidu", "🔍 手动输入"])
        chatbot = gr.Chatbot()
        with gr.Row():
            with gr.Column(min_width=50, scale=1):
                chat_empty_btn = gr.Button("🧹", variant="secondary")
            with gr.Column(scale=12):
                chat_input = gr.Textbox(show_label=False, placeholder="在此输入...").style(container=False)
            with gr.Column(min_width=50, scale=1):
                chat_submit_btn = gr.Button("🚀", variant="primary")
        suggested_user_turns = gr.Dropdown(choices=[], label="推荐的回复")


    with gr.Tab("对话设置"):
        with gr.Row():
            sim_k = gr.Slider(1, 10, 1, step=1, label="尝试次数", interactive=True, show_label=True)
            tempurature = gr.Slider(0, 2, 0.5, step=0.1, label="回答灵活性", interactive=True, show_label=True)
        tmpl_select = gr.Radio(prompt_tmpl_list, value="MZhao Mode", label="Prompt模板", interactive=True)
        prompt_tmpl = gr.Textbox(value=prompt_tmpl_dict["MZhao Mode"] ,lines=10, max_lines=40 ,show_label=False)


    with gr.Tab("构建索引"):
        with gr.Row():
            with gr.Column():
                upload_file = gr.Files(label="上传文件(支持 .txt, .pdf, .epub, .docx等)")
                with gr.Row():
                    max_input_size = gr.Slider(256, 4096, 4096, step=1, label="提问tokens限制", interactive=True, show_label=True)
                    num_outputs = gr.Slider(256, 4096, 512, step=1, label="回答tokens限制", interactive=True, show_label=True)
                with gr.Row():
                    max_chunk_overlap = gr.Slider(0, 100, 20, step=1, label="选段重复度（单位tokens）", interactive=True, show_label=True)
                    chunk_size_limit = gr.Slider(256, 4096, 512, step=1, label="选段长度限制", interactive=True, show_label=True)
                new_index_name = gr.Textbox(placeholder="新索引名称：", show_label=False).style(container=False)
                construct_btn = gr.Button("⚒️ 构建", variant="primary")
            with gr.Row():
                with gr.Column():
                    with gr.Row():
                        with gr.Column(min_width=50, scale=1):
                            json_refresh_btn = gr.Button("🔄")
                        with gr.Column(scale=7):
                            json_select = gr.Dropdown(choices=refresh_json_list(plain=True), show_label=False, multiselect=False).style(container=False)
                        with gr.Column(min_width=50, scale=1):
                            json_confirm_btn = gr.Button("🔎")
                    json_display = gr.JSON(label="查看所选json文件")
               
    index_refresh_btn.click(refresh_json_list, None, [index_select])
               
    chat_input.submit(chat_ai, [api_key, index_select, chat_input, prompt_tmpl, sim_k, chat_tone, chat_context, chatbot, search_options_checkbox, suggested_user_turns], [chat_context, chatbot, suggested_user_turns])
    chat_input.submit(reset_textbox, [], [chat_input])
    chat_submit_btn.click(chat_ai, [api_key, index_select, chat_input, prompt_tmpl, sim_k, chat_tone, chat_context, chatbot, search_options_checkbox, suggested_user_turns], [chat_context, chatbot, suggested_user_turns])
    chat_submit_btn.click(reset_textbox, [], [chat_input])
    chat_empty_btn.click(lambda: ([], []), None, [chat_context, chatbot])
    
    tmpl_select.change(change_prompt_tmpl, [tmpl_select], [prompt_tmpl])

    construct_btn.click(construct_index, [api_key, upload_file, new_index_name, max_input_size, num_outputs, max_chunk_overlap], [index_select, json_select])
    json_confirm_btn.click(display_json, [json_select], [json_display])
    json_refresh_btn.click(refresh_json_list, None, [json_select])

if __name__ == "__main__":
    demo.queue().launch(server_name=args["host"], server_port=args["port"], share=args["share"])
