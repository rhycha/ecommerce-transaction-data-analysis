#%%
import pandas as pd

#%%
# Load the data
# file_path = 'Online Retail_small.csv'
# data = pd.read_csv(file_path)
file_path = 'Online Retail.xlsx'
data = pd.read_excel(file_path)


#%%
# Display the first few rows of the dataset
data.head(), data.columns


# %%
# Calculate the number of unique values for each column
unique_counts = data.nunique()

# Show the number of unique values per column
unique_counts

# %%
import matplotlib.pyplot as plt

# Create a bar chart for visualizing the unique counts
plt.figure(figsize=(10, 6))
unique_counts.plot(kind='bar', color='skyblue')
plt.title('Count of Unique Values Per Column in the Dataset')
plt.xlabel('Columns')
plt.ylabel('Number of Unique Values')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()


# %%
# Step 1: Check for missing values
missing_values = data.isnull().sum()

# Step 2: Review data types
data_types = data.dtypes

missing_values, data_types

# %%
# Step 1: Convert InvoiceDate to datetime format
data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])


# %%
# Define true duplicates considering multiple fields that should be identical for an order
# Assuming these columns together uniquely identify a transaction record
duplicate_criteria = ['InvoiceNo', 'StockCode', 'Description', 'Quantity', 'InvoiceDate', 'UnitPrice', 'CustomerID']

# %%

# Finding duplicates based on the specified criteria, marking all occurrences
data['is_duplicate'] = data.duplicated(subset=duplicate_criteria, keep=False)

# Filter to get only the duplicates
duplicates = data[data['is_duplicate'] == True]

# Sort the duplicates to better analyze them
duplicates_sorted = duplicates.sort_values(by=['InvoiceNo', 'StockCode', 'InvoiceDate'])

# Display the duplicates
print(duplicates_sorted[['InvoiceNo', 'StockCode', 'Description', 'Quantity', 'InvoiceDate', 'UnitPrice', 'CustomerID']])


# %%
# Finding duplicates based on the specified criteria
duplicates = data[data.duplicated(subset=duplicate_criteria, keep=False)]

# Sorting by 'InvoiceNo' and 'InvoiceDate' to review duplicates more easily
duplicates_sorted = duplicates.sort_values(by=['InvoiceNo', 'InvoiceDate'])

# Displaying the duplicates
print(duplicates_sorted)

# %%

# Finding duplicates based on the specified criteria, marking all occurrences
data['is_duplicate'] = data.duplicated(subset=duplicate_criteria, keep=False)

# Filter to get only the duplicates
duplicates = data[data['is_duplicate'] == True]

# Sort the duplicates to better analyze them
duplicates_sorted = duplicates.sort_values(by=['InvoiceNo', 'StockCode', 'InvoiceDate'])

# Display the duplicates
print(duplicates_sorted[['InvoiceNo', 'StockCode', 'Description', 'Quantity', 'InvoiceDate', 'UnitPrice', 'CustomerID']])