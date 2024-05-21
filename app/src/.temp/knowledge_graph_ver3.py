import pandas as pd
import re
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
from itertools import combinations
import matplotlib.colors as mcolors
from utils import load_data


def preprocess_data(data):
    # Ensure 'InvoiceNo' column is treated as string and handle non-string entries
    data['InvoiceNo'] = data['InvoiceNo'].astype(str)

    # Remove cancellation invoices (starting with 'C' or having negative quantity)
    data = data[~data['InvoiceNo'].str.startswith('C', na=False)]
    data = data[data['Quantity'] > 0]

    # Aggregate data by InvoiceNo and StockCode
    data = data.groupby(['InvoiceNo', 'StockCode'], as_index=False).agg({
        'Description': 'first',
        'Quantity': 'sum',
        'InvoiceDate': 'first',
        'UnitPrice': 'mean',
        'CustomerID': 'first',
        'Country': 'first'
    })

    return data


# Load the dataset
data = load_data()  
data = preprocess_data(data)

# Ensure 'Description' column is treated as string and handle non-string entries
data['Description'] = data['Description'].astype(str)

# Preprocess descriptions: lowercasing and removing non-alphabetic characters
data['Description'] = data['Description'].str.lower().apply(lambda x: re.sub(r'[^a-z\s]', '', x))

# Tokenize descriptions
data['tokens'] = data['Description'].apply(lambda x: x.split())

# Calculate word frequencies
word_freq = Counter()
for tokens in data['tokens']:
    word_freq.update(tokens)

# Set a threshold for word frequency
threshold = 8000
filtered_words = {word for word, count in word_freq.items() if count >= threshold}

# Create a co-occurrence matrix with filtered words
co_occurrence = Counter()
for tokens in data['tokens']:
    filtered_tokens = [word for word in tokens if word in filtered_words]
    for pair in combinations(set(filtered_tokens), 2):
        co_occurrence[pair] += 1

# Create a graph with filtered words
G = nx.Graph()
for (word1, word2), count in co_occurrence.items():
    G.add_edge(word1, word2, weight=count)

# Normalize edge weights for color mapping
weights = nx.get_edge_attributes(G, 'weight')
max_weight = max(weights.values())
min_weight = min(weights.values())

# Create a color map
norm = mcolors.Normalize(vmin=min_weight, vmax=max_weight)
cmap = plt.get_cmap('viridis')

# Draw the graph
plt.figure(figsize=(15, 10))
ax = plt.gca()  # Get current Axes instance
pos = nx.spring_layout(G, k=0.15, iterations=20)
edges = nx.draw_networkx_edges(
    G, pos, edge_color=[cmap(norm(weights[edge])) for edge in G.edges], alpha=0.7, ax=ax
)
nodes = nx.draw_networkx_nodes(G, pos, node_size=50, ax=ax)
labels = nx.draw_networkx_labels(G, pos, font_size=10, ax=ax)

# Add colorbar
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
plt.colorbar(sm, ax=ax, label='Edge Weight')
plt.title('Knowledge Graph of Product Descriptions')
plt.axis('off')
plt.show()

