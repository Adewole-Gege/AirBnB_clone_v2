#!/usr/bin/python3
"""
FileStorage module for the HBNB project.

This module defines a class to manage file storage in JSON format.
"""

import json


class FileStorage:
    """
    Serializes instances to a JSON file and deserializes JSON file to instances.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """
        Returns the dictionary __objects.
        If cls is provided, returns objects of that type.
        """
        if cls:
            return {k: v for k, v in self.__objects.items() if isinstance(v, cls)}
        return self.__objects

    def new(self, obj):
        """
        Sets in __objects the obj with key <obj class name>.id.
        """
        if obj:
            key = f"{obj.__class__.__name__}.{obj.id}"
            self.__objects[key] = obj

    def save(self):
        """
        Serializes __objects to the JSON file (path: __file_path).
        """
        with open(self.__file_path, "w", encoding="utf-8") as f:
            temp = {key: obj.to_dict() for key, obj in self.__objects.items()}
            json.dump(temp, f)

    def reload(self):
        """
        Deserializes the JSON file to __objects (only if the JSON file exists).
        """
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review
        from models.place import Place

        classes = {
            "BaseModel": BaseModel,
            "User": User,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Review": Review,
            "Place": Place
        }
        try:
            with open(self.__file_path, "r", encoding="utf-8") as f:
                obj_dict = json.load(f)
            for key, value in obj_dict.items():
                cls_name = value["__class__"]
                if cls_name in classes:
                    self.__objects[key] = classes[cls_name](**value)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """
        Deletes obj from __objects if it exists.
        """
        if obj is not None:
            key = f"{obj.__class__.__name__}.{obj.id}"
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """
        Calls reload() method for deserializing the JSON file to objects.
        """
        self.reload()
