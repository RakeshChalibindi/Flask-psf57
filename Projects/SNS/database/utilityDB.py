from database.connectiondb import DatabaseConnection



def getUserbyEmail(email: str):
    try:
        db_config = DatabaseConnection()
        cursor = db_config.cursor()
        get_user_by_email = """
            SELECT * FROM USERS
            WHERE EMAIL = %s;
        """
        cursor.execute(get_user_by_email, (email,))
        user = cursor.fetchone()
        cursor.close()
        db_config.close()
        if not user:
            return True
        else:
            return False
    except Exception as e:
        print(f"Something wrong in insetQueries.py: insertNewRecord - {e}")