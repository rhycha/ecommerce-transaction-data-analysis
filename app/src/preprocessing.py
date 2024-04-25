

def remove_duplicated_order_in_one_invoice(data):
    # Define true duplicates considering multiple fields that should be identical for an order
    # Assuming these columns together uniquely identify a transaction record
    duplicate_criteria = ['InvoiceNo', 'StockCode', 'Description', 'Quantity', 'InvoiceDate', 'UnitPrice', 'CustomerID']

    # Re-check for duplicates based on this more detailed criteria
    initial_row_count = data.shape[0]
    data = data.drop_duplicates(subset=duplicate_criteria)
    redefined_duplicate_count = initial_row_count - data.shape[0]
    print(f"Removed {redefined_duplicate_count} duplicates based on the redefined criteria.")
    return data