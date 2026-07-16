from app.database.database import get_connection

conn = get_connection()

cursor = conn.cursor()

cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type='table'
""")

for row in cursor.fetchall():
    print(row["name"])

conn.close()