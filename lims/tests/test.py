import datetime
import sys
import os
app_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, app_path.rstrip('tests'))
import unittest
from unittest.mock import patch, MagicMock
from mysql.connector import connect, Error
from main import receive_sample
from src.customer import Customer
import config


class ReceiveSampleTestCase(unittest.TestCase):
    
    def test_access_database_returns_values(self):
        # integration test with the database to make sure it works
        connection_config = {
            "host": 'localhost',
            "user": config.connection_config['user'],
            "password": config.connection_config['password'],
            "database": config.connection_config['database']
        }
    
        with connect(**connection_config) as connection:
                connection.reconnect()
                if connection.is_connected():
                    cursor = connection.cursor()
                    cursor.execute("select * from customer where customer_id=6")
                    result = cursor.fetchone()

        self.assertTrue(len(result) == 4)

        info_from_db = []
        for data in result:  # add all data in the database to a list
            info_from_db.append(data)

        self.assertListEqual(   # All the information matches in the database
            [6, 'Sangeetha', 'Bheeman', datetime.datetime(2021, 6, 26, 23, 29, 15)], info_from_db
        )

    @patch("src.customer.Customer")
    def test_save_customer_details(self, mock_customer):
        #Create test Customer
        customer_obj = Customer("John", "Smith")
        customer_obj.save_customer_details()

        mock
        mock_conn = MagicMock(spec=['cursor'])
        mock_conn.autocommit = True
        
        self.assertTrue(mock_conn.cursor.execute.called)

        
if __name__ == '__main__':
    #unittest.main()