import os

XML_DIR = os.path.dirname(os.path.abspath(__file__))


def xml_data(file_name):
    with open(f"{XML_DIR}/{file_name}.xml", "rb") as xml_file:
        data = xml_file.read()
    return data
