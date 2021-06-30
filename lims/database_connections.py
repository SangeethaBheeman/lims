from mysql.connector import connect, Error
import logging
import config


class DBConnection:
    def __init__(self):
        self.connection_config = {
            "host": config.connection_config['host'],
            "user": config.connection_config['user'],
            "password": config.connection_config['password'],
            "database": config.connection_config['database']
        }

    def create_connection(self):
        try:
            with connect(**self.connection_config) as connection:
                if connection.is_connected():
                    return connection
        except Error as e:
            logging.error("Database connection error %s", e)
            print(e)  




