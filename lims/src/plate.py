import time
import datetime
import random
from database_connections import DBConnection

class Plate:

    def __init__(self, plate_barcode):
        self.plate_barcode = plate_barcode

    def connect_to_db(self):
        db_connection = DBConnection()
        connection = db_connection.create_connection()
        connection.reconnect()
        return connection

    def create_or_update_plate(self, state=None):
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        no_of_wells = random.choice([96, 384])
        try:
            connection = self.connect_to_db()
            cursor = connection.cursor()
            query = "insert into plate(plate_barcode, no_of_wells, state) values(%s,%s,%s)\
                                        on duplicate key update state=%s, updated_date=%s"
            values = (self.plate_barcode, no_of_wells, state, state, timestamp)
            cursor.execute(query, values)
            connection.commit()
            print("updated successfully") 
        except Error as e:
            print("Error:%s", e)


    def update_plate_state(self, state):
        try:
            connection = self.connect_to_db()
            cursor = connection.cursor()
            query = "update plate set state=%s where plate_barcode=%s"
                                        
            values = (state, self.plate_barcode)
            cursor.execute(query, values)
            connection.commit()
            print("updated successfully") 
        except Error as e:
            print("Error:%s", e)
    

    def get_well_count(self):
        try:
            connection = self.connect_to_db()
            cursor = connection.cursor()
            query = "select no_of_wells from plate where plate_barcode=%s"
            value = (self.plate_barcode,)
            cursor.execute(query, value)
            record = cursor.fetchone()
            if record:
                well_count = record[0]
                return well_count
            else:
                print("Plate not found")
                raise error
        except Error as e:
            print("Error:%s", e)