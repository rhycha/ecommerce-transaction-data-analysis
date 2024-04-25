import pandas as pd

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


def add_date_and_time_columns_and_monetary(df):
    # Create a copy of the dataframe
    df_selected = df.copy()

    # Create aggregated variable (Amount)
    df_selected['Total_Amount_Spent'] = df_selected['Quantity'] * df_selected['UnitPrice']

    # Separate InvoiceDate into Date and Time
    df_selected['Date'] = df_selected['InvoiceDate'].dt.date
    df_selected['Time'] = df_selected['InvoiceDate'].dt.time

    # Filter out rows without values in all variables 
    df_selected = df_selected.dropna()

    return df_selected


def aggregated_by_costomerid_with_rfm(df_selected):
    # Compare RFM variables to 2012-01-01 
    today_date = pd.to_datetime("2012-01-01")

    # Group by CustomerID, calculate Recency, Frequency, and Monetary variables
    rfm_dataset = df_selected.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (today_date - x.max()).days,  # Calculate Recency
        'Quantity': 'count',  # Calculate Frequency
        'Total_Amount_Spent': 'sum'  # Calculate Monetary
    })

    # Rename the columns for clarity
    rfm_dataset.rename(columns={
        "InvoiceDate": "Recency",
        "Quantity": 'Frequency',
        "Total_Amount_Spent": "Monetary"
    },
        inplace=True
    )

    # Filter rows with Monetary variable value not equal to 0
    rfm_dataset = rfm_dataset[rfm_dataset['Monetary'] != 0]

    return rfm_dataset


def davis(df):
    df = add_date_and_time_columns_and_monetary(df)
    df = aggregated_by_costomerid_with_rfm(df)
    return df


if __name__ == '__main__':
    # data = pd.read_excel('Online Retail.xlsx')
    data = pd.read_excel('app/src/Online Retail.xlsx')
    data = remove_duplicated_order_in_one_invoice(data)
    df_selected = add_date_and_time_columns_and_monetary(data)
    rfm_dataset = aggregated_by_costomerid_with_rfm(df_selected)
    print(rfm_dataset.head())
    print(davis(data).head())
    print("Done")