# AirBnB_clone Project

<div align="center">

  <h1>HBNB - The Console <img src="https://i.imgur.com/elr4ah9.png" width=55 align=center> </h1>
</div>

<img align="center" src="https://i.imgur.com/MQq3ABc.png" alt="Logo">

## Description

The first part of this project involves simulating an Airbnb application by creating a control system for the modules used on our web page. We achieve this by implementing a JSON-format database and leveraging object-oriented programming, Python data translation, and command interpretation. The result is a local database that can be easily modified using specific commands, providing a flexible and efficient way to manage data.

<img src="https://i.imgur.com/fcl4PRY.png" alt="Structure">

### Functionalities of the command interpreter

* Creates new object (ex: a new User or a new Place)
* Retrieves an object from a file, a database etc...
* Does operations on objects (count, compute stats, etc...)
* Updates attributes of an object
* Destroys an object

## Table of Content

* [Environment](#environment)
* [Installation](#installation)
* [File Descriptions](#file-descriptions)
* [How to use:](#how-to-use:)
* [Authors](#authors)
* [Licence](#licence)

## Environment

This project is interpreted/tested on Ubuntu 22.04 LTS using python3 (version 3.12.2)

## Installation

* Clone this repository: `git clone "https://github.com/Tafara-N/AirBnB_clone.git"`
* Access AirBnb directory: `cd AirBnB_clone`
* Run hbnb(interactively): `./console` and press enter
* Run hbnb(non-interactively): `echo "<command>" | ./console.py`

## File Descriptions

[console.py](console.py) - The console contains the entry point of the command interpreter.
List of commands this console current supports:

* `EOF` - exits console
* `quit` - exits console
* `<emptyline>` - Overwrites default emptyline method and does nothing
* `create` - Creates a new instance of`BaseModel`, saves it (to the JSON file) and prints the id
* `destroy` - Deletes an instance based on the class name and id (save the change into the JSON file).
* `show` - Prints the string representation of an instance based on the class name and id.
* `all` - Prints all string representation of all instances based or not on the class name.
* `update` - Updates an instance based on the class name and id by adding or updating attribute (save the change into the JSON file).

## `models/` Directory contains classes used for this project

[base_model.py](/models/base_model.py) - The BaseModel class from which future classes will be derived

* `def __init__(self, *args, **kwargs)` - Initialization of the base model
* `def __str__(self)` - String representation of the BaseModel class
* `def save(self)` - Updates the attribute `updated_at` with the current datetime
* `def to_dict(self)` - Returns a dictionary containing all keys/values of the instance

Classes inherited from Base Model:

* [amenity.py](/models/amenity.py)
* [city.py](/models/city.py)
* [place.py](/models/place.py)
* [review.py](/models/review.py)
* [state.py](/models/state.py)
* [user.py](/models/user.py)

## `/models/engine` Directory containing File Storage class that handles JSON serialization and deserialization

[file_storage.py](/models/engine/file_storage.py) - Serializing instances to a JSON file & deserializes back to instances

* `def all(self)` - Returns dictionary __objects
* `def new(self, obj)` - Sets in __objects the obj with key <obj class name>.id
* `def save(self)` - Serializing __objects to the JSON file (path:__file_path)
* `def reload(self)` - Deserializing the JSON file to __objects

## `/tests` Directory contains all unit test cases of this project

[test_console.py](/tests/test_console.py)
Tests classes:

* `class TestHBNBCommandPrompting(unitest.TestCase)` - Testing the HBNB command interpreter's prompting
* `class TestHBNBCommandHelp (unitest.TestCase)` - Testing the HBNB command interpreter's help message
* `class TestHBNBCommandExit (unitest.TestCase)` Testing the HBNB command interpreter's quit/exit
* `class TestHBNBCommandCreate (unitest.TestCase)` Testing the HBNB command interpreter's create
* `class TestHBNBCommandShow (unitest.TestCase)` - Testing the HBNB command interpreter's show
* `class TestHBNBCommandDestroy (unitest.TestCase)` - Testing the HBNB command interpreter's destroy
* `class TestHBNBCommandAll (unitest.TestCase)` - Testing the HBNB command interpreter's all
* `class TestHBNBCommandUpdate (unitest.TestCase)` - Testing the HBNB command interpreter's update
* `class TestHBNBCommandCount(unittest.TestCase)` - Testing the HBNB command interpreter's count


[/test_models/test_base_model.py](/tests/test_models/test_base_model.py) - Contains the TestBaseModel and TestBaseModelDocs classes

TestBaseModel classes

[/test_models/test_amenity.py](/tests/test_models/test_amenity.py) - Contains the TestAmenity class

[/test_models/test_city.py](/tests/test_models/test_city.py) - Contains the TestCity class

[/test_models/test_file_storage.py](/tests/test_models/test_file_storage.py) - Contains the TestFileStorage class:

[/test_models/test_place.py](/tests/test_models/test_place.py) - Contains the TestPlace class

[/test_models/test_review.py](/tests/test_models/test_review.py) - Contains the TestReview class

[/test_models/state.py](/tests/test_models/test_state.py) - Contains the TestState class

[/test_models/user.py](/tests/test_models/test_user.py) - Contains the TestUser class

## How to use

```python
vagrantAirBnB_clone$ ./console.py
(hbnb) help

Documented commands (type help <topic>):
========================================
EOF  all  create  destroy  help  quit  show  update

(hbnb) all MyModel
** class doesn't exist **
(hbnb) create BaseModel
7da56403-cc45-4f1c-ad32-bfafeb2bb050
(hbnb) all BaseModel
[[BaseModel] (7da56403-cc45-4f1c-ad32-bfafeb2bb050) {'updated_at': datetime.datetime(2017, 9, 28, 9, 50, 46, 772167), 'id': '7da56403-cc45-4f1c-ad32-bfafeb2bb050', 'created_at': datetime.datetime(2017, 9, 28, 9, 50, 46, 772123)}]
(hbnb) show BaseModel 7da56403-cc45-4f1c-ad32-bfafeb2bb050
[BaseModel] (7da56403-cc45-4f1c-ad32-bfafeb2bb050) {'updated_at': datetime.datetime(2017, 9, 28, 9, 50, 46, 772167), 'id': '7da56403-cc45-4f1c-ad32-bfafeb2bb050', 'created_at': datetime.datetime(2017, 9, 28, 9, 50, 46, 772123)}
(hbnb) destroy BaseModel 7da56403-cc45-4f1c-ad32-bfafeb2bb050
(hbnb) show BaseModel 7da56403-cc45-4f1c-ad32-bfafeb2bb050
** no instance found **
(hbnb) quit
```

## Authors

* Tafara Nyamhunga - [Github](https://github.com/tafara-n)

## License

Public Domain. No copy write protection.

