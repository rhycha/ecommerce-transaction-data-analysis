import pandas as pd
import re
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
from itertools import combinations
import matplotlib.colors as mcolors
from adjustText import adjust_text
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

# Define stop words
stop_words = {'in', 'of', 'at', 'a', 'the', 'and', 'is', 'to', 'with'}

# Tokenize descriptions and remove stop words
data['tokens'] = data['Description'].apply(lambda x: [word for word in x.split() if word not in stop_words])

# Calculate word frequencies
word_freq = Counter()
for tokens in data['tokens']:
    word_freq.update(tokens)

# Set a threshold for word frequency
threshold = 9000    
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

# Draw the graph with specified color, font, and transparency settings
plt.figure(figsize=(15, 10), facecolor='black')
ax = plt.gca()  # Get current Axes instance
ax.set_facecolor('black')
pos = nx.fruchterman_reingold_layout(G, k=0.5, iterations=2000)  # Increase k and iterations
edges = nx.draw_networkx_edges(
    G, pos, edge_color=[cmap(norm(weights[edge])) for edge in G.edges], alpha=0.5, ax=ax
)
nodes = nx.draw_networkx_nodes(G, pos, node_size=5, ax=ax, node_color='white')  # Smaller node size

# Adjust labels to be above the points and use adjustText to avoid overlap
texts = []
for node, (x, y) in pos.items():
    texts.append(plt.text(x, y + 0.02, node, fontsize=8, color='white', ha='center'))  # Move text above nodes

adjust_text(texts, arrowprops=dict(arrowstyle='-', color='white'))

# Add colorbar
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax, label='Edge Weight')
cbar.ax.yaxis.set_tick_params(color='white')
plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')

total_invoices = data['InvoiceNo'].nunique()
plt.title(f'Knowledge Graph of Product Descriptions\nTotal Invoices: {total_invoices}', color='white')
plt.axis('off')
plt.show()
