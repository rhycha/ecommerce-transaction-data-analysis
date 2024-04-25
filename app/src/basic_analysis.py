#%%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


#%%
# Load the data
# file_path = 'Online Retail_small.csv'
# data = pd.read_csv(file_path)
file_path = 'src/Online Retail.xlsx'
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

# Missing value visualization
missing_data_ratio = (data.isnull().sum() / len(data)) * 100
missing_data_ratio = missing_data_ratio[missing_data_ratio > 0]  # Filter columns with missing values

plt.figure(figsize=(10, 5))
sns.barplot(x=missing_data_ratio.index, y=missing_data_ratio.values, palette='viridis')
plt.title('Percentage of Missing Values Per Column')
plt.xlabel('Columns')
plt.ylabel('Percentage of Missing Data (%)')
plt.show()


# %%
