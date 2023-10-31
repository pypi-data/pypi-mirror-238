'''
:authors: Hleb0227
:license: Apache License, Version 2.0, see LICENSE file

:copyright: (c) 2023 Hleb0227
'''

from json import dumps, loads, load
from .json_db_exceptions import JsonDBError

class json_db:
    def __init__(self, name: str) -> None: #create file for database
        self.name = name
        try:
            with open(f'{name}.json') as f:
                file = load(f)
            self.json = file
        except:
            file1 = open(f"{name}.json", "w")
            self.json = {}
            file1.write(dumps(self.json))
            file1.close()

    def commit(self) -> None: #update information in file.json
        try:
            a = False
            file = open(f"{self.name}.json", "w")
            file.write(dumps(self.json))
            file.close()
        except:
            a = True
        if a:
            raise JsonDBError('Undefindet error. Maybe you deleted file with database?')

    def update(self) -> None: #get new self.json from file.json
        try:
            a = False
            file = open(f"{self.name}.json", "r")
            self.json = loads(file.read())
            file.close()
        except:
            a = True
        if a:
            raise JsonDBError('Undefindet error. Maybe you deleted file with database?')

    def get(self, name: str) -> list: #get somebody from database
        try:
            return self.json[name]
        except KeyError:
            pass
        raise JsonDBError('Name undefindet')
    
    def delete(self, name: str) -> None: #delete somebody from database
        try:
            del self.json[name]
            return None
        except KeyError:
            pass 
        raise JsonDBError('Name undefindet')
    
    def redact(self, name: str, new_dict: list = []) -> None: #create and redact type in database
        if type(new_dict) != list:
            raise JsonDBError('type variable "new_dict" must be "dict"')
        self.json[name] = new_dict
        return None
    
