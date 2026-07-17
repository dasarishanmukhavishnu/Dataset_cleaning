import pandas as pd
import numpy as np

data = pd.read_csv('../data/raw/Messy_Employee_dataset.csv')
raw_df = pd.DataFrame(data)
df = raw_df.copy()

print("\n---===  DATA INSPECTION  ===---")
print(df.head(20).to_string(index=False))
print(df.sample())

print(df.shape)
print(df.info())

print("\n---=== MISSING VALUES ===---")
print(df.isnull().sum()/len(df)*100)

print("\n---=== PRIMARY KEY===---")
print(f"Employee_ID : {df['Employee_ID'].astype(str).str.strip().is_unique}")

print("\n---=== DUPLICATE ROWS===---")
#df = df[df.duplicated()]    # According to the duplicated command the whole rows are not duplicated
df_dup = df[df.duplicated(subset=['First_Name','Last_Name','Email'])]
df_dup = df_dup.sort_values(by=['First_Name','Last_Name','Email'])  # By this line we can say that the first,last names and email are same but not all the persons are different
print(f"Original shape : {df.shape}")  
print(f"Dup_names and Emails : {df_dup.shape}")  # you can see the shape as per the 8 unique first and last names you get 64 unique names but 1020 rows means dups are present around 956 rows of same names

print("\n---=== NUMERICAL COLUMNS SUMMARY===---")
print(df.describe().round())

print("\n---=== CATEGORICAL COLUMNS===---")
for col in ['Status','Performance_Score','Remote_Work']:
    print(f"Percentage : {df[col].value_counts()/len(df)*100}")

if df['Age'].isnull().sum() > 0:   # age null values are filled 
    age_median = df['Age'].median()
    df['Age'] = df['Age'].fillna(age_median).astype(int)

if 'Department_Region' in df.columns:
    df[['Department','Region']] = df['Department_Region'].str.split('-',expand=True)
    df = df.drop(columns=['Department_Region'])

if 'Join_Date' in df.columns:
    df['Join_Date'] = df['Join_Date'].astype(str).str.strip()
    df['Join_Date'] = pd.to_datetime(df['Join_Date'], format='mixed', errors='coerce')
    df['Join_Date'] = df['Join_Date'].dt.strftime('%d/%m/%Y')

if df['Salary'].isnull().sum() > 0:
    avg_salary = df['Salary'].mean()
    df['Salary'] = df['Salary'].fillna(avg_salary).round(2)

df = df.sort_values(by=['Email','Join_Date'])
#df['Employee_Log_Times'] = df.groupby('Email').cumcount()

df['Phone'] = df['Phone'].abs().astype(str).str.strip('[]')
df['phno_is_valid'] = np.where(df['Phone'].str.len() != 10,False,True)

print(f"The number of True and False (%) of ph_no : {df['phno_is_valid'].value_counts()/len(df)*100}")
df_clean  = df.drop_duplicates(subset=['First_Name','Last_Name','Email','Join_Date','Department','Region','Salary'],keep='first')


print("\n---=== DATA INSCPECTION AFTER CLEANING===---")
print(df_clean.head(20).to_string(index=False))
print(df_clean.sample())
print(df_clean.info())
print(df_clean.isnull().sum()/len(df)*100)

print(f"Original shape : {df.shape}")  
print(f"Cleaned shape : {df_clean.shape}")  
df_clean = df_clean.sort_values(by='Employee_ID').reset_index(drop=True)
print(df_clean)
df_clean.to_csv('../data/cleaned/Cleaned_Employee_Dataset.csv',index=False)