import pandas as pd
import numpy as np
from google.colab import files
import requests

# Download the CSV file
url = "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/user_behavior_dataset-UxLrK4gd7ptajTBnAzeAngHpdJ56cn.csv"
response = requests.get(url)
with open("user_behavior_dataset.csv", "wb") as f:
    f.write(response.content)

def clean_and_transform_data(csv_file):
    # Load the CSV file into a Pandas dataframe
    df = pd.read_csv(csv_file)

    # 1. Data Cleaning
    # Drop any rows with missing values
    df = df.dropna()

    # Drop any duplicated rows
    df = df.drop_duplicates()

    # Replace any string values that indicate missing data with NaN
    missing_data_values = ['N/A', 'NA', 'n/a', 'na', 'NULL', 'null', '', ' ', '-']
    df = df.replace(missing_data_values, np.nan)

    # 2. Data Transformation
    # Convert numeric columns to appropriate data types
    numeric_columns = ['App Usage Time (min/day)', 'Screen On Time (hours/day)', 'Battery Drain (mAh/day)', 'Number of Apps Installed', 'Data Usage (MB/day)', 'Age', 'User Behavior Class']
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

    # Normalize 'App Usage Time' and 'Data Usage'
    df['Normalized App Usage'] = (df['App Usage Time (min/day)'] - df['App Usage Time (min/day)'].mean()) / df['App Usage Time (min/day)'].std()
    df['Normalized Data Usage'] = (df['Data Usage (MB/day)'] - df['Data Usage (MB/day)'].mean()) / df['Data Usage (MB/day)'].std()

    # 3. Data Integration (Not applicable in this case as we have only one dataset)

    # Reset the index of the dataframe
    df = df.reset_index(drop=True)

    return df

# Clean and transform the data
cleaned_df = clean_and_transform_data("user_behavior_dataset.csv")

# Display the first few rows of the cleaned dataset
print(cleaned_df.head())

# Display basic statistics of the cleaned dataset
print(cleaned_df.describe())

# Save the cleaned dataset
cleaned_df.to_csv("cleaned_user_behavior_dataset.csv", index=False)
files.download("cleaned_user_behavior_dataset.csv")