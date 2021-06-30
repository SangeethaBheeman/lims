import json
from database_connections import DBConnection
from mysql.connector import Error

def connect_to_db():
    db_connection = DBConnection()
    connection = db_connection.create_connection()
    connection.reconnect()
    return connection

def get_tags_from_library_tube(library_tube_barcode):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        query = "select sample_tag_list from library_tube where library_tube_barcode=%s"
        value = (library_tube_barcode,)
        cursor.execute(query, value)
        record = cursor.fetchone()
        tags = []
        if record:
            tags = json.loads(record[0])
        else:
            "Library tube not found"

        return tags
    except Error as e:
        print("Error:%s", e)