import pandas as pd
from pathlib import Path
import os
from datetime import datetime

def convert_excel_date(excel_date):
    """Convert Excel date number to datetime"""
    try:
        return pd.Timestamp('1899-12-30') + pd.Timedelta(days=float(excel_date))
    except:
        return None

def read_stock_data(csv_folder_path):
    """Read all CSV files and combine them into a single DataFrame"""
    all_data = []
    
    # Convert to Path object and ensure folder exists
    folder_path = Path(csv_folder_path)
    if not folder_path.exists():
        print(f"Error: Folder {csv_folder_path} does not exist")
        return None
    
    # List all CSV files
    csv_files = list(folder_path.glob('*.csv'))
    if not csv_files:
        print(f"Error: No CSV files found in {csv_folder_path}")
        return None
    
    print(f"Found {len(csv_files)} CSV files")
    
    # Read each file
    for file in csv_files:
        try:
            print(f"Reading file: {file}")
            # Read CSV file
            df = pd.read_csv(file)
            
            # Check if DataFrame is empty
            if df.empty:
                print(f"Warning: {file} is empty")
                continue
            
            # Clean column names
            df.columns = [col.strip().lower() for col in df.columns]
            
            # Convert date and month columns from Excel format
            if 'date' in df.columns:
                df['date'] = df['date'].apply(convert_excel_date)
            
            if 'month' in df.columns:
                df['month'] = pd.to_datetime(df['month'], format='%Y-%m')
            
            # Convert numeric columns
            numeric_cols = ['open', 'high', 'low', 'close', 'volume']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Extract symbol from filename (remove '_data.csv')
            symbol = file.stem.split('_')[0]
            df['symbol'] = symbol
            
            print(f"Processed {symbol} - Shape: {df.shape}")
            all_data.append(df)
            
        except Exception as e:
            print(f"Error reading {file}: {str(e)}")
            continue
    
    if not all_data:
        print("Error: No data could be read from any CSV files")
        return None
    
    # Combine all DataFrames
    print("Combining all DataFrames...")
    combined_df = pd.concat(all_data, ignore_index=True)
    print(f"Final combined shape: {combined_df.shape}")
    
    # Sort by symbol and date
    combined_df = combined_df.sort_values(['symbol',  'date'])
    
    return combined_df

def save_to_mysql(df, mysql_config):
    """Save DataFrame to MySQL database"""
    try:
        from sqlalchemy import create_engine
        
        # Create SQLAlchemy engine
        connection_string = (
            f"mysql+pymysql://{mysql_config['user']}:{mysql_config['password']}"
            f"@{mysql_config['host']}/{mysql_config['database']}"
        )
        engine = create_engine(connection_string)
        
        # Save to MySQL
        df.to_sql('stock_data', engine, if_exists='replace', index=False)
        print("Successfully saved data to MySQL")
        
    except Exception as e:
        print(f"Error saving to MySQL: {str(e)}")

def main():
    # Set your paths and configurations
    csv_folder_path = r"D:\stock_analysis\csv_folder_path"
    
    mysql_config = {
         'host': 'user_hostname',
        'user': 'username',
        'password': 'user_password',
        'database': 'stock_analysis'
    }
    
    print(f"Reading data from folder: {csv_folder_path}")
    df = read_stock_data(csv_folder_path)
    
    if df is not None:
        print("\nSuccessfully read data")
        print(f"Total rows: {len(df)}")
        print(f"Columns: {df.columns.tolist()}")
        
        # Display sample data
        print("\nFirst few rows of data:")
        print(df.head())
        
        # Display summary statistics
        print("\nBasic statistics:")
        numeric_cols = ['open', 'high', 'low', 'close', 'volume']
        print(df[numeric_cols].describe())
        
        # Save to MySQL
        save_to_mysql(df, mysql_config)
    else:
        print("Failed to read data. Please check the errors above.")

if __name__ == "__main__":
    main()

