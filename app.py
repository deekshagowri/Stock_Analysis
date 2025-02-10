import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from sqlalchemy import create_engine

class StockAnalysisDashboard:
    def __init__(self):
        """Initialize the dashboard with database connection and initial data."""
        # Database configuration
        self.mysql_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'Deeksha!18',
            'database': 'stock_analysis'
        }
        
        # Set page configuration
        st.set_page_config(
            page_title="Stock Market Analysis",
            page_icon="📈",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Apply custom CSS
        self.apply_custom_css()
        
        # Create SQLAlchemy engine
        self.engine = create_engine(
            f"mysql+pymysql://{self.mysql_config['user']}:{self.mysql_config['password']}"
            f"@{self.mysql_config['host']}/{self.mysql_config['database']}"
        )
        
        # Load data
        self.load_data()

    def apply_custom_css(self):
        """Apply custom CSS styling to the dashboard."""
        st.markdown("""
            <style>
                .stApp {
                    background-color: #f5f5f5;
                }
                .main {
                    padding: 2rem;
                }
                .metric-card {
                    background-color: white;
                    padding: 1rem;
                    border-radius: 0.5rem;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                .chart-container {
                    background-color: white;
                    padding: 1rem;
                    border-radius: 0.5rem;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    margin: 1rem 0;
                }
                .sidebar .sidebar-content {
                    background-color: #262730;
                }
                h1, h2, h3 {
                    color: #1f1f1f;
                }
            </style>
        """, unsafe_allow_html=True)
    
    def load_data(self):
        """Load stock data from MySQL database or create dummy data."""
        try:
            self.stock_data = pd.read_sql('SELECT * FROM stock_data', self.engine)
            self.preprocess_data()
        except Exception as e:
            st.error(f"Error loading data: {e}")
            self.create_dummy_data()
    
    def create_dummy_data(self):
        """Create dummy data for demonstration."""
        np.random.seed(42)
        dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
        symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'META']
        
        data = []
        for symbol in symbols:
            base_price = np.random.randint(50, 500)
            volatility = np.random.uniform(0.01, 0.03)
            symbol_data = pd.DataFrame({
                'date': dates,
                'symbol': symbol,
                'close': base_price * (1 + np.random.normal(0, volatility, len(dates))).cumprod()
            })
            data.append(symbol_data)
        
        self.stock_data = pd.concat(data, ignore_index=True)
    
    def preprocess_data(self):
        """Preprocess the loaded data for analysis."""
        self.stock_data['date'] = pd.to_datetime(self.stock_data['date'])
        self.stock_data['daily_return'] = self.stock_data.groupby('symbol')['close'].pct_change()
        self.stock_data['cumulative_return'] = (1 + self.stock_data['daily_return']).cumprod() - 1
    
    def render_dashboard(self):
        """Main method to render the Streamlit dashboard."""
        # Sidebar navigation
        with st.sidebar:
            st.image("https://www.example.com/logo.png", width=50)  # Replace with your logo
            st.title("Navigation")
            analysis_type = st.radio(
                'Select Analysis Type',
                ['Home', 'Market Overview', 'Stock Performance', 'Volatility Analysis', 'Correlation Matrix']
            )
        
        # Render appropriate analysis based on selection
        if analysis_type == 'Home':
            self.render_home_page()
        elif analysis_type == 'Market Overview':
            self.render_market_overview()
        elif analysis_type == 'Stock Performance':
            self.render_stock_performance()
        elif analysis_type == 'Volatility Analysis':
            self.render_volatility_analysis()
        else:
            self.render_correlation_matrix()

    def render_home_page(self):
        """Render an attractive home page with key metrics and market summary."""
        st.title("📊 Stock Market Analytics Hub")
        
        # Welcome message
        st.markdown("""
            <div style='background-color: white; padding: 1.5rem; border-radius: 0.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                <h2>Welcome to the Stock Market Analytics Dashboard</h2>
                <p>Your comprehensive platform for market analysis and stock performance tracking.</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Key metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        # Calculate metrics
        total_stocks = self.stock_data['symbol'].nunique()
        avg_return = self.stock_data.groupby('symbol')['daily_return'].mean().mean() * 100
        volatility = self.stock_data['daily_return'].std() * 100
        market_trend = "🟢 Bullish" if avg_return > 0 else "🔴 Bearish"
        
        with col1:
            self.metric_card("Total Stocks", f"{total_stocks}", "📈")
        with col2:
            self.metric_card("Avg Return", f"{avg_return:.2f}%", "💹")
        with col3:
            self.metric_card("Volatility", f"{volatility:.2f}%", "📊")
        with col4:
            self.metric_card("Market Trend", market_trend, "🎯")
        
        # Market summary
        st.markdown("### Recent Market Summary")
        latest_date = self.stock_data['date'].max()
        recent_data = self.stock_data[self.stock_data['date'] == latest_date]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=recent_data['symbol'],
            y=recent_data['daily_return'] * 100,
            marker_color=['red' if x < 0 else 'green' for x in recent_data['daily_return']],
            name='Daily Returns'
        ))
        fig.update_layout(
            title='Latest Daily Returns by Stock',
            xaxis_title='Stock Symbol',
            yaxis_title='Daily Return (%)',
            template='plotly_white'
        )
        st.plotly_chart(fig, use_container_width=True)

    def metric_card(self, title, value, icon):
        """Create a styled metric card."""
        st.markdown(f"""
            <div class='metric-card'>
                <h3>{icon} {title}</h3>
                <h2>{value}</h2>
            </div>
        """, unsafe_allow_html=True)
    
    def render_market_overview(self):
        """Render market overview with key metrics and insights."""
        st.title('📈 Market Overview')
        
        # Calculate metrics
        total_stocks = self.stock_data['symbol'].nunique()
        green_stocks = self.stock_data.groupby('symbol')['daily_return'].mean() > 0
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric('Total Stocks', total_stocks)
            st.metric('Green Stocks', sum(green_stocks))
        
        with col2:
            st.metric('Red Stocks', total_stocks - sum(green_stocks))
        
        # Top 10 performing stocks
        top_performers = self.stock_data.groupby('symbol')['cumulative_return'].last().nlargest(10)
        
        st.subheader('🏆 Top 10 Performing Stocks')
        fig = px.bar(
            x=top_performers.index,
            y=top_performers.values * 100,
            labels={'x':'Symbol', 'y':'Cumulative Return (%)'},
            template='plotly_white'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    def render_stock_performance(self):
        """Detailed stock performance analysis with interactive elements."""
        st.title('📊 Stock Performance Analysis')
        
        selected_stocks = st.multiselect(
            'Select Stocks to Analyze',
            self.stock_data['symbol'].unique().tolist(),
            default=self.stock_data['symbol'].unique()[:3]
        )
        
        if not selected_stocks:
            st.warning("Please select at least one stock.")
            return
        
        filtered_data = self.stock_data[self.stock_data['symbol'].isin(selected_stocks)]
        
        fig = go.Figure()
        for stock in selected_stocks:
            stock_data = filtered_data[filtered_data['symbol'] == stock]
            fig.add_trace(go.Scatter(
                x=stock_data['date'],
                y=stock_data['cumulative_return'] * 100,
                mode='lines',
                name=stock
            ))
        
        fig.update_layout(
            title='Cumulative Returns Over Time',
            xaxis_title='Date',
            yaxis_title='Cumulative Return (%)',
            template='plotly_white',
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    def render_volatility_analysis(self):
        """Volatility analysis with standard deviation of returns."""
        st.title('📉 Stock Volatility Analysis')
        
        volatility = self.stock_data.groupby('symbol')['daily_return'].std() * 100
        top_volatile = volatility.nlargest(10)
        
        if top_volatile.empty:
            st.warning("Not enough data to calculate volatility.")
            return
        
        fig = px.bar(
            x=top_volatile.index,
            y=top_volatile.values,
            labels={'x':'Symbol', 'y':'Volatility (%)'},
            title='Top 10 Most Volatile Stocks',
            template='plotly_white'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    def render_correlation_matrix(self):
        """Stock price correlation heatmap."""
        st.title('🔄 Stock Correlation Analysis')
        
        correlation_data = self.stock_data.pivot_table(
            index='date',
            columns='symbol',
            values='close'
        )
        
        correlation_matrix = correlation_data.corr()
        
        if correlation_matrix.empty:
            st.warning("Not enough data to calculate correlation matrix.")
            return
        
        fig = px.imshow(
            correlation_matrix,
            labels=dict(x="Stock", y="Stock", color="Correlation"),
            x=correlation_matrix.columns,
            y=correlation_matrix.index,
            color_continuous_scale='RdBu_r',
            template='plotly_white'
        )
        fig.update_layout(
            title='Stock Price Correlation Heatmap',
            width=800,
            height=800
        )
        st.plotly_chart(fig, use_container_width=True)

def main():
    """Main function to run the Streamlit application."""
    dashboard = StockAnalysisDashboard()
    dashboard.render_dashboard()

if __name__ == '__main__':
    main()
