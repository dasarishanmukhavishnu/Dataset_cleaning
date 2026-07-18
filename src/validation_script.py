import pandas as pd 
import numpy as np 
import sys

def data_validation_pipeline(file_path):
    print("\n---=== STARTING DATA QUALITY AUDIT(DQA)===---")
    
    try:
        df= pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"\nThe filepath :'{file_path}' doesn't exsist please check you cleaning script or path")
        sys.exit(1)

    failures = 0
    critical_col = ['Employee_ID','First_Name','Last_Name','Age','Join_Date','Salary','Email']
    null_count = df[critical_col].isnull().sum()

    if null_count.sum() == 0:
        print("\nTest 1 : PASSED (0% MISSING VALUES)")
    else:
        print(f"\nTest 1 : FAILED FOUND MISSING VALUES IN : {null_count[null_count > 0]}")
        failures += 1
    
    duplicates = df.duplicated(subset= ['First_Name','Last_Name','Join_Date','Salary','Email','Department','Region']).sum()
    if duplicates == 0:
        print("Test 2 : PASSED (NO EXACT DUPLICATE)")
    else:
        print(f"Test 2 : FAILED THERE ARE {duplicates} DUPLICATED ROWS")
        failures += 1
    
    invalid_dates = df['Join_Date'].astype(str).str.contains('NaN|None|NaT',case=False).sum()
    strict_indian_pattern = r'^(?:0[1-9]|[1-2][0-9]|3[0-1])\/(?:0[1-9]|1[0-2])\/\d{4}$'
    wrong_format_count = df[~df['Join_Date'].astype(str).str.match(strict_indian_pattern,na=False)].shape[0]
    wrong_length = (df['Join_Date'].astype(str).str.len() != 10).sum()

    if invalid_dates == 0 and wrong_format_count == 0 and wrong_length == 0:
        print("Test 3 : DATE FORMAT CHECK PASSED ")
    else:
        print("Test 3 : FAILED")
        failures += 1
    
    invalid_phone = df[(df['phno_is_valid'] == True) & (df['Phone'].astype(str).str.len() != 10)].shape[0]
    wrong_length = (df['Phone'].astype(str).str.len() != 10).sum()
    if invalid_phone == 0:
        print("Test 4 : PHONE NUMBERS CHECK PASSED")
        print(f"BUT THERE ARE {wrong_length} WRONG PHONE NUMBER ENTRIES... ")
    else:
        print(f"Test 4 : FAILED THERE ARE {invalid_phone} INVALID PH_NO")
        failures += 1
    
    print("\n======================================================")

    if failures == 0:
        print("SUCESS 100% CLEAN")
        print("THE DATA QUALITY AUDIT SUCESSFULLY COMPLETED DATA IS READY FOR SQL INGESTION\n")
        return True
    else:
        print(f"THE DATA QUALITY AUDIT FAILED BECAUSE OF {failures} FAILURES WHILE PROCESSING...!\n")
        return False

if __name__ == "__main__":
    data_validation_pipeline('../data/cleaned/Cleaned_Employee_Dataset.csv')