<div align="right">
  <!-- 语言: -->
  简体中文 | <a title="English" href="README_en.md">English</a>
</div>

# Llama_difu —— Llama Do it for You

[![LICENSE](https://img.shields.io/github/license/MZhao-ouo/Llama_difu)](https://github.com/MZhao-ouo/Llama_difu/blob/main/LICENSE)
[![Web-UI](https://img.shields.io/badge/WebUI-Gradio-fb7d1a?style=flat)](https://gradio.app/)
[![base](https://img.shields.io/badge/Base-Llama_index-cdc4d6?style=flat&logo=github)](https://github.com/jerryjliu/gpt_index)

---

为 [Llama_index](https://github.com/jerryjliu/gpt_index) (gpt_index)做了个便于使用的图形界面。可以让ChatGPT访问自定义的内容，甚至是数据库！

![演示视频](https://user-images.githubusercontent.com/70903329/225239555-a29fa01b-e7ba-4041-bbce-187ac3f7d333.gif)

## 特点

* [X] 允许ChatGPT访问您自己的数据库
* [X] 新谷歌：像新必应一样，但使用谷歌！
* [X] 简单查询
* [X] 简单构建索引（目前仅支持GPTSimpleVectorIndex）
  * [X] 支持 .txt，.pdf，.docx，.epub
* [X] 自定义提示模板
* [X] 自定义PromptHelper
* [X] .json视图
* [X] 聊天
* [X] 多文件支持
* [ ] 更多LLMPredictor
* [ ] 更多索引方法

## 用法

**克隆此仓库**

```bash
git clone https://github.com/MZhao-ouo/Llama_difu.git
cd Llama_difu
```

**安装依赖项**

```bash
pip install -r requirements.txt
```

**运行**

```bash
python main.py
```

**(可选) 默认API密钥**

创建 `args.json` 文件：

```json
{
    "api-key": "",
    "host": "127.0.0.1",
    "port": 7860,
    "share": false
}
```
