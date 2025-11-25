import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import pdfParse from 'pdf-parse';
import mammoth from 'mammoth';
import xlsx from 'xlsx';
import config from '../config/index.js';
import { generateEmbeddings } from './gemini.js';

/* eslint-disable no-underscore-dangle */
const filename = fileURLToPath(import.meta.url);
const dirname = path.dirname(filename);
/* eslint-enable no-underscore-dangle */

class RAGSystem {
  constructor() {
    this.documents = [];
    this.embeddings = [];
    this.isInitialized = false;
  }

  async initialize() {
    if (!config.RAG_ENABLED) {
      console.log('RAG system is disabled');
      return;
    }

    if (!config.GEMINI_API_KEY) {
      console.log('RAG system requires GEMINI_API_KEY');
      return;
    }

    try {
      console.log('Initializing RAG system...');
      await this.loadDocuments();
      this.isInitialized = true;
      console.log(`RAG system initialized with ${this.documents.length} documents`);
    } catch (error) {
      console.error('Failed to initialize RAG system:', error.message);
    }
  }

  async loadDocuments() {
    const documentsPath = path.resolve(
      path.dirname(dirname),
      config.RAG_DOCUMENTS_PATH,
    );

    if (!fs.existsSync(documentsPath)) {
      fs.mkdirSync(documentsPath, { recursive: true });
      console.log(`Created documents directory: ${documentsPath}`);
      return;
    }

    const files = fs.readdirSync(documentsPath);
    const supportedExtensions = ['.txt', '.pdf', '.docx', '.xlsx', '.xls'];

    // Filter supported files and parse them in parallel
    const supportedFiles = files.filter((file) => {
      const ext = path.extname(file).toLowerCase();
      return supportedExtensions.includes(ext);
    });

    const parsePromises = supportedFiles.map(async (file) => {
      const ext = path.extname(file).toLowerCase();
      const filePath = path.join(documentsPath, file);
      console.log(`Loading document: ${file}`);

      try {
        const qaPairs = await this.parseDocument(filePath, ext);
        return qaPairs;
      } catch (error) {
        console.error(`Error parsing ${file}:`, error.message);
        return [];
      }
    });

    const results = await Promise.all(parsePromises);
    const allQAPairs = results.flat();

    if (allQAPairs.length === 0) {
      console.log('No Q&A pairs found in documents');
      return;
    }

    this.documents = allQAPairs;

    const texts = allQAPairs.map((qa) => qa.question);
    console.log(`Generating embeddings for ${texts.length} questions...`);
    this.embeddings = await generateEmbeddings(texts);
  }

  async parseDocument(filePath, ext) {
    switch (ext) {
      case '.txt':
        return this.parseTxt(filePath);
      case '.pdf':
        return this.parsePdf(filePath);
      case '.docx':
        return this.parseDocx(filePath);
      case '.xlsx':
      case '.xls':
        return this.parseExcel(filePath);
      default:
        return [];
    }
  }

  parseTxt(filePath) {
    const content = fs.readFileSync(filePath, 'utf-8');
    return this.extractQAPairs(content);
  }

  async parsePdf(filePath) {
    const dataBuffer = fs.readFileSync(filePath);
    const data = await pdfParse(dataBuffer);
    return this.extractQAPairs(data.text);
  }

  async parseDocx(filePath) {
    const result = await mammoth.extractRawText({ path: filePath });
    return this.extractQAPairs(result.value);
  }

  // eslint-disable-next-line class-methods-use-this
  parseExcel(filePath) {
    const workbook = xlsx.readFile(filePath);
    const sheetName = workbook.SheetNames[0];
    const worksheet = workbook.Sheets[sheetName];
    const data = xlsx.utils.sheet_to_json(worksheet, { header: 1 });

    const qaPairs = [];
    let startRow = 0;

    if (data.length > 0 && data[0].length >= 2) {
      const firstRow = data[0];
      const hasHeader = firstRow.some((cell) => typeof cell === 'string'
        && (cell.includes('問') || cell.includes('答') || cell.toLowerCase().includes('question') || cell.toLowerCase().includes('answer')));

      if (hasHeader) {
        startRow = 1;
      }
    }

    for (let i = startRow; i < data.length; i += 1) {
      const row = data[i];
      if (row.length >= 2 && row[0] && row[1]) {
        qaPairs.push({
          question: String(row[0]).trim(),
          answer: String(row[1]).trim(),
          source: path.basename(filePath),
        });
      }
    }

    return qaPairs;
  }

  // eslint-disable-next-line class-methods-use-this
  extractQAPairs(text) {
    const qaPairs = [];
    const lines = text.split('\n');

    let currentQuestion = null;
    let currentAnswer = null;

    lines.forEach((item) => {
      const line = item.trim();

      if (!line || line === '---') {
        if (currentQuestion && currentAnswer) {
          qaPairs.push({
            question: currentQuestion,
            answer: currentAnswer,
          });
          currentQuestion = null;
          currentAnswer = null;
        }
        return;
      }

      if (line.match(/^Q[:：]/i)) {
        if (currentQuestion && currentAnswer) {
          qaPairs.push({
            question: currentQuestion,
            answer: currentAnswer,
          });
        }
        currentQuestion = line.replace(/^Q[:：]\s*/i, '').trim();
        currentAnswer = null;
      } else if (line.match(/^A[:：]/i)) {
        currentAnswer = line.replace(/^A[:：]\s*/i, '').trim();
      } else if (currentQuestion && !currentAnswer) {
        currentQuestion += ` ${line}`;
      } else if (currentAnswer) {
        currentAnswer += ` ${line}`;
      }
    });

    if (currentQuestion && currentAnswer) {
      qaPairs.push({
        question: currentQuestion,
        answer: currentAnswer,
      });
    }

    return qaPairs;
  }

  // eslint-disable-next-line class-methods-use-this
  cosineSimilarity(vecA, vecB) {
    const dotProduct = vecA.reduce((sum, a, i) => sum + a * vecB[i], 0);
    const magnitudeA = Math.sqrt(vecA.reduce((sum, a) => sum + a * a, 0));
    const magnitudeB = Math.sqrt(vecB.reduce((sum, b) => sum + b * b, 0));
    return dotProduct / (magnitudeA * magnitudeB);
  }

  async search(query) {
    if (!this.isInitialized || this.documents.length === 0) {
      return [];
    }

    try {
      const queryEmbedding = await generateEmbeddings([query]);
      const similarities = this.embeddings.map((embedding, index) => ({
        index,
        similarity: this.cosineSimilarity(queryEmbedding[0], embedding),
        document: this.documents[index],
      }));

      const sortedResults = similarities
        .filter((result) => result.similarity >= config.RAG_SIMILARITY_THRESHOLD)
        .sort((a, b) => b.similarity - a.similarity)
        .slice(0, config.RAG_TOP_K);

      return sortedResults;
    } catch (error) {
      console.error('Error during RAG search:', error.message);
      return [];
    }
  }
}

const ragSystem = new RAGSystem();

export default ragSystem;
