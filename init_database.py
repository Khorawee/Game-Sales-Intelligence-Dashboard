# -*- coding: utf-8 -*-
import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path
import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

# Create connection string from environment variables
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "game_sales")

if not DB_PASSWORD:
    raise ValueError("Please set DB_PASSWORD in the .env file")

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
        print("Loading CSV...")
        
        # Use relative path
        csv_path = Path(__file__).parent / "data" / "vgsales.csv"
        
        # Check if file exists
        if not csv_path.exists():
            raise FileNotFoundError(f"CSV file not found at: {csv_path}")
        
        df = pd.read_csv(csv_path)
        print(f"Data loaded successfully: {len(df):,} rows")

        print("\nCleaning data...")
        df = df.dropna(subset=["Name", "Platform", "Genre", "Publisher"])
        df["Year"] = df["Year"].fillna(0).astype(int)
        print(f"Data after cleaning: {len(df):,} rows")

        # INSERT UNIQUE DIMENSION VALUES (SAFE)
        print("\nInserting Platform/Genre/Publisher data...")

        insert_unique("platform", df["Platform"].unique())
        print(f"  Platform: {df['Platform'].nunique()} items")
        
        insert_unique("genre", df["Genre"].unique())
        print(f"  Genre: {df['Genre'].nunique()} items")
        
        insert_unique("publisher", df["Publisher"].unique())
        print(f"  Publisher: {df['Publisher'].nunique()} items")

        # LOAD ID MAPPING
        print("\nLoading ID mapping...")

        plat_map = pd.read_sql("SELECT id, name FROM platform", engine).set_index("name")["id"]
        genre_map = pd.read_sql("SELECT id, name FROM genre", engine).set_index("name")["id"]
        pub_map = pd.read_sql("SELECT id, name FROM publisher", engine).set_index("name")["id"]

        # Map to FK
        df["platform_id"] = df["Platform"].map(plat_map)
        df["genre_id"] = df["Genre"].map(genre_map)
        df["publisher_id"] = df["Publisher"].map(pub_map)
        
        # Check for NULL values
        null_count = df[["platform_id", "genre_id", "publisher_id"]].isnull().sum().sum()
        if null_count > 0:
            print(f"Unmapped data found: {null_count} rows")
            df = df.dropna(subset=["platform_id", "genre_id", "publisher_id"])
            print(f"Incomplete data removed, remaining: {len(df):,} rows")

        # INSERT INTO VGSALES (FACT TABLE)
        print("\nInserting data into vgsales table...")

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
                    
                    if (idx + 1) % 1000 == 0:
                        print(f"  ... Processed {idx + 1:,}/{len(df):,} rows")
                        
                except Exception as e:
                    print(f"Error at row {idx}: {e}")
                    continue

        print(f"\nData inserted successfully: {inserted_count:,} rows")
        print("\nDatabase preparation completed!")
        
        print("\nDatabase Statistics:")
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) as count FROM vgsales")).fetchone()
            print(f"  - Total Games: {result[0]:,} games")
            
            result = conn.execute(text("SELECT COUNT(*) as count FROM platform")).fetchone()
            print(f"  - Total Platforms: {result[0]} platforms")
            
            result = conn.execute(text("SELECT COUNT(*) as count FROM genre")).fetchone()
            print(f"  - Total Genres: {result[0]} types")
            
            result = conn.execute(text("SELECT COUNT(*) as count FROM publisher")).fetchone()
            print(f"  - Total Publishers: {result[0]} publishers")

    except FileNotFoundError as e:
        print(f"\nError: {e}")
        print("Please check if vgsales.csv exists in the 'data' folder")
    except ValueError as e:
        print(f"\nConfiguration Error: {e}")
    except Exception as e:
        print(f"\nUnexpected Error: {e}")
        raise


if __name__ == "__main__":
    main()