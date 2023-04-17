#!/usr/bin/python3
"""
Contains the FileStorage class, which is used to serialize instances to a JSON file and
deserialize back to instances.
"""

import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

# A dictionary mapping class names to their corresponding classes.
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class FileStorage:
    """A class used to serialize instances to a JSON file and deserialize back to instances."""

    # The path to the JSON file.
    __file_path = "file.json"
    # A dictionary that stores all objects by <class name>.id.
    __objects = {}

    def all(self, cls=None):
        """
        Returns a dictionary of all objects stored in __objects.

        If cls is specified, returns a new dictionary containing only the objects
        that match the specified class.
        """
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects

    def new(self, obj):
        """
        Adds the specified object to __objects with the key <obj class name>.id.
        """
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """
        Serializes __objects to the JSON file at the path specified in __file_path.
        """
        json_objects = {}
        for key in self.__objects:
            json_objects[key] = self.__objects[key].to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """
        Deserializes the JSON file at the path specified in __file_path into __objects.
        """
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            for key in jo:
                self.__objects[key] = classes[jo[key]["__class__"]](**jo[key])
        except Exception:
            pass

    def delete(self, obj=None):
        """
        Deletes the specified object from __objects if it is stored.
        """
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """
        Calls reload() to deserialize the JSON file into objects.
        """
        self.reload()

    def get(self, cls, id):
        """
        Returns the object with the specified class and ID, or None if it is not found.
        """
        if cls is None or id is None:
            return None
        else:
            all_obj = self.all(cls)
            for obj in all_obj.values():
                if obj.id == id:
                    return obj
            return None

    def count(self, cls=None):
        """
        Returns the number of objects stored in __objects that match the specified class.

        If no class is specified, returns the count of all objects in __objects.
        """
        return len(self.all(cls))