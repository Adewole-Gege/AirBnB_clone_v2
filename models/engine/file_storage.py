#!/usr/bin/python3
"""
<<<<<<< HEAD
This module defines a class to manage file storage for the hbnb clone.
"""
=======
FileStorage module for the HBNB project.

This module defines a class to manage file storage in JSON format.
"""

>>>>>>> main
import json


class FileStorage:
    """
<<<<<<< HEAD
    This class manages storage of hbnb models in JSON format.
    """
    __file_path = 'file.json'
=======
    Serializes instances to a JSON file and deserializes JSON file to instances.
    """
    __file_path = "file.json"
>>>>>>> main
    __objects = {}

    def all(self, cls=None):
        """
<<<<<<< HEAD
        Returns a dictionary of models currently in storage.
        If a class is provided, filters objects of that class.
        """
        if cls is not None:
=======
        Returns the dictionary __objects.
        If cls is provided, returns objects of that type.
        """
        if cls:
>>>>>>> main
            return {k: v for k, v in self.__objects.items() if isinstance(v, cls)}
        return self.__objects

    def new(self, obj):
        """
<<<<<<< HEAD
        Adds new object to storage dictionary.
        """
        self.__objects[f"{obj.__class__.__name__}.{obj.id}"] = obj

    def save(self):
        """
        Saves storage dictionary to a JSON file.
        """
        with open(self.__file_path, 'w') as f:
            temp = {k: v.to_dict() for k, v in self.__objects.items()}
=======
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
>>>>>>> main
            json.dump(temp, f)

    def reload(self):
        """
<<<<<<< HEAD
        Loads storage dictionary from a JSON file.
        """
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
=======
        Deserializes the JSON file to __objects (only if the JSON file exists).
        """
        from models.base_model import BaseModel
        from models.user import User
>>>>>>> main
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review
<<<<<<< HEAD

        classes = {
            'BaseModel': BaseModel, 'User': User, 'Place': Place,
            'State': State, 'City': City, 'Amenity': Amenity,
            'Review': Review
        }
        try:
            with open(self.__file_path, 'r') as f:
                temp = json.load(f)
                self.__objects = {k: classes[v['__class__']](
                    **v) for k, v in temp.items()}
=======
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
>>>>>>> main
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """
        Deletes obj from __objects if it exists.
<<<<<<< HEAD
        Does nothing if obj is None.
        """
        if obj is not None:
            key = f"{obj.__class__.__name__}.{obj.id}"
            self.__objects.pop(key, None)

    def close(self):
        """
        Call reload() method for deserializing the JSON file to objects.
=======
        """
        if obj is not None:
            key = f"{obj.__class__.__name__}.{obj.id}"
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """
        Calls reload() method for deserializing the JSON file to objects.
>>>>>>> main
        """
        self.reload()
