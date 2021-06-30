connection_config = {
    "host": "localhost", #"rajkumars-MacBook-Pro.local",
    "user": "root",
    "password": "root",
    "database": "lims"
}



well_matrix = {
    96: {
        'rows': 8, 
        'columns': 12,
        'row_starts_with': 'A',
        'row_ends_with': 'H'
    },
    384: {
        'rows': 16,
        'columns': 24,
        'row_starts_with': 'A',
        'row_ends_with': 'P'
    }
}

args_to_receive_sample = {
        'cmd': 'receive_sample',
        'cmd_help': 'Collect customer name and sample name',
        'no_of_args': 3,
        'func': 'receive_sample',
        'arg1': {
            'arg_name': 'first_name',
            'optional': True,
            'required': True,
            'help': 'first name'
        },
        'arg2': {
            'arg_name': 'last_name',
            'optional': True,
            'required': True,
            'help': 'last name'
        },
        'arg3': {
            'arg_name': 'sample_name',
            'optional': True,
            'required': False,
            'help': 'sample name'
        }
    }

args_to_record_receipt = {
        'cmd': 'record_receipt',
        'cmd_help': 'Add sample to sample tube',
        'no_of_args': 2,
        'func': 'record_receipt',
        'arg1': {
            'arg_name': 'sample_name',
            'optional': True,
            'required': True,
            'help': 'sample name'
        },
        'arg2': {
            'arg_name': 'sample_tube_barcode',
            'optional': True,
            'required': True,
            'help': 'sample tube barcode'
        }
    }

args_to_find_sample = {
    'cmd': 'find_sample',
    'cmd_help': 'find sample name with sample tube barcode',
    'no_of_args': 1,
    'func': 'find_sample',
    'arg1': {
        'arg_name': 'tube_barcode',
        'optional': True,
        'required': True,
        'help': 'sample tube barcode'
    }
}

args_to_tag_sample = {
    'cmd': 'tag',
    'cmd_help': 'Append tag to samples',
    'no_of_args': 2,
    'func': 'tag',
    'arg1': {
        'arg_name': 'sample_name',
        'optional': True,
        'required': True,
        'help': 'sample name',
    },
    'arg2': {
        'arg_name': 'tag',
        'optional': True,
        'required': True,
        'help': 'DNA sequence'
    }
}

args_for_multiplexing = {
    'cmd': 'multiplex',
    'cmd_help': 'Load tagged samples to library tube',
    'no_of_args': 2,
    'func': 'multiplex',
    'arg1': {
        'arg_name': 'tagged_samples',
        'optional': True,
        'required': True,
        'help': 'tag names',
        'nargs': "+"
    },
    'arg2': {
        'arg_name': 'library_tube_barcode',
        'optional': True,
        'required': True,
        'help': 'library tube barcode'
    }
}


args_for_adding_to_plate = {
    'cmd': 'add',
    'cmd_help': 'Add sample to a plate',
    'no_of_args': 2,
    'func': 'add',
    'arg1': {
        'arg_name': 'sample_name',
        'optional': True,
        'required': True,
        'help': 'sample name',
    },
    'arg2': {
        'arg_name': 'plate_barcode',
        'optional': True,
        'required': True,
        'help': 'plate barcode'
    }
}


args_to_list_samples = {
    'cmd': 'list_samples',
    'cmd_help': 'List samples in a library tube/plate',
    'no_of_args': 1,
    'func': 'list_samples',
    'arg1': {
        'arg_name': 'barcode',
        'optional': True,
        'required': True,
        'help': 'library tube/ plate barcode',
    }
}


args_to_move_samples = {
    'cmd': 'move_samples',
    'cmd_help': 'Move samples from a source library tube/plate to a destination tube/plate',
    'no_of_args': 2,
    'func': 'move_samples',
    'arg1': {
        'arg_name': 'source_tube_barcode',
        'optional': True,
        'required': True,
        'help': 'library tube/ plate barcode',
    },
    'arg2': {
        'arg_name': 'destination_tube_barcode',
        'optional': True,
        'required': True,
        'help': 'library tube/ plate barcode',
    }
}



args_for_methods = [
    args_to_receive_sample,
    args_to_record_receipt,
    args_to_find_sample,
    args_to_tag_sample,
    args_for_multiplexing,
    args_for_adding_to_plate,
    args_to_list_samples,
    args_to_move_samples
] 