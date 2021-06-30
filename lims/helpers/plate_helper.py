import sys
import os
app_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, app_path.rstrip('helpers'))
from src.plate import Plate
from src.well import Well
from . import well_helper
from database_connections import DBConnection


def connect_to_db():
    db_connection = DBConnection()
    connection = db_connection.create_connection()
    connection.reconnect()
    return connection

def get_samples_from_plate(plate_barcode):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        query = "select sample_name from wells where plate_barcode=%s group by sample_name;"
        value = (plate_barcode,)
        cursor.execute(query, value)
        records = cursor.fetchall()
        samples = []
        if records:
            for row in records:
                samples.append(row[0])
        else:
            "Plate not found/empty"    
        return samples
    except Error as e:
        print("Error:%s", e)


def add_sample_to_plate(sample_name, plate_barcode):
    """Add sample to a plate"""
    plate_obj = Plate(plate_barcode)
    no_of_wells = plate_obj.get_well_count()
    well_position = well_helper.get_empty_well_position(plate_barcode, no_of_wells)
    well_obj = Well(plate_barcode, well_position)
    well_obj.add_sample_to_well(sample_name)


def add_samples_to_plate(samples, plate_barcode):
    plate_obj = Plate(plate_barcode)
    plate_obj.create_or_update_plate('pending')
    no_of_wells = plate_obj.get_well_count()
    well_position = well_helper.get_empty_well_position(plate_barcode, no_of_wells)
    well_obj = Well(plate_barcode, well_position)
    for index, sample_name in enumerate(samples):
        if index == (len(samples)-1):
            plate_obj.update_plate_state('passed')
            add_sample_to_plate(sample_name, plate_barcode)
        else:
            plate_obj.update_plate_state('started')
            add_sample_to_plate(sample_name, plate_barcode)


def delete_samples_from_plate(sample_names, plate_barcode):
    delete_samples_from_well(sample_names, plate_barcode)
    


