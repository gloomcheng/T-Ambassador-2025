# AI Customer Service Assistant with RAG

<div align="center">

[![license](https://img.shields.io/pypi/l/ansicolortags.svg)](LICENSE) [![Release](https://img.shields.io/github/release/memochou1993/gpt-ai-assistant)](https://GitHub.com/memochou1993/gpt-ai-assistant/releases/)

</div>

An AI-powered customer service chatbot with RAG (Retrieval-Augmented Generation) capabilities, integrated with LINE Messaging API. Supports multiple AI providers: OpenAI (standard & Assistant API) and Google Gemini.

## Features

- **Multiple AI Providers** - Choose from OpenAI GPT, OpenAI Assistant API, or Google Gemini
- **RAG Knowledge Base** - Automatic Q&A matching from documents (TXT/PDF/Word/Excel)
- **Flexible Architecture** - RAG works with all AI providers for hybrid intelligence
- **Cost Optimized** - 70% cheaper using Gemini (~$1-2 per 1000 conversations)
- **Free Tier** - 3M tokens/day free with Gemini API
- **Multi-format Support** - Easy knowledge base management for non-technical users
- **LINE Integration** - Seamless chatbot experience on LINE

## Quick Start

### 1. Installation

```bash
npm install
```

### 2. Choose Your AI Provider

This project supports three AI provider modes:

| Provider | Best For | Setup Complexity | Cost |
|----------|----------|-----------------|------|
| **Gemini** (Recommended) | New projects, cost-sensitive | Easy | Free tier + $0.075/1M tokens |
| **OpenAI Standard** | Existing OpenAI users | Easy | $0.50/1M tokens |
| **OpenAI Assistant** | Advanced workflows | Medium | $0.50/1M tokens + Assistant fees |

### 3. Get API Keys

**Option A: Gemini API** (Recommended):
- Visit: https://makersuite.google.com/app/apikey
- Free tier: 3M tokens/day, 60 RPM

**Option B: OpenAI API**:
- Visit: https://platform.openai.com/api-keys
- For Assistant mode, also create an Assistant at https://platform.openai.com/assistants

**LINE Messaging API** (Required):
- Visit: https://developers.line.biz/console/

### 4. Configuration

Copy `.env.example` to `.env` and configure based on your provider:

**For Gemini (Recommended)**:
```bash
# AI Provider Selection
AI_PROVIDER=gemini

# Gemini API
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.0-flash-exp

# RAG Knowledge Base
RAG_ENABLED=true
RAG_SIMILARITY_THRESHOLD=0.7
RAG_DOCUMENTS_PATH=./data/documents

# LINE Integration
LINE_CHANNEL_ACCESS_TOKEN=your_line_token
LINE_CHANNEL_SECRET=your_line_secret
```

**For OpenAI Standard**:
```bash
AI_PROVIDER=openai
OPENAI_API_KEY=your_openai_key
OPENAI_COMPLETION_MODEL=gpt-3.5-turbo

# RAG (optional)
RAG_ENABLED=true

# LINE Integration
LINE_CHANNEL_ACCESS_TOKEN=your_line_token
LINE_CHANNEL_SECRET=your_line_secret
```

**For OpenAI Assistant** (Christine Bear's contribution):
```bash
AI_PROVIDER=openai-assistant
OPENAI_API_KEY=your_openai_key
OPENAI_ASSISTANT_ID=asst_xxxxxxxxxxxxx

# RAG (optional, works with Assistant)
RAG_ENABLED=true

# LINE Integration
LINE_CHANNEL_ACCESS_TOKEN=your_line_token
LINE_CHANNEL_SECRET=your_line_secret
```

### 5. Prepare Knowledge Base

Add Q&A documents to `data/documents/`:

**Option A: Excel (Easiest for non-technical users)**

| Question | Answer |
|----------|--------|
| What are your business hours? | Mon-Fri 9:00-18:00 |
| How to contact support? | Call 0800-123-456 |

**Option B: Text File**

```
Q: What are your business hours?
A: Mon-Fri 9:00-18:00

Q: How to contact support?
A: Call 0800-123-456
```

**Option C: PDF**

Simply drop PDF files (manuals, policies) into `data/documents/`

### 6. Run

```bash
npm start
```

You should see:

```
Initializing RAG system...
Loading document: sample_qa.txt
Generating embeddings for 6 questions...
RAG system initialized with 6 documents
```

## How It Works

```
User Message → RAG Search (if enabled) → Match Found?
                                          ├─ Yes → Return Answer (Fast & Accurate)
                                          └─ No  → AI Provider Processing
                                                   ├─ openai → GPT Standard API
                                                   ├─ openai-assistant → Assistant API
                                                   └─ gemini → Gemini API
```

**RAG Priority**: When enabled, RAG searches knowledge base first. If similarity threshold is met, returns direct answer. Otherwise, falls back to selected AI provider.

## Project Structure

```
gpt-ai-assistant/
├── data/
│   └── documents/              # Knowledge base files (TXT/PDF/Word/Excel)
│       ├── sample_qa.txt
│       └── KNOWLEDGE_BASE_FORMAT.md
├── services/
│   ├── gemini.js              # Gemini API integration
│   ├── rag.js                 # RAG system
│   └── openai.js              # OpenAI API (optional)
├── .env                        # Configuration
└── .env.example               # Configuration template
```

## Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `AI_PROVIDER` | AI provider (`openai`, `openai-assistant`, `gemini`) | No | `openai` |
| `OPENAI_API_KEY` | OpenAI API key | Conditional | - |
| `OPENAI_ASSISTANT_ID` | OpenAI Assistant ID (for `openai-assistant` mode) | Conditional | - |
| `GEMINI_API_KEY` | Gemini API key (for `gemini` mode) | Conditional | - |
| `RAG_ENABLED` | Enable RAG knowledge base | No | `false` |
| `LINE_CHANNEL_ACCESS_TOKEN` | LINE token | ✅ Yes | - |
| `LINE_CHANNEL_SECRET` | LINE secret | ✅ Yes | - |
| `RAG_SIMILARITY_THRESHOLD` | Match threshold (0-1) | No | `0.7` |
| `RAG_TOP_K` | Max results | No | `3` |
| `APP_DEBUG` | Debug mode | No | `false` |

### Similarity Threshold

- `0.9` - Strict (only exact matches)
- `0.7` - Recommended (balanced)
- `0.5` - Loose (may match unrelated)

## Cost Comparison

| Service | Input | Output | Monthly (1K conversations) |
|---------|-------|--------|---------------------------|
| **Gemini 2.0 Flash** | $0.075/1M | $0.30/1M | **$1-2** |
| OpenAI GPT-3.5 | $0.50/1M | $1.50/1M | $5-10 |

**Save 70-80% with Gemini!**

## Documentation

- **Knowledge Base Format**: `data/documents/KNOWLEDGE_BASE_FORMAT.md`
- **Technical Setup**: `data/RAG_SETUP.md`
- **Configuration**: `.env.example`

## Project Evolution

This project has evolved through three major phases:

1. **Original (Memo Chou)** - OpenAI GPT standard API integration with LINE
2. **Assistant API (Christine Bear, 2024)** - Added OpenAI Assistant API support for advanced workflows
3. **RAG + Gemini (Current, 2025)** - Added RAG knowledge base system and Gemini API for cost optimization

All three modes are now available as alternatives based on your needs.

## What's New

- **2025-10-30**: Added RAG system with Gemini 2.0 Flash support and unified AI provider selection
- **2024**: Christine Bear contributed OpenAI Assistant API integration
- 2024-07-10: The `4.9` version now support `gpt-4o` OpenAI model
- 2023-05-03: The `4.6` version now support `gpt-4` OpenAI model
- 2023-03-05: The `4.1` version now support the audio message of LINE and `whisper-1` OpenAI model
- 2023-03-02: The `4.0` version now support `gpt-3.5-turbo` OpenAI model

## Original Documentation

- <a href="https://memochou1993.github.io/gpt-ai-assistant-docs/" target="_blank">中文</a>
- <a href="https://memochou1993.github.io/gpt-ai-assistant-docs/en" target="_blank">English</a>

## Credits

### Original Contributors
- [jayer95](https://github.com/jayer95) - Debugging and testing
- [kkdai](https://github.com/kkdai) - Idea of `sum` command
- [Dayu0815](https://github.com/Dayu0815) - Idea of `search` command
- [mics8128](https://github.com/mics8128) - Implementing new features
- [myh-st](https://github.com/myh-st) - Implementing new features
- [Jakevin](https://github.com/Jakevin) - Implementing new features
- [cdcd72](https://github.com/cdcd72) - Implementing new features
- [All other contributors](https://github.com/memochou1993/gpt-ai-assistant/graphs/contributors)

### RAG Version Contributors
- **Christine Bear** ([chr901122-afk](https://github.com/chr901122-afk), chr901122@gmail.com) - OpenAI Assistant API customization via [gpt-ai-assistant-custom](https://github.com/chr901122-afk/gpt-ai-assistant-custom)
- **Gloom Cheng** (gloomcheng@gmail.com) - RAG system architecture, Gemini API integration, multi-format document parsing, and comprehensive documentation

## Contact

For questions about this RAG-enabled version, please contact gloomcheng@gmail.com.

For questions about the original project, please contact memochou1993@gmail.com.

## Changelog

Detailed changes for each release are documented in the [release notes](https://github.com/memochou1993/gpt-ai-assistant/releases).

## License

[MIT](LICENSE)

This project is based on [gpt-ai-assistant](https://github.com/memochou1993/gpt-ai-assistant) by Memo Chou, with additional RAG system and Gemini API integration. The RAG implementation is inspired by [gpt-ai-assistant-custom](https://github.com/chr901122-afk/gpt-ai-assistant-custom) by Christine Bear.
