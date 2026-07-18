import pandas as pd
import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine,types

load_dotenv()

def load_verified_data_to_sql(file_path):
    print("\n---=== STARTING SQL INGESTION===---")
    try:
        df= pd.read_csv(file_path)
        print(f"\nSuccesfully loaded the {len(df)} rows from the CSV storage...")
    except:
        print(f"\nPIPELINE ERROR : Verified file not found : {file_path}")
        sys.exit(1)
    
    USER=os.getenv("DB_USER")
    PASSWORD=os.getenv("DB_PASSWORD")
    HOST=os.getenv("DB_HOST")
    PORT=os.getenv("DB_PORT")
    DATABASE=os.getenv("DB_NAME")

    if not all(['USER','PASSWORD','HOST','PORT','DATABASE']):
        print("\nCONFIGURATION ERROR : Please check your .env file credentials ")
        sys.exit(1)
    
    connection_string= f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
    engine = create_engine(connection_string)
    
    df["Join_Date"] = pd.to_datetime(
    df["Join_Date"],
    format="%d/%m/%Y"
    )

    explicit_schema_map = {
        'Employee_ID': types.VARCHAR(20),
        'First_Name': types.VARCHAR(100),
        'Last_Name': types.VARCHAR(100),
        'Age': types.INTEGER(),
        'Status': types.VARCHAR(50),
        'Join_Date': types.DATE(),
        'Salary': types.DECIMAL(10,2),
        'Email': types.VARCHAR(255),
        'Phone': types.VARCHAR(10),
        'Performance_Score': types.VARCHAR(15),
        'Remote_Work': types.VARCHAR(20),
        'Department': types.VARCHAR(100),
        'Region': types.VARCHAR(100),
        'phno_is_valid': types.VARCHAR(10)
    }

    table_name = 'Employees'
    try:
        df.to_sql(
            name=table_name,
            con=engine,
            if_exists='replace',
            index=False,
            dtype=explicit_schema_map
        )
        print(f"TABLE {table_name} CREATED IN YOUR {DATABASE} DATABASE...\n")
    except Exception as e:
        print(f"INGESTION FAILURE : Database server rejected.\n Details : {e}")
        sys.exit(1)
    

if __name__ == "__main__":
    load_verified_data_to_sql('../data/cleaned/Cleaned_Employee_Dataset.csv')