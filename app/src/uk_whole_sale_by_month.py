import pandas as pd
import matplotlib.pyplot as plt
from utils import load_data

data = load_data()
# Convert 'InvoiceDate' to datetime
data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])

# Calculate total price for each row
data['TotalPrice'] = data['Quantity'] * data['UnitPrice']

# Filter data to include only sales from the United Kingdom
uk_sales_data = data[data['Country'] == 'United Kingdom']

# Extract the month from the 'InvoiceDate'
uk_sales_data['Month'] = uk_sales_data['InvoiceDate'].dt.month

# Group by month and calculate total sales
monthly_sales = uk_sales_data.groupby('Month')['TotalPrice'].sum()

# Plotting the total sales by month to visualize the trend
plt.figure(figsize=(10, 6))
monthly_sales.plot(kind='bar', color='skyblue')
plt.title('Total Sales by Month for United Kingdom')
plt.xlabel('Month')
plt.ylabel('Total Sales (in USD)')
plt.xticks(rotation=45)
plt.show()

# Calculate the average sales for the last quarter (October, November, December)
last_quarter_sales = monthly_sales.loc[[10, 11, 12]].mean()

# Calculate the average sales for the rest of the year (January to September)
rest_of_year_sales = monthly_sales.loc[[1, 2, 3, 4, 5, 6, 7, 8, 9]].mean()

last_quarter_sales, rest_of_year_sales
