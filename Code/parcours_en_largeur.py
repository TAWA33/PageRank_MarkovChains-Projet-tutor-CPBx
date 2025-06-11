import gzip
import csv
from tqdm import tqdm
from collections import deque

#Fichiers CSV d'enregistrement de la sous-base de donnée
nodes_csv = "filtered_nodes.csv" 
edges_csv = "filtered_edges.csv"

#Fichiers GZ de la base de donnée d'origine de Common Crawl
nodes_file_path = "cc-main-2024-oct-nov-dec-domain-vertices.txt.gz"
edges_file_path = "cc-main-2024-oct-nov-dec-domain-edges.txt.gz"

#Site d'origine et Profondeur du graphe à déterminer par l'utilisateur
seed_site = "fr.u-bordeaux"
max_depth = 4

def find_id(seed_site):
    """
    Parcourt le fichier des nœuds compressé, qui répertorie les relations 'node_ID, domaine',
    et renvoie l'ID du domaine correspondant au site recherché.

    :param seed_site: Nom du domaine à rechercher
    :return: L'ID du domaine si trouvé, sinon None
    """
    with gzip.open(nodes_file_path, "rt") as f:
        for line in tqdm(f, total=98727688, desc="Exploration des nœuds"):
            line = line.strip()
            if not line: #Évite les lignes mal-formatées
                continue
            try:
                parts = line.split()
                node_id = parts[0]
                domain = parts[1]
                if domain == seed_site:
                    print(node_id)
                    return(node_id)
            except IndexError:
                continue
    return None

print(find_id(seed_site))
def bfs(start_id, max_depth):
    """
    Effectue un parcours en largeur (BFS) pour explorer le graphe jusqu'à une profondeur donnée.

    :param start_id: L'ID du nœud de départ (site central)
    :param max_depth: Profondeur maximale d'exploration
    :return: Ensemble des nœuds explorés et liste des arêtes trouvées
    """
    distances = {start_id: 0}  # Stocke les nœuds explorés et leur distance au site central
    queue = deque([start_id])  # File d'attente pour le BFS
    filtered_edges = []  # Liste des arêtes filtrées (source, cible)

    print(f"Début du BFS depuis {start_id} jusqu'à profondeur {max_depth}")

    while queue:
        current_node = queue.popleft()
        current_depth = distances[current_node]

        if current_depth >= max_depth:
            continue

        voisins=0 # Compteur du nombre de voisins traités

        with gzip.open(edges_file_path, "rt") as f:
            for line in tqdm(f, total=1753180580, desc="Exploration du graphe"):
                if not line:
                    continue
                try:
                    line=line.strip()
                    part=line.split()
                    source, target = part[0], part[1]

                    if source == current_node:
                        if target not in distances: 
                            distances[target] = current_depth + 1
                            queue.append(target)

                        print((source, target))
                        filtered_edges.append((source, target))
                        voisins+=1

                        if voisins>= 5: # Limite à 5 voisins pour éviter une explosion de la mémoire et du temps de calcul
                            break
                except ValueError:
                    continue

    print(f"Exploration terminée : {len(distances)} nœuds trouvés, {len(filtered_edges)} arêtes")
    return distances.keys(), filtered_edges


def extract_domains(node_ids):
    """Récupère les domaines de tous les nœuds trouvés."""
    domains = {}
    max_id = max(node_ids)

    with gzip.open(nodes_file_path, "rt") as f:
        for line in tqdm(f, desc="Extraction des domaines"):
            if not line:
                continue
            try:
                line=line.strip()
                part=line.split()
                node_id, domain = int(part[0]), part[1]

                if node_id > int(max_id): 
                    break # On arrête si on dépasse le plus grand ID rencontré
            
                if node_id in node_ids:
                    domains[node_id] = domain
            except ValueError:
                continue
    return domains


def save_results(edges, domains):
    """
    Sauvegarde les résultats dans les fichiers CSV.

    :param edges: Liste des arêtes filtrées (relations entre sites)
    :param domains: Dictionnaire associant chaque ID de site à son domaine
    """
    with open(edges_csv, "w", newline="") as f_out:
        writer = csv.writer(f_out)
        writer.writerow(["Source", "Target"])
        writer.writerows(edges)

    with open(nodes_csv, "w", newline="") as f_out:
        writer = csv.writer(f_out)
        writer.writerow(["ID_Node", "Domain"])
        for node_id, domain in domains.items():
            writer.writerow([node_id, domain])



def main():
    """Exécute le programme complet en appelant les autres fonctions"""
    start_id = find_id(seed_site)
    if start_id is None:
        print("Site non trouvé.")
        return

    node_ids, edges = bfs(start_id, max_depth)
    domains = extract_domains(node_ids)
    save_results(edges, domains)

    print("Résultats sauvegardés dans nodes.csv et edges.csv.")

#main()
