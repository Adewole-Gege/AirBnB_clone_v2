#!/usr/bin/python3
"""
FileStorage module for the HBNB project.

Contains the FileStorage class that serializes instances to a JSON file
and deserializes JSON file to instances.
"""
import json


class FileStorage:
    """
    Serializes instances to a JSON file and deserializes
    JSON file to instances.
    """

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """
        Returns a dictionary of all objects, or objects of a specific class.
        """
        if cls:
            return {
                k: v for k, v in self.__objects.items() if isinstance(v, cls)
            }
        return self.__objects

    def new(self, obj):
        """
        Adds a new object to the storage dictionary.
        """
        if obj:
            key = f"{obj.__class__.__name__}.{obj.id}"
            self.__objects[key] = obj

    def save(self):
        """
        Saves the current dictionary of objects to the JSON file.
        """
        with open(self.__file_path, "w", encoding="utf-8") as f:
            temp = {
                key: obj.to_dict() for key, obj in self.__objects.items()
            }
            json.dump(temp, f)

    def reload(self):
        """
        Loads data from the JSON file into __objects.
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
        Call reload() method for deserializing the JSON file to objects.
        """
        self.reload()
