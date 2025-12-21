import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Gafiw9515",
        database="game_sales"
    )

    if conn.is_connected():
        print(" Connected to MySQL database successfully!")
        print("Database:", conn.database)

except mysql.connector.Error as e:
    print("❌ MySQL Error:", e)

finally:
    if 'conn' in locals() and conn.is_connected():
        conn.close()
