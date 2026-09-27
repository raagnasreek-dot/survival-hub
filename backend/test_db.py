from database import get_connection

conn = get_connection()

if conn:
    cursor = conn.cursor()

    cursor.execute("SHOW TABLES")

    print("\nTables:")

    for table in cursor:
        print(table[0])

    cursor.close()
    conn.close()