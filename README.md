# Game-Sales-Dashboard
🎮 Game Sales Intelligence Dashboard
A comprehensive full-stack data analytics platform that combines interactive visualization, database management, and machine learning to analyze and predict video game sales trends across multiple regions and platforms.

📊 Features
Interactive Dashboard

Real-time Filtering - Dynamic filters for platforms and genres
6 Analysis Tabs - Comprehensive views of sales data
Responsive Design - Glass-morphism UI with smooth animations

Visualizations

📈 Trends Analysis - Time-series sales trends
🏆 Rankings - Top publishers, genres, and games
🌍 Regional Distribution - Sales by geographic region
🔥 Heatmaps - Platform × Genre sales matrix
🔗 Correlation Analysis - Feature relationship exploration
🔮 ML Predictions - Sales forecasting with XGBoost

Machine Learning

XGBoost Regressor - Trained on 16,000+ game records
Feature Engineering - Publisher track records, platform popularity
Model Performance - R² score of 0.85+
Real-time Predictions - Instant sales forecasting

🚀 Quick Start
Prerequisites
bashPython 3.8+
MySQL 8.0+
pip (Python package manager)
Installation

Clone the repository

bashgit clone https://github.com/yourusername/game-sales-dashboard.git
cd game-sales-dashboard

Install dependencies

bashpip install -r requirements.txt

Setup environment variables
Create a .env file in the root directory:

envDB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_NAME=game_sales

Initialize database

bash# Create database schema
mysql -u root -p < game_sales_schema.sql

# Load data
python init_database.py

Train ML model

bashpython train_model.py

Run the dashboard

bashstreamlit run app.py
Visit http://localhost:8501 in your browser.
📁 Project Structure
game-sales-dashboard/
│
├── app.py                      # Main Streamlit dashboard
├── train_model.py              # ML model training script
├── init_database.py            # Database initialization
├── preprocessor.py             # Custom data preprocessor
├── game_sales_schema.sql       # Database schema
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (create this)
│
├── data/
│   └── vgsales.csv            # Source data
│
├── models/
│   ├── model_xgb.pkl          # Trained XGBoost model
│   ├── model_rf.pkl           # Random Forest model
│   ├── model_et.pkl           # Extra Trees model
│   └── preprocessor.pkl       # Fitted preprocessor
│
└── README.md
🗄️ Database Schema
Tables

vgsales - Main fact table with game sales data
platform - Gaming platforms (PS4, Xbox, etc.)
genre - Game genres (Action, Sports, etc.)
publisher - Game publishers
predictions - ML prediction results
model_info - ML model metadata

Normalized Design (3NF)

Foreign key relationships
Indexed for fast queries
Unique constraints on game + platform + year

🤖 Machine Learning Pipeline
Data Preprocessing

Target Encoding - Publisher names
One-Hot Encoding - Platform and Genre
Feature Engineering:

Total known sales
Publisher average sales
Platform game count



Model Training

Algorithm: XGBoost Regressor
Hyperparameter Tuning: RandomizedSearchCV
Cross-Validation: 5-fold
Metrics: RMSE, R²

Model Performance
XGBoost    → R²: 0.85+  | RMSE: ~0.8
RandomForest → R²: 0.82  | RMSE: ~0.9
ExtraTrees   → R²: 0.81  | RMSE: ~0.95
📊 Dashboard Tabs
1. 📈 Trends

Global sales over time
Peak year identification
Annual sales averages

2. 🏆 Rankings

Top 10 publishers by sales
Top 10 genres by sales
Top 10 best-selling games
Quick statistics

3. 🌍 Regions

Regional sales distribution (NA, EU, JP, Other)
Bar charts and pie charts
Market share analysis

4. 🔥 Heatmap

Platform × Genre sales matrix
Top 10 genres × Top 12 platforms
Best combination insights

5. 🔗 Correlations

Feature correlation matrix
Scatter plot analysis
Relationship insights

6. 🔮 ML Prediction

Interactive prediction form
Real-time sales forecasting
Visual result comparison

🛠️ Technologies Used
Backend

Python 3.8+ - Core programming language
MySQL 8.0+ - Relational database
SQLAlchemy - Database ORM
Pandas - Data manipulation
NumPy - Numerical computing

Frontend

Streamlit - Web framework
Plotly - Interactive visualizations
HTML/CSS - Custom styling

Machine Learning

Scikit-learn - ML algorithms and preprocessing
XGBoost - Gradient boosting
Category Encoders - Target encoding
Joblib - Model serialization

📈 Usage Examples
Filter Data
python# Select platforms in sidebar
selected_platform = ["PS4", "Xbox One", "PC"]

# Select genres
selected_genre = ["Action", "Sports"]
Make Predictions
python# Input game details
Platform: PS4
Genre: Action
Publisher: Electronic Arts
Year: 2024
Regional Sales: NA=2.0M, EU=1.5M, JP=0.5M, Other=0.3M

# Get prediction
Predicted Global Sales: 4.8M Units
🔧 Configuration
Database Settings
Edit .env file:
envDB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_NAME=game_sales
Model Parameters
Edit train_model.py:
pythonxgb_params = {
    "n_estimators": [200, 300, 400],
    "max_depth": [4, 5, 6, 7],
    "learning_rate": [0.02, 0.03, 0.05]
}
📝 Data Source
The dataset contains video game sales data with:

16,000+ game records
31 platforms
12 genres
Sales regions: North America, Europe, Japan, Other
Time period: 1980-2020
