# Stock Market Analysis Project

## Overview
This project provides a comprehensive solution for analyzing stock market data, featuring both a real-time interactive Streamlit dashboard and Power BI visualizations. The system processes stock data from multiple sources, stores it in a MySQL database, and provides various analytical tools for market analysis.

## Features
- Data processing pipeline for converting YAML to CSV format
- MySQL database integration for efficient data storage
- Interactive Streamlit dashboard with real-time analysis
- Power BI dashboard for detailed stock performance visualization
- Technical analysis indicators and metrics
- Sector-wise performance analysis
- Volume analysis and trading patterns

## Project Structure
```
stock_analysis/
├── legacy/
│   └── stock_analysis.py    # Original analysis script
├── src/
│   ├── __init__.py
│   ├── dashboard.py         # Enhanced Streamlit dashboard
│   ├── data_processor.py    # Data processing utilities
│   └── config.py           # Configuration settings
├── powerbi/
│   └── stock_analysis.pbix  # Power BI dashboard file
├── requirements.txt
└── README.md
```

## Prerequisites
- Python 3.8 or higher
- MySQL Server
- Power BI Desktop (for visualization dashboard)
- Required Python packages (listed in requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/stock-analysis.git
cd stock-analysis
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Set up MySQL database:
```sql
CREATE DATABASE stock_analysis;
USE stock_analysis;

-- Create stock_data table
CREATE TABLE stock_data (
    date DATE,
    symbol VARCHAR(10),
    open FLOAT,
    high FLOAT,
    low FLOAT,
    close FLOAT,
    volume BIGINT,
    PRIMARY KEY (date, symbol)
);

-- Create sector_data table
CREATE TABLE sector_data (
    symbol VARCHAR(10) PRIMARY KEY,
    sector VARCHAR(50),
    industry VARCHAR(50)
);
```

5. Configure database connection:
Update the MySQL configuration in `src/config.py` with your credentials:
```python
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'stock_analysis'
}
```

## Usage

### Data Processing
To process and load stock data:
```python
python src/data_processor.py
```

### Streamlit Dashboard
To run the interactive dashboard:
```bash
streamlit run src/dashboard.py
```

### Power BI Dashboard
1. Open Power BI Desktop
2. Open the `powerbi/stock_analysis.pbix` file
3. Refresh data connection with your MySQL database

## Features Detail

### Streamlit Dashboard
- Real-time stock price monitoring
- Technical indicators visualization
- Volume analysis
- Sector performance comparison
- Custom date range selection
- Interactive charts and graphs

### Power BI Visualizations
- Stock performance metrics
- Sector-wise analysis
- Heat maps
- Correlation matrices
- Custom DAX measures for advanced analytics

## Data Processing Pipeline
The project includes a robust data processing pipeline that:
1. Converts YAML files to CSV format
2. Cleans and validates data
3. Calculates technical indicators
4. Loads processed data into MySQL database

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Technical Documentation

### Key Components

#### Data Processor
- Handles YAML to CSV conversion
- Implements data validation and cleaning
- Manages database operations

#### Streamlit Dashboard
- Real-time data visualization
- Interactive user interface
- Technical analysis tools

#### Power BI Integration
- Custom DAX measures
- Advanced visualizations
- Sector analysis

### Performance Optimization
- Efficient SQL queries
- Data caching for faster retrieval
- Optimized data structures

## Troubleshooting

### Common Issues

1. Database Connection Errors
```python
# Check database connection
from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://user:password@localhost/stock_analysis')
try:
    connection = engine.connect()
    print("Database connection successful")
except Exception as e:
    print(f"Error connecting to database: {e}")
```

2. Data Loading Issues
- Verify CSV file format
- Check data types in MySQL tables
- Ensure sufficient disk space

3. Visualization Errors
- Update Streamlit to latest version
- Verify data integrity
- Check Python package versions

## License
This project is licensed under the MIT License - see the LICENSE file for details

## Acknowledgments
- Data provided by [Your Data Source]
- Built with Streamlit and Power BI
- Python data analysis community

## Contact
Your Name - [@yourtwitter](https://twitter.com/yourtwitter)
Project Link: [https://github.com/yourusername/stock-analysis](https://github.com/yourusername/stock-analysis)
