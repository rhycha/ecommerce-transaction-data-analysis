import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
from utils import load_data

# Load the dataset
data = load_data()

# Remove rows with missing CustomerID
data = data.dropna(subset=['CustomerID'])

# Convert InvoiceDate to datetime
data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])

# Calculate Monetary Value
data['TotalAmount'] = data['Quantity'] * data['UnitPrice']

# Create a snapshot date (e.g., one day after the last invoice date in the dataset)
snapshot_date = data['InvoiceDate'].max() + pd.Timedelta(days=1)

# Aggregate data by CustomerID to create Recency, Frequency, and Monetary features
customer_data = data.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (snapshot_date - x.max()).days,  # Recency
    'InvoiceNo': 'nunique',                                   # Frequency
    'TotalAmount': 'sum'                                      # Monetary
}).reset_index()

# Rename columns
customer_data.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']

# Scale the data
scaler = StandardScaler()
scaled_data = scaler.fit_transform(customer_data[['Recency', 'Frequency', 'Monetary']])

# Elbow method to find the optimal number of clusters
inertia = []
for n in range(1, 11):
    kmeans = KMeans(n_clusters=n, max_iter=300, random_state=42)
    kmeans.fit(scaled_data)
    inertia.append(kmeans.inertia_)

# Plot the elbow chart
plt.figure(figsize=(10, 6))
plt.plot(range(1, 11), inertia, marker='o')
plt.title('Elbow Method for Optimal Number of Clusters')
plt.xlabel('Number of Clusters')
plt.ylabel('Inertia')
plt.grid(True)
plt.show()

# Apply K-Means with the chosen number of clusters (e.g., 3)
kmeans = KMeans(n_clusters=3, max_iter=300, random_state=42)
customer_data['Cluster'] = kmeans.fit_predict(scaled_data)

# Save the clustered data to a CSV file
customer_data.to_csv('customer_clusters.csv', index=False)

# Plot pairplot of the clusters
sns.pairplot(customer_data[['Recency', 'Frequency', 'Monetary', 'Cluster']], hue='Cluster', diag_kind='kde', palette='viridis')
plt.suptitle('Customer Clusters - Recency, Frequency, Monetary', y=1.02)
plt.show()

# 3D scatter plot for the clusters
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot each cluster with a different color
colors = ['blue', 'green', 'red', 'purple']
for cluster in range(3):
    clustered_data = customer_data[customer_data['Cluster'] == cluster]
    ax.scatter(clustered_data['Recency'], clustered_data['Frequency'], clustered_data['Monetary'], 
               label=f'Cluster {cluster}', color=colors[cluster], s=50)

# Set labels
ax.set_xlabel('Recency')
ax.set_ylabel('Frequency')
ax.set_zlabel('Monetary')
# Set title and legend
ax.set_title('Customer Clusters')
ax.legend()
plt.show()
