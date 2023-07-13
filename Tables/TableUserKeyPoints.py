import psycopg2

def get_connection():
    return psycopg2.connect("dbname=test_db user=postgres password=Password1!")

def createTableUserKeyPoints():
    with get_connection() as connection:
        cursor_object = connection.cursor()
        cursor_object.execute("Create Table UserKeyPoints("
                          "Username varchar(50) primary key not null, "
                          "KeyPointSequence text[] not null)")
    # cursor_object.execute("Insert into UserKeyPoints(Username, KeyPointSequence) values ('abcd',Array [2, 0,8])")
    # cursor_object.execute("Insert into UserKeyPoints(Username, KeyPointSequence) values ('abcdef', Array [3, 6, 10])")
    # cursor_object.execute("Drop table Images")
        connection.commit()

def createTableUser():
    with get_connection() as connection:
        cursor_object = connection.cursor()
        cursor_object.execute("Create Table Users("
                          "Username varchar(50) primary key not null, "
                          "Email varchar(50) null)")
    # cursor_object.execute("Insert into UserKeyPoints(Username, KeyPointSequence) values ('abcd',Array [2, 0,8])")
    # cursor_object.execute("Insert into UserKeyPoints(Username, KeyPointSequence) values ('abcdef', Array [3, 6, 10])")
    # cursor_object.execute("Drop table Images")
        connection.commit()

def insertTableUser(username):
    conn = None
    try:
        with get_connection() as conn:
            cursor_object = conn.cursor()
            cursor_object.execute(f"Insert into Users(Username, Email) values ('{username}' ,null )")
        cursor_object.close()

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.commit()


def insertTableUserKeyPoints(username, keyPoint):
    conn = None
    try:
        with get_connection() as conn:
            cursor_object = conn.cursor()
            cursor_object.execute(f"Insert into UserKeyPoints(Username, KeyPointSequence) values ('{username}' ,Array {keyPoint} )")
        cursor_object.close()

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.commit()

def getDataFromTableUserKeyPoints(username):
    with get_connection() as conn:
            cursor_object = conn.cursor()
            cursor_object.execute(f"Select count(Username) from UserKeyPoints where username = '{username}'")
            data = cursor_object.fetchall()
            response = data[0][0]
            cursor_object.close()
            print("logs are here")
            return str(response)

def getDataFromTableUsers(username):
    with get_connection() as conn:
            cursor_object = conn.cursor()
            cursor_object.execute(f"Select count(Username) from Users where username = '{username}'")
            data = cursor_object.fetchall()
            response = data[0][0]
            cursor_object.close()
            print("logs are here")
            return str(response)
    
def getKeyPointsFromTableUserKeyPoints(username):
    with get_connection() as conn:
            cursor_object = conn.cursor()
            cursor_object.execute(f"Select keypointsequence from UserKeyPoints where username = '{username}'")
            data = cursor_object.fetchall()
            response = data[0][0]
            cursor_object.close()
            print("logs are here")
            return list(response)
        
# createTableUserKeyPoints()

# insertTableUser('myuser1')

# createTableUserKeyPoints()