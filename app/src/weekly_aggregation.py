import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils import load_data

data = load_data()

# Preprocessing function
def preprocess_data(data):
    # Ensure 'InvoiceNo' column is treated as string and handle non-string entries
    data['InvoiceNo'] = data['InvoiceNo'].astype(str)

    # Remove UnitPrice values that are less than or equal to 0 for further analysis
    data = data[data['UnitPrice'] > 0]
    
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

# Preprocess the data
data = preprocess_data(data)

# Convert InvoiceDate to datetime format
data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])

# Calculate total sales for each transaction
data['TotalSales'] = data['Quantity'] * data['UnitPrice']

# Set InvoiceDate as the index
data.set_index('InvoiceDate', inplace=True)


# Calculate the entire sales value
total_sales_value = data['TotalSales'].sum()
print(f'Total Sales Value: {total_sales_value}')


# Resample data to weekly frequency, summing the TotalSales
weekly_sales = data['TotalSales'].resample('W').sum()

# Plot the weekly sales trend
plt.figure(figsize=(12, 6))
sns.lineplot(data=weekly_sales)
plt.title('Weekly Sales Trend')
plt.xlabel('Week')
plt.ylabel('Total Sales')
plt.grid(True)
plt.show()



# Resample data to weekly frequency, summing the TotalSales
weekly2_sales = data['TotalSales'].resample('2W').sum()

# Plot the weekly sales trend
plt.figure(figsize=(12, 6))
sns.lineplot(data=weekly2_sales)
plt.title('Weekly Sales Trend')
plt.xlabel('Week')
plt.ylabel('Total Sales')
plt.grid(True)
plt.show()


