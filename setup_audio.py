import os

os.makedirs("static/audio", exist_ok=True)

phrases = {
    "schifezza_1.wav": "Questa mostra sarà senza dubbio una schifezza",
    "schifezza_2.wav": "Un trionfo della fuffa curatoriale. Lascia stare",
    "schifezza_3.wav": "La classica trappola pretenziosa. Evitala come la peste",
    "schifezza_4.wav": "Mi dispiace dirtelo, ma è solo fumo negli occhi",
    "schifezza_5.wav": "Meglio fissare il muro di casa tua. Almeno è gratis",
    
    "capolavoro_1.wav": "Se non vai a vederla sei un pirla",
    "capolavoro_2.wav": "Questa è la mostra dell'anno. Muovi le gambe e vacci",
    "capolavoro_3.wav": "Un evento per cui vale assolutamente la pena fare il biglietto",
    "capolavoro_4.wav": "Stai ancora leggendo? Corri a vederla prima che chiuda",
    "capolavoro_5.wav": "Pura estasi per gli occhi. Non fartela scappare per nessun motivo",
    
    "sbirciata_1.wav": "Forse potrebbe valere la pena dare una sbirciata",
    "sbirciata_2.wav": "Nulla di sconvolgente, ma se piove e non hai di meglio da fare...",
    "sbirciata_3.wav": "Mmm interessante, ma non farti troppe illusioni",
    "sbirciata_4.wav": "Passabile, dai. Entra solo se l'ingresso è libero o scontato",
    "sbirciata_5.wav": "Ha i suoi momenti, ma potresti anche dimenticartela domani"
}

for filename, text in phrases.items():
    filepath = os.path.join("static/audio", filename)
    # Ignoriamo il timeout o errori, generiamo semplicemente.
    cmd = f'say "{text}" -o {filepath} --data-format=LEF32@44100'
    os.system(cmd)

print("Generazione audio alternative completate.")
