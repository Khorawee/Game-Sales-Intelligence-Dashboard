# -*- coding: utf-8 -*-
import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path
import os
from dotenv import load_dotenv

# โหลดค่าจาก .env
load_dotenv()

# สร้าง connection string จาก environment variables
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "game_sales")

if not DB_PASSWORD:
    raise ValueError("❌ กรุณาตั้งค่า DB_PASSWORD ในไฟล์ .env")

engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")


def insert_unique(table, values):
    """Insert unique items safely using INSERT IGNORE."""
    with engine.begin() as conn:
        for v in values:
            conn.execute(
                text(f"INSERT IGNORE INTO {table} (name) VALUES (:val)"),
                {"val": v}
            )


def main():
    try:
        print("📥 กำลังโหลด CSV...")
        
        # ใช้เส้นทางแบบสัมพัทธ์ (relative path)
        csv_path = Path(__file__).parent / "data" / "vgsales.csv"
        
        # ตรวจสอบว่าไฟล์มีอยู่จริง
        if not csv_path.exists():
            raise FileNotFoundError(f"❌ ไม่พบไฟล์ CSV ที่: {csv_path}")
        
        df = pd.read_csv(csv_path)
        print(f"✔ โหลดข้อมูลสำเร็จ: {len(df):,} แถว")

        print("\n🧹 ทำความสะอาดข้อมูล...")
        df = df.dropna(subset=["Name", "Platform", "Genre", "Publisher"])
        df["Year"] = df["Year"].fillna(0).astype(int)
        print(f"✔ ข้อมูลหลังทำความสะอาด: {len(df):,} แถว")

        # =====================================================
        # INSERT UNIQUE DIMENSION VALUES (SAFE)
        # =====================================================
        print("\n📦 กำลังเพิ่มข้อมูล Platform/Genre/Publisher...")

        insert_unique("platform", df["Platform"].unique())
        print(f"  ✔ Platform: {df['Platform'].nunique()} รายการ")
        
        insert_unique("genre", df["Genre"].unique())
        print(f"  ✔ Genre: {df['Genre'].nunique()} รายการ")
        
        insert_unique("publisher", df["Publisher"].unique())
        print(f"  ✔ Publisher: {df['Publisher'].nunique()} รายการ")

        # =====================================================
        # LOAD ID MAPPING
        # =====================================================
        print("\n🔗 กำลังโหลด ID mapping...")

        plat_map = pd.read_sql("SELECT id, name FROM platform", engine).set_index("name")["id"]
        genre_map = pd.read_sql("SELECT id, name FROM genre", engine).set_index("name")["id"]
        pub_map = pd.read_sql("SELECT id, name FROM publisher", engine).set_index("name")["id"]

        # Map to FK
        df["platform_id"] = df["Platform"].map(plat_map)
        df["genre_id"] = df["Genre"].map(genre_map)
        df["publisher_id"] = df["Publisher"].map(pub_map)
        
        # ตรวจสอบว่ามีค่า NULL หรือไม่
        null_count = df[["platform_id", "genre_id", "publisher_id"]].isnull().sum().sum()
        if null_count > 0:
            print(f"⚠️ พบข้อมูลที่ map ไม่ได้: {null_count} แถว")
            df = df.dropna(subset=["platform_id", "genre_id", "publisher_id"])
            print(f"✔ ลบข้อมูลที่ไม่สมบูรณ์แล้ว เหลือ: {len(df):,} แถว")

        # =====================================================
        # INSERT INTO VGSALES (FACT TABLE)
        # =====================================================
        print("\n🗃 กำลังเพิ่มข้อมูลลงตาราง vgsales...")

        inserted_count = 0
        with engine.begin() as conn:
            for idx, row in df.iterrows():
                try:
                    conn.execute(text("""
                        INSERT IGNORE INTO vgsales
                        (`Rank`, game_name, Year,
                         NA_Sales, EU_Sales, JP_Sales, Other_Sales, Global_Sales,
                         platform_id, genre_id, publisher_id)
                        VALUES
                        (:rank, :name, :year,
                         :na, :eu, :jp, :other, :global,
                         :platform, :genre, :publisher)
                    """), {
                        "rank": int(row["Rank"]),
                        "name": str(row["Name"]),
                        "year": int(row["Year"]),
                        "na": float(row["NA_Sales"]),
                        "eu": float(row["EU_Sales"]),
                        "jp": float(row["JP_Sales"]),
                        "other": float(row["Other_Sales"]),
                        "global": float(row["Global_Sales"]),
                        "platform": int(row["platform_id"]),
                        "genre": int(row["genre_id"]),
                        "publisher": int(row["publisher_id"]),
                    })
                    inserted_count += 1
                    
                    # แสดงความคืบหน้า
                    if (idx + 1) % 1000 == 0:
                        print(f"  ... ประมวลผลแล้ว {idx + 1:,}/{len(df):,} แถว")
                        
                except Exception as e:
                    print(f"⚠️ ข้อผิดพลาดที่แถว {idx}: {e}")
                    continue

        print(f"\n✔ เพิ่มข้อมูลสำเร็จ: {inserted_count:,} แถว")
        print("\n🎉 เสร็จสิ้นการเตรียมฐานข้อมูล!")
        
        # แสดงสถิติข้อมูล
        print("\n📊 สถิติข้อมูลในฐานข้อมูล:")
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) as count FROM vgsales")).fetchone()
            print(f"  • จำนวนเกมทั้งหมด: {result[0]:,} เกม")
            
            result = conn.execute(text("SELECT COUNT(*) as count FROM platform")).fetchone()
            print(f"  • จำนวน Platform: {result[0]} แพลตฟอร์ม")
            
            result = conn.execute(text("SELECT COUNT(*) as count FROM genre")).fetchone()
            print(f"  • จำนวน Genre: {result[0]} ประเภท")
            
            result = conn.execute(text("SELECT COUNT(*) as count FROM publisher")).fetchone()
            print(f"  • จำนวน Publisher: {result[0]} ผู้เผยแพร่")

    except FileNotFoundError as e:
        print(f"\n❌ ข้อผิดพลาด: {e}")
        print("💡 กรุณาตรวจสอบว่าไฟล์ vgsales.csv อยู่ในโฟลเดอร์ 'data'")
    except ValueError as e:
        print(f"\n❌ ข้อผิดพลาดการตั้งค่า: {e}")
    except Exception as e:
        print(f"\n❌ เกิดข้อผิดพลาดที่ไม่คาดคิด: {e}")
        raise


if __name__ == "__main__":
    main()