import sqlite3
import mysql.connector

sqlite_conn = sqlite3.connect('db.sqlite3')
sqlite_cursor = sqlite_conn.cursor()

mysql_conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="jaguarmarket"
)
mysql_cursor = mysql_conn.cursor()

def sincronizar(tabla, columnas):
    print(f"\n🔄 Sincronizando tabla: {tabla}")
    columnas_str = ', '.join(columnas)
    placeholders = ', '.join(['%s'] * len(columnas))

    mysql_cursor.execute(f"DELETE FROM {tabla}")

    sqlite_cursor.execute(f"SELECT {columnas_str} FROM {tabla}")
    registros = sqlite_cursor.fetchall()

    for fila in registros:
        mysql_cursor.execute(
            f"INSERT INTO {tabla} ({columnas_str}) VALUES ({placeholders})",
            fila
        )

tablas = {
    "auth_user": [
        "id", "password", "last_login", "is_superuser", "username",
        "last_name", "email", "is_staff", "is_active", "date_joined", "first_name"
    ],
    "productos_categoria": ["id", "nombre"],
    "productos_producto": [
        "id", "nombre", "descripcion", "precio", "categoria_id", "publicado_por_id", "imagen"
    ],
    "productos_perfilusuario": ["id", "carrera", "usuario_id", "telefono", "foto"],
    "productos_mensaje": [
        "id", "contenido", "timestamp", "emisor_id", "producto_id", "receptor_id", "leido"
    ],
}

for tabla, columnas in tablas.items():
    sincronizar(tabla, columnas)

mysql_conn.commit()
mysql_conn.close()
sqlite_conn.close()

print("\n✅ Sincronización completa. Revisa phpMyAdmin.")
