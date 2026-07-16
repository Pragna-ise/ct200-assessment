from app.database.database import get_connection

conn = get_connection()

cursor = conn.cursor()

print("DOCUMENTS")

for row in cursor.execute(
    "SELECT * FROM documents"
):
    print(dict(row))

print("\nVERSIONS")

for row in cursor.execute(
    "SELECT * FROM document_versions"
):
    print(dict(row))

print("\nNODES")

for row in cursor.execute(
    "SELECT * FROM nodes LIMIT 5"
):
    print(dict(row))

conn.close()