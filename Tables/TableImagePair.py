import psycopg2


def createTableImagePairs():
    db_conn = psycopg2.connect("dbname=test_db user=postgres password=Password1!")
    cursor_object = db_conn.cursor()
    cursor_object.execute("Create Table ImagePairs("
                          "Username varchar(50) not null, "
                          "Constraint fk_username Foreign Key(Username) References UserKeyPoints(Username), "
                          "ImageId1 int not null, "
                          "Constraint fk_imageid1 Foreign Key(ImageId1) References Images1(ImageId), "
                          "ImageId2 int not null, "
                          "Constraint fk_imageid2 Foreign Key(ImageId2) References Images1(ImageId))")
    db_conn.commit()


def insertTableImagePairs(Username, grid1, grid2):
    db_conn = psycopg2.connect("dbname=test_db user=postgres password=Password1!")
    cursor_object = db_conn.cursor()
    # cursor_object.execute("Insert into ImagePairs(Username, ImageId1, ImageId2) values ('abcd',Array [2, 0,8])")
    cursor_object.execute("Insert into ImagePairs (username, imageid1, imageid2) values "
                          f"((select username from UserKeyPoints where username = '{Username}'), "
                          f"(select imageid from Images1 where imageid = '{grid1}'), "
                          f"(select imageid from Images1 where imageid = '{grid2}'))")
    db_conn.commit()


def getimagePair(Username, gridpoint):
    db_conn = psycopg2.connect("dbname=test_db user=postgres password=Password1!")
    cursor_object = db_conn.cursor()
    cursor_object.execute(f"select imageid2 from ImagePairs where username='{Username}' and imageid1= '{gridpoint}' UNION select imageid1 from ImagePairs where username='{Username}' and imageid2= '{gridpoint}'")
    db_conn.commit()

# createTableImagePairs()