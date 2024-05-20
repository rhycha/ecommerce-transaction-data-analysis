import pandas as pd
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

# Aggregate data by CustomerID to create Recency, Frequency, and Monetary Value features
customer_data = data.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (snapshot_date - x.max()).days,  # Recency
    'InvoiceNo': 'nunique',                                   # Frequency
    'TotalAmount': 'sum'                                      # Monetary Value
}).reset_index()

# Rename columns
customer_data.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']

customer_data.head()


from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Scale the data
scaler = StandardScaler()
scaled_data = scaler.fit_transform(customer_data[['Recency', 'Frequency', 'Monetary']])

# Determine the optimal number of clusters using the elbow method
sse = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(scaled_data)
    sse.append(kmeans.inertia_)

# Plot the elbow curve
plt.figure(figsize=(10, 6))
plt.plot(range(1, 11), sse, marker='o')
plt.title('Elbow Method For Optimal k')
plt.xlabel('Number of clusters')
plt.ylabel('Sum of squared distances (SSE)')
plt.show()

# Apply K-Means with 4 clusters
kmeans = KMeans(n_clusters=4, max_iter=300, random_state=42)
customer_data['Cluster'] = kmeans.fit_predict(scaled_data)

# Calculate the mean values of Recency, Frequency, and Monetary for each cluster
cluster_summary = customer_data.groupby('Cluster').mean().reset_index()

cluster_summary


