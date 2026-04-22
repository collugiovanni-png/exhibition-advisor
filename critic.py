import hashlib
import re

# Repertorio di riflessioni dialettiche e meta-consapevoli.
# Unione di rigore del '900, rimediazione contemporanea e consapevolezza algoritmica.

CRITICAL_CITATIONS = [
    "Delineando il valore espositivo dell'opera attraverso il rumore del dispositivo,",
    "Se consideriamo la crisi dell'arte come un'inevitabile entropia del progetto,",
    "Incrociando la fenomenologia della percezione con la serialità del dato,",
    "Seguendo la stratificazione del senso in un'epoca di saturazione visuale,",
    "In una prospettiva che rimedia il concetto di 'dispositivo' nell'era post-digitale,",
    "Analizzando la mostra come luogo di frizione tra l'opera e la sua decodifica,",
    "Prendendo atto della fluidità dei confini in un sistema di informazione circolare,",
    "Nell'ottica di una prassi artistica che si fa indagine sulle strutture del visibile,"
]

CONCEPT_OBSERVATIONS = {
    "fotografia": [
        "la fotografia si riafferma come atto di resistenza alla velocità del flusso visuale.",
        "il mezzo fotografico viene rinegoziato come stratificazione che ne svela la natura post-digitale.",
        "questa ricerca sull'immagine è una rimediazione dell'istante, sospesa tra documento e rumore."
    ],
    "pittura": [
        "il ritorno alla pittura è la necessità del segno di riappropriarsi di uno spazio non virtuale.",
        "la superficie pittorica diventa un ecosistema in cui la necessità espressiva si fa corpo e materia.",
        "l'atto del dipingere è inteso come un'indagine fenomenologica sulla persistenza della forma seriale."
    ],
    "scultura": [
        "la tridimensionalità è un'interrogazione immersiva sulla nostra presenza fisica nel dispositivo.",
        "l'oggetto plastico si pone come punto di frizione tra stabilità della materia e fluidità del concetto.",
        "la scultura riemerge come dispositivo dialettico capace di dare struttura all'incertezza del reale."
    ],
    "corpo": [
        "il corpo diventa il luogo di una ricerca politica che trascende la semplice esibizione del sé.",
        "la corporeità viene esplorata nella sua urgenza carnale come unica misura di verità nel presente.",
        "l'indagine sul corpo svela una stratificazione che tocca la radice stessa del dispositivo umano."
    ],
    "natura": [
        "l'elemento naturale non è scenario, ma un interlocutore in una dialettica di sopravvivenza ecologica.",
        "il rapporto uomo-natura viene rinegoziato attraverso un'estetica che ne svela l'urgenza e la fragilità.",
        "la natura riemerge come struttura di senso primaria, capace di resettare uno sguardo ormai alienato."
    ],
    "tecnologia": [
        "l'uso della tecnologia è uno strumento di ibridazione che espande i confini del sensibile.",
        "il digitale è inteso come un linguaggio d'indagine capace di scavare nelle pieghe della realtà virtuale.",
        "il dispositivo tecnologico si fa trasparente, lasciando emergere una ricerca sulla struttura della visione."
    ],
    "archivio": [
        "l'archivio è una prassi attiva che riscrive le narrazioni attraverso frammenti di un passato seriale.",
        "l'organizzazione del dato diventa una ricerca formale che svela la natura fluida della memoria collettiva.",
        "il lavoro sui documenti è una stratificazione poetica che ridà voce a ciò che era silenziato dal sistema."
    ]
}

CRITICAL_TEMPLATES = {
    "consensus": [
        "Si osserva una convergenza di analisi che delinea la necessità di questa operazione culturale.",
        "L'accordo tra le varie prospetive critiche evidenzia una solidità strutturale senza ambiguità.",
        "L'unanimità di vedute segnala una rara coerenza tra l'istanza dell'artista e la sua ricezione seriale.",
        "Questa sintonia sottolinea l'urgenza di una proposta che intercetta perfettamente l'entropia del tempo."
    ],
    "collision": [
        "La diversità di letture sottolinea la complessità e la natura intrinsecamente dialettica dell'evento.",
        "L'attrito tra le interpretazioni apre uno spazio necessario sull'ambiguità del linguaggio contemporaneo.",
        "Questa collisione di prospettive testimonia la vitalità di un'opera che rifiuta definizioni univoche.",
        "Nello scarto tra queste visioni si intravede la portata innovativa di una ricerca che sfida il sistema."
    ],
    "isolation": [
        "Questa analisi solitaria mette in luce un'operazione che si pone in una dimensione di resistenza critica.",
        "L'unicità di questa riflessione ne sottolinea la natura di indagine profonda fuori dai circuiti mediatici.",
        "Questo sguardo isolato costringe a un confronto diretto con la purezza del dispositivo espositivo.",
        "L'assenza di un dibattito è forse il segno di una proposta che attende ancora di essere decodificata."
    ]
}

CRITICAL_SUFFIXES = {
    "isolation": [
        "Un'indagine che merita di essere approfondita per la sua capacità di generare interrogativi sul presente.",
        "Restiamo in attesa che questa ricerca trovi spazio all'interno di un dibattito culturale più ampio.",
        "Il rigore di questa proposta rimane una traccia fondamentale per comprendere le derive della forma.",
        "Un lavoro che richiede attenzione, lontano dalla bulimia visuale dell'industria contemporanea.",
        "In questa sospensione del discorso collettivo si intravede la possibilità di un nuovo inizio."
    ],
    "consensus": [
        "Questa sincronia conferma la maturità di una ricerca che ha saputo farsi discorso universale.",
        "Una coincidenza di analisi che ribadisce l'urgenza di un confronto serio con queste tematiche.",
        "L'aderenza strutturale intorno a questo lavoro ne sancisce lo status di tassello della scena attuale.",
        "Un traguardo espressivo che sembra aver trovato la sintesi perfetta tra tradizione e rimediazione.",
        "Rimane l'evidenza di una proposta che ha intercettato le pieghe più sottili della sensibilità attuale."
    ],
    "collision": [
        "Nel conflitto tra queste letture si rigenera il senso dell'atto critico come indagine aperta.",
        "Queste fratture interpretative sono il segno di un'opera che produce senso oltre la chiusura formale.",
        "Una dissonanza necessaria che ci ricorda come l'arte sia ancora luogo di reale contraddizione.",
        "Un momento di autentica dialettica che spezza la monotonia del consenso mediatico dominante.",
        "La vitalità del dibattito conferma una ricerca capace di scuotere le fondamenta del visibile."
    ]
}

META_REFLECTIONS = [
    " In questa decodifica seriale, il dato artistico si fa pura entropia informativa.",
    " Mentre l'algoritmo scansiona il feed, percepiamo il silenzio dell'opera dietro il rumore della sua pubblicazione.",
    " Questa analisi non è che un riflesso speculare della circolarità del mercato.",
    " L'automazione del giudizio mette a nudo la stanchezza del dispositivo critico contemporaneo.",
    " Il dato artistico viene qui rinegoziato come pura evidenza statistica.",
    " In questa processazione del visibile, ci interroghiamo sulla persistenza del senso nell'era della saturazione.",
    " La macchina rileva la struttura, ma la verità dell'opera rimane un glitch imprevisto."
]

def detect_concept(text_list):
    """Trova il concetto predominante in una lista di testi."""
    combined_text = " ".join(text_list).lower()
    scores = {concept: 0 for concept in CONCEPT_OBSERVATIONS}
    
    keywords = {
        "fotografia": ["foto", "fotograf", "immagine", "scatto"],
        "pittura": ["pittur", "pinto", "tela", "colore", "olio", "pennello"],
        "scultura": ["scultur", "marmo", "bronzo", "volume", "materia", "plastico"],
        "corpo": ["corpo", "body", "carne", "performance", "gesto", "identità"],
        "natura": ["natura", "paesaggio", "ecologia", "ambiente", "piant", "terra"],
        "tecnologia": ["tecnolog", "digital", "video", "computer", "algoritmo", "schermo"],
        "archivio": ["archivio", "documento", "memoria", "storia", "passato"]
    }
    
    for concept, words in keywords.items():
        for word in words:
            if word in combined_text:
                scores[concept] += 1
                
    sorted_concepts = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    if sorted_concepts[0][1] > 0:
        return sorted_concepts[0][0]
    return None

def generate_intellectual_synthesis(cluster):
    """
    Genera una sintesi critica 'consapevole' (Meta-Machine).
    """
    num_sources = len(cluster)
    seed_text = "".join(sorted([e["title"] for e in cluster]))
    hash_val = int(hashlib.md5(seed_text.encode("utf-8")).hexdigest(), 16)
    
    summaries = [e.get("summary", "") for e in cluster]
    concept = detect_concept(summaries)
    
    observation = ""
    if concept:
        observations_pool = CONCEPT_OBSERVATIONS[concept]
        observation = observations_pool[hash_val % len(observations_pool)]
        observation = f" È evidente come {observation}"

    citation = ""
    if (hash_val % 100) < 70:
        citation = CRITICAL_CITATIONS[hash_val % len(CRITICAL_CITATIONS)] + " "

    # Meta-Riflessione (25% di probabilità)
    meta = ""
    if (hash_val % 100) < 25:
        meta = META_REFLECTIONS[hash_val % len(META_REFLECTIONS)]

    if num_sources == 1:
        template = CRITICAL_TEMPLATES["isolation"][hash_val % len(CRITICAL_TEMPLATES["isolation"])]
        suffix = CRITICAL_SUFFIXES["isolation"][hash_val % len(CRITICAL_SUFFIXES["isolation"])]
        return {
            "text": f"{citation}{template}{observation} {suffix}{meta}",
            "tone": "speculativo"
        }
    
    categories = [e["judgment"]["category"] for e in cluster if "judgment" in e]
    unique_cats = list(set(categories))
    
    if len(unique_cats) <= 1:
        template = CRITICAL_TEMPLATES["consensus"][hash_val % len(CRITICAL_TEMPLATES["consensus"])]
        suffix = CRITICAL_SUFFIXES["consensus"][hash_val % len(CRITICAL_SUFFIXES["consensus"])]
        cat_desc = unique_cats[0] if unique_cats else "indecifrabile"
        middle = f" Si è giunti a una sintonia sul valore di '{cat_desc}', ma {observation.lower() if observation else 'questa unanimità rivela una robustezza strutturale'}."
        return {
            "text": f"{citation}{template}{middle} {suffix}{meta}",
            "tone": "seriale"
        }
    else:
        template = CRITICAL_TEMPLATES["collision"][hash_val % len(CRITICAL_TEMPLATES["collision"])]
        suffix = CRITICAL_SUFFIXES["collision"][hash_val % len(CRITICAL_SUFFIXES["collision"])]
        conflict_desc = " e ".join(unique_cats)
        middle = f" Nello scontro tra {conflict_desc} emerge come {observation.lower() if observation else 'la dialettica stessa sia il cuore della ricerca'}."
        return {
            "text": f"{citation}{template}{middle} {suffix}{meta}",
            "tone": "entropico"
        }
