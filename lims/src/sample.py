import config
from database_connections import DBConnection


class Sample:

    def __init__(self, sample_name):
        self.sample_name = sample_name

    def connect_to_db(self):
        db_connection = DBConnection()
        connection = db_connection.create_connection()
        connection.reconnect()
        return connection

    def save_sample(self, customer_id):
        try:
            connection = self.connect_to_db()
            cursor = connection.cursor()

            query = "INSERT INTO sample (sample_name, customer_id) VALUES (%s, %s)"
            values = (self.sample_name, customer_id)
            cursor.execute(query, values)
            connection.commit()
            cursor.close()
            
            if connection:
                connection.close()
            print("Saved sample")
        except Error as e:
            print("Error:%s", e)

    def add_sample_tube_barcode(self, sample_tube_barcode):
        try:
            connection = self.connect_to_db()
            cursor = connection.cursor()        
            query = "update sample set sample_tube_barcode=%s where sample_name=%s"
            values = (sample_tube_barcode, self.sample_name)
            cursor.execute(query, values)
            connection.commit()
            print("updated successfully") 
        except Error as e:
            print("Error:%s", e)

    def add_tag(self, tag):
        try:
            connection = self.connect_to_db()
            cursor = connection.cursor()        
            query = "update sample set tag=%s where sample_name=%s"
            values = (tag, self.sample_name)
            cursor.execute(query, values)
            connection.commit()
            print("updated successfully") 
        except Error as e:
            print("Error:%s", e)



    


 

    
    
    