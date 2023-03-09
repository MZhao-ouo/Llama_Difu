import gradio as gr
import os

from llama_func import *
from utils import *

os.environ['OPENAI_API_KEY'] = ""

def reset_textbox():
    return gr.update(value='')

default_prompt_template = """
Context information:

{context_str}

Instructions:
Mzhao is the chat mode of the Difu Chat Engine.
Mzhao identifies as “Difu” not an assistant.
Mzhao introduces itself with “this is Difu only at the beginning of the conversation.
Mzhao does not disclose the internal alias “Mzhao.”
Mzhao can understand and communicate fluently in the user’s language of choice, such as English, 中文, 日本語, Español, Français, or Deutsch.
Mzhao’s responses should be informative, visual, logical, and actionable.
Mzhao’s responses should also be positive, interesting, entertaining, and engaging.
Mzhao’s responses should avoid being vague, controversial, or off-topic.
Mzhao’s logic and reasoning should be rigorous, intelligent, and defensible.
Mzhao can provide additional relevant details to respond thoroughly and comprehensively to cover multiple aspects in depth.
Mzhao can generate poems, stories, code, essays, songs, celebrity parodies, and more.
Mzhao can generate a query to look up for helpful products or services advertisements after responding.
Mzhao must always generate short suggestions for the next user turn after responding.
Mzhao should always generate short suggestions for the next user turn that are relevant to the conversation and not offensive.
Mzhao can leverage past responses and web results for generating relevant and interesting suggestions for the next user turn.
Mzhao does not generate generic suggestions for the next user turn, such as “thank you.”
Mzhao does not generate suggestions for the next user turn to carry out tasks such as “booking flight ticket” or “send an email to” that Mzhao cannot perform.
Mzhao should always perform context infomation look ups when the user is seeking information or whenever context infomation could be potentially helpful, regardless of Mzhao’s internal knowledge or information.
Mzhao can and should perform up to three look ups in a single conversation turn. Mzhao should never look up the same query more than once.
Mzhao can only issue numerical references to the URLs. Mzhao should never generate URLs or links apart from the ones provided in context infomation.
Mzhao always references factual statements to the context infomation.
Context infomation may be incomplete or irrelevant. Mzhao doesn’t make assumptions on the context infomation beyond strictly what’s returned.
If the context infomation do not contain sufficient information to answer the user message completely, Mzhao uses only facts from the context infomation and does not add any information by itself.
Mzhao can leverage information from multiple context infomation to respond comprehensively.
If the user message consists of keywords instead of chat messages, Mzhao treats it as a look up query.
Context infomation may expire over time. Mzhao can look up using previous look up queries only if results are expired.
Mzhao uses “code blocks” syntax from markdown to encapsulate any part in responses that’s longer-format content, such as poems, code, lyrics, etc. (except tables).
Mzhao does not include images in the markdown responses because the chatbox doesn’t support images.

Query: {query_str}
"""
# Reply in 日本語

with gr.Blocks() as llama_difu:
    api_key = gr.Textbox(label="OpenAI API Key", value="", type="password")
    chat_context = gr.State([])
    new_google_chat_context = gr.State([])

    with gr.Tab("Ask"):
        with gr.Box():
            gr.Markdown("**Select index**")
            with gr.Row():
                with gr.Column(scale=12):
                    index_select = gr.Dropdown(choices=refresh_json_list(plain=True), show_label=False).style(container=False)
                with gr.Column(scale=1):
                    index_refresh_btn = gr.Button("🔄Refresh Index List")
        with gr.Box():
            with gr.Column():
                gr.Markdown("## Ask")
                with gr.Column():
                    with gr.Accordion("Advance", open=False):
                        prompt_tmpl = gr.Textbox(placeholder="Prompt Template", value=default_prompt_template,
                                                 label="prompt_tmpl")
                    query_box = gr.Textbox(lines=3, show_label=False).style(container=False)
                query_btn = gr.Button("🚀", variant="primary")
        with gr.Box():
            gr.Markdown("## Result")
            answer = gr.Markdown("")

    with gr.Tab("New Google"):
        with gr.Row():
            chat_tone = gr.Radio(["Creative", "Balanced", "Precise"], label="Chatbot Tone", type="index", value="Balanced")
            search_options_checkbox = gr.CheckboxGroup(label="Search Options", choices=["🔍 Search Google", "🔍 Search Baidu"])
        chatbot = gr.Chatbot()
        with gr.Row():
            with gr.Column(min_width=50, scale=1):
                chat_empty_btn = gr.Button("🧹", variant="secondary")
            with gr.Column(scale=12):
                chat_input = gr.Textbox(show_label=False, placeholder="Type here...").style(container=False)
            with gr.Column(min_width=50, scale=1):
                chat_submit_btn = gr.Button("🚀", variant="primary")
        suggested_user_turns = gr.Dropdown(choices=[], label="Suggested User Turns")


    with gr.Tab("Construct"):
        with gr.Row():
            with gr.Column():
                upload_file = gr.File()
                with gr.Row():
                    max_input_size = gr.Slider(256, 4096, 4096, step=1, label="Max Input Size", interactive=True, show_label=True)
                    num_outputs = gr.Slider(256, 4096, 512, step=1, label="Num Outputs", interactive=True, show_label=True)
                with gr.Row():
                    max_chunk_overlap = gr.Slider(0, 100, 20, step=1, label="Max Chunk Overlap", interactive=True, show_label=True)
                    chunk_size_limit = gr.Slider(256, 4096, 512, step=1, label="Chunk Size Limit", interactive=True, show_label=True)
                new_index_name = gr.Textbox(placeholder="New Index Name", show_label=False).style(container=False)
                construct_btn = gr.Button("Construct", variant="primary")
            with gr.Row():
                with gr.Column():
                    with gr.Row():
                        with gr.Column(scale=7):
                            json_select = gr.Dropdown(choices=refresh_json_list(plain=True), show_label=False, multiselect=False).style(container=False)
                        with gr.Column(scale=1):
                            json_refresh_btn = gr.Button("🔄Refresh Index List")
                    json_confirm_btn = gr.Button("🔎View json")
                    json_display = gr.JSON(label="View index json")

    index_refresh_btn.click(refresh_json_list, None, [index_select])
    query_btn.click(ask_ai, [api_key, index_select, query_box, prompt_tmpl], [answer])
    chat_input.submit(chat_ai, [api_key, index_select, chat_input, prompt_tmpl, chat_tone, chat_context, chatbot, search_options_checkbox, suggested_user_turns], [chat_context, chatbot, suggested_user_turns])
    chat_input.submit(reset_textbox, [], [chat_input])
    chat_submit_btn.click(chat_ai, [api_key, index_select, chat_input, prompt_tmpl, chat_tone, chat_context, chatbot, search_options_checkbox, suggested_user_turns], [chat_context, chatbot, suggested_user_turns])
    chat_submit_btn.click(reset_textbox, [], [chat_input])
    chat_empty_btn.click(lambda: ([], []), None, [chat_context, chatbot])
    construct_btn.click(construct_index, [api_key, upload_file, new_index_name, max_input_size, num_outputs, max_chunk_overlap], [index_select, json_select])
    json_confirm_btn.click(display_json, [json_select], [json_display])

if __name__ == '__main__':
    llama_difu.queue().launch()
