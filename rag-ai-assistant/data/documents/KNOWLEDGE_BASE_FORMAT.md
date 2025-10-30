# RAG Knowledge Base Usage Guide

## Overview

This folder is used to store customer service knowledge base documents. The system automatically scans all documents in this folder during startup and builds a Q&A knowledge base.

## Supported File Formats

### 1. Text Files (.txt) or Word Documents (.docx)

Use `Q:` and `A:` markers for Q&A pairs:

```
Q: What are your business hours?
A: Our business hours are Monday to Friday, 9:00 AM to 6:00 PM

Q: How to contact customer service?
A: You can call our customer service hotline: 0800-123-456

---

Q: What is your return policy?
A: Returns are accepted within 7 days of receipt
```

**Rules**:
- `Q:` prefix indicates a question
- `A:` prefix indicates an answer
- Use blank lines or `---` to separate different Q&A pairs
- Both English and Chinese colons (`:` or `：`) are supported

### 2. Excel Files (.xlsx or .xls)

Create a two-column table:

| Question | Answer |
|----------|--------|
| What are your business hours? | Monday to Friday 9:00-18:00 |
| How to contact customer service? | Please call 0800-123-456 |
| What is your return policy? | Returns accepted within 7 days |

**Rules**:
- Column A (first column): Questions
- Column B (second column): Answers
- First row can be headers (automatically skipped by system)
- Each row represents one Q&A pair

### 3. PDF Files (.pdf)

Simply place PDF files in this folder. The system will:
- Automatically extract text content
- Parse according to `Q:` and `A:` markers if present
- Otherwise, use the entire document content as reference material

**Suitable for**: Product manuals, policy documents, user guides, etc.

## How to Add/Update Knowledge Base

### Method 1: Using Excel (Recommended for Non-Technical Users)

1. Open Excel
2. Create a new worksheet
3. Write questions in the first column, answers in the second column
4. Save as `.xlsx` file
5. Place the file in this folder
6. Notify technical staff to restart the service

### Method 2: Using Notepad/Word

1. Open Notepad or Word
2. Write in `Q:` and `A:` format
3. Save as `.txt` or `.docx` file
4. Place the file in this folder
5. Notify technical staff to restart the service

### Method 3: Direct PDF Upload

1. Copy PDF file to this folder
2. Notify technical staff to restart the service

## Important Notes

1. **File Names**: Can use Chinese or English, filename doesn't affect functionality
2. **Multiple Files**: Multiple files can coexist, system will load all
3. **Changes Take Effect**: Service restart required after modifying files
4. **Q&A Quality**:
   - Questions should be clear and specific
   - Answers should be concise
   - Avoid overly lengthy responses
5. **Similar Questions**: Can write multiple similar questions with different phrasing, system will intelligently match

## Sample Files

The `sample_qa.txt` file in this folder is a sample that you can reference for format.

## Technical Details (For Developers)

- **Similarity Threshold**: Default 0.7 (configurable via `RAG_SIMILARITY_THRESHOLD` in `.env`)
- **Max Results**: Default 3 (configurable via `RAG_TOP_K` in `.env`)
- **Embedding Model**: Uses Gemini text-embedding-004
- **Vector Search**: Uses Cosine Similarity
