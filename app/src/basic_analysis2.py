# %%
import pandas as pd 

data_type = {"CustomerID": str}
df = pd.read_excel('Online Retail.xlsx', dtype = data_type)


# %%
#Data preprocessing

selected_variables = ['InvoiceNo', 'StockCode', 'Description', 'Quantity', 'InvoiceDate',
       'UnitPrice', 'CustomerID', 'Country']

df_selected = df[selected_variables]

# Create aggregated variable (Amount)
df_selected['Total_Amount_Spent'] = df_selected['Quantity'] * df_selected['UnitPrice']

# Separate InvoiceDate into Date and Time
df_selected['Date'] = df_selected['InvoiceDate'].dt.date
df_selected['Time'] = df_selected['InvoiceDate'].dt.time

# Filter out rows without values in all variables 
df_selected = df_selected.dropna()

df_selected.head()


# %%
#compare RFM variables to 2012-01-01 
today_date = pd.to_datetime("2012-01-01")

print(df_selected.dtypes)

# Group by Country, calculate Recency, Frequency, and Monetary variables
rfm_dataset = df_selected.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (today_date - x.max()).days,  # Calculate Recency
    'Quantity': 'count',  # Calculate Frequency
    'Total_Amount_Spent': 'sum'  # Calculate Monetary
})

# Rename the columns for clarity
rfm_dataset.rename(columns = {
    "InvoiceDate": "Recency", 
    "Quantity": 'Frequency',
    "Total_Amount_Spent": "Monetary"
    },
    inplace = True
)

# Filter rows with Monetary variable value not equal to 0
rfm_dataset = rfm_dataset[rfm_dataset['Monetary'] != 0]

# Display the result
rfm_dataset.head()


