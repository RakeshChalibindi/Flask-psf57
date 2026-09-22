from database.connectiondb import DatabaseConnection


#check user alredy exist or not 
def getUserByEmail(email:str, data=False):
    try:
        db_config = DatabaseConnection()
        cusror = db_config.cursor(dictionary=True)
        get_user_by_email = """SELECT * FROM USERS
                            WHERE EMAIL = %s;"""
        cusror.execute(get_user_by_email, (email,))
        user = cusror.fetchone() 
        cusror.close()
        db_config.close()
        if data==True:
            if user:
                return True, user
            else:
                return False, "Check your user credentials"
        
            
        if not user: # if record not found
            return True # user not exists
        else:
            return False # user exists
    except Exception as e:
        return f"Something wrong in database/utilityDB.py:getUserByEmail: {e}"


# insert user data into table
def insertUserRecord(name:str, email:str, hash_pasword:bytes):
    try:
        db_config = DatabaseConnection()
        cusror = db_config.cursor()
        insert_record_query = """INSERT INTO USERS(USERNAME,EMAIL, HASHPASSWORD, IS_ACTIVE)
                                VALUES(%s, %s, %s, %s);"""
        cusror.execute(insert_record_query, (name,email,hash_pasword, 1))
        db_config.commit()
        cusror.close()
        db_config.close()
        return True, "User Successfully Registred"
    except Exception as e:
        return False, f"Something wrong in database/utilityDB.py:getUserByEmail: {e}"


def insertNotesRecord(userid: int, title: str, content: str):

    try:

        db_config = DatabaseConnection()

        cursor = db_config.cursor()

        query = """
        INSERT INTO NOTES
        (USERID, TITLE, CONTENT)
        VALUES (%s, %s, %s)
        """

        cursor.execute(
            query,
            (userid, title, content)
        )

        db_config.commit()

        cursor.close()
        db_config.close()

        return True, "Note Saved Successfully"

    except Exception as e:

        return False, f"Database Error: {e}"



# get Notes by userid
def getNotesByUserid(userid:int):
    try:
        db_config = DatabaseConnection()
        cusror = db_config.cursor(dictionary=True)
        get_notes_query = """select * from notes where userid = %s 
                            order by updated_at desc;"""
        cusror.execute(get_notes_query, (userid,))
        notes = cusror.fetchall()
        cusror.close()
        db_config.close()
        return True, notes
    except Exception as e:
        return False, f"Something wrong in database/utilityDB.py:getNotesByUserid: {e}"


# get notes by notes id
def getNotesByNotesid(notesid:int):
    try:
        db_config = DatabaseConnection()
        cusror = db_config.cursor(dictionary=True)
        get_notes_query = """select * from notes where notesid = %s;"""
        cusror.execute(get_notes_query, (notesid,))
        notes = cusror.fetchone()
        cusror.close()
        db_config.close()
        return True, notes
    except Exception as e:
        return False, f"Something wrong in database/utilityDB.py:getNotesByNotesid: {e}"

# update notes
def updateNotesRecord(notesid: int, userid: int, title: str, content: str):
    try:
        db_config = DatabaseConnection()
        cusror = db_config.cursor()
        update_notes_query = """
        UPDATE NOTES
        SET TITLE = %s,
            CONTENT = %s
        WHERE NOTESID = %s
        AND USERID = %s;
        """

        cusror.execute(
            update_notes_query,
            (title, content, notesid, userid)
        )

        db_config.commit()
        cusror.close()
        db_config.close()
        return True, "Notes Updated"
    except Exception as e:
        return False, f"Something wrong in utilityDB.py:updateNotesRecord: {e}"

def updateNotesRecord(notesid: int, userid: int, title: str, content: str):
    try:
        db_config = DatabaseConnection()
        cursor = db_config.cursor()

        query = """
        UPDATE NOTES
        SET TITLE = %s,
            CONTENT = %s
        WHERE NOTESID = %s
        AND USERID = %s
        """

        cursor.execute(
            query,
            (title, content, notesid, userid)
        )

        db_config.commit()

        cursor.close()
        db_config.close()

        return True, "Notes Updated"

    except Exception as e:
        return False, f"Database Error: {e}"


def deleteNotesRecord(notesid: int, userid: int):

    try:
        db_config = DatabaseConnection()
        cursor = db_config.cursor()

        query = """
        DELETE FROM NOTES
        WHERE NOTESID = %s
        AND USERID = %s
        """

        cursor.execute(
            query,
            (notesid, userid)
        )

        db_config.commit()

        cursor.close()
        db_config.close()

        return True, "Notes Deleted"

    except Exception as e:
        return False, f"Database Error: {e}"

# # Insert file record into database
def insertFileRecord(userid: int, filename: str, filepath: str, filetype: str):
    try:
        db_config = DatabaseConnection()
        cursor = db_config.cursor()

        query = """
        INSERT INTO FILES
        (USERID, FILENAME, FILEPATH, FILETYPE)
        VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (userid, filename, filepath, filetype)
        )

        db_config.commit()

        cursor.close()
        db_config.close()

        return True, "File inserted successfully"

    except Exception as e:
        return False, f"Database Error: {e}"


# Get files by user ID
def getFileByUserID(userid: int):
    try:
        db_config = DatabaseConnection()
        cursor = db_config.cursor(dictionary=True)

        query = """
        SELECT *
        FROM FILES
        WHERE USERID = %s
        ORDER BY FILEID DESC
        """

        cursor.execute(query, (userid,))

        files = cursor.fetchall()

        cursor.close()
        db_config.close()

        return True, files

    except Exception as e:
        return False, f"Database Error: {e}"


def updateUserPassword(email, hash_password):

    try:

        connection = DatabaseConnection()
        cursor = connection.cursor()

        query = """
            UPDATE USERS
            SET HASHPASSWORD = %s
            WHERE EMAIL = %s
        """

        cursor.execute(
            query,
            (hash_password, email)
        )

        connection.commit()

        cursor.close()
        connection.close()

        return True, "Password updated successfully"

    except Exception as e:

        return False, str(e)