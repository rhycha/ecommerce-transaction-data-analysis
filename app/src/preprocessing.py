import pandas as pd
import re


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

def aggregaed_by_orderid_and_product_code(df):
    pass


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


def fix_datatype(data):
    data['CustomerID'] = data['CustomerID'].astype(str)
    data['InvoiceNo'] = data['InvoiceNo'].astype(str)
    # Convert InvoiceDate to datetime format
    data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])

    return data

def remove_cancelled_transactions(data):
    # Filter out cancellation transactions
    data_clean = data[~data['InvoiceNo'].str.startswith('C')]

    return data_clean

def add_total_sales_column(data):
    # Create a new column for total sales per line item
    data['TotalSales'] = data['Quantity'] * data['UnitPrice']

    return data

def group_by_country_and_month(data):
    # Group by country and month, summing up the total sales
    monthly_sales_by_country = data.set_index('InvoiceDate').groupby([pd.Grouper(freq='M'), 'Country'])['TotalSales'].sum().unstack(fill_value=0)
    print(monthly_sales_by_country.head())
    return monthly_sales_by_country


def prep_top5_total_sales_by_country(data):
    data = fix_datatype(data)
    data = add_total_sales_column(data)

    Monetary_Country = data[['Country', 'TotalSales']]

    Monetary_Country= Monetary_Country.groupby('Country')['TotalSales'].sum().reset_index()

    Monetary_Country = Monetary_Country.sort_values(by='TotalSales', ascending=False)

    Monetary_Country = Monetary_Country.head(5)
    
    return Monetary_Country

def prep_monthly_sales_by_country(data):
    # data = remove_duplicated_order_in_one_invoice(data)
    # data = add_date_and_time_columns_and_monetary(data)
    data = fix_datatype(data)
    data = remove_cancelled_transactions(data)
    data = add_total_sales_column(data)
    data = group_by_country_and_month(data)
    return data

def focus_on_uk(data):
    # Filter the data for the United Kingdom
    data_uk = data[data['Country'] == 'United Kingdom']

    return data_uk


def generate_keywords(data):

    # Explicitly create a copy of the DataFrame to work on if necessary
    data = data.copy()

    # Clean and preprocess descriptions
    data['Description'] = data['Description'].astype(str).str.lower()
    data['Description'] = data['Description'].apply(lambda x: re.sub(r'[^a-z\s]', '', x))
    print("Cleaned Descriptions:")
    print(data['Description'].head())

    # Expand the descriptions into separate words
    words = data['Description'].str.split(expand=True).stack()
    words.index = words.index.droplevel(1)  # Drop the inner level of multi-index
    words.name = 'Keyword'
    print("Expanded Words:")
    print(words.head())

    # Associate words with sales
    keywords_with_sales = data.loc[words.index, ['TotalSales']].join(words)
    print("Keywords Associated with Sales:")
    print(keywords_with_sales.head())

    # Aggregate sales by keywords
    keyword_sales = keywords_with_sales.groupby('Keyword')['TotalSales'].sum().sort_values(ascending=False)
    print("Aggregated Sales by Keyword:")
    print(keyword_sales.head(10))
    return keyword_sales

def preprocess_and_aggregate_with_recency(data):
    # Remove rows with missing CustomerID
    data = data.dropna(subset=['CustomerID'])
    
    # Parse InvoiceDate to datetime
    data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])
    
    # Calculate TotalRevenue for each row
    data['TotalRevenue'] = data['Quantity'] * data['UnitPrice']
    
    # Find the most recent date in the dataset as the reference date
    reference_date = data['InvoiceDate'].max()
    
    # Aggregate data by CustomerID
    aggregated_data = data.groupby('CustomerID').agg(
        TotalQuantity=('Quantity', 'sum'),
        TotalRevenue=('TotalRevenue', 'sum'),
        UniqueInvoices=('InvoiceNo', 'nunique'),
        LastPurchaseDate=('InvoiceDate', 'max')
    ).reset_index()
    
    # Calculate recency as the difference 
    # between the reference date and the last purchase date
    aggregated_data['RecencyDays'] = \
    (reference_date - aggregated_data['LastPurchaseDate']).dt.days
    
    # Drop the LastPurchaseDate column as it's no longer needed
    aggregated_data = aggregated_data.drop(columns=['LastPurchaseDate'])
    
    return aggregated_data



def chatgpt_package(data):
    import pandas as pd
    import re
    import numpy as np
    import networkx as nx
    import matplotlib.pyplot as plt
    from itertools import combinations

    # Ensure all descriptions are strings
    data['Description'] = data['Description'].astype(str)

    # Preprocess descriptions
    data['CleanedDescription'] = data['Description'].apply(lambda x: re.sub(r'[^a-z\s]', '', x.lower()).split())

    # Build co-occurrence matrix
    all_keywords = set(word for desc in data['CleanedDescription'] for word in desc)
    # Convert set to list before using it as an index
    all_keywords = list(all_keywords)
    co_occ = pd.DataFrame(index=all_keywords, columns=all_keywords).fillna(0)

    for keywords in data['CleanedDescription']:
        for (word1, word2) in combinations(set(keywords), 2):
            co_occ.at[word1, word2] += 1
            co_occ.at[word2, word1] += 1

    # Create a network graph
    G = nx.from_pandas_adjacency(co_occ)

    # Draw the graph
    nx.draw_networkx(G, with_labels=True)
    plt.show()


def davis(df):
    df = add_date_and_time_columns_and_monetary(df)
    df = aggregated_by_costomerid_with_rfm(df)
    return df



if __name__ == '__main__':
    from utils import load_data
    data = load_data()
    chatgpt_package(data)
    # # data = pd.read_excel('Online Retail.xlsx')
    # data = pd.read_excel('app/src/Online Retail.xlsx')
    # data = remove_duplicated_order_in_one_invoice(data)
    # df_selected = add_date_and_time_columns_and_monetary(data)
    # rfm_dataset = aggregated_by_costomerid_with_rfm(df_selected)
    # print(rfm_dataset.head())
    # print(davis(data).head())
    # print("Done")
    # Apply the preprocessing function to the data

