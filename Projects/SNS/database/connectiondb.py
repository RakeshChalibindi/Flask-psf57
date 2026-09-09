import mysql.connector as SQLC

def  DatabaseConnection():
    try:
        db_config = SQLC.connect(
            host="localhost",
            user="root",
            password="Root",
            database="SNS_Management"
        )
        return db_config
    except Exception as e:
        return f"Something wrong in database/connection.py:{e}"