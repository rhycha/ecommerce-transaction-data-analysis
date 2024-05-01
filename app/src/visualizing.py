import matplotlib.pyplot as plt

def show_duplicate(data):
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


def plot_monthly_sales_by_country(data):

    # Sum sales across all months to identify the top countries
    top_countries = data.sum().nlargest(5).index

    # Plot monthly sales trends for the top 5 countries
    plt.figure(figsize=(14, 8))
    for country in top_countries:
        data[country].plot(label=country)

    plt.title('Monthly Sales Trends by Country')
    plt.xlabel('Month')
    plt.ylabel('Total Sales')
    plt.legend()
    plt.grid(True)
    plt.show()
