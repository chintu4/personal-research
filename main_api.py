from fastapi import FastAPI, UploadFile, File, Form, Request
from typing import List
from src.preprocessing.preprocessing import extract_text_from_file, clean_text
from src.summarization.summarization import summarize_texts
from src.knowledge_graph.knowledge_graph import build_concept_graph
from src.qa.qa import simple_qa
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.integrations.gemini import have_gemini, gemini_summarize, gemini_answer
from fastapi.responses import RedirectResponse
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="web/static"), name="static")
templates = Jinja2Templates(directory="web/templates")

@app.get("/")
def read_root():
    return RedirectResponse(url="/ui")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/ui")
def ui(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/status")
def status():
    key_set = bool(os.getenv("GEMINI_API_KEY"))
    gemini_active = have_gemini()
    return {
        "gemini": {
            "key_set": key_set,
            "active": gemini_active,
            "used_for": {
                "summarize": "gemini" if gemini_active else "local_stub",
                "qa": "gemini" if gemini_active else "local_stub",
            },
        },
    }

@app.post("/summarize/")
async def summarize(files: List[UploadFile] = File(...)):
    texts: List[str] = []
    for f in files:
        data = await f.read()
        txt = extract_text_from_file(data, f.filename)
        texts.append(clean_text(txt))
    if have_gemini():
        try:
            summary = gemini_summarize(texts)
        except Exception:
            summary = summarize_texts(texts)
    else:
        summary = summarize_texts(texts)
    return {"summary": summary}

@app.post("/knowledge-graph/")
async def build_knowledge_graph(files: List[UploadFile] = File(...)):
    texts: List[str] = []
    for f in files:
        data = await f.read()
        txt = extract_text_from_file(data, f.filename)
        texts.append(clean_text(txt))
    graph = build_concept_graph(texts)
    return graph

@app.post("/qa/")
async def answer_question(question: str = Form(...), files: List[UploadFile] = File(...)):
    texts: List[str] = []
    for f in files:
        data = await f.read()
        txt = extract_text_from_file(data, f.filename)
        texts.append(clean_text(txt))
    if have_gemini():
        try:
            ans, score = gemini_answer(question, texts)
        except Exception:
            ans, score = simple_qa(question, texts)
    else:
        ans, score = simple_qa(question, texts)
    return {"question": question, "answer": ans, "score": score}
