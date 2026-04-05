import feedparser
import requests
from bs4 import BeautifulSoup

ARTRIBUNE_FEED = "https://www.artribune.com/feed/"
EXIBART_RECENSIONI = "https://www.exibart.com/argomento/arte-contemporanea/feed/"
ATP_DIARY_FEED = "https://atpdiary.com/feed/"
SEGNO_FEED = "https://segnonline.it/feed/"

def clean_html(raw_html: str) -> str:
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text(separator=" ", strip=True)

def scrape_exhibitions():
    exhibitions = []
    
    # 1. Scraping Artribune via RSS
    try:
        artribune = feedparser.parse(ARTRIBUNE_FEED)
        for entry in artribune.entries[:5]:
            desc = clean_html(entry.get("description", ""))
            content = ""
            if "content" in entry:
                content = clean_html(entry.content[0].value)
            
            full_text = f"{entry.title} {desc} {content}"
            exhibitions.append({
                "source": "Artribune",
                "title": entry.title,
                "link": entry.link,
                "date": entry.get("published", ""),
                "text": full_text,
                "summary": desc[:200] + "..." if len(desc) > 200 else desc
            })
    except Exception as e:
        print(f"Errore scraping Artribune: {e}")

    # 2. Scraping Exibart via RSS
    try:
        exibart = feedparser.parse(EXIBART_RECENSIONI)
        for entry in exibart.entries[:5]:
            desc = clean_html(entry.get("description", ""))
            content = ""
            if "content" in entry:
                content = clean_html(entry.content[0].value)
            
            full_text = f"{entry.title} {desc} {content}"
            exhibitions.append({
                "source": "Exibart",
                "title": entry.title,
                "link": entry.link,
                "date": entry.get("published", ""),
                "text": full_text,
                "summary": desc[:200] + "..." if len(desc) > 200 else desc
            })
    except Exception as e:
        print(f"Errore scraping Exibart: {e}")

    # 3. Scraping ATP Diary via RSS
    try:
        atp = feedparser.parse(ATP_DIARY_FEED)
        for entry in atp.entries[:4]:
            desc = clean_html(entry.get("description", ""))
            content = ""
            if "content" in entry:
                content = clean_html(entry.content[0].value)
            
            full_text = f"{entry.title} {desc} {content}"
            exhibitions.append({
                "source": "ATP Diary",
                "title": entry.title,
                "link": entry.link,
                "date": entry.get("published", ""),
                "text": full_text,
                "summary": desc[:200] + "..." if len(desc) > 200 else desc
            })
    except Exception as e:
        print(f"Errore scraping ATP Diary: {e}")

    # 4. Scraping Segno via RSS
    try:
        segno = feedparser.parse(SEGNO_FEED)
        for entry in segno.entries[:4]:
            desc = clean_html(entry.get("description", ""))
            content = ""
            if "content" in entry:
                content = clean_html(entry.content[0].value)
            
            full_text = f"{entry.title} {desc} {content}"
            exhibitions.append({
                "source": "Segno",
                "title": entry.title,
                "link": entry.link,
                "date": entry.get("published", ""),
                "text": full_text,
                "summary": desc[:200] + "..." if len(desc) > 200 else desc
            })
    except Exception as e:
        print(f"Errore scraping Segno: {e}")

    return exhibitions

def scrape_article(url: str):
    """Estrae un articolo partendo da un URL specifico."""
    try:
        req = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(req.content, "html.parser")
        title = soup.find("h1").get_text(strip=True) if soup.find("h1") else "Articolo"
        
        # Cerca div che di solito contengono il testo
        content_div = soup.find("div", class_="entry-content") or soup.find("article") or soup
        text = content_div.get_text(separator=" ", strip=True)
        return {
            "source": "Link Diretto",
            "title": title,
            "link": url,
            "date": "",
            "text": text,
            "summary": text[:200] + "..."
        }
    except Exception as e:
        print(f"Errore nello scraping di {url}: {e}")
        return None
