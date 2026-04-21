import hashlib
import re

# Repertorio di riflessioni dialettiche che uniscono rigore del '900 e fluidità contemporanea.
# Termini chiave: dialettica, struttura, fenomenologia, immersività, ibridazione, urgenza, rimediazione.

CRITICAL_CITATIONS = [
    "Delineando quello che Benjamin definiva il valore espositivo dell'opera,",
    "Se consideriamo, in senso squisitamente Arganiano, la crisi dell'arte come progetto,",
    "Incrociando la fenomenologia della percezione con le urgenze del presente,",
    "Seguendo la riflessione di Barthes sulla stratificazione del senso,",
    "In una prospettiva che rimedia il concetto di 'estetica relazionale',",
    "Analizzando il dispositivo della mostra come luogo di frizione tra reale e digitale,",
    "Prendendo atto di quella fluidità dei confini che caratterizza la ricerca attuale,",
    "Nell'ottica di una prassi artistica che si fa indagine sulle strutture stesse del visibile,"
]

CONCEPT_OBSERVATIONS = {
    "fotografia": [
        "la fotografia si riafferma come atto di resistenza alla velocità del flusso visuale contemporaneo.",
        "il mezzo fotografico viene qui rinegoziato attraverso una stratificazione che ne svela la natura post-digitale.",
        "questa ricerca sull'immagine non è che una rimediazione dell'istante, sospesa tra documento e finzione."
    ],
    "pittura": [
        "il ritorno alla pittura non è un rifugio nel passato, ma una necessità del segno di riappropriarsi dello spazio.",
        "la superficie pittorica diventa un ecosistema di segni in cui la necessità espressiva si fa corpo e materia.",
        "l'atto del dipingere viene qui inteso come un'indagine fenomenologica sulla persistenza della forma."
    ],
    "scultura": [
        "la tridimensionalità non è solo occupazione dello spazio, ma un'interrogazione immersiva sulla nostra presenza fisica.",
        "l'oggetto plastico si pone come punto di frizione tra la stabilità della materia e la fluidità del concetto.",
        "la scultura riemerge qui come dispositivo dialettico, capace di dare struttura all'incertezza del reale."
    ],
    "corpo": [
        "il corpo diventa il luogo di una ricerca politica e identitaria che trascende la semplice performance.",
        "la corporeità viene esplorata nella sua urgenza carnale, ponendosi come unica misura di verità nel presente.",
        "l'indagine sul corpo svela una stratificazione di significati che toccano la radice stessa del dispositivo umano."
    ],
    "natura": [
        "l'elemento naturale non è più scenario, ma un interlocutore attivo in una dialettica di sopravvivenza ed ecologia.",
        "il rapporto uomo-natura viene rinegoziato attraverso un'estetica che ne svela l'urgenza e la fragilità.",
        "la natura riemerge come struttura di senso primaria, capace di resettare il nostro sguardo alienato."
    ],
    "tecnologia": [
        "l'uso della tecnologia non è mai fine a se stesso, ma uno strumento di ibridazione che espande i confini del sensibile.",
        "il digitale viene qui inteso come un nuovo linguaggio d'indagine, capace di scavare nelle pieghe della realtà virtuale.",
        "il dispositivo tecnologico si fa trasparente, lasciando emergere una ricerca che tocca la struttura stessa della visione."
    ],
    "archivio": [
        "l'archivio non è solo memoria, ma una prassi attiva che riscrive le narrazioni del presente attraverso i frammenti del passato.",
        "l'organizzazione del dato diventa qui una ricerca formale che svela la natura fluida della nostra storia collettiva.",
        "il lavoro sui documenti si trasforma in una stratificazione poetica che ridà voce a ciò che era rimasto inascoltato."
    ]
}

CRITICAL_TEMPLATES = {
    "consensus": [
        "Si osserva una convergenza di analisi che delinea chiaramente la necessità di questa operazione culturale.",
        "L'accordo tra le varie prospetive critiche evidenzia una solidità strutturale che non lascia adito a dubbi interpretativi.",
        "L'unanimità di vedute intorno a questo evento segnala una rara coerenza tra l'istanza dell'artista e la sua ricezione.",
        "Questa sintonia tra le fonti sottolinea la rilevanza e l'urgenza di una proposta che intercetta perfettamente lo spirito del tempo."
    ],
    "collision": [
        "La diversità di letture critiche sottolinea la complessità e la natura intrinsecamente dialettica di questa mostra.",
        "L'attrito tra le varie interpretazioni apre uno spazio di riflessione necessario sull'ambiguità del linguaggio contemporaneo.",
        "Questa collisione di prospettive testimonia la vitalità di un'opera che rifiuta di chiudersi in una definizione univoca.",
        "Nello scarto tra queste visioni si intravede la reale portata innovativa di una ricerca che sfida le convenzioni."
    ],
    "isolation": [
        "Questa analisi solitaria mette in luce un'operazione che si pone quasi in una dimensione di resistenza critica.",
        "L'unicità di questa riflessione ne sottolinea la natura di indagine profonda, al di fuori dei grandi circuiti mediatici.",
        "Questo sguardo isolato ci costringe a un confronto diretto e senza filtri con la purezza del dispositivo espositivo.",
        "L'assenza di un dibattito diffuso è forse il segno di una proposta che attende ancora di essere pienamente decodificata."
    ]
}

CRITICAL_SUFFIXES = {
    "isolation": [
        "Un'indagine che merita di essere approfondita per la sua capacità di generare nuovi interrogativi sul presente.",
        "Restiamo in attesa che questa ricerca trovi il giusto spazio all'interno di un dibattito culturale più ampio.",
        "Il rigore di questa proposta rimane una traccia fondamentale per comprendere le derive della forma attuale.",
        "Un lavoro che richiede pazienza e attenzione, lontano dalla bulimia visuale dell'industria contemporanea.",
        "In questa sospensione del discorso collettivo si intravede la possibilità di un nuovo inizio espressivo."
    ],
    "consensus": [
        "Questa sincronia di giudizio conferma la maturità di una ricerca che ha saputo farsi discorso universale.",
        "Una coincidenza di analisi che non fa che ribadire l'urgenza di un confronto serio con queste tematiche.",
        "L'aderenza strutturale intorno a questo lavoro ne sancisce lo status di tassello imprescindibile della scena attuale.",
        "Un traguardo espressivo che sembra aver trovato la sintesi perfetta tra tradizione e innovazione.",
        "Rimane l'evidenza di una proposta che ha saputo intercettare le pieghe più sottili della sensibilità contemporanea."
    ],
    "collision": [
        "Nel conflitto tra queste letture si rigenera il senso stesso dell'atto critico come forma di indagine aperta.",
        "Queste fratture interpretative sono il segno di un'opera che continua a produrre senso oltre la propria chiusura formale.",
        "Una dissonanza necessaria, che ci ricorda come l'arte sia ancora luogo di scontro e di reale contraddizione.",
        "Un momento di autentica dialettica che spezza la monotonia del consenso mediatico dominante.",
        "La vitalità del dibattito conferma che siamo di fronte a una ricerca capace di scuotere le fondamenta del visibile."
    ]
}

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
                
    # Restituisce il concetto con più occorrenze, o None
    sorted_concepts = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    if sorted_concepts[0][1] > 0:
        return sorted_concepts[0][0]
    return None

def generate_intellectual_synthesis(cluster):
    """
    Genera una sintesi critica 'intellettuale' basata sulle fonti nel cluster.
    Usa un approccio deterministico basato sulla composizione delle fonti.
    """
    num_sources = len(cluster)
    
    # Crea un seme stabile per la scelta del template basato sui titoli
    seed_text = "".join(sorted([e["title"] for e in cluster]))
    hash_val = int(hashlib.md5(seed_text.encode("utf-8")).hexdigest(), 16)
    
    # Rilevamento concetto se c'è un sommario
    summaries = [e.get("summary", "") for e in cluster]
    concept = detect_concept(summaries)
    
    # Costruiamo il blocco dell'osservazione sul concetto/medium
    observation = ""
    if concept:
        observations_pool = CONCEPT_OBSERVATIONS[concept]
        observation = observations_pool[hash_val % len(observations_pool)]
        observation = f" È evidente come {observation}"

    # Blocco citazione (presente al 70% per non essere troppo ripetitivo)
    citation = ""
    if (hash_val % 100) < 70:
        citation = CRITICAL_CITATIONS[hash_val % len(CRITICAL_CITATIONS)] + " "

    if num_sources == 1:
        template = CRITICAL_TEMPLATES["isolation"][hash_val % len(CRITICAL_TEMPLATES["isolation"])]
        suffix = CRITICAL_SUFFIXES["isolation"][hash_val % len(CRITICAL_SUFFIXES["isolation"])]
        return {
            "text": f"{citation}{template}{observation} {suffix}",
            "tone": "snob"
        }
    
    # Controlla la varietà delle opinioni
    categories = [e["judgment"]["category"] for e in cluster if "judgment" in e]
    unique_cats = list(set(categories))
    
    if len(unique_cats) <= 1:
        # Piattezza del consenso
        template = CRITICAL_TEMPLATES["consensus"][hash_val % len(CRITICAL_TEMPLATES["consensus"])]
        suffix = CRITICAL_SUFFIXES["consensus"][hash_val % len(CRITICAL_SUFFIXES["consensus"])]
        cat_desc = unique_cats[0] if unique_cats else "indecifrabile"
        
        # Aggiungiamo un tocco di "depth" anche qui
        middle = f" Si è giunti a una sintonia sul valore di '{cat_desc}', ma {observation.lower() if observation else 'questa unanimità rivela una robustezza strutturale'}."
        
        return {
            "text": f"{citation}{template}{middle} {suffix}",
            "tone": "iper-critico"
        }
    else:
        # Dialettica in atto
        template = CRITICAL_TEMPLATES["collision"][hash_val % len(CRITICAL_TEMPLATES["collision"])]
        suffix = CRITICAL_SUFFIXES["collision"][hash_val % len(CRITICAL_SUFFIXES["collision"])]
        conflict_desc = " e ".join(unique_cats)
        
        middle = f" Nello scontro tra {conflict_desc} emerge come {observation.lower() if observation else 'la dialettica stessa sia il cuore della ricerca'}."
        
        return {
            "text": f"{citation}{template}{middle} {suffix}",
            "tone": "dialettico"
        }
