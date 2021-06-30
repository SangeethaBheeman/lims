import config
from database_connections import DBConnection

def connect_to_db():
    db_connection = DBConnection()
    connection = db_connection.create_connection()
    connection.reconnect()
    return connection

def get_empty_well_position(plate_barcode, no_of_wells):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        query = "select well_position from wells where plate_barcode=%s \
                    order by created_date, well_position desc limit 1"
        
        values = (plate_barcode,)
        cursor.execute(query,values)
        record = cursor.fetchone()
        well_config = config.well_matrix[no_of_wells]
        if record:
            last_filled_well = record[0]
            
            if int(last_filled_well[1:]) < well_config['columns']:
                next_empty_well = last_filled_well[0] + str(int(last_filled_well[1:])+1)
            else:
                next_empty_well = chr(ord(last_filled_well[0]) + 1) + '1'
        else:
            next_empty_well = well_config['row_starts_with'] + '1'

        return next_empty_well
    except Error as e:
        print("Error:%s", e)

