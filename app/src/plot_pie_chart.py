import os
import pandas as pd
import matplotlib.pyplot as plt
from utils import load_data
# Load the data from the CSV file
data = load_data()

# Calculate total sales for each row
data['TotalSales'] = data['Quantity'] * data['UnitPrice']

# Group by country and sum the sales
country_sales = data.groupby('Country')['TotalSales'].sum().reset_index()

# Calculate total sales for each country
total_sales_sum = country_sales['TotalSales'].sum()

# Determine the threshold for 2% of total sales
threshold = 0.01 * total_sales_sum

# Separate major countries from others
major_countries = country_sales[country_sales['TotalSales'] >= threshold]
other_countries = country_sales[country_sales['TotalSales'] < threshold]

# Calculate the total sales for "Other" category
other_sales_sum = other_countries['TotalSales'].sum()

# Append the "Other" category to major countries
major_countries = pd.concat(
    [major_countries, pd.DataFrame({'Country': ['Other'], 'TotalSales': [other_sales_sum]})],
    ignore_index=True
)

# Plotting the updated pie chart
plt.figure(figsize=(10, 8))
plt.pie(major_countries['TotalSales'], labels=major_countries['Country'], autopct='%1.1f%%', startangle=140)
plt.title('Total Sales by Country')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Save the figure to the specified directory
output_dir = 'app/data'
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'total_sales_by_country_pie_chart.png')
plt.savefig(output_path)

plt.show()
