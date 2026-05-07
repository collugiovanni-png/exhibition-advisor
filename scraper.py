import feedparser
import requests
from bs4 import BeautifulSoup

ARTRIBUNE_FEED = "https://www.artribune.com/feed/"
EXIBART_RECENSIONI = "https://www.exibart.com/argomento/arte-contemporanea/feed/"
ATP_DIARY_FEED = "https://atpdiary.com/feed/"
SEGNO_FEED = "https://segnonline.it/feed/"

import re

def clean_html(raw_html: str) -> str:
    soup = BeautifulSoup(raw_html, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    
    # Rimuove diciture pubblicitarie/attribuzioni comuni dei feed (es. "L'articolo... proviene da...")
    patterns_to_remove = [
        r"L'articolo .* proviene da .* \.",
        r"L'articolo .* proviene da .*",
        r"proviene da segnonline \.",
        r"proviene da segnonline",
        r"proviene da atpdiary",
        r"proviene da artribune"
    ]
    
    for pattern in patterns_to_remove:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE)
    
    return text.strip()

def extract_image(entry):
    """Estrae un URL immagine da un entry di feedparser in modo robusto."""
    # 1. Cerca in media_content
    if 'media_content' in entry and len(entry.media_content) > 0:
        return entry.media_content[0]['url']
    
    # 2. Cerca in enclosures
    if 'enclosures' in entry:
        for enc in entry.enclosures:
            if enc.get('type', '').startswith('image/'):
                return enc.href
    
    # 3. Cerca in media_thumbnail
    if 'media_thumbnail' in entry and len(entry.media_thumbnail) > 0:
        return entry.media_thumbnail[0]['url']
    
    # 4. Cerca tag <img> nella descrizione o nel contenuto
    html_content = entry.get("description", "")
    if 'content' in entry:
        html_content += entry.content[0].value
        
    if html_content:
        soup = BeautifulSoup(html_content, "html.parser")
        img = soup.find("img")
        if img:
            src = img.get("src")
            if src and src.startswith("http"):
                # Filtriamo i placeholder comuni (es. blank.png, pixel.gif, etc)
                placeholders = ["blank", "spacer", "pixel", "logo", "icon", "advertisement", "spinner"]
                if not any(p in src.lower() for p in placeholders):
                    return src
            
    return None

def scrape_zero():
    cities = ["milano", "roma", "torino", "bologna", "firenze", "napoli", "venezia"]
    results = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
    
    for city in cities:
        url = f"https://zero.eu/it/{city}/eventi/mostre-in-corso/"
        try:
            req = requests.get(url, headers=headers, timeout=10)
            if req.status_code != 200:
                continue
            
            soup = BeautifulSoup(req.content, "html.parser")
            articles = soup.select("a.event-preview")
            
            count = 0
            for art in articles:
                if count >= 3:
                    break
                
                title_tag = art.find(["h3", "h4", "h2"])
                link = art.get("href")
                
                if title_tag and link:
                    title = title_tag.get_text(strip=True)
                    if link.startswith("/"):
                        link = "https://zero.eu" + link
                    
                    desc_tag = art.find("p")
                    desc = desc_tag.get_text(strip=True) if desc_tag else ""
                    
                    # Estrazione immagine da Zero.eu
                    img_tag = art.find("img")
                    image_url = img_tag.get("src") if img_tag else None
                    
                    # Filtro placeholder anche per Zero
                    if image_url:
                        placeholders = ["blank", "spacer", "pixel", "logo", "icon", "spinner"]
                        if any(p in image_url.lower() for p in placeholders):
                            image_url = None
                            
                    results.append({
                        "source": f"Zero ({city.capitalize()})",
                        "city": city.capitalize(),
                        "title": title,
                        "link": link,
                        "date": "In corso",
                        "text": f"{title} {desc}",
                        "summary": desc[:200] + "..." if len(desc) > 200 else desc,
                        "image": image_url
                    })
                    count += 1
        except Exception as e:
            print(f"Errore scraping Zero {city}: {e}")
            
    return results

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
                "city": None,
                "title": entry.title,
                "link": entry.link,
                "date": entry.get("published", ""),
                "text": full_text,
                "summary": desc[:200] + "..." if len(desc) > 200 else desc,
                "image": extract_image(entry)
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
                "city": None,
                "title": entry.title,
                "link": entry.link,
                "date": entry.get("published", ""),
                "text": full_text,
                "summary": desc[:200] + "..." if len(desc) > 200 else desc,
                "image": extract_image(entry)
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
                "city": None,
                "title": entry.title,
                "link": entry.link,
                "date": entry.get("published", ""),
                "text": full_text,
                "summary": desc[:200] + "..." if len(desc) > 200 else desc,
                "image": extract_image(entry)
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
                "city": None,
                "title": entry.title,
                "link": entry.link,
                "date": entry.get("published", ""),
                "text": full_text,
                "summary": desc[:200] + "..." if len(desc) > 200 else desc,
                "image": extract_image(entry)
            })
    except Exception as e:
        print(f"Errore scraping Segno: {e}")

    # 5. Scraping Zero.eu (Multi-città)
    try:
        zero_events = scrape_zero()
        exhibitions.extend(zero_events)
    except Exception as e:
        print(f"Errore integrazione Zero: {e}")

    return exhibitions

def scrape_article(url: str):
    """Estrae un articolo partendo da un URL specifico."""
    try:
        req = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        # Utilizziamo clean_html per pulire il testo dai pattern di attribuzione
        text = clean_html(req.content)
        
        soup = BeautifulSoup(req.content, "html.parser")
        title = soup.find("h1").get_text(strip=True) if soup.find("h1") else "Articolo"
        
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
