from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from scraper import scrape_exhibitions, scrape_article
from analyzer import analyze_text
from tts import generate_title_audio
from clusterer import cluster_exhibitions
from critic import generate_intellectual_synthesis
from dotenv import load_dotenv
import os
import uvicorn
import hashlib

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
    
    # Primo passaggio: analizziamo ogni articolo singolarmente (per avere i badge)
    processed_items = []
    for exh in raw_exhibitions:
        analysis = analyze_text(exh.get("text", ""))
        exh.pop("text", None) # Teniamo il JSON leggero
        item = {**exh, "judgment": analysis}
        processed_items.append(item)
        
    # Secondo passaggio: Raggruppiamo per evento
    clusters = cluster_exhibitions(processed_items)
    
    final_results = []
    for cluster in clusters:
        # Generiamo la sintesi intellettuale (Anni '60-'70) per il gruppo
        synthesis = generate_intellectual_synthesis(cluster)
        
        # Usiamo il titolo della prima mostra come principale
        main_exh = cluster[0]
        title_audio = generate_title_audio(main_exh["title"])
        
        final_results.append({
            "id": hashlib.md5(main_exh["title"].encode()).hexdigest(),
            "main_title": main_exh["title"],
            "city": main_exh.get("city"),
            "title_audio_file": title_audio,
            "synthesis": synthesis,
            "articles": cluster,
            "sources_count": len(cluster)
        })
        
    return {"clusters": final_results}

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
