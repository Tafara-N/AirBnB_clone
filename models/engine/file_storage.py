#!/usr/bin/python3

"""
FileStorage class
"""

import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """
    Abstracted storage engine.

    Attributes:
        __file_path (str): File name to save objects to
        __objects (dict): Dictionary of instantiated objects
    """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """ The dictionary __objects """

        return FileStorage.__objects

    def new(self, obj):
        """
        Setting in __objects obj with key <obj_class_name>.id
        """

        ocname = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(ocname, obj.id)] = obj

    def save(self):
        """
        Serializing __objects to JSON file __file_path.
        """

        odict = FileStorage.__objects
        objdict = {obj: odict[obj].to_dict() for obj in odict.keys()}
        with open(FileStorage.__file_path, "w") as f:
            json.dump(objdict, f)

    def reload(self):
        """
        Deserializing JSON file __file_path to __objects, only if it exists
        """

        try:
            with open(FileStorage.__file_path) as f:
                objdict = json.load(f)
                for obj in objdict.values():
                    cls_name = obj["__class__"]
                    del obj["__class__"]
                    self.new(eval(cls_name)(**obj))
        except FileNotFoundError:
            return
