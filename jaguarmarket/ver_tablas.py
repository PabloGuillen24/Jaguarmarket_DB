import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Obtener todas las tablas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tablas = cursor.fetchall()

for tabla in tablas:
    nombre_tabla = tabla[0]
    print(f"\n📄 Tabla: {nombre_tabla}")
    cursor.execute(f"PRAGMA table_info({nombre_tabla});")
    columnas = cursor.fetchall()
    for col in columnas:
        print(f"  • {col[1]} ({col[2]})")

conn.close()
