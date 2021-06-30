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

MYSQL_DB = "testdb"

class ReceiveSampleTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        connection_config = {
            "host": 'localhost',
            "user": config.connection_config['user'],
            "password": config.connection_config['password'],
            #"database": MYSQL_DB
        }
        cnx = connect(**connection_config)
        cursor = cnx.cursor(dictionary=True)

        # drop database if it already exists
        try:
            cursor.execute("DROP DATABASE IF EXISTS {}".format(MYSQL_DB))
            cursor.close()
            print("DB dropped")
        except Error as err:
            print("{}{}".format(MYSQL_DB, err))

        cursor = cnx.cursor(dictionary=True)
        try:
            cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(MYSQL_DB))
        except Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)
        cnx.database = MYSQL_DB

        query = """CREATE TABLE `customer` (
        `customer_id` smallint(10) NOT NULL AUTO_INCREMENT,
        `first_name` varchar(40) NOT NULL,
        `last_name` varchar(40) NOT NULL,
        `created_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (`customer_id`)
        ) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1"""

        try:
            cursor.execute(query)
            cnx.commit()
        except Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("table already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

        insert_data_query = """INSERT INTO customer (first_name, last_name) VALUES ('John', 'Smith')"""
        try:
            cursor.execute(insert_data_query)
            cnx.commit()
        except Error as err:
            print("Data insertion to test_table failed \n" + err)
        cursor.close()
        cnx.close()

    @classmethod
    def tearDownClass(cls):
        connection_config = {
            "host": 'localhost',
            "user": config.connection_config['user'],
            "password": config.connection_config['password'],
            #"database": MYSQL_DB
        }
        cnx = connect(**connection_config)
        
        cursor = cnx.cursor(dictionary=True)

        # drop test database
        try:
            cursor.execute("DROP DATABASE {}".format(MYSQL_DB))
            cnx.commit()
            cursor.close()
        except mysql.connector.Error as err:
            print("Database {} does not exists. Dropping db failed".format(MYSQL_DB))
        cnx.close()


    def test_save_customer_details(self):
        # integration test with the database to make sure it works
        
        customer_obj = Customer("Peter", "Parker")
        customer_obj.save_customer_details()

        connection_config = {
            "host": 'localhost',
            "user": config.connection_config['user'],
            "password": config.connection_config['password'],
            "database": MYSQL_DB
        }
    
        with connect(**connection_config) as connection:
                connection.reconnect()
                if connection.is_connected():
                    cursor = connection.cursor()
                    cursor.execute("select * from customer")
                    result = cursor.fetchone()
        self.assertTrue(len(result) == 4)
        self.assertListEqual(result[1],'Peter')
        
        

    
if __name__ == '__main__':
    #unittest.main()
        
