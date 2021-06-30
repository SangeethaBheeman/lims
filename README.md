Requirements:

Python 3.6.1
Mysql
pip install pipenv
pipenv install mysql-connector-python

MySQL:

MySQL dump for the database is attached 

Class Diagram:

ER and class diagrams are attached.

Assumptions made to complete the code:

1. Included "receive_sample" command to collect customer name and an optional sample name field.
Sample name will be auto generated.

2. Move samples is done between library tube to library tube or between plates.

3. Library tube is designed to store list/array of samples.


Tests:

Started writing tests, but are incomplete.

The method signatures for the user stories can be run using the following commands:

python main.py receive_sample  --first_name Harry --last_name Potter
Saved customer details
Saved sample

python main.py record_receipt --sample_name yBZpQyfVxA --sample_tube_barcode NT00001
updated successfully


python main.py find_sample --tube_barcode NT00001
Sample name: yBZpQyfVxA


python main.py tag --sample_name yBZpQyfVxA --tag TAACCGCAT
updated successfully

python main.py multiplex --tagged_samples TAACCGCAT  --library_tube_barcode NT00001
Record saved


python main.py add --sample_name cjjQVrrTGW --plate_barcode DN00001
Sample name not found


python main.py add --sample_name ANaErJtHto --plate_barcode DN00001
updated successfully

python main.py list_samples --barcode DN00001
Sample       Tag
ANaErJtHto None


python main.py move_samples --source_tube_barcode NT00001 --destination_tube_barcode NT00002
Record saved
Removed samples from library tube

