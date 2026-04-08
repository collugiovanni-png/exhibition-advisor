from difflib import SequenceMatcher

def cluster_exhibitions(exhibitions):
    """
    Raggruppa le mostre che parlano dello stesso evento basandosi sulla similarità del titolo.
    Ritorna una lista di cluster, dove ogni cluster è una lista di dizionari (articoli).
    """
    clusters = []
    processed = set()
    
    # Ordiniamo per lunghezza titolo decrescente per avere base più solida per il match
    sorted_exh = sorted(exhibitions, key=lambda x: len(x["title"]), reverse=True)
    
    for i, exh1 in enumerate(sorted_exh):
        if i in processed:
            continue
            
        current_cluster = [exh1]
        processed.add(i)
        
        for j, exh2 in enumerate(sorted_exh):
            if j in processed:
                continue
            
            # Calcolo similarità del titolo
            # Soglia del 0.6 per catturare variazioni ma non match casuali
            similarity = SequenceMatcher(None, exh1["title"].lower(), exh2["title"].lower()).ratio()
            
            if similarity > 0.6:
                current_cluster.append(exh2)
                processed.add(j)
        
        clusters.append(current_cluster)
        
    return clusters
