import psycopg2


def get_connection():
    return psycopg2.connect("dbname=test_db user=postgres password=Password1!")


def createTableImages():
    db_conn = psycopg2.connect("dbname=test_db user=postgres password=Password1!")
    cursor_object = db_conn.cursor()
    cursor_object.execute("Create Table Images1("
                          "ImageId SERIAL primary key not null, "
                          "ImageFileName char(50) not null, "
                          "ImageAddress bytea not null)")
    # cursor_object.execute("Drop table Images")
    db_conn.commit()


def convert_To_Binary(filename):
    with open(filename, 'rb') as file:
        data = file.read()
    return data


def insertTableImages(FileName):
    conn = None
    try:
        conn = psycopg2.connect("dbname=test_db user=postgres password=Password1!")
        cur = conn.cursor()
        file_data = convert_To_Binary(FileName)
        BLOB = psycopg2.Binary(file_data)
        cur.execute(
            "INSERT INTO Images1(ImageFileName, ImageAddress) VALUES(%s,%s)", (FileName, BLOB))
        cur.close()

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.commit()


# insertTableImages('static\Apple.jpg')
# insertTableImages('static\Bulb.jpg')
# insertTableImages('static\Candle.png')
# insertTableImages('static\Cactus.png')
# insertTableImages('static\Hat.jpg')
# insertTableImages('static\Star.png')
# insertTableImages('static\Camera.jpg')
# insertTableImages('static\Tree.jpg')

# insertTableImages('..\static\Star.png')

# createTableImages()


def Binary_To_File(BLOB, FileName, oldFileName):
    with open(f"{FileName}", 'wb') as file:
        file.write(BLOB)
    print(f"{oldFileName} File saved With Name name {FileName}")


def readTableImages(serial, newFileName):
    conn = None
    try:
        conn = psycopg2.connect("dbname=test_db user=postgres password=Password1!")

        cur = conn.cursor()
        cur.execute('SELECT * FROM Images1')
        db = cur.fetchall()
        BLOB = db[serial][2]
        Binary_To_File(BLOB, newFileName, db[serial][1])
        cur.close()

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.commit()


# readTableImages(4, 'C:\Workspace\Imagication\Images\SampleImagefromDB.jpg')
def getImageidFromTableImages(newFileName):
    with get_connection() as conn:
        cursor_object = conn.cursor()
        cursor_object.execute(f"Select imageid from Images1 where ImageFileName = '{newFileName}'")
        data = cursor_object.fetchall()
        print(data)
        response = data[0][0]
        cursor_object.close()
        print("logs are here")
        return str(response)
