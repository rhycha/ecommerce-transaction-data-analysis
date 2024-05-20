import pandas as pd
import matplotlib.pyplot as plt
from utils import load_data

# Load the dataset
data = load_data()

# Convert 'InvoiceDate' to datetime
data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])

# Calculate total price for each row
data['TotalPrice'] = data['Quantity'] * data['UnitPrice']

# Extract the day of the week from 'InvoiceDate'
data['DayOfWeek'] = data['InvoiceDate'].dt.day_name()

# Group by 'DayOfWeek' and sum the total prices
total_sales_per_day = data.groupby('DayOfWeek')['TotalPrice'].sum()

# Count the number of occurrences of each day to get the number of days
days_count = data['DayOfWeek'].value_counts()

# Calculate the average sales per weekday
average_sales_per_day = total_sales_per_day / days_count

# Reorder the index to match the days of the week
average_sales_per_day = average_sales_per_day.reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

# Replace NaN values with 0, as there are no records for Saturday
average_sales_per_day = average_sales_per_day.fillna(0)

# Plotting the average sales by weekday
plt.figure(figsize=(10, 6))
average_sales_per_day.plot(kind='bar', color='skyblue')
plt.title('Average Sales by Weekday')
plt.xlabel('Weekday')
plt.ylabel('Average Sales (in USD)')
plt.xticks(rotation=45)
plt.show()
