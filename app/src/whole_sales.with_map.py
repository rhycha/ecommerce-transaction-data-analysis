import plotly.express as px
from utils import load_data

# Load the data from the uploaded CSV file
data = load_data()

# Step 1: Calculate total sales for each row
data['TotalSales'] = data['Quantity'] * data['UnitPrice']

# Step 2: Group by country and sum the sales
country_sales = data.groupby('Country')['TotalSales'].sum().reset_index()

# Identify the sales value for the UK
uk_sales = country_sales[country_sales['Country'] == 'United Kingdom']['TotalSales'].values[0]

# Exclude the UK sales from the color scale calculation
non_uk_sales = country_sales[country_sales['Country'] != 'United Kingdom']

# Plotting the map using Plotly without UK
fig = px.choropleth(
    non_uk_sales,
    locations="Country",
    locationmode='country names',
    color="TotalSales",
    hover_name="Country",
    color_continuous_scale=px.colors.sequential.OrRd,
    range_color=(0, non_uk_sales['TotalSales'].max()),
    title="Total Sales by Country (Excluding UK)"
)


# Re-add the UK sales to the map using the same color scale
fig.add_trace(px.choropleth(
    country_sales[country_sales['Country'] == 'United Kingdom'],
    locations="Country",
    locationmode='country names',
    color="TotalSales",
    hover_name="Country",
    color_continuous_scale=px.colors.sequential.OrRd,
    range_color=(0, non_uk_sales['TotalSales'].max())
).data[0])


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

print(file_path_html_updated)
