

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
