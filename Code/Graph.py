import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# Charger le fichier CSV contenant les arêtes
df = pd.read_csv('filtered_edges.csv')  # Assurez-vous que votre fichier CSV est bien dans le bon répertoire

# Créer un graphe dirigé
G = nx.DiGraph()

# Ajouter les arêtes au graphe
for index, row in df.iterrows():
    G.add_edge(row['Source'], row['Target'])

# Visualisation du graphe avec un layout plus clair et ajustements
plt.figure(figsize=(12, 12))  # Ajuster la taille de l'image

# Utilisation du layout 'spring_layout' pour une meilleure disposition des nœuds
pos = nx.spring_layout(G, seed=42)  # 'seed' permet de rendre la disposition stable

# Dessin du graphe
node_colors = ['red' if node == 25331911 else 'darkviolet' if node == 67187005 else 'skyblue' for node in G.nodes()]
node_size = [2000 if node == 25331911 else 2000 if node == 67187005 else 200 for node in G.nodes()]

nx.draw(G, pos, with_labels=True, node_size=node_size, font_size=10, font_color="black", node_color=node_colors, 
        arrows=True, edge_color='gray', linewidths=1.5, font_weight="normal")

# Améliorer l'affichage (grille, titres, etc.)
plt.title("Graphique des Arêtes du Graphe Dirigé", fontsize=15)
plt.grid(True)

# Enregistrer l'image avec un fond transparent
plt.savefig("graphique_graphe_transparent.png", dpi=300, transparent=False)  # Fond transparent

# Afficher le graphique
plt.show()