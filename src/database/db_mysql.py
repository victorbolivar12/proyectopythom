from decouple import config
import pymysql

def get_connection():
    try:
        return pymysql.connect(
            host=config('MYSQL_HOST'),
            user=config('MYSQL_USER'),
            password=config('MYSQL_PASSWORD'),
            db=config('MYSQL_DB'),
            auth_plugin='mysql_native_password'  # Cambia el método de autenticación
        )
    except Exception as ex:
        print("Error al conectar la base de datos: ", ex)

