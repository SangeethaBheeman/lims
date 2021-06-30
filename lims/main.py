import argparse
from mysql.connector import Error
from src.customer import Customer
from src.sample import Sample
from src.library_tube import LibraryTube
from src.plate import Plate
from src.well import Well
from helpers import helper, plate_helper, library_tube_helper, well_helper
import config


def receive_sample(first_name, last_name, sample_name=None):
    customer_obj = Customer(first_name, last_name)
    customer_obj.save_customer_details()
    customer_id = customer_obj.get_customer_id()
    
    if not sample_name:
        sample_name = helper.create_sample_name()
    
    sample_obj = Sample(sample_name)
    sample_obj.save_sample(customer_id)


def record_receipt(sample_name, sample_tube_barcode):
    result = helper.get_sample_by_sample_name(sample_name)
    if result:
        sample_obj = Sample(sample_name)
        sample_obj.add_sample_tube_barcode(sample_tube_barcode)
    else:
        print("Sample name not found")


def find_sample(sample_tube_barcode):
    try:
        connection = helper.connect_to_db()
        cursor = connection.cursor()
        query = "select * from sample where sample_tube_barcode=%s"
        value = (sample_tube_barcode,)
        cursor.execute(query, value)
        result = cursor.fetchone()
        if result:
            print("Sample name: {0}".format(result[0]))
    except Error as e:
        print("Error:%s", e)


def tag(sample_name, tag):
    result = helper.get_sample_by_sample_name(sample_name)
    if result:
        sample_obj = Sample(sample_name)
        sample_obj.add_tag(tag)
    else:
        print("Sample name not found")


def multiplex(tagged_samples, library_tube_barcode):
    tagged_samples = tagged_samples.split(',')
    sample_not_found = []
    for tag in tagged_samples:
        result = helper.get_sample_by_tag(tag)
        if not result:
            sample_not_found.append(tag)
    
    if len(sample_not_found) > 0:
        print("Sample not found for tag/tags {0}".format(sample_not_found))
        for tag in sample_not_found:
            tagged_samples.remove(tag)

    tags = library_tube_helper.get_tags_from_library_tube(library_tube_barcode)
    if tags:
        tagged_samples.extend(tags)
    library_tube_obj = LibraryTube(library_tube_barcode)
    library_tube_obj.add_samples_to_library_tube(tagged_samples)


def add(sample_name, plate_barcode):
    """Add sample to a plate"""
    result = helper.get_sample_by_sample_name(sample_name)
    if result:
        plate_obj = Plate(plate_barcode)
        plate_obj.create_or_update_plate()
        no_of_wells = plate_obj.get_well_count()
        well_position = well_helper.get_empty_well_position(plate_barcode, no_of_wells)
        well_obj = Well(plate_barcode, well_position)
        well_obj.add_sample_to_well(sample_name)
    else:
        print("Sample name not found")


def list_samples(barcode):
    if barcode[:2] == 'DN':
        samples = plate_helper.get_samples_from_plate(barcode)
        if samples:
            records = helper.fetch_all_from_sample_list(samples)
            helper.display_sample_and_tags(records)
        else:
            print("Plate not found")
                    
    elif barcode[:2] == 'NT':
        tags = library_tube_helper.get_tags_from_library_tube(barcode)
        if tags:
            records = helper.get_sample_list_from_tags(tags)
            helper.display_sample_and_tags(records) 
        else:
            print("Library tube not found")
    else:
        print("Barcode not found")
        raise error


def move_samples(source_tube_barcode, destination_tube_barcode):
    if source_tube_barcode[:2] == 'DN':
        sample_names = plate_helper.get_samples_from_plate(source_tube_barcode)
        if sample_names:
            plate_helper.add_samples_to_plate(sample_names, destination_tube_barcode)
            plate_obj = Plate(source_tube_barcode)
            no_of_wells = plate_obj.get_well_count()
            well_position = well_helper.get_empty_well_position(source_tube_barcode, no_of_wells)
            well_obj = Well(source_tube_barcode, well_position)
            well_obj.delete_samples_from_well(sample_names)
    elif source_tube_barcode[:2] == 'NT':
        tags = library_tube_helper.get_tags_from_library_tube(source_tube_barcode)
        if tags:
            library_tube_obj = LibraryTube(destination_tube_barcode)
            library_tube_obj.add_samples_to_library_tube(tags)
            source_library_tube_obj = LibraryTube(source_tube_barcode)
            source_library_tube_obj.delete_samples_from_library_tube()
    else:
        print("Invalid Source tube barcode")


def add_subparser(subparsers, **kwargs):

    parser = subparsers.add_parser(kwargs['cmd'], help = kwargs['cmd_help'])
    
    for i in range(1, kwargs['no_of_args'] + 1):
        arg_dict = kwargs['arg' + str(i)]
        if arg_dict['optional'] == True:
            arg_name = '--'+ arg_dict['arg_name'] 
        else:
            arg_name = arg_dict['arg_name'] 


        if arg_dict.get('nargs') is not None:
            parser.add_argument(arg_name, required=arg_dict['required'],
                            help=arg_dict['help'])
        else:    
            parser.add_argument(arg_name, required=arg_dict['required'],
                            help=arg_dict['help'])


    if kwargs.get('func') is not None:
        parser.set_defaults(func=eval(kwargs['func']))


def main():

    parser = argparse.ArgumentParser(description='Labware & Containers LIMS')
    subparsers = parser.add_subparsers(dest='cmd',
                                       help='sub-command help')
    subparsers.required = True

    for args_name in config.args_for_methods:
        add_subparser(subparsers, **args_name)

    args = parser.parse_args()
    
    if args.cmd == 'receive_sample':
        args.func(args.first_name, args.last_name, args.sample_name)
    elif args.cmd == 'record_receipt':
        args.func(args.sample_name, args.sample_tube_barcode)
    elif args.cmd == 'find_sample':
        args.func(args.tube_barcode)
    elif args.cmd == 'tag':
        args.func(args.sample_name, args.tag)
    elif args.cmd == 'multiplex':
        args.func(args.tagged_samples, args.library_tube_barcode)
    elif args.cmd == 'add':
        args.func(args.sample_name, args.plate_barcode)
    elif args.cmd == 'list_samples':
        args.func(args.barcode)
    elif args.cmd == 'move_samples':
        args.func(args.source_tube_barcode, args.destination_tube_barcode)

    
    

if __name__ == "__main__":
    main()

