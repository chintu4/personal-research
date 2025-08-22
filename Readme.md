
# Personal Research Assistant

An AI-powered personal assistant for researchers and students. This system ingests PDFs, research papers, and handwritten notes, then auto-summarizes, generates concept maps, builds knowledge graphs, and answers domain-specific queries using advanced NLP, IR, graph theory, and multimodal AI techniques.

## Features
- Ingest and preprocess documents (PDFs, research papers, handwritten notes)
- Summarize content using transformer-based LLMs
- Generate concept maps and knowledge graphs
- Answer domain-specific questions
- Multimodal support (OCR for handwriting, image captioning)
- FastAPI-based backend for easy cloud deployment

## Getting Started
1. Install requirements: `pip install -r requirements.txt`
2. Run the API: `uvicorn main_api:app --reload`
3. Access endpoints for summarization, knowledge graph, and QA

## Folder Structure
- `src/` - Source code modules
- `data/` - Input data
- `models/` - Model files
- `outputs/` - Results and outputs
- `notebooks/` - Experiments and research
- `scripts/` - Utility scripts

---
Customize and extend as your personal research assistant!
