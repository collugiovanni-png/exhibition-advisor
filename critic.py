import hashlib

# Repertorio di riflessioni dialettiche anni '60-'70
# Termini chiave: dialettica, alienazione, struttura, semantica, scarto, dispositivo, fenomenico.

CRITICAL_TEMPLATES = {
    "consensus": [
        "Siamo di fronte a una inquietante convergenza di pareri che rivela l'appiattimento dialettico del sistema dell'arte.",
        "La coincidenza di vedute tra le fonti segnala una sospetta assenza di frizione critica, un'omologazione del gusto che puzza di ideologia.",
        "Il consenso unanime di queste testate è il sintomo lampante di una 'repressive tolerance' che neutralizza ogni scarto inventivo.",
        "Questa aderenza strutturale tra i testi tradisce l'assenza di un vero interrogativo fenomenico: l'evento è già consumato."
    ],
    "collision": [
        "L'attrito semantico tra queste visioni discordanti è l'unico sussulto vitale in un'operazione altrimenti sterile.",
        "Nello scarto tra queste interpretazioni si intravede la frattura tra l'ideologia curatoriale e il dato fenomenico reale.",
        "Questa collisione di prospettive rompe il soliloquio del potere culturale, aprendo uno spiraglio di autentica contraddizione.",
        "Il conflitto tra le recensioni testimonia che il dispositivo della mostra non ha ancora del tutto alienato il fruitore."
    ],
    "isolation": [
        "Un soliloquio che fatica a farsi discorso collettivo, restando prigioniero dell'autoreferenzialità.",
        "L'assenza di un coro di voci intorno a questo evento ne sottolinea la natura di 'non-accadimento' strutturale: una bolla privata.",
        "Isolata nel suo silenzio critico, questa proposta sembra non riuscire a innescare alcun processo dialettico con la realtà.",
        "Senza il confronto con l'altro da sé, l'operazione artistica si svuota di ogni carica sovversiva, degradandosi a feticismo.",
        "Una monade che si specchia nella propria estetica, ignorando la complessità del tessuto sociale circostante.",
        "Questo isolamento mediatico è forse il segno di una radicalità incompresa o, più probabilmente, di una fatuità congenita."
    ]
}

CRITICAL_SUFFIXES = {
    "isolation": [
        "Il nostro sguardo, imbevuto di un rigore forse anacronistico, preferisce sospendere il giudizio.",
        "Restiamo in attesa che il tempo, questo grande setaccio della storia, faccia il suo lavoro.",
        "Un silenzio che parla più di mille comunicati stampa pre-confezionati.",
        "Ci limitiamo a osservare questa deriva, con la pazienza di chi ha già visto tutto.",
        "Un fenomeno che non merita lo sforzo di una smentita, ma solo il peso del disinteresse."
    ],
    "consensus": [
        "Ma è davvero possibile una tale aderenza strutturale? Noi ne dubitiamo con spocchiosa fermezza.",
        "Dietro questa cortina di fumo entusiasta intravediamo il vuoto di un'epoca senza padri.",
        "Un trionfo del banale che si veste da capolavoro per rassicurare il pubblico borghese.",
        "Il coro è perfetto, ma la melodia è del tutto assente.",
        "Dov'è il dissenso? Dov'è la vita? Qui c'è solo l'anestesia del consenso."
    ],
    "collision": [
        "Nel gioco di specchi dell'industria culturale, questo scontro è l'unica verità possibile.",
        "Queste fratture sono l'humus su cui potrebbe rifiorire una vera coscienza critica.",
        "Godiamoci questa dissonanza, prima che il mercato la riassorba nel suo grigiore.",
        "Un momento di verità in un oceano di mistificazioni.",
        "La dialettica vive ancora, nonostante gli sforzi della critica istituzionale per ucciderla."
    ]
}

def generate_intellectual_synthesis(cluster):
    """
    Genera una sintesi critica 'intellettuale' basata sulle fonti nel cluster.
    Usa un approccio deterministico basato sulla composizione delle fonti.
    """
    num_sources = len(cluster)
    
    # Crea un seme stabile per la scelta del template basato sui titoli
    seed_text = "".join(sorted([e["title"] for e in cluster]))
    hash_val = int(hashlib.md5(seed_text.encode("utf-8")).hexdigest(), 16)
    
    if num_sources == 1:
        template = CRITICAL_TEMPLATES["isolation"][hash_val % len(CRITICAL_TEMPLATES["isolation"])]
        suffix = CRITICAL_SUFFIXES["isolation"][hash_val % len(CRITICAL_SUFFIXES["isolation"])]
        return {
            "text": f"{template} {suffix}",
            "tone": "snob"
        }
    
    # Controlla la varietà delle opinioni (basandosi sulla categoria del giudizio originale)
    categories = [e["judgment"]["category"] for e in cluster if "judgment" in e]
    unique_cats = list(set(categories))
    
    if len(unique_cats) <= 1:
        # Piattezza del consenso
        template = CRITICAL_TEMPLATES["consensus"][hash_val % len(CRITICAL_TEMPLATES["consensus"])]
        suffix = CRITICAL_SUFFIXES["consensus"][hash_val % len(CRITICAL_SUFFIXES["consensus"])]
        cat_desc = unique_cats[0] if unique_cats else "indecifrabile"
        return {
            "text": f"{template} (Verdetto di '{cat_desc}'). {suffix}",
            "tone": "iper-critico"
        }
    else:
        # Dialettica in atto
        template = CRITICAL_TEMPLATES["collision"][hash_val % len(CRITICAL_TEMPLATES["collision"])]
        suffix = CRITICAL_SUFFIXES["collision"][hash_val % len(CRITICAL_SUFFIXES["collision"])]
        conflict_desc = " e ".join(unique_cats)
        return {
            "text": f"{template} (Attrito tra {conflict_desc}). {suffix}",
            "tone": "dialettico"
        }
