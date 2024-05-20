import pandas as pd
import re
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
from itertools import combinations
from utils import load_data

data = load_data()  

# Ensure 'Description' column is treated as string and handle non-string entries
data['Description'] = data['Description'].astype(str)

# Preprocess descriptions: lowercasing and removing non-alphabetic characters
data['Description'] = data['Description'].str.lower().apply(lambda x: re.sub(r'[^a-z\s]', '', x))

# Tokenize descriptions
data['tokens'] = data['Description'].apply(lambda x: x.split())

# Create a co-occurrence matrix
co_occurrence = Counter()
for tokens in data['tokens']:
    for pair in combinations(set(tokens), 2):
        co_occurrence[pair] += 1

# Create a graph
G = nx.Graph()
for (word1, word2), count in co_occurrence.items():
    G.add_edge(word1, word2, weight=count)

# Draw the graph
plt.figure(figsize=(15, 10))
pos = nx.spring_layout(G, k=0.15, iterations=20)
nx.draw(G, pos, with_labels=True, node_size=50, font_size=10, width=[d['weight']*0.1 for (_, _, d) in G.edges(data=True)])
plt.title('Knowledge Graph of Product Descriptions')
plt.show()
