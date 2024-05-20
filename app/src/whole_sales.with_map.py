import pandas as pd
import plotly.express as px
from utils import load_data 
# Load the data from the uploaded CSV file
data = load_data()


# Step 1: Calculate total sales for each row
data['TotalSales'] = data['Quantity'] * data['UnitPrice']

# Step 2: Group by country and sum the sales
country_sales = data.groupby('Country')['TotalSales'].sum().reset_index()

# Display the total sales by country
country_sales.head()



# Plotting the map using Plotly
fig = px.choropleth(
    country_sales,
    locations="Country",
    locationmode='country names',
    color="TotalSales",
    hover_name="Country",
    color_continuous_scale=px.colors.sequential.OrRd,
    title="Total Sales by Country"
)

fig.show()


# Define a new color scale with a distinct color for the UK
custom_color_scale = [
    (0.0, "rgb(255, 255, 204)"),   # Light yellow
    (0.2, "rgb(255, 237, 160)"),
    (0.4, "rgb(254, 217, 118)"),
    (0.6, "rgb(254, 178, 76)"),
    (0.8, "rgb(253, 141, 60)"),
    (0.9, "rgb(240, 59, 32)"),
    (0.95, "rgb(189, 0, 38)"),
    (1.0, "rgb(128, 0, 38)")       # Dark red
]

# Create the map using Plotly
fig = px.choropleth(
    country_sales,
    locations="Country",
    locationmode='country names',
    color="TotalSales",
    hover_name="Country",
    color_continuous_scale=custom_color_scale,
    range_color=(0, 30000),
    title="Total Sales by Country"
)

# Set a distinct color for the UK
uk_sales = country_sales[country_sales['Country'] == 'United Kingdom']['TotalSales'].values[0]
fig.add_scattergeo(
    locations=["United Kingdom"],
    locationmode='country names',
    text=f"United Kingdom: {uk_sales:.2f}",
    marker=dict(size=15, color='blue'),
    hoverinfo='text',
    showlegend=False
)

fig.update_layout(
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    ),
    margin={"r":0,"t":0,"l":0,"b":0}
)


# Save the figure to an HTML file
file_path_html_updated = 'app/data/total_sales_by_country_updated.html'
fig.write_html(file_path_html_updated)

file_path_html_updated
