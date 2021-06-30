import config
from database_connections import DBConnection

class Customer:
    
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
    
    def connect_to_db(self):
        db_connection = DBConnection()
        connection = db_connection.create_connection()
        connection.reconnect()
        return connection

    def get_customer_id(self):
        connection = self.connect_to_db()
        cursor = connection.cursor()
        query = "select customer_id from customer where first_name = %s and last_name = %s order by created_date desc"
        values = (self.first_name, self.last_name)
        cursor.execute(query, values)
        record = cursor.fetchone()
        #cursor.close()
        if connection:
            connection.close()
        return record[0]


    def save_customer_details(self):
        connection = self.connect_to_db()
        cursor = connection.cursor()
        query = "INSERT INTO customer (first_name, last_name) VALUES (%s, %s)"
        values = (self.first_name, self.last_name)
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        
        if connection:
            connection.close()
        print("Saved customer details")   