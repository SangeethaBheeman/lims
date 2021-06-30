import mysql.connector
from mysql.connector import errorcode
from unittest import TestCase
from mock import patch
import config

MYSQL_USER = "root"
MYSQL_PASSWORD = "root"
MYSQL_DB = "lims"
MYSQL_HOST = "localhost"
#MYSQL_PORT = "3306"


def add_data(query, cursor, cnx):
    try:
        cursor.execute(query)
        cnx.commit()
    except mysql.connector.Error as err:
        print("Data insertion to test_table failed \n" + err)


def add_table(query, cursor, cnx):
    try:
        cursor.execute(query)
        cnx.commit()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("test_table already exists.")
        else:
            print(err.msg)
    else:
        print("OK")


class MockDB(TestCase):
    @classmethod
    def setUpClass(cls):
        app.testing = True
        cls.app = app.test_client
        
        cnx = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
        )
        cursor = cnx.cursor(dictionary=True)

        # drop database if it already exists
        try:
            cursor.execute("DROP DATABASE {}".format(MYSQL_DB))
            cursor.close()
            print("DB dropped")
        except mysql.connector.Error as err:
            # print("{}".format(MYSQL_DB))
            pass

        cursor = cnx.cursor(dictionary=True)
        try:
            cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(MYSQL_DB))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)
        
        cnx.database = MYSQL_DB

        add_table("""CREATE TABLE `customer` (
        `customer_id` smallint(10) NOT NULL AUTO_INCREMENT,
        `first_name` varchar(40) NOT NULL,
        `last_name` varchar(40) NOT NULL,
        `created_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (`customer_id`)
        ) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1""", cursor, cnx)
        
        add_table("""CREATE TABLE `sample` (
        `sample_name` varchar(40) NOT NULL,
        `customer_id` varchar(40) NOT NULL,
        `sample_tube_barcode` varchar(40) DEFAULT NULL,
        `tag` varchar(20) DEFAULT NULL,
        `library_tube_barcode` varchar(40) DEFAULT NULL,
        `created_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        `updated_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (`sample_name`)
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1""", cursor, cnx)
        
        add_table("""CREATE TABLE `library_tube` (
        `library_tube_barcode` varchar(40) NOT NULL,
        `sample_tag_list` varchar(200) DEFAULT NULL,
        `state` varchar(15) DEFAULT NULL,
        `created_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        `updated_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (`library_tube_barcode`)
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1""", cursor, cnx)
                
        add_table("""CREATE TABLE `plate` (
        `plate_barcode` varchar(40) NOT NULL,
        `no_of_wells` int(11) DEFAULT NULL,
        `state` varchar(15) DEFAULT NULL,
        `created_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        `updated_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (`plate_barcode`)
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1""", cursor, cnx)
        
        add_table("""CREATE TABLE `wells` (
        `well_position` varchar(5) NOT NULL,
        `plate_barcode` varchar(40) NOT NULL,
        `sample_name` varchar(40) DEFAULT NULL,
        `is_empty` tinyint(1) DEFAULT NULL,
        `created_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        `updated_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (`well_position`,`plate_barcode`),
        KEY `plate_barcode` (`plate_barcode`),
        KEY `sample_name` (`sample_name`),
        CONSTRAINT `wells_ibfk_1` FOREIGN KEY (`plate_barcode`) REFERENCES `plate` (`plate_barcode`) ON DELETE CASCADE,
        CONSTRAINT `wells_ibfk_2` FOREIGN KEY (`sample_name`) REFERENCES `sample` (`sample_name`) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1 |""", cursor, cnx)
        

        add_data("""INSERT INTO customer (first_name, last_name) VALUES ('Sangeetha', 'Bheeman')""", cursor, cnx)
        add_data("""INSERT INTO sample (sample_name, customer_id) VALUES ('ezlCuTEDNl', '1')""", cursor, cnx)
        add_data("""insert into library_tube(library_tube_barcode, sample_tag_list)
                     values('NT0001','["GATCGCAT", "ATTGGCAT"]')""", cursor, cnx)

        add_data("""insert into plate(plate_barcode, no_of_wells) values('DN00001', 96);""",cursor, cnx)
        add_data("""insert into wells(well_position, plate_barcode, sample_name) values('A1','DN00001','ezlCuTEDNl');""", cursor, cnx)

        cursor.close()
        cnx.close()

        testconfig = {
            'host': MYSQL_HOST,
            'user': MYSQL_USER,
            'password': MYSQL_PASSWORD,
            'database': MYSQL_DB
        }
        cls.mock_db_config = patch.dict(config.connection_config, testconfig)

    @classmethod
    def tearDownClass(cls):
        cnx = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD
        )
        cursor = cnx.cursor(dictionary=True)

        # drop test database
        try:
            cursor.execute("DROP DATABASE {}".format(MYSQL_DB))
            cnx.commit()
            cursor.close()
        except mysql.connector.Error as err:
            print("Database {} does not exists. Dropping db failed".format(MYSQL_DB))
        cnx.close()
