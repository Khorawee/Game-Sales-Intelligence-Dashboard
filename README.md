# 🎮 Game Sales Intelligence Dashboard

Full-stack analytics platform with MySQL, Streamlit, and ML prediction for video game sales analysis.

## 🚀 Quick Setup

### 1. Clone & Install
```bash
git clone (https://github.com/Khorawee/Game-Sales-Intelligence-Dashboard.git)
cd game-sales-dashboard
pip install -r requirements.txt
```

### 2. Create `.env` File
```env
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_NAME=game_sales
```

### 3. Setup Database
```bash
mysql -u root -p < game_sales_schema.sql
python init_database.py
```

### 4. Train Model & Run
```bash
python train_model.py
streamlit run app.py
```

## 📁 Required Files

```
game-sales-dashboard/
├── app.py                    # Main dashboard
├── train_model.py            # ML training
├── init_database.py          # Database setup
├── preprocessor.py           # Data preprocessing
├── game_sales_schema.sql     # Database schema
├── requirements.txt          # Dependencies
├── .env                      # Config (CREATE THIS)
├── data/
│   └── vgsales.csv          # Source data
└── models/                   # Created after training
    ├── model_xgb.pkl
    ├── model_rf.pkl
    ├── model_et.pkl
    └── preprocessor.pkl
```

## ✅ What to Create

### Must Create:
1. **`.env`** - Database credentials
2. **`data/` folder** - Put `vgsales.csv` inside
3. **MySQL database** - Run schema SQL first

### Auto-Generated:
- `models/` folder (after running `train_model.py`)
- `.pkl` model files (after training)

## 🛠️ Tech Stack

**Backend:** Python, MySQL, SQLAlchemy, Pandas  
**Frontend:** Streamlit, Plotly  
**ML:** XGBoost, Scikit-learn, Category Encoders

## 📊 Features

- 📈 Sales trends & rankings
- 🌍 Regional analysis
- 🔥 Platform × Genre heatmap
- 🔗 Correlation analysis
- 🔮 ML-powered predictions (R² 0.85+)
- 🎛️ Real-time filters

## 📝 Step-by-Step Guide

### Step 1: Prepare Database
```bash
# Login to MySQL
mysql -u root -p

# Create database
CREATE DATABASE game_sales;
exit;

# Import schema
mysql -u root -p < game_sales_schema.sql
```

### Step 2: Prepare Data
```bash
# Create data folder
mkdir data

# Put vgsales.csv in data/ folder
# Then load data
python init_database.py
```

### Step 3: Train ML Model
```bash
python train_model.py
# Wait 5-10 minutes for training
# Models saved in models/ folder
```

### Step 4: Run Dashboard
```bash
streamlit run app.py
# Open browser: http://localhost:8501
```
