import networkx as nx 
import pandas as pd 
import time
import numpy as np

def page_rank(graph, max_iter=100, tol=1e-6, a=0.85):
    """
    Implémente l'algorithme PageRank pour un graphe dirigé.
    
    Paramètres :
    - graph : Graphe dirigé NetworkX.
    - max_iter : Nombre maximal d'itérations pour la convergence.
    - tol : Tolérance pour la convergence.
    - a : Facteur de téléportation (probabilité de suivre un lien, 0.85).
    
    Retourne :
    - Dictionnaire associant chaque nœud à son score PageRank.
    """
    num_nodes = len(graph)  # Nombre de nœuds dans le graphe
    
    # Initialisation du PageRank : chaque nœud reçoit un score initial égal
    pr = {node: 1 / num_nodes for node in graph}
    
    
    # Itérations pour mettre à jour les scores PageRank
    for _ in range(max_iter):
        new_pr = {}  # Dictionnaire pour stocker les nouveaux scores
        for node in graph:
            rank_sum = 0  # Somme des contributions des voisins
            for neighbor in graph.predecessors(node):  # Parcours des prédécesseurs
                # Ajout de la contribution du voisin au PageRank du nœud
                rank_sum += pr[neighbor] / len(list(graph.successors(neighbor)))
            
            # Application de la formule du PageRank
            new_pr[node] = (1 - a) / num_nodes + a * rank_sum
        
        # Vérification de la convergence en mesurant la différence avec l'itération précédente
        diff = sum(abs(new_pr[node] - pr[node]) for node in pr)
        if diff < tol:
            break  # Arrêt si la différence est inférieure au seuil de tolérance
        
        pr = new_pr  # Mise à jour des scores PageRank
    
    # Normalisation des scores pour que la somme soit égale à 1
    total_score = sum(pr.values())
    pr_normalized = {k: v / total_score for k, v in pr.items()}
    

    return pr_normalized  # Retourne le dictionnaire des scores PageRank normalisés

# Chargement du fichier contenant les liens entre sites web
df = pd.read_csv('filtered_edges_modifié.txt')

# Création d'un graphe orienté
G = nx.DiGraph()

# Ajout des arêtes au graphe en fonction du fichier CSV
for index, row in df.iterrows():
    G.add_edge(row['Source'], row['Target'])

# Calcul du PageRank sur le graphe construit
start_time=time.time()
pr_values = page_rank(G)
elapsed_time = time.time() - start_time
print("temps de calcul notre algo", elapsed_time )



G = nx.DiGraph()
for index, row in df.iterrows():
    G.add_edge(row['Source'], row['Target'])

nx_start = time.time()
pr_nx = nx.pagerank(G, alpha=0.85, tol=1e-6)
nx_time = time.time() - nx_start
print("temps NetworkX", nx_time)


# Tri des sites en fonction de leur score PageRank (ordre décroissant)
sorted_pr = sorted(pr_values.items(), key=lambda x: x[1], reverse=True)
sorted_pr_nx = sorted(pr_nx.items(), key=lambda x: x[1], reverse=True)

# Affichage des 5 sites les plus référencés
print("Top 5 sites les plus référencés :")
for site, rank in sorted_pr[:10]:
    print(f"{site}: {rank}")
print("-------------------------------")
for site, rank in sorted_pr_nx[:10]:
    print(f"{site}: {rank}")

# Identification du site ayant le score PageRank maximal
max_site = max(pr_values, key=pr_values.get)
print(f"Le site le plus référencé est : {max_site} avec un PageRank de {pr_values[max_site]}")








import matplotlib.pyplot as plt
import numpy as np

# Calcul des erreurs relatives
errors = []
for node in pr_values:
    if pr_nx[node] > 0:  # Éviter la division par zéro
        rel_error = abs(pr_values[node] - pr_nx[node]) / pr_nx[node]
        errors.append(rel_error)

# Conversion en array numpy pour l'analyse
errors = np.array(errors)

plt.figure(figsize=(10, 6))



_,bins = np.histogram(errors, bins=20)
logbins = np.logspace(np.log10(bins[0]), np.log10(bins[-1]), len(bins))

plt.hist(errors, bins=logbins, color='orange', edgecolor='red', weights=np.ones_like(errors)/len(errors) )


# Ligne de la moyenne
mean_error = np.median(errors)
plt.axvline(mean_error, color='green', linestyle='--', 
            label=f'Erreur médiane: {mean_error:.2e}')

# Paramètres esthétiques
plt.xscale('log')  # Échelle logarithmique pour mieux voir les petites variations
plt.title('Distribution des erreurs relatives entre les implémentations')
plt.xlabel('Erreur relative (échelle log)')
plt.ylabel('Proportion du nombre de nœuds')
plt.legend()
plt.grid(True, which="both", ls="--")

# Sauvegarde
plt.savefig('error_comparison.png', dpi=300, bbox_inches='tight')
plt.close()