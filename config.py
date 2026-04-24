import os

# Update by Saim Ali on 2026-04-24 for Assignment A2 branch 1
class Config:
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'sakila-db-server')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'admin')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'sakila')
    CONNECTION_TIMEOUT = int(os.environ.get('CONNECTION_TIMEOUT', '30'))
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here-change-this-in-production')