# 儿童语音读物生成器

输入儿童题材，AI 自动创作故事并生成语音读物。

## 功能

- **故事生成**：基于 OpenAI API，根据输入题材自动创作适合儿童的故事
- **语音合成**：使用 Edge TTS 将故事转为自然流畅的中文语音
- **多种声音**：支持多种适合儿童故事的朗读声音
- **年龄分级**：支持 3-6 岁、7-9 岁、10-12 岁三个年龄段
- **故事编辑**：生成后可编辑故事内容，重新合成语音
- **音频下载**：支持下载生成的 MP3 音频文件

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，填入你的 OpenAI API Key
```

### 3. 启动应用

```bash
python app.py
```

访问 http://localhost:5000 即可使用。

## 技术栈

- **后端**：Flask + OpenAI API + Edge TTS
- **前端**：HTML/CSS/JavaScript（原生，无框架依赖）
- **语音引擎**：Microsoft Edge TTS（免费，无需额外 API Key）

## 项目结构

```
├── app.py                  # Flask 主应用
├── backend/
│   ├── story_generator.py  # AI 故事生成模块
│   └── tts_engine.py       # 语音合成模块
├── frontend/
│   ├── templates/
│   │   └── index.html      # 主页面模板
│   └── static/
│       ├── css/style.css   # 样式
│       └── js/app.js       # 前端逻辑
├── requirements.txt        # Python 依赖
└── .env.example            # 环境变量示例
```

## 环境变量

| 变量 | 必填 | 说明 |
|------|------|------|
| `OPENAI_API_KEY` | 是 | OpenAI API 密钥 |
| `OPENAI_BASE_URL` | 否 | 自定义 API 地址（兼容接口） |
| `OPENAI_MODEL` | 否 | 模型名称，默认 `gpt-4o-mini` |
| `TTS_VOICE` | 否 | 默认语音，默认 `zh-CN-XiaoxiaoNeural` |
| `PORT` | 否 | 服务端口，默认 `5000` |
