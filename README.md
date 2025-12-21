# 🎮 Game Sales Analytics & Prediction Dashboard

โปรเจกต์นี้คือระบบวิเคราะห์และพยากรณ์ยอดขายวิดีโอเกม (Video Game Sales) แบบครบวงจร ตั้งแต่การจัดเก็บข้อมูลลงฐานข้อมูล MySQL, การวิเคราะห์ข้อมูล (Data Analytics), การสร้างโมเดล Machine Learning เพื่อทำนายยอดขาย และการแสดงผลผ่าน Web Application ด้วย Streamlit

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange)
![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn-yellow)

## ✨ ฟีเจอร์หลัก (Features)

* **📊 Interactive Dashboard:** แสดงแนวโน้มยอดขาย, อันดับเกมยอดนิยม, ส่วนแบ่งการตลาดตาม Platform และ Genre
* **🤖 ML Sales Prediction:** ระบบทำนายยอดขายเกม (Global Sales) โดยใช้โมเดล **XGBoost, Random Forest และ Extra Trees**
* **🗄️ Normalized Database:** ออกแบบฐานข้อมูลแบบ 3NF เพื่อลดความซ้ำซ้อนและเพิ่มประสิทธิภาพ
* **🔄 Automated Pipeline:** สคริปต์อัตโนมัติสำหรับโหลดข้อมูล (ETL), เทรนโมเดล และรันเซิร์ฟเวอร์
* **📈 Advanced Visualization:** กราฟโต้ตอบได้สวยงามด้วย Plotly

---

## 🛠️ Tech Stack

* **Language:** Python
* **Database:** MySQL
* **Web Framework:** Streamlit
* **Data Processing:** Pandas, NumPy, SQLAlchemy
* **Machine Learning:** Scikit-learn, XGBoost, Category Encoders
* **Visualization:** Plotly Express/Go

---

## ⚙️ การติดตั้ง (Installation)

### 1. Clone Repository
```bash
git clone [https://github.com/Khorawee/Game-Sales-Intelligence-Dashboard.git]
cd game-sales-dashboard
2. ติดตั้ง Dependencies
แนะนำให้สร้าง Virtual Environment ก่อนติดตั้ง

Bash

pip install -r requirements.txt
3. ตั้งค่าฐานข้อมูล (Database Setup)
ตรวจสอบให้แน่ใจว่าคุณติดตั้ง MySQL Server เรียบร้อยแล้ว

Import ไฟล์ Schema เข้าสู่ MySQL:

Bash

mysql -u root -p < game_sales_schema.sql
4. ตั้งค่า Environment Variables
สร้างไฟล์ .env ในโฟลเดอร์หลักของโปรเจกต์ และใส่ข้อมูลการเชื่อมต่อฐานข้อมูล:

Ini, TOML

# .env file
DB_USER=root
DB_PASSWORD=password
DB_HOST=localhost
DB_NAME=game_sales
5. เตรียมข้อมูล (Data)
ดาวน์โหลดไฟล์ Dataset (เช่นจาก Kaggle) และเปลี่ยนชื่อเป็น vgsales.csv นำไปวางไว้ในโฟลเดอร์ data/

Plaintext

project_root/
└── data/
    └── vgsales.csv
🚀 การใช้งาน (Usage)
คุณสามารถรันโปรเจกต์ทั้งหมด (เตรียมฐานข้อมูล + เทรนโมเดล + เปิดแอป) ได้ด้วยคำสั่งเดียว:

Bash

python run_pipeline.py
ระบบจะทำการ:

ตรวจสอบและติดตั้ง Libraries ที่จำเป็น

โหลดข้อมูลจาก CSV ลงสู่ฐานข้อมูล MySQL (init_database.py)

เทรนโมเดล Machine Learning และบันทึกผล (train_model.py)

เปิดหน้าเว็บ Dashboard ขึ้นมาโดยอัตโนมัติ (app.py)

📂 โครงสร้างโปรเจกต์ (Project Structure)
Plaintext

├── app.py                  # ไฟล์หลักสำหรับรัน Streamlit Dashboard
├── run_pipeline.py         # สคริปต์ Automation สำหรับรันทุกขั้นตอน
├── init_database.py        # สคริปต์ ETL โหลดข้อมูล CSV เข้า MySQL
├── train_model.py          # สคริปต์สร้างและเทรนโมเดล ML
├── preprocessor.py         # Class สำหรับจัดการข้อมูล (Preprocessing Pipeline)
├── game_sales_schema.sql   # ไฟล์โครงสร้างฐานข้อมูล (SQL Script)
├── requirements.txt        # รายชื่อ Libraries ที่ต้องใช้
├── .env                    # ไฟล์ตั้งค่า Database (ต้องสร้างเอง)
├── data/
│   └── vgsales.csv         # ไฟล์ข้อมูลดิบ
└── models/                 # โฟลเดอร์เก็บโมเดลที่เทรนเสร็จแล้ว (.pkl)
🔮 หน้าจอการใช้งาน (Screenshots)
Dashboard Overview
(ใส่รูปภาพ Screenshot ของหน้า Dashboard ที่นี่)

ML Prediction Interface
(ใส่รูปภาพ Screenshot ของหน้า Prediction ที่นี่)
