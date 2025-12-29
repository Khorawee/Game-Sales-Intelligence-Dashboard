# Game Sales Analytics & Prediction Dashboard

โปรเจกต์นี้คือระบบวิเคราะห์และพยากรณ์ยอดขายวิดีโอเกม (Video Game Sales) แบบครบวงจร ตั้งแต่การจัดเก็บข้อมูลลงฐานข้อมูล MySQL, การวิเคราะห์ข้อมูล (Data Analytics), การสร้างโมเดล Machine Learning เพื่อทำนายยอดขาย และการแสดงผลผ่าน Web Application ด้วย Streamlit

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange)
![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn-yellow)

## Features

* **Interactive Dashboard:** แสดงแนวโน้มยอดขาย, อันดับเกมยอดนิยม, ส่วนแบ่งการตลาดตาม Platform และ Genre
* **ML Sales Prediction:** ระบบทำนายยอดขายเกม (Global Sales) โดยเปรียบเทียบโมเดล XGBoost, Random Forest และ Extra Trees เพื่อเลือกโมเดลที่ดีที่สุด
* **Normalized Database:** ออกแบบฐานข้อมูลแบบ 3NF เพื่อลดความซ้ำซ้อนและเพิ่มประสิทธิภาพในการ Query
* **Automated Pipeline:** สคริปต์อัตโนมัติสำหรับโหลดข้อมูล (ETL), เทรนโมเดล และรันเซิร์ฟเวอร์ในคำสั่งเดียว
* **Advanced Visualization:** กราฟโต้ตอบได้สวยงามด้วย Plotly

---

## Tech Stack

* **Language:** Python 3.8+
* **Database:** MySQL
* **Web Framework:** Streamlit
* **Data Processing:** Pandas, NumPy, SQLAlchemy
* **Machine Learning:** Scikit-learn, XGBoost, Category Encoders
* **Visualization:** Plotly Express/Go

---

## Installation

### 1. Clone Repository
```bash
git clone [https://github.com/Khorawee/Game-Sales-Intelligence-Dashboard.git](https://github.com/Khorawee/Game-Sales-Intelligence-Dashboard.git)
cd game-sales-dashboard
2. Install Dependencies
แนะนำให้สร้าง Virtual Environment ก่อนติดตั้ง

Bash
# สร้าง Virtual Environment (Optional)
python -m venv venv
source venv/bin/activate  # สำหรับ Mac/Linux
# venv\Scripts\activate   # สำหรับ Windows

# ติดตั้ง Libraries
pip install -r requirements.txt

3. Database Setup
ตรวจสอบให้แน่ใจว่าคุณติดตั้ง MySQL Server เรียบร้อยแล้ว จากนั้น Import ไฟล์ Schema:

Bash
mysql -u root -p < game_sales_schema.sql

4. Environment Variables
สร้างไฟล์ .env ในโฟลเดอร์หลักของโปรเจกต์ และใส่ข้อมูลการเชื่อมต่อฐานข้อมูล:

# .env file
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_NAME=game_sales

5. Prepare Data
ดาวน์โหลดไฟล์ Dataset (เช่นจาก Kaggle) เปลี่ยนชื่อเป็น vgsales.csv และนำไปวางไว้ในโฟลเดอร์ data/

Plaintext

project_root/
└── data/
    └── vgsales.csv
Usage
คุณสามารถรันโปรเจกต์ทั้งหมด (เตรียมฐานข้อมูล + เทรนโมเดล + เปิดแอป) ได้ด้วยคำสั่งเดียว:

Bash
python run_pipeline.py

ระบบจะทำงานตามลำดับดังนี้:

ตรวจสอบและติดตั้ง Libraries ที่จำเป็น

โหลดข้อมูลจาก CSV ลงสู่ฐานข้อมูล MySQL (init_database.py)

เทรนโมเดล Machine Learning และบันทึกผล (train_model.py)

เปิดหน้าเว็บ Dashboard ขึ้นมาโดยอัตโนมัติ (app.py)

Project Structure
Plaintext

├── app.py                  # ไฟล์หลักสำหรับรัน Streamlit Dashboard
├── run_pipeline.py         # สคริปต์ Automation สำหรับรันทุกขั้นตอน
├── init_database.py        # สคริปต์ ETL โหลดข้อมูล CSV เข้า MySQL
├── train_model.py          # สคริปต์สร้างและเทรนโมเดล ML
├── preprocessor.py         # Class สำหรับจัดการข้อมูล (Preprocessing Pipeline)
├── game_sales_schema.sql   # ไฟล์โครงสร้างฐานข้อมูล (SQL Script)
├── requirements.txt        # รายชื่อ Libraries ที่ต้องใช้
├── .env                    # ไฟล์ตั้งค่า Database (User ต้องสร้างเอง)
├── data/
│   └── vgsales.csv         # ไฟล์ข้อมูลดิบ
└── models/                 # โฟลเดอร์เก็บโมเดลที่เทรนเสร็จแล้ว (.pkl)

## Screenshots

### Dashboard Overview

![Dashboard Overview 1](image/Screenshot%202025-12-22%20205556.png)

![Dashboard Overview 2](image/Screenshot%202025-12-22%20205604.png)

![Dashboard Overview 3](image/Screenshot%202025-12-22%20205612.png)

![Dashboard Overview 4](image/Screenshot%202025-12-22%20205625.png)

![Dashboard Overview 5](image/Screenshot%202025-12-22%20205632.png)

### ML Prediction Interface

![ML Prediction Interface](image/Screenshot%202025-12-22%20205643.png)