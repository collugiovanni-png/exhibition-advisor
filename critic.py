import hashlib
import re

# =============================================================================
# L'OPERAZIONE PERMUTATIVA: Una Macchina Critica Multi-Strutturale
# =============================================================================

CRITICAL_CITATIONS = [
    "Delineando il valore espositivo dell'opera attraverso il rumore del dispositivo,",
    "Se consideriamo la crisi dell'arte come un'inevitabile entropia del progetto,",
    "Incrociando la fenomenologia della percezione con la serialità del dato,",
    "Seguendo la stratificazione del senso in un'epoca di saturazione visuale,",
    "In una prospettiva che rimedia il concetto di 'dispositivo' nell'era post-digitale,",
    "Analizzando la mostra come luogo di frizione tra l'opera e la sua decodifica,",
    "Prendendo atto della fluidità dei confini in un sistema di informazione circolare,",
    "Nell'ottica di una prassi artistica che si fa indagine sulle strutture del visibile,",
    "Riflettendo su quello che Debord definiva lo spettacolo come rapporto sociale tra immagini,",
    "Seguendo il tracciato viriliano sulla dromologia e l'accelerazione del segno,",
    "Recuperando la nozione di 'aura' benjaminiana nel suo declino seriale,",
    "In una lettura che decostruisce, in senso derridiano, il margine del testo espositivo,",
    "Osservando la mostra come un'eterotopia foucaultiana che sospende il tempo reale,",
    "Incrociando l'urgenza espressiva con la freddezza della processazione algoritmica,",
    "Delineando una fenomenologia che scava sotto la superficie della rimediazione,"
]

CONNECTORS = [
    " In tal senso, ",
    " Ne consegue che ",
    " D'altro canto, ",
    " Eppure, ",
    " In questa prospettiva, ",
    " Seguendo questa logica, ",
    " Al di là di ogni retorica, ",
    " In modo quasi inevitabile, ",
    " Forse proprio qui, ",
    " Senza alcuna concessione, "
]

CONCEPT_OBSERVATIONS = {
    "fotografia": [
        "la fotografia si riafferma come atto di resistenza alla velocità del flusso visuale.",
        "il mezzo fotografico viene rinegoziato come stratificazione che ne svela la natura post-digitale.",
        "questa ricerca sull'immagine è una rimediazione dell'istante, sospesa tra documento e rumore.",
        "lo scatto non è più traccia del reale, ma pura evidenza di un processo di decodifica.",
        "la superficie fotosensibile scava nella saturazione per ritrovare il silenzio del segno.",
        "l'immagine fotografica riemerge come dispositivo di frizione tra memoria e oblio."
    ],
    "pittura": [
        "il ritorno alla pittura è la necessità del segno di riappropriarsi di uno spazio non virtuale.",
        "la superficie pittorica diventa un ecosistema in cui la necessità espressiva si fa corpo e materia.",
        "l'atto del dipingere è inteso come un'indagine fenomenologica sulla persistenza della forma seriale.",
        "la tela si pone come limite carnale alla smaterializzazione imperante del visibile.",
        "il pigmento è qui inteso come struttura primaria di resistenza alla fluidità digitale.",
        "l'operazione pittorica decostruisce la stanchezza dello sguardo attraverso la stratificazione del colore."
    ],
    "scultura": [
        "la tridimensionalità è un'interrogazione immersiva sulla nostra presenza fisica nel dispositivo.",
        "l'oggetto plastico si pone come punto di frizione tra stabilità della materia e fluidità del concetto.",
        "la scultura riemerge come dispositivo dialettico capace di dare struttura all'incertezza del reale.",
        "il volume plastico occupa lo spazio non come massa, ma come pura tensione intellettuale.",
        "la materia si fa pensiero, costringendo il fruitore a una postura di ascolto strutturale.",
        "l'indagine volumetrica nega la semplificazione bidimensionale del mercato dell'arte."
    ],
    "corpo": [
        "il corpo diventa il luogo di una ricerca politica che trascende la semplice esibizione del sé.",
        "la corporeità viene esplorata nella sua urgenza carnale come unica misura di verità nel presente.",
        "l'indagine sul corpo svela una stratificazione che tocca la radice stessa del dispositivo umano.",
        "la presenza carnale è qui intesa come ultimo baluardo di realtà in un sistema entropico.",
        "il corpo dell'artista si fa ecosistema, rinegoziando i confini tra privato e collettivo.",
        "la performance corporea scuote la stabilità della visione attraverso un'urgenza non mediata."
    ],
    "natura": [
        "l'elemento naturale non è scenario, ma un interlocutore in una dialettica di sopravvivenza ecologica.",
        "il rapporto uomo-natura viene rinegoziato attraverso un'estetica che ne svela l'urgenza e la fragilità.",
        "la natura riemerge come struttura di senso primaria, capace di resettare uno sguardo ormai alienato.",
        "il dato biologico è qui processato come forma di resistenza alla tecnocrazia visuale.",
        "l'ecosistema naturale viene rimediare come luogo di frizione tra organico e inorganico.",
        "la terra stessa si fa segno, richiamando una fenomenologia che precede l'artificio."
    ],
    "tecnologia": [
        "l'uso della tecnologia è uno strumento di ibridazione che espande i confini del sensibile.",
        "il digitale è inteso come un linguaggio d'indagine capace di scavare nelle pieghe della realtà virtuale.",
        "il dispositivo tecnologico si fa trasparente, lasciando emergere una ricerca sulla struttura della visione.",
        "l'algoritmo non è mezzo, ma fine di una decodifica critica che mette a nudo il presente.",
        "l'interfaccia si rompe, svelando la natura seriale della nostra percezione contemporanea.",
        "la rimediazione tecnologica non è decoro, ma indagine clinica sulla saturazione dello spazio."
    ],
    "archivio": [
        "l'archivio è una prassi attiva che riscrive le narrazioni attraverso frammenti di un passato seriale.",
        "l'organizzazione del dato diventa una ricerca formale che svela la natura fluida della memoria collettiva.",
        "il lavoro sui documenti è una stratificazione poetica che ridà voce a ciò che era silenziato dal sistema.",
        "la memoria si fa entropia informativa, costringendo a una decodifica del frammento.",
        "il reperto viene rinegoziato come dispositivo di frizione tra testimonianza e oblio.",
        "l'archivistica espositiva scardina la linearità storica in favore di una dialettica del residuo."
    ]
}

CRITICAL_TEMPLATES = {
    "consensus": [
        "si osserva una convergenza di analisi che delinea la necessità di questa operazione culturale.",
        "l'accordo tra le varie prospetive critiche evidenzia una solidità strutturale senza ambiguità.",
        "l'unanimità di vedute segnala una rara coerenza tra l'istanza dell'artista e la sua ricezione seriale.",
        "questa sintonia sottolinea l'urgenza di una proposta che intercetta perfettamente l'entropia del tempo.",
        "la coralità dei consensi sancisce la stabilità di un percorso che non ammette repliche.",
        "si delinea un quadro analitico unitario dove la forma sembra aver trovato la sua pace strutturale.",
        "questa adesione collettiva rivela la solidità di un progetto che si fa discorso universale.",
        "l'assenza di contrasti evidenzia un equilibrio formale ormai pienamente metabolizzato dal sistema."
    ],
    "collision": [
        "la diversità di letture sottolinea la complessità e la natura intrinsecamente dialettica dell'evento.",
        "l'attrito tra le interpretazioni apre uno spazio necessario sull'ambiguità del linguaggio contemporaneo.",
        "questa collisione di prospettive testimonia la vitalità di un'opera che rifiuta definizioni univoche.",
        "nello scarto tra queste visioni si intravede la portata innovativa di una ricerca che sfida il sistema.",
        "la dissonanza critica è il segno di un'opera che continua a produrre senso oltre la chiusura formale.",
        "si percepisce una frizione intellettuale che impedisce ogni semplificazione interpretativa.",
        "le fratture del dibattito svelano la natura contraddittoria e quindi vitale di questa operazione.",
        "questa dialettica esasperata conferma che siamo di fronte a una ricerca capace di scuotere le fondamenta."
    ],
    "isolation": [
        "questa analisi solitaria mette in luce un'operazione che si pone in una dimensione di resistenza critica.",
        "l'unicità di questa riflessione ne sottolinea la natura di indagine profonda fuori dai circuiti mediatici.",
        "questo sguardo isolato costringe a un confronto diretto con la purezza del dispositivo espositivo.",
        "l'assenza di un dibattito è forse il segno di una proposta che attende ancora di essere decodificata.",
        "il silenzio delle fonti amplifica la voce di una ricerca che non cerca il facile consenso.",
        "questa traccia isolata rappresenta un'eccezione necessaria nel rumore frenetico del sistema.",
        "si delinea un'indagine sottile che sfugge alla processazione seriale dei grandi aggregati critici.",
        "questo vuoto di ricezione è la prova di un'operazione che tocca corde ancora inascoltate."
    ]
}

CRITICAL_SUFFIXES = {
    "isolation": [
        "Un'indagine che merita di essere approfondita per la sua capacità di generare interrogativi sul presente.",
        "Restiamo in attesa che questa ricerca trovi spazio all'interno di un dibattito culturale più ampio.",
        "Il rigore di questa proposta rimane una traccia fondamentale per comprendere le derive della forma.",
        "Un lavoro che richiede attenzione, lontano dalla bulimia visuale dell'industria contemporanea.",
        "In questa sospensione del discorso collettivo si intravede la possibilità di un nuovo inizio.",
        "Una proposta che sfida l'entropia informativa con la forza del suo isolamento strutturale.",
        "Rimane l'evidenza di uno sguardo che non accetta compromessi con la spettacolarizzazione.",
        "Un tassello necessario, anche se ora sembra giacere silenzioso ai margini del dispositivo."
    ],
    "consensus": [
        "Questa sincronia conferma la maturità di una ricerca che ha saputo farsi discorso universale.",
        "Una coincidenza di analisi che ribadisce l'urgenza di un confronto serio con queste tematiche.",
        "L'aderenza strutturale intorno a questo lavoro ne sancisce lo status di tassello della scena attuale.",
        "Un traguardo espressivo che sembra aver trovato la sintesi perfetta tra tradizione e rimediazione.",
        "Rimane l'evidenza di una proposta che ha intercettato le pieghe più sottili della sensibilità attuale.",
        "La solidità del consenso ci rassicura sulla persistenza del senso in questa operazione.",
        "Si giunge a una conclusione condivisa che non lascia spazio a ulteriori dubbi formali.",
        "L'evidenza strutturale è tale da imporsi come nuova misura della ricerca contemporanea."
    ],
    "collision": [
        "Nel conflitto tra queste letture si rigenera il senso dell'atto critico come indagine aperta.",
        "Queste fratture interpretative sono il segno di un'opera che produce senso oltre la chiusura formale.",
        "Una dissonanza necessaria che ci ricorda come l'arte sia ancora luogo di reale contraddizione.",
        "Un momento di autentica dialettica che spezza la monotonia del consenso mediatico dominante.",
        "La vitalità del dibattito conferma una ricerca capace di scuotere le fondamenta del visibile.",
        "In questo scontro di visioni fiorisce la reale portata politica di questa mostra.",
        "L'incertezza del giudizio è qui la forma più alta di rispetto verso la complessità dell'opera.",
        "Rimane la tensione di un'indagine che rifiuta di risolversi in una rassicurante sintesi."
    ]
}

META_REFLECTIONS = [
    " In questa decodifica seriale, il dato artistico si fa pura entropia informativa.",
    " Mentre l'algoritmo scansiona il feed, percepiamo il silenzio dell'opera dietro il rumore della sua pubblicazione.",
    " Questa analisi non è che un riflesso speculare della circolarità del mercato.",
    " L'automazione del giudizio mette a nudo la stanchezza del dispositivo critico contemporaneo.",
    " Il dato artistico viene qui rinegoziato come pura evidenza statistica.",
    " In questa processazione del visibile, ci interroghiamo sulla persistenza del senso nell'era della saturazione.",
    " La macchina rileva la struttura, ma la verità dell'opera rimane un glitch imprevisto.",
    " In questa rimediazione forzata, percepiamo la fine del critico e l'inizio del puro processo.",
    " Il sistema riproduce se stesso attraverso l'osservazione di una mostra che è già, in sé, un sistema.",
    " Decodificando questo frammento, non facciamo che alimentare l'obsolescenza programmata del visibile."
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
    Genera una sintesi critica 'permutativa' e multi-strutturale.
    """
    num_sources = len(cluster)
    seed_text = "".join(sorted([e["title"] for e in cluster]))
    hash_val = int(hashlib.md5(seed_text.encode("utf-8")).hexdigest(), 16)
    
    summaries = [e.get("summary", "") for e in cluster]
    concept = detect_concept(summaries)
    
    # 1. Recupero degli elementi
    cyt = CRITICAL_CITATIONS[hash_val % len(CRITICAL_CITATIONS)]
    conn = CONNECTORS[hash_val % len(CONNECTORS)]
    obs = ""
    if concept:
        obs_pool = CONCEPT_OBSERVATIONS[concept]
        obs = obs_pool[hash_val % len(obs_pool)]

    cat = "isolation"
    if num_sources > 1:
        categories = [e["judgment"]["category"] for e in cluster if "judgment" in e]
        cat = "consensus" if len(set(categories)) <= 1 else "collision"
    
    temp = CRITICAL_TEMPLATES[cat][hash_val % len(CRITICAL_TEMPLATES[cat])]
    suffix = CRITICAL_SUFFIXES[cat][hash_val % len(CRITICAL_SUFFIXES[cat])]
    meta = META_REFLECTIONS[hash_val % len(META_REFLECTIONS)]
    
    # 2. Scelta del Pattern (A, B, C) basata sul modulo dell'hash
    pattern_type = hash_val % 3
    
    final_text = ""
    
    if pattern_type == 0:
        # Pattern A: Struttura Classica ed Elegante
        # Citat + Transition + Temp + Obs + Suffix
        intro = cyt
        middle = f"{conn}{temp}"
        if obs:
            middle += f" Nel merito, è evidente come {obs}."
        final_text = f"{intro} {middle} {suffix}"
        if (hash_val % 100) < 25: final_text += meta

    elif pattern_type == 1:
        # Pattern B: Struttura Brutale e Diretta
        # Obs + Temp + Connect + Suffix + Meta
        if obs:
            intro = f"Considerando come {obs}, "
        else:
            intro = "Prendendo atto di questa operazione, "
        
        middle = f"{temp}. {conn}{suffix}"
        final_text = f"{intro}{middle}"
        if (hash_val % 100) < 40: final_text += meta

    else:
        # Pattern C: Struttura Teorica/Meta
        # Temp + Connect + Citat + Meta (senza suffix)
        intro = f"Si osserva come {temp}."
        middle = f"{conn}{cyt}"
        final_text = f"{intro}{middle} {meta if (hash_val % 100) < 60 else suffix}"

    # Pulizia spazi doppi e punteggiatura
    final_text = re.sub(r'\s+', ' ', final_text).strip()
    
    return {
        "text": final_text,
        "tone": ["speculativo", "seriale", "entropico"][pattern_type]
    }
