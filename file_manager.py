import json
import os
import datetime
import decimal
from enum import Enum

def converter(o):
    if isinstance(o, datetime.datetime):
        return o.strftime("%d/%m/%yT%H:%M:%SZ")
    elif isinstance(o, datetime.date):
        return o.strftime("%d/%m/%y")
    try: 
        return json.dumps(o)
    except Exception as e:
        return str(o)

class DumpJsonFormat(Enum):
    JsonRow = 'json_rows'
    ListOfObjects = 'list_of_objects'


class DumpJSONMetadata:
    '''Fields:
    {
        'format': 'json_rows' or 'list_of_objects' default: 'list_of_objects'
    }
    '''

    def __init__(self,metadata:dict):
        self.save_path = metadata.get('save_path', '')
        self.filename = metadata.get('filename', converter(datetime.datetime.now))
        if self.save_path != '' and self.save_path[-1] != '/':
            self.save_path += '/'
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
        jsonformat = metadata.get('format', 'list_of_objects')
        if jsonformat == DumpJsonFormat.JsonRow._value_:
            self.format = DumpJsonFormat.JsonRow
        elif jsonformat == DumpJsonFormat.ListOfObjects._value_:
            self.format = DumpJsonFormat.ListOfObjects
        else:
            raise AttributeError(
                f'El formato de salida {jsonformat} no esta especificado')


def create_json_file(file_path,file_name,data):
    config = {"save_path":file_path,"filename":file_name}
    save(DumpJSONMetadata(config),data)

def save(djs:DumpJSONMetadata,data):
    json_filename = f'{djs.filename}.json'

    with open(djs.save_path + json_filename, 'w') as output:
        if djs.format == DumpJsonFormat.JsonRow:

            for l in data:
                output.write(json.dumps(l) + '\n')

        elif djs.format == DumpJsonFormat.ListOfObjects:
            output.write(json.dumps(data, default=converter))