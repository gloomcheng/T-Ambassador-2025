# RAG Customer Service System Setup Guide

## Quick Start

### 1. Install Dependencies

```bash
npm install
```

This will install the following new packages:
- `@google/generative-ai` - Gemini AI SDK
- `pdf-parse` - PDF document parsing
- `mammoth` - Word document parsing
- `xlsx` - Excel document parsing

### 2. Configure Environment Variables

Create a `.env` file in the project root (or modify existing):

```bash
# Gemini API (Required)
GEMINI_API_KEY=your_gemini_api_key_here

# Optional: Specify models
GEMINI_MODEL=gemini-2.0-flash-exp
GEMINI_EMBEDDING_MODEL=text-embedding-004

# RAG Settings
RAG_ENABLED=true
RAG_SIMILARITY_THRESHOLD=0.7
RAG_TOP_K=3
RAG_DOCUMENTS_PATH=./data/documents

# Debug mode (shows RAG match details)
APP_DEBUG=true
```

### 3. Get Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Get API key"
3. Select or create a project
4. Copy the API key
5. Paste it in your `.env` file as `GEMINI_API_KEY`

**Free Tier**:
- 3 million tokens/day
- 60 requests/minute
- Sufficient for general customer service systems

### 4. Prepare Knowledge Base Documents

Add Q&A documents to the `data/documents/` folder:

**Option 1: Use Excel (Easiest)**
- Open Excel
- Column A for questions, Column B for answers
- First row can be headers
- Save as `.xlsx`

**Option 2: Use Text Files**
- Create a `.txt` file
- Use `Q:` and `A:` markers for Q&A pairs
- Separate with blank lines

**Option 3: Direct PDF Upload**
- Copy PDF files to the folder
- System auto-parses

See `data/documents/KNOWLEDGE_BASE_FORMAT.md` for detailed format instructions

### 5. Start Service

```bash
npm start
```

Or development mode (auto-restart):

```bash
npm run dev
```

## System Workflow

```
User Question
    ↓
RAG Search (Check Knowledge Base)
    ↓
Match Found?
    ├─ Yes → Return Answer Directly
    └─ No  → Call Gemini AI to Generate Response
```

## Environment Variables

### Gemini API Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Gemini API key (required) | - |
| `GEMINI_MODEL` | Conversation generation model | `gemini-2.0-flash-exp` |
| `GEMINI_EMBEDDING_MODEL` | Vectorization model | `text-embedding-004` |
| `GEMINI_TIMEOUT` | API timeout (ms) | `9000` |

### RAG Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `RAG_ENABLED` | Enable RAG | `false` |
| `RAG_SIMILARITY_THRESHOLD` | Similarity threshold (0-1) | `0.7` |
| `RAG_TOP_K` | Number of results to return | `3` |
| `RAG_DOCUMENTS_PATH` | Documents folder path | `./data/documents` |

### Similarity Threshold Adjustment Guide

- **0.9+**: Very strict, only almost exact matches
- **0.7-0.9**: Recommended, balances accuracy and coverage
- **0.5-0.7**: Looser, may answer less relevant questions
- **Below 0.5**: Not recommended, prone to incorrect answers

## Updating Knowledge Base

### Add or Modify Documents

1. Edit files in `data/documents/`
2. Save files
3. Restart service

### Check Loading Status

On startup, you'll see:

```
Initializing RAG system...
Loading document: sample_qa.txt
Generating embeddings for 6 questions...
RAG system initialized with 6 documents
```

### Debug Mode

Set `APP_DEBUG=true`, when RAG finds an answer it will display:

```
RAG match found (similarity: 0.852)
Q: What are your business hours?
A: Our business hours are Monday to Friday, 9:00 AM to 6:00 PM
```

## Common Issues

### Q: Why isn't the knowledge base being used?

**Possible Reasons**:
1. `RAG_ENABLED` not set to `true`
2. Missing `GEMINI_API_KEY`
3. Similarity below threshold
4. Incorrect document format

**Solutions**:
- Enable `APP_DEBUG=true` for detailed info
- Lower `RAG_SIMILARITY_THRESHOLD`
- Check document format

### Q: Can I use only OpenAI without Gemini?

Yes. If `GEMINI_API_KEY` is not set, system falls back to OpenAI API. However, RAG functionality requires Gemini embedding API.

### Q: Is there a limit to knowledge base document count?

Recommended: no more than 1000 Q&A pairs. More may affect startup speed and memory usage.

### Q: Can knowledge base be updated in real-time?

Currently requires service restart. Hot reload feature may be added in future.

### Q: What languages are supported?

Supports all languages supported by Gemini embedding, including Traditional Chinese, Simplified Chinese, English, Japanese, etc.

## Cost Estimation

### Gemini Free Tier

- 3 million tokens/day
- 60 requests/minute

### Actual Usage Estimate

Assuming 1000 conversations per day:
- Average 500 tokens per conversation
- Total: 500K tokens/day
- **Conclusion**: Free tier is more than sufficient

### Paid Plans

Beyond free tier:
- Input: $0.075 / 1M tokens
- Output: $0.30 / 1M tokens
- Embedding: $0.00001 / 1K tokens

About 70% cheaper than OpenAI GPT-3.5

## Technical Architecture

```
services/
  ├── gemini.js          # Gemini API integration
  ├── rag.js             # RAG core logic
  └── openai.js          # OpenAI API (keeps DALL-E/Whisper)

data/
  └── documents/         # Knowledge base documents folder
      ├── sample_qa.txt
      └── 使用說明.md

app/handlers/
  └── talk.js           # Conversation handler with RAG integration
```

## Advanced Features (Future Plans)

- [ ] Hot reload knowledge base (no restart needed)
- [ ] LINE document upload functionality
- [ ] Knowledge base management interface
- [ ] Multi-language knowledge bases
- [ ] Conversation quality scoring
- [ ] Auto-learn new Q&A pairs
