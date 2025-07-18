# -*- coding: utf-8 -*-
"""success_data_preprocessing.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Lqz198xmF9Md8NT-882hJK70YU4wRC9L
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

data = pd.read_excel('/content/startup_success_dataset_template (1).xlsx')

data.head()

data.info()

data.shape

# prompt: write a python code that make augmentation for the 100 row of this dataset convert it to 500 rows

# Assuming 'data' is your pandas DataFrame loaded from the Excel file
# Let's focus on augmenting the first 100 rows to generate 400 new rows (100 + 400 = 500 total)

# Select the first 100 rows
rows_to_augment = data.head(100).copy()

# Function to perform simple augmentation
# This is a placeholder function. You should customize this based on your data and the type of augmentation needed.
# For numerical columns, you could add small random noise.
# For categorical columns, you could randomly swap values or duplicate rows.
# This example just duplicates rows with some random value addition for simplicity on numerical columns.
def augment_row(row):
  new_row = row.copy()
  # Example: Add small random noise to numerical columns
  for col in new_row.index:
    # Check if the value is numeric before attempting augmentation
    if pd.api.types.is_numeric_dtype(new_row[col]):
        try:
            # Convert to numeric, coercing errors to NaN
            numeric_value = pd.to_numeric(new_row[col], errors='coerce')
            if not pd.isna(numeric_value):
                new_row[col] = numeric_value + np.random.normal(0, abs(numeric_value)*0.05) # Add up to 5% random noise
        except:
            # If conversion fails or any other error occurs, skip augmentation for this value
            pass
  return new_row

augmented_rows_list = []

# Augment each of the first 100 rows multiple times to reach the target of 500 rows.
# We need 400 additional rows. We'll augment each of the initial 100 rows 4 times.
num_augmentations_per_row = 4

for index, row in rows_to_augment.iterrows():
  for _ in range(num_augmentations_per_row):
    augmented_row_data = augment_row(row)
    augmented_rows_list.append(augmented_row_data)

# Create a DataFrame from the augmented rows
augmented_data_df = pd.DataFrame(augmented_rows_list)

# Combine the original data with the augmented data
# We only need the original rows that were not augmented (from row 101 onwards)
remaining_original_data = data.iloc[100:].copy()

# Concatenate the augmented data with the remaining original data
# Reset the index of the augmented data to avoid duplicate index values
augmented_data_df = augmented_data_df.reset_index(drop=True)

# Combine the original 100 rows, the remaining original rows, and the augmented rows
# This approach keeps the first 100 original rows and adds the 400 augmented rows,
# and also keeps any original rows beyond the first 100.
# To get exactly 500 rows (100 original + 400 augmented), we should just combine
# the original first 100 rows with the augmented data.

combined_data = pd.concat([rows_to_augment, augmented_data_df], ignore_index=True)

print("Original number of rows:", data.shape[0])
print("Number of rows after augmentation:", combined_data.shape[0])
print(combined_data.head())
print(combined_data.tail())

# prompt: download the augmented dataset genetared before in csv file called 'augmented_dataset'

from google.colab import files

# Save the augmented dataframe to a CSV file
combined_data.to_csv('augmented_dataset.csv', index=False)

# Download the CSV file
files.download('augmented_dataset.csv')

"""***Data Preprocessing***"""

df = pd.read_csv('/content/augmented_dataset.csv')

df.head()

for col in df.columns:
  print (col)
  print(df[col].unique())
  print (10*'-')

df = df.drop(['startup_name','founder_age'], axis=1)

df = df.drop(['founder_experience_years','previous_startup_experience'], axis=1)

df.shape

#percentage of each unique val in founder_education

df['founder_education'].value_counts(normalize=True) * 100

df = df.drop(['founder_education'], axis=1)

#remove question marks from the founded year column

df['founded_year'] = df['founded_year'].astype(str).str.replace('?', '', regex=False)
df['founded_year'] = pd.to_numeric(df['founded_year'], errors='coerce')
print(df['founded_year'].unique())

"""***Clean City column***"""

print (df['city'].unique())

# convert Cairo/UK to Cairo and convert Asyut to Assiut and convert Aswin to Aswan

df['city'] = df['city'].str.replace('/UK', '', regex=False)
df['city'] = df['city'].str.replace(r'Port Said?', 'Portsaid', regex=False)
df['city'] = df['city'].str.replace(r'Port Said', 'Portsaid', regex=False)
df['city'] = df['city'].str.replace('Asyut', 'Assiut', regex=False)
df['city'] = df['city'].str.replace('Aswin', 'Aswan', regex=False)
print (df['city'].unique())

"""Continue..."""

df.info()

"""***initial_funding column***"""

#count of unique values in initial_funding column

print(df['initial_funding'].value_counts())

df = df.drop(['initial_funding'], axis=1)

df.shape

"""***number of employees column***"""

# prompt: show the count of unique vals in num_employees column

print(df['num_employees'].value_counts())

# prompt: remove '~' and '+' chars in num_employees column

df['num_employees'] = df['num_employees'].astype(str).str.replace('~', '', regex=False)
df['num_employees'] = df['num_employees'].str.replace('+', '', regex=False)
print(df['num_employees'].value_counts())

#convert 20 per branch to 20

df['num_employees'] = df['num_employees'].str.replace(' per branch', '', regex=False)
print(df['num_employees'].value_counts())

# prompt: fill null values in num_employees column

#fill null values using median

df['num_employees'] = pd.to_numeric(df['num_employees'], errors='coerce')
df['num_employees'] = df['num_employees'].fillna(df['num_employees'].median())
print(df['num_employees'].unique())
df.info()
print(df['num_employees'].value_counts())

print(df['num_employees'].value_counts())

# prompt: convert float vals to integer vals

df['num_employees'] = df['num_employees'].astype(int)
print(df['num_employees'].unique())
print(df['num_employees'].value_counts())
df.info()

"""***number of founder column***"""

# show the number of each unique value in the column num_founder

print(df['num_founders'].value_counts())

#fill the null values in the num_founders column

# Replace '—' with NaN for proper numerical handling
df['num_founders'] = df['num_founders'].replace('—', np.nan)

# Convert the column to numeric, coercing errors to NaN
df['num_founders'] = pd.to_numeric(df['num_founders'], errors='coerce')

# Assuming the missing values are represented as NaN
# We can fill NaNs with a median, mean, or a specific value (like 1 for founder count).
# Using median is generally safer if there are outliers.
# Let's check the distribution first to decide.
print(df['num_founders'].describe())
print(df['num_founders'].median())

# Option 1: Fill NaNs with the median of the column
df['num_founders'].fillna(df['num_founders'].median(), inplace=True)

# Option 2: Fill NaNs with a specific value (e.g., 1, assuming a single founder is a common scenario)
# df['num_founders'].fillna(1, inplace=True)

# Verify that NaNs have been filled
print("\nAfter filling NaNs:")
print(df['num_founders'].value_counts())
print(df['num_founders'].isnull().sum()) # Should be 0

"""***Online presence column***"""

#percentage of unique vals in the has_online_presence column
df['has_online_presence'].value_counts(normalize=True) * 100

"""***Continue ...***"""

df.info()

"""***Market competition level***"""

# prompt: show the counts of market_competition_level column including null vals

print(df['market_competition_level'].value_counts(dropna=False))

# prompt: fill null vals in this column

# Check the percentage of null values in the 'market_competition_level' column
print("Percentage of null values in 'market_competition_level':")
print(df['market_competition_level'].isnull().sum() / len(df) * 100)

# Based on the value counts and info() call, the null values are represented as NaN (checked by dropna=False in value_counts)
# Fill null values with the mode (most frequent value) as it's a categorical column
# Calculate the mode
mode_competition = df['market_competition_level'].mode()[0]

# Fill the null values
df['market_competition_level'].fillna(mode_competition, inplace=True)

# Verify that null values have been filled
print("\nAfter filling null values in 'market_competition_level':")
print(df['market_competition_level'].value_counts(dropna=False))
print(df['market_competition_level'].isnull().sum()) # Should be 0

# prompt: convert Low–Medium to Low

df['market_competition_level'] = df['market_competition_level'].replace('Low–Medium', 'Low')
print(df['market_competition_level'].value_counts(dropna=False))

"""***Startup Stage Column***"""

print(df['startup_stage'].value_counts())

# prompt: convert Concept to Market entry and Launch to Market entry and Initiative to Market entry and Market entry? to Market entry

df['startup_stage'] = df['startup_stage'].replace(['Concept', 'Launch', 'Initiative', 'Market entry?'], 'Market entry')

print(df['startup_stage'].value_counts())

# prompt: convert Market? to Market

df['startup_stage'] = df['startup_stage'].str.replace('?', '', regex=False)
print(df['startup_stage'].value_counts())

# prompt: convert Traction to Growth

df['startup_stage'] = df['startup_stage'].replace('Traction', 'Growth')
print(df['startup_stage'].value_counts())

"""***external funding column***"""

# prompt: print the count of unique values of got_external_funding column

print(df['got_external_funding'].value_counts())

# prompt: remove all '?' marks from got_external_funding column

df['got_external_funding'] = df['got_external_funding'].astype(str).str.replace('?', '', regex=False)
print(df['got_external_funding'].value_counts())

"""***Continue ...***"""

df.info()

"""***is_successful***"""

print(df['is_successful'].value_counts())

# prompt: remove '*' and '?' chars from the column

df['is_successful'] = df['is_successful'].astype(str).str.replace('*', '', regex=False)
df['is_successful'] = df['is_successful'].str.replace('?', '', regex=False)
print(df['is_successful'].value_counts())

# prompt: fill the missing val in is_successful with mode

# Assuming the missing values are represented as NaN after the previous cleaning steps
# Calculate the mode of the 'is_successful' column
mode_successful = df['is_successful'].mode()[0]

# Fill null values with the mode
df['is_successful'].fillna(mode_successful, inplace=True)

# Verify that null values have been filled
print("\nAfter filling null values in 'is_successful':")
print(df['is_successful'].value_counts(dropna=False))
print(df['is_successful'].isnull().sum()) # Should be 0

print(df['is_successful'].value_counts())

df.info()

"""***made_profit_in_3y***"""

print(df['made_profit_in_3y'].value_counts())

df=df.drop(['made_profit_in_3y'], axis=1)

"""***years_to_failure***"""

print(df['years_to_failure'].value_counts())

df = df.drop(['years_to_failure'], axis=1)

df.shape

"""***market_need_level***"""

print(df['market_need_level'].value_counts())

# prompt: fill nan vals with mode in market_need_level column

print(df['market_need_level'].value_counts(dropna=False))
print("Percentage of null values in 'market_need_level':")
print(df['market_need_level'].isnull().sum() / len(df) * 100)

# Calculate the mode
mode_market_need = df['market_need_level'].mode()[0]

# Fill the null values with the mode
df['market_need_level'].fillna(mode_market_need, inplace=True)

# Verify that null values have been filled
print("\nAfter filling null values in 'market_need_level':")
print(df['market_need_level'].value_counts(dropna=False))
print(df['market_need_level'].isnull().sum()) # Should be 0

"""***num_direct_competitors column***"""

# prompt: show counts of unique vals in  num_direct_competitors  column

print(df['num_direct_competitors'].value_counts(dropna=False))

# prompt: fill null values with mode in num_direct_competitors column

# Check the percentage of null values in the 'num_direct_competitors' column
print("Percentage of null values in 'num_direct_competitors':")
print(df['num_direct_competitors'].isnull().sum() / len(df) * 100)

# Based on the value counts and info() call, the null values are represented as NaN (checked by dropna=False in value_counts)
# Fill null values with the mode (most frequent value) as it's likely a discrete numerical column
# Calculate the mode
mode_competitors = df['num_direct_competitors'].mode()[0]

# Fill the null values
df['num_direct_competitors'].fillna(mode_competitors, inplace=True)

# Verify that null values have been filled
print("\nAfter filling null values in 'num_direct_competitors':")
print(df['num_direct_competitors'].value_counts(dropna=False))
print(df['num_direct_competitors'].isnull().sum()) # Should be 0

"""***Incubator Support Column***"""

print(df['incubator_support'].value_counts())

print(df['incubator_support'].unique())

# prompt: fill nan values with mode

# Based on the value counts and info() call, the null values are represented as NaN (checked by dropna=False in value_counts)
# Fill null values with the mode (most frequent value) as it's a categorical column
# Calculate the mode
mode_incubator = df['incubator_support'].mode()[0]

# Fill the null values
df['incubator_support'].fillna(mode_incubator, inplace=True)

# Verify that null values have been filled
print("\nAfter filling null values in 'incubator_support':")
print(df['incubator_support'].value_counts(dropna=False))
print(df['incubator_support'].isnull().sum()) # Should be 0

# prompt: convert float vals to int vals in incubator_support column

df['incubator_support'] = df['incubator_support'].astype(int)
print(df['incubator_support'].value_counts())
print(df['incubator_support'].unique())



"""***check data after cleaning***"""

df.info()

# prompt: print unique values in each column

for col in df.columns:
  print(f"Unique values in column '{col}':")
  print(df[col].unique())
  print("-" * 20)

# prompt: save the df in csv file called 'cleaned_augmented_success_prediction_dataset' and download it

# Save the cleaned DataFrame to a CSV file
df.to_csv('cleaned_augmented_success_prediction_dataset.csv', index=False)

# Download the CSV file
files.download('cleaned_augmented_success_prediction_dataset.csv')