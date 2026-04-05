import hashlib
import re
import random

# Liste di parole chiave e pattern (adattate per l'arte contemporanea in italiano)
SCHIFEZZA_WORDS = [
    r"provocatori[oa]", r"già vist[oa]", r"noios[oa]", r"banale", r"superficiale",
    r"deludent[e]", r"sopravvalutat[oa]", r"pretenzios[oa]", r"esercizio di stile",
    r"commerciale", r"vuot[oa]", r"ripetitiv[oa]", r"stereotipat[oa]", r"kitsch",
    r"pacchian[oa]", r"inutil[e]", r"fredd[oa]", r"autoreferenzial[e]", r"patriarcato",
    r"brand",
    r"debol[e]", r"confus[oa]", r"incompleto", r"amatoriale", r"forzat[oa]",
    r"pretensios[oa]", r"effetto social", r"instagrammabil[e]", r"merchandising",
    r"delusione", r"atteso di più", r"non convince", r"fiacco", r"anonim[oa]",
]

CAPOLAVORO_WORDS = [
    r"imperdibil[e]", r"capolavoro", r"storic[oa]", r"genial[e]", r"unic[oa]",
    r"straordinari[oa]", r"memorabil[e]", r"rivoluzionari[oa]", r"epocal[e]",
    r"must-see", r"eccezional[e]", r"fondamental[e]", r"spettacolar[e]",
    r"retrospettiva definitiva", r"mai vist[oa] prima", r"maestos[oa]",
    r"indimenticabil[e]", r"sublim[e]", r"mozzafiato",
    r"da non perdere", r"da vedere", r"potente", r"intens[oa]", r"emozionant[e]",
    r"rigoros[oa]", r"visionari[oa]", r"esemplare", r"punto di riferimento",
    r"riuscit[oa]", r"coinvolgent[e]", r"brillant[e]", r"superbo",
]

# Parole “morbide” molto frequenti nei feed: peso ridotto per non finire sempre in sbirciata
SBIRCIATA_WORDS = [
    (r"interessant[e]", 0.6),
    (r"promettent[e]", 0.7),
    (r"curios[oa]", 0.7),
    (r"emergent[e]", 0.8),
    (r"novità", 0.7),
    (r"piacevol[e]", 0.6),
    (r"fres[ca]o", 0.7),
    (r"scoperta", 0.75),
    (r"ricerca", 0.65),
    (r"sperimentazion[e]", 0.75),
    (r"particolar[e]", 0.65),
    (r"indagin[e]", 0.75),
    (r"prospettiva", 0.65),
    (r"esplorazion[e]", 0.75),
    (r"stimolant[e]", 0.7),
    (r"original[e]", 0.75),
    (r"inconsuet[oa]", 0.8),
]

# Testi 1–5: voce Scarpa (stesso copione delle frasi base).
# Ordine delle 15 frasi inviate per Livio: schifezza 6→10, poi capolavoro 6→10, poi sbirciata 6→10.
JUDGMENTS = {
    "schifezza": [
        {"file": "schifezza_1.mp3", "text": "Questa mostra sarà senza dubbio una schifezza."},
        {"file": "schifezza_2.mp3", "text": "Un trionfo della fuffa curatoriale. Lascia stare."},
        {"file": "schifezza_3.mp3", "text": "La classica trappola pretenziosa. Evitala come la peste."},
        {"file": "schifezza_4.mp3", "text": "Mi dispiace dirtelo, ma è solo fumo negli occhi."},
        {"file": "schifezza_5.mp3", "text": "Meglio fissare il muro di casa tua. Almeno è gratis."},
        # Livio schifezza_6 … schifezza_10 (ordine = prime 5 frasi del blocco inviato)
        {"file": "schifezza_6.mp3", "text": "Questa mostra sarà senza dubbio una schifezza."},
        {"file": "schifezza_7.mp3", "text": "Un trionfo della fuffa curatoriale. Lascia stare."},
        {"file": "schifezza_8.mp3", "text": "La classica trappola pretenziosa. Evitala come la peste."},
        {"file": "schifezza_9.mp3", "text": "Mi dispiace dirtelo, ma è solo fumo negli occhi."},
        {"file": "schifezza_10.mp3", "text": "Meglio fissare il muro di casa tua. Almeno è gratis."},
    ],
    "capolavoro": [
        {"file": "capolavoro_1.mp3", "text": "Se non vai a vederla sei un pirla."},
        {"file": "capolavoro_2.mp3", "text": "Questa è la mostra dell'anno. Muovi le gambe e vacci."},
        {"file": "capolavoro_3.mp3", "text": "Un evento per cui vale assolutamente la pena fare il biglietto."},
        {"file": "capolavoro_4.mp3", "text": "Stai ancora leggendo? Corri a vederla prima che chiuda."},
        {"file": "capolavoro_5.mp3", "text": "Pura estasi per gli occhi. Non fartela scappare per nessun motivo."},
        # Livio capolavoro_6 … capolavoro_10 (ordine = successive 5 frasi)
        {"file": "capolavoro_6.mp3", "text": "Se non vai a vederla sei un pirla."},
        {"file": "capolavoro_7.mp3", "text": "Questa è la mostra dell'anno. Muovi le gambe e vacci."},
        {"file": "capolavoro_8.mp3", "text": "Un evento per cui vale assolutamente la pena fare il biglietto."},
        {"file": "capolavoro_9.mp3", "text": "Stai ancora leggendo? Corri a vederla prima che chiuda."},
        {"file": "capolavoro_10.mp3", "text": "Pura estasi per gli occhi. Non fartela scappare per nessun motivo."},
    ],
    "sbirciata": [
        {"file": "sbirciata_1.mp3", "text": "Forse potrebbe valere la pena dare una sbirciata."},
        {"file": "sbirciata_2.mp3", "text": "Nulla di sconvolgente, ma se piove e non hai di meglio da fare…"},
        {"file": "sbirciata_3.mp3", "text": "Mmm interessante, ma non farti troppe illusioni."},
        {"file": "sbirciata_4.mp3", "text": "Passabile, dai. Entra solo se l'ingresso è libero o scontato."},
        {"file": "sbirciata_5.mp3", "text": "Ha i suoi momenti, ma potresti anche dimenticartela domani."},
        # Livio sbirciata_6 … sbirciata_10 (ordine = ultime 5 frasi)
        {"file": "sbirciata_6.mp3", "text": "Forse potrebbe valere la pena dare una sbirciata."},
        {"file": "sbirciata_7.mp3", "text": "Nulla di sconvolgente, ma se piove e non hai di meglio da fare…"},
        {"file": "sbirciata_8.mp3", "text": "Mmm interessante, ma non farti troppe illusioni."},
        {"file": "sbirciata_9.mp3", "text": "Passabile, dai. Entra solo se l'ingresso è libero o scontato."},
        {"file": "sbirciata_10.mp3", "text": "Ha i suoi momenti, ma potresti anche dimenticartela domani."},
    ],
}


def _weighted_sbirciata_score(text_lower: str) -> float:
    total = 0.0
    for pattern, weight in SBIRCIATA_WORDS:
        if re.search(pattern, text_lower):
            total += weight
    return total


def _pick_judgment(category: str, text: str) -> dict:
    """Battuta stabile per lo stesso testo, distribuita tra i file MP3 disponibili."""
    entries = JUDGMENTS[category]
    idx = int(hashlib.md5(text.encode("utf-8")).hexdigest(), 16) % len(entries)
    return entries[idx]


# Virgolette tipografiche / ASCII da non mostrare come parte del giudizio
_JUDGMENT_QUOTES = frozenset('"\'\u201c\u201d\u2018\u2019«»')


def _strip_wrapping_quotes(s: str) -> str:
    """Rimuove virgolette iniziali/finali se presenti (es. da copia-incolla)."""
    t = s.strip()
    while len(t) >= 2 and t[0] in _JUDGMENT_QUOTES and t[-1] in _JUDGMENT_QUOTES:
        t = t[1:-1].strip()
    return t


def analyze_text(text: str) -> dict:
    """
    Analizza il testo della mostra ed emette un giudizio basato sulle parole chiave.
    Ritorna un dizionario con la categoria e il nome del file audio associato.
    """
    if not text:
        choice = random.choice(JUDGMENTS["sbirciata"])
        return {
            "category": "sbirciata",
            "audio_file": choice["file"],
            "judgment": _strip_wrapping_quotes(choice["text"]),
        }

    text_lower = text.lower()
    raw_schifezza = sum(1 for word in SCHIFEZZA_WORDS if re.search(word, text_lower))
    raw_capolavoro = sum(1 for word in CAPOLAVORO_WORDS if re.search(word, text_lower))
    raw_sbirciata = _weighted_sbirciata_score(text_lower)

    # Stesso articolo → stesso esito (hash), ma tra articoli diversi più varietà
    rng = random.Random(int(hashlib.md5(text.encode("utf-8")).hexdigest(), 16))

    # Nessun match: non forzare sempre sbirciata
    if raw_schifezza == 0 and raw_capolavoro == 0 and raw_sbirciata == 0:
        cat = rng.choices(
            ["schifezza", "capolavoro", "sbirciata"],
            weights=[0.28, 0.28, 0.44],
            k=1,
        )[0]
        choice = _pick_judgment(cat, text)
        return {
            "category": cat,
            "audio_file": choice["file"],
            "judgment": _strip_wrapping_quotes(choice["text"]),
        }

    score_schifezza = raw_schifezza * 1.65 + rng.uniform(0, 1.15)
    score_capolavoro = raw_capolavoro * 1.65 + rng.uniform(0, 1.15)
    score_sbirciata = raw_sbirciata * 0.85 + rng.uniform(0, 1.0)

    if score_schifezza >= score_capolavoro and score_schifezza > score_sbirciata:
        cat = "schifezza"
    elif score_capolavoro > score_schifezza and score_capolavoro > score_sbirciata:
        cat = "capolavoro"
    else:
        cat = "sbirciata"

    choice = _pick_judgment(cat, text)
    return {
        "category": cat,
        "audio_file": choice["file"],
        "judgment": _strip_wrapping_quotes(choice["text"]),
    }
