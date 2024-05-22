#%%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

from utils import load_data

# Example usage
data = load_data()

#%%
# Display the first few rows of the dataset
data.head(), data.columns

#%%
#%%
data.info()
data.describe()

#%%    
# Calculate the number of unique values for each column
unique_counts = data.nunique()

# Show the number of unique values per column
unique_counts

#%%

# Create a bar chart for visualizing the unique counts
plt.figure(figsize=(10, 6))
unique_counts.plot(kind='bar', color='skyblue')
plt.title('Count of Unique Values Per Column in the Dataset')
plt.xlabel('Columns')
plt.ylabel('Number of Unique Values')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

#%%
# Step 1: Check for missing values
missing_values = data.isnull().sum()

# Step 2: Review data types
data_types = data.dtypes

missing_values, data_types

#%%
# Step 1: Convert InvoiceDate to datetime format
data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])

#%%
# Missing value visualization
missing_data_ratio = (data.isnull().sum() / len(data)) * 100
missing_data_ratio = missing_data_ratio[missing_data_ratio > 0]  # Filter columns with missing values

plt.figure(figsize=(10, 5))
sns.barplot(x=missing_data_ratio.index, y=missing_data_ratio.values, palette='viridis')
plt.title('Percentage of Missing Values Per Column')
plt.xlabel('Columns')
plt.ylabel('Percentage of Missing Data (%)')
plt.show()

#%%
# For records with missing 'Description'
missing_description = data[data['Description'].isnull()]
print(missing_description)

#%%
# For records with missing 'CustomerID'
missing_customerid = data[data['CustomerID'].isnull()]
print(missing_customerid)

#%%
# Filter and display the rows with UnitPrice equal to 0
zero_unitprice_df = data[data['UnitPrice'] == 0]
print(zero_unitprice_df)

# Count the number of zero values in UnitPrice
zero_unitprice_count = zero_unitprice_df.shape[0]
print(f'Number of zero values in UnitPrice: {zero_unitprice_count}')

# Remove UnitPrice values that are less than or equal to 0 for further analysis
data = data[data['UnitPrice'] > 0]

# Calculate the frequency of unique UnitPrice values
unitprice_counts = data['UnitPrice'].value_counts().reset_index()
unitprice_counts.columns = ['UnitPrice', 'Frequency']

#%%
# Unique UnitPrice distribution - Scatter Plot
plt.figure(figsize=(12, 6))
plt.scatter(unitprice_counts['UnitPrice'], unitprice_counts['Frequency'], alpha=0.6, edgecolors='w', s=100)
plt.title('Unique UnitPrice Distribution')
plt.xlabel('UnitPrice')
plt.ylabel('Frequency')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

#%%
# Unique UnitPrice distribution - Strip Plot
plt.figure(figsize=(12, 6))
sns.stripplot(x='UnitPrice', y='Frequency', data=unitprice_counts, jitter=True, palette='viridis')
plt.title('Unique UnitPrice Distribution')
plt.xlabel('UnitPrice')
plt.ylabel('Frequency')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# %%
data['UnitPrice'].describe()
# %%
