# Game Sales Analytics & Prediction Dashboard

โปรเจกต์นี้คือระบบวิเคราะห์และพยากรณ์ยอดขายวิดีโอเกม (Video Game Sales) แบบครบวงจร  
ครอบคลุมตั้งแต่การจัดเก็บข้อมูลลงฐานข้อมูล MySQL, การวิเคราะห์ข้อมูล (Data Analytics),  
การสร้างโมเดล Machine Learning เพื่อทำนายยอดขาย และการแสดงผลผ่าน Web Application ด้วย Streamlit

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange)
![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn-yellow)

---

## Features

- **Interactive Dashboard**  
  แสดงแนวโน้มยอดขาย อันดับเกมยอดนิยม และส่วนแบ่งการตลาดตาม Platform และ Genre

- **ML Sales Prediction**  
  ระบบทำนายยอดขายเกม (Global Sales) โดยเปรียบเทียบโมเดล  
  **XGBoost, Random Forest และ Extra Trees**

- **Normalized Database (3NF)**  
  ออกแบบฐานข้อมูลเชิงสัมพันธ์เพื่อลดความซ้ำซ้อนและเพิ่มประสิทธิภาพในการ Query

- **Automated Pipeline**  
  รัน ETL, เทรนโมเดล และเปิด Dashboard ได้ในคำสั่งเดียว

- **Advanced Visualization**  
  แสดงผลกราฟโต้ตอบได้ด้วย Plotly

---

## Tech Stack

- **Language:** Python 3.8+
- **Database:** MySQL
- **Web Framework:** Streamlit
- **Data Processing:** Pandas, NumPy, SQLAlchemy
- **Machine Learning:** Scikit-learn, XGBoost, Category Encoders
- **Visualization:** Plotly Express / Plotly Graph Objects

---

## Installation

### 1. Clone Repository
```bash
git clone https://github.com/Khorawee/Game-Sales-Dashboard.git
cd Game-Sales-Dashboard
2. Install Dependencies
แนะนำให้สร้าง Virtual Environment ก่อนติดตั้ง

bash
Copy code
# Create virtual environment (optional)
python -m venv venv
source venv/bin/activate   # Mac / Linux
# venv\Scripts\activate    # Windows

# Install required libraries
pip install -r requirements.txt
3. Database Setup
ตรวจสอบให้แน่ใจว่าติดตั้ง MySQL Server แล้ว จากนั้น import schema:

bash
Copy code
mysql -u root -p < game_sales_schema.sql
4. Environment Variables
สร้างไฟล์ .env ในโฟลเดอร์หลักของโปรเจกต์

env
Copy code
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_NAME=game_sales
5. Prepare Dataset
ดาวน์โหลด Dataset (เช่นจาก Kaggle)
เปลี่ยนชื่อเป็น vgsales.csv และวางไว้ที่:

text
Copy code
data/vgsales.csv
Usage
รันทุกขั้นตอน (ETL + Train Model + Launch Dashboard) ด้วยคำสั่งเดียว:

bash
Copy code
python run_pipeline.py
ระบบจะทำงานตามลำดับ:

โหลดข้อมูลจาก CSV ลง MySQL

เทรนและประเมินโมเดล Machine Learning

เปิดหน้า Streamlit Dashboard อัตโนมัติ

Project Structure
text
Copy code
├── app.py                  # Streamlit dashboard
├── run_pipeline.py         # Automation script
├── init_database.py        # ETL: CSV → MySQL
├── train_model.py          # Train & evaluate ML models
├── preprocessor.py         # Data preprocessing pipeline
├── game_sales_schema.sql   # Database schema (3NF)
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables
├── data/
│   └── vgsales.csv         # Raw dataset
├── image/                  # Screenshots
└── models/                 # Trained ML models (.pkl)
## Screenshots

### Dashboard Overview
![Dashboard Overview 1](./image/Screenshot%202025-12-22%20205556.png)
![Dashboard Overview 2](./image/Screenshot%202025-12-22%20205604.png)
![Dashboard Overview 3](./image/Screenshot%202025-12-22%20205612.png)
![Dashboard Overview 4](./image/Screenshot%202025-12-22%20205625.png)
![Dashboard Overview 5](./image/Screenshot%202025-12-22%20205632.png)

### ML Prediction Interface
![ML Prediction Interface](./image/Screenshot%202025-12-22%20205643.png)

