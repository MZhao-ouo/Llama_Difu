<div align="right">
  <!-- Language: -->
  <a title="Chinese" href="README.md">简体中文</a> | English
</div>

# Llama_difu —— Llama Do it for You

[![LICENSE](https://img.shields.io/github/license/MZhao-ouo/Llama_difu)](https://github.com/MZhao-ouo/Llama_difu/blob/main/LICENSE)
[![Web-UI](https://img.shields.io/badge/WebUI-Gradio-fb7d1a?style=flat)](https://gradio.app/)
[![base](https://img.shields.io/badge/Base-Llama_index-cdc4d6?style=flat&logo=github)](https://github.com/jerryjliu/gpt_index)

---

A Web-UI for [Llama_index](https://github.com/jerryjliu/gpt_index) (gpt_index). Allow ChatGPT to access your own content, even databases!

![演示视频](https://user-images.githubusercontent.com/70903329/225239555-a29fa01b-e7ba-4041-bbce-187ac3f7d333.gif)

## Feature

## Features

- [X] Allow ChatGPT to access your own databases
- [X] New Google: Like New Bing, but using Google!
- [X] More convenient and advanced index building
- [X] Customizable Prompt templates
- [X] Multi-file support (and support for different formats)
- [ ] More LLMPredictor

## Usage

**Clone this repo**

```bash
git clone https://github.com/MZhao-ouo/Llama_difu.git
cd Llama_difu
```

**Install dependencies**

```bash
pip install -r requirements.txt
```

**Run**

```bash
python main.py
```

**(Optional) default api-key**

Create  `args.json` :

```json
{
    "api-key": "",
    "host": "127.0.0.1",
    "port": 7860,
    "share": false
}
```
