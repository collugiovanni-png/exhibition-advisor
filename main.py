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
import re
import hashlib

def clean_redundant_phrase(data):
    """Pulisce ricorsivamente qualsiasi stringa contenente la frase fastidiosa."""
    if isinstance(data, str):
        # Pattern molto aggressivo che becca "singola fonte", "proviene da", "feed" etc.
        patterns = [
            r"L'informazione.*singola fonte.*feed\.?",
            r"L'informazione.*proviene.*singola fonte\.?",
            r"proviene da una singola fonte\.?",
            r"presente in una singola fonte\.?",
            r"presente nei feed\.?",
            r"L'articolo .* proviene da .*"
        ]
        text = data
        for p in patterns:
            text = re.sub(p, "", text, flags=re.IGNORECASE)
        return text.strip()
    elif isinstance(data, list):
        return [clean_redundant_phrase(item) for item in data]
    elif isinstance(data, dict):
        return {k: clean_redundant_phrase(v) for k, v in data.items()}
    return data

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
    featured_image = None
    
    image_found = False
    for cluster in clusters:
        # Cerchiamo la prima immagine valida per l'header dinamico
        if not image_found:
            for exh in cluster:
                if exh.get("image"):
                    featured_image = exh["image"]
                    image_found = True
                    break

        # Generiamo la sintesi intellettuale (Anni '60-'70) per il gruppo
        synthesis = generate_intellectual_synthesis(cluster)
        
        # Usiamo il titolo della prima mostra come principale
        main_exh = cluster[0]
        title_audio = generate_title_audio(main_exh["title"])
        
        final_results.append({
            "id": hashlib.md5(main_exh["title"].encode()).hexdigest(),
            "main_title": clean_redundant_phrase(main_exh["title"]),
            "city": main_exh.get("city"),
            "title_audio_file": title_audio,
            "synthesis": {
                "text": clean_redundant_phrase(synthesis["text"]),
                "tone": synthesis["tone"]
            },
            "articles": cluster,
            "sources_count": len(cluster)
        })
        
    return clean_redundant_phrase({
        "clusters": final_results,
        "featured_image": featured_image
    })

@app.post("/api/analyze_url")
def analyze_url(req: ArticleRequest):
    article = scrape_article(req.url)
    if not article:
        raise HTTPException(status_code=400, detail="Cannot scrape the article")
    
    # Generiamo la sintesi per il singolo articolo trattandolo come un cluster di 1
    synthesis = generate_intellectual_synthesis([article])
    
    title_audio = generate_title_audio(article.get("title", "Titolo Sconosciuto"))
    analysis = analyze_text(article.get("text", ""))
    article.pop("text", None)
    
    item = {
        **article, 
        "title": clean_redundant_phrase(article.get("title", "")),
        "judgment": analysis,
        "synthesis": {
            "text": clean_redundant_phrase(synthesis["text"]),
            "tone": synthesis["tone"]
        }
    }
    
    if title_audio:
        item["title_audio_file"] = title_audio
    return clean_redundant_phrase({"article": item})

from fastapi.responses import FileResponse
@app.get("/")
def read_root():
    return FileResponse("static/index.html")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
