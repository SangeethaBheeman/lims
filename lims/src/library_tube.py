import json
from mysql.connector import Error
from database_connections import DBConnection

class LibraryTube:

    def __init__(self, library_tube_barcode):
        self.library_tube_barcode = library_tube_barcode

    def connect_to_db(self):
        db_connection = DBConnection()
        connection = db_connection.create_connection()
        connection.reconnect()
        return connection

    def add_samples_to_library_tube(self, tagged_samples):
        try:
            connection = self.connect_to_db()
            cursor = connection.cursor()

            query = "insert into library_tube(library_tube_barcode, sample_tag_list) values(%s,%s)\
                            on duplicate key update sample_tag_list=%s"

            json_str = json.dumps(tagged_samples)
            values = (self.library_tube_barcode, json_str, json_str)
            cursor.execute(query, values)
            connection.commit()
            print("Record saved")    
        except Error as e:
            print("Error:%s", e)

    def delete_samples_from_library_tube(self):
        try:
            connection = self.connect_to_db()
            cursor = connection.cursor()
            query = "update library_tube set sample_tag_list = NULL where \
                                                    library_tube_barcode=%s"
            values = (self.library_tube_barcode,)
            cursor.execute(query, values) 
            connection.commit()
            print("Removed samples from library tube")
        except Error as e:
            print("Error:%s", e)

