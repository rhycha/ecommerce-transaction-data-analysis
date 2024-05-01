import pandas as pd
import numpy as np
import os

import os
import pandas as pd

def load_data():
    # Get the current working directory
    current_path = os.getcwd()
    print("Current Working Directory:", current_path)
    
    # Determine the correct file path based on the current directory
    if current_path.endswith('app'):
        file_path = 'src/Online Retail.xlsx'
    elif current_path.endswith('app/src'):
        file_path = 'Online Retail.xlsx'
    elif current_path.endswith('ecommerce-transaction-data-analysis'):
        file_path = 'app/src/Online Retail.xlsx'
    else:
        print("The script is not in the expected directory.")
        return None

    # Load the data from the determined file path
    try:
        data = pd.read_excel(file_path)
        return data
    except Exception as e:
        print(f"Failed to load data: {e}")
        return None




def sampling(filename,path=None):
    # Adjust the fraction to the amount of data you want to sample, e.g., 0.1 for 10%
    fraction = 0.1

    # Load your data
    # Replace 'your_data.csv' with the path to your file
    df = pd.read_excel(filename)

    # Sample the data
    sampled_df = df.sample(frac=fraction, random_state=1)  # random_state for reproducibility

    # Save the sampled data to a new file
    filename.replace('.xlsx','')
    sampled_df.to_csv(f'{filename}_small.csv', index=False)


if __name__=="__main__":
    filename = f"src/Online Retail.xlsx"
    sampling(filename)