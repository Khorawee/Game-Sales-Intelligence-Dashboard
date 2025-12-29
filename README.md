# 🎮 Game Sales Analytics & Prediction Dashboard

โปรเจกต์นี้คือระบบวิเคราะห์และพยากรณ์ยอดขายวิดีโอเกม (Video Game Sales) แบบครบวงจร ครอบคลุมตั้งแต่การจัดเก็บข้อมูลลงฐานข้อมูล MySQL, การวิเคราะห์ข้อมูล (Data Analytics), การสร้างโมเดล Machine Learning เพื่อทำนายยอดขาย และการแสดงผลผ่าน Streamlit Web Application

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange)
![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn-yellow)

## Features

### Interactive Dashboard
* วิเคราะห์แนวโน้มยอดขายเกมระดับโลก (NA, EU, JP, Other)
* แสดงอันดับเกมยอดนิยม
* วิเคราะห์ส่วนแบ่งตลาดตาม Platform และ Genre
* กราฟแบบ Interactive ด้วย Plotly

### ML Sales Prediction
* ทำนายยอดขาย Global Sales
* เปรียบเทียบประสิทธิภาพโมเดล: XGBoost, Random Forest, Extra Trees
* วัดผลด้วย R² และ RMSE

### Normalized Database (3NF)
* ออกแบบฐานข้อมูลเชิงสัมพันธ์ (Relational Database)
* ลดความซ้ำซ้อนของข้อมูล
* เพิ่มประสิทธิภาพในการ Query

### Automated Pipeline
* โหลดข้อมูล (ETL)
* เทรนโมเดล
* เปิด Dashboard
* รันได้ด้วยคำสั่งเดียว

---

## Tech Stack

* **Language:** Python 3.8+
* **Database:** MySQL
* **Web Framework:** Streamlit
* **Data Processing:** Pandas, NumPy, SQLAlchemy
* **Machine Learning:** Scikit-learn, XGBoost, Category Encoders
* **Visualization:** Plotly Express, Plotly Graph Objects

---

## Installation

### 1. Clone Repository
```bash
git clone https://github.com/Khorawee/Game-Sales-Dashboard.git
cd Game-Sales-Dashboard
```

### 2. Install Dependencies
แนะนำให้สร้าง Virtual Environment ก่อน
```bash
# Create virtual environment (optional)
python -m venv venv
source venv/bin/activate        # Mac / Linux
# venv\Scripts\activate         # Windows
```

```bash
pip install -r requirements.txt
```

### 3. Database Setup
ตรวจสอบว่าติดตั้ง MySQL Server แล้ว จากนั้น import schema
```bash
mysql -u root -p < game_sales_schema.sql
```

### 4. Environment Variables
สร้างไฟล์ .env ในโฟลเดอร์หลัก

```env
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_NAME=game_sales
```

### 5. Prepare Dataset
ดาวน์โหลด Dataset (เช่นจาก Kaggle) เปลี่ยนชื่อเป็น vgsales.csv และวางไว้ที่โฟลเดอร์ data/vgsales.csv

## Usage
รันทุกขั้นตอน (ETL + Train Model + Launch Dashboard) ด้วยคำสั่งเดียว

```bash
python run_pipeline.py
```
### Project Structure
```text
├── app.py                  # Streamlit dashboard
├── run_pipeline.py         # Automation script
├── init_database.py        # ETL: CSV → MySQL
├── train_model.py          # Train & evaluate ML models
├── preprocessor.py         # Data preprocessing pipeline
├── game_sales_schema.sql   # Database schema (3NF)
├── requirements.txt
├── .env
├── data/
│   └── vgsales.csv
├── image/
└── models/
```

### Dashboard Overview
![Dashboard Overview 1](./image/Screenshot%202025-12-22%20205556.png)
![Dashboard Overview 2](./image/Screenshot%202025-12-22%20205604.png)
![Dashboard Overview 3](./image/Screenshot%202025-12-22%20205612.png)
![Dashboard Overview 4](./image/Screenshot%202025-12-22%20205625.png)
![Dashboard Overview 5](./image/Screenshot%202025-12-22%20205632.png)

### ML Prediction Interface
![ML Prediction Interface](./image/Screenshot%202025-12-22%20205643.png)
