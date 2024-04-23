import pandas as pd
import numpy as np


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