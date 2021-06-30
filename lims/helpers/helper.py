import random
import string
from database_connections import DBConnection

def connect_to_db():
    db_connection = DBConnection()
    connection = db_connection.create_connection()
    connection.reconnect()
    return connection

def get_random_string():
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(10))
    return result_str

def check_if_sample_name_exists(sample_name):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "select sample_name from sample"
    cursor.execute(query)
    records = cursor.fetchall()
    is_sample_name_exists = False
    for row in records:
        if sample_name == row[0]:
            is_sample_name_exists = True
    
    cursor.close()
    if connection:
        connection.close()
    return is_sample_name_exists


def create_sample_name():
    sample_name = get_random_string()
    is_duplicate = check_if_sample_name_exists(sample_name)
    while(is_duplicate):
        sample_name = get_random_string()
        is_duplicate = check_if_sample_name_exists(sample_name)

    return sample_name


def get_sample_by_sample_name(sample_name):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        query = "select * from sample where sample_name=%s"
        value = (sample_name,)
        cursor.execute(query, value)
        result = cursor.fetchone()
        return result
    except Error as e:
        print("Error:%s", e)


def get_sample_by_tag(tag):
    try: 
        connection = connect_to_db()
        cursor = connection.cursor()
        query = "select * from sample where tag=%s"
        value = (tag,)
        cursor.execute(query, value)
        result = cursor.fetchone()
        return result
    except Error as e:
        print("Error:%s", e)


def get_sample_list_from_tags(tag_list):
    format_strings = ','.join(['%s'] * len(tag_list))
    try: 
        connection = connect_to_db()
        cursor = connection.cursor()
        query = "select * from sample where tag in (%s)" % format_strings
                
        cursor.execute(query, tag_list) 
        records = cursor.fetchall()
        samples = []
        if records:
            for row in records:
                samples.append(row)
        else:
            "Samples not found"
        
        return samples
    except Error as e:
        print("Error:%s", e)


def fetch_all_from_sample_list(sample_name_list):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        format_strings = ','.join(['%s'] * len(sample_name_list))
        query = "select * from sample where sample_name in (%s)" % format_strings
                
        cursor.execute(query, sample_name_list) 
        records = cursor.fetchall()
        return records
    except Error as e:
        print("Error:%s", e)


def display_sample_and_tags(sample_records):
    print("Sample       Tag")
    for row in sample_records:
        print(row[0], row[3])