import os
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv

# Localiza a pasta principal SQL-Sales-Analytics
BASE_DIR = Path(__file__).resolve().parent.parent

# Carrega as configurações do arquivo .env
load_dotenv(BASE_DIR / ".env", override=True)


def conectar_mysql():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        database=os.getenv("MYSQL_DATABASE", "sql_sales_analytics"),
        connection_timeout=10
    )