from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from scraper import scrape_exhibitions, scrape_article
from analyzer import analyze_text
from tts import generate_title_audio
from dotenv import load_dotenv
import os
import uvicorn

load_dotenv()

app = FastAPI(title="Exhibition Advisor")

# Ensure static/audio directory exists
os.makedirs("static/audio", exist_ok=True)

# Mount static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

class ArticleRequest(BaseModel):
    url: str

@app.get("/api/exhibitions")
def get_exhibitions():
    raw_exhibitions = scrape_exhibitions()
    results = []
    for exh in raw_exhibitions:
        title_audio = generate_title_audio(exh["title"])
        analysis = analyze_text(exh["text"])
        # Remove the full text to keep JSON light
        exh.pop("text", None)
        item = {**exh, "judgment": analysis}
        if title_audio:
            item["title_audio_file"] = title_audio
        results.append(item)
    return {"exhibitions": results}

@app.post("/api/analyze_url")
def analyze_url(req: ArticleRequest):
    article = scrape_article(req.url)
    if not article:
        raise HTTPException(status_code=400, detail="Cannot scrape the article")
    
    title_audio = generate_title_audio(article.get("title", "Titolo Sconosciuto"))
    analysis = analyze_text(article.get("text", ""))
    article.pop("text", None)
    item = {**article, "judgment": analysis}
    if title_audio:
        item["title_audio_file"] = title_audio
    return {"article": item}

from fastapi.responses import FileResponse
@app.get("/")
def read_root():
    return FileResponse("static/index.html")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
