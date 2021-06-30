from database_connections import DBConnection
from mysql.connector import Error

class Well:

    def __init__(self, plate_barcode, well_position):
        self.plate_barcode = plate_barcode
        self.well_position = well_position

    def connect_to_db(self):
        db_connection = DBConnection()
        connection = db_connection.create_connection()
        connection.reconnect()
        return connection
    

    def add_sample_to_well(self, sample_name):
        try:
            connection = self.connect_to_db()
            cursor = connection.cursor()
            query = "insert into wells(well_position, plate_barcode, sample_name, is_empty) \
                            values(%s,%s,%s,%s)"
            values = (self.well_position, self.plate_barcode, sample_name, False)

            cursor.execute(query, values)
            connection.commit()
            print("Updated successfully")
        except Error as e:
            print("Error:%s", e)


    def delete_samples_from_well(self, sample_names):
        try:
            connection = self.connect_to_db()
            cursor = connection.cursor()
            format_strings = ','.join(['%s'] * len(sample_names))

            sub_query = "select sample_name from wells where plate_barcode=%s and sample_name !='NULL'  group by sample_name" % self.plate_barcode

            query = "delete from wells where sample_name in (%s) and plate_barcode=%s"
            values = (sub_query, self.plate_barcode)
            cursor.execute(query, values) 
            connection.commit()
            print("Deleted the wells")
        except Error as e:
            print("Error:%s", e)
