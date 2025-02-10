import pandas as pd
from pathlib import Path

def read_sector_data(sector_file_path):
    """Read sector data CSV file"""
    try:
        print(f"\nReading sector data from: {sector_file_path}")
        sector_df = pd.read_csv(sector_file_path)
        
        # Clean column names
        sector_df.columns = [col.strip().lower() for col in sector_df.columns]
        
        # Display data quality checks
        print("\nSector Data Quality Checks:")
        print(f"Shape: {sector_df.shape}")
        print("\nColumns:", sector_df.columns.tolist())
        print("\nFirst few rows:")
        print(sector_df.head())
        print("\nMissing values:")
        print(sector_df.isnull().sum())
        
        return sector_df
        
    except Exception as e:
        print(f"Error reading sector data: {str(e)}")
        return None

def save_to_mysql(df, table_name, mysql_config):
    """Save DataFrame to MySQL database"""
    try:
        from sqlalchemy import create_engine
        
        connection_string = (
            f"mysql+pymysql://{mysql_config['user']}:{mysql_config['password']}"
            f"@{mysql_config['host']}/{mysql_config['database']}"
        )
        engine = create_engine(connection_string)
        
        # Save to MySQL
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"Successfully saved data to MySQL table: {table_name}")
        
    except Exception as e:
        print(f"Error saving to MySQL: {str(e)}")

def main():
    # Set your paths and configurations
    sector_file_path = r"D:\stock_analysis\sector_data.csv"
    
    mysql_config = {
        'host': 'user_hostname',
        'user': 'username',
        'password': 'user_password',
        'database': 'stock_analysis'
    }
    
    # Read and process sector data
    print("\nProcessing Sector Data:")
    sector_df = read_sector_data(sector_file_path)
    
    if sector_df is not None:
        print("\nSuccessfully read sector data")
        print(f"Total rows: {len(sector_df)}")
        
        # Save sector data to MySQL
        save_to_mysql(sector_df, 'sector_data', mysql_config)
    else:
        print("Failed to read sector data. Please check the errors above.")

if __name__ == "__main__":
    main()
