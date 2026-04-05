# Exhibition Advisor

Un'applicazione per valutare con tono di voce spietato e perentorio le mostre d'arte contemporanea. L'applicazione preleva articoli da diversi feed RSS (Artribune, Exibart, ATP Diary, Segno), ne analizza il contenuto e assegna loro un giudizio critico utilizzando un sistema di valutazione e sintesi vocale.

## Prerequisiti

Assicurati di avere Python 3.9 o superiore installato sul tuo sistema.

## Installazione

1. Crea e attiva un Virtual Environment (consigliato):
   ```bash
   python -m venv venv
   # Su Mac/Linux:
   source venv/bin/activate
   # Su Windows (Command Prompt):
   venv\Scripts\activate
   ```

2. Installa le dipendenze fornite nel file `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

## Esecuzione

Per avviare l'applicazione, utilizza il server Uvicorn fornito:

```bash
python main.py
```
*(Oppure `uvicorn main:app --reload`)*

L'applicazione sarà disponibile all'indirizzo: **http://localhost:8000**

## Funzionamento e Architettura
- **Scraping**: `scraper.py` analizza i feed o gli URL diretti alla ricerca di testi di mostre.
- **Analisi**: `analyzer.py` definisce quale giuzidio (Schifezza, Capolavoro, Sbirciata) assegnare interpretando le keyword del testo dell'articolo.
- **Frontend / Audio**: L'UI, sviluppata in HTML/CSS/JS moderni, esegue in background le presentazioni audio generate e vi applica bilanciamenti dinamici sfruttando le librerie Web Audio API del browser. Le tracce pre-generate risiedono in `static/audio/`.
