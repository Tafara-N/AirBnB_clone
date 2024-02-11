#!/usr/bin/python3

"""
AirBnB_clone console for the AirBnB project
"""


import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(arg):
    curly_brackets = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_brackets is None:
        if brackets is None:
            return [x.strip(",") for x in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            retl = [x.strip(",") for x in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:curly_brackets.span()[0]])
        retl = [x.strip(",") for x in lexer]
        retl.append(curly_brackets.group())
        return retl


class HBNBCommand(cmd.Cmd):
    """
    AirBnb_clone (HolbertonBnB) command interpreter

    Attributes:
        prompt (str): Command prompt
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """ Does nothing when it receives an empty line """
        pass

    def default(self, arg):
        """
        Behavior of the cmd module when input is invalid
        """

        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)

        if match is not None:
            argl = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", argl[1])
            if match is not None:
                command = [argl[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = "{} {}".format(argl[0], command[1])
                    return argdict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """ Quit (exits) program """

        return True

    def do_EOF(self, arg):
        """ EOF's signal to exit the program """

        print("")
        return True

    def do_create(self, arg):
        """
        Usage: create <class>
        Creates a new class instance and print its id.
        """

        argl = parse(arg)
        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(argl[0])().id)
            storage.save()

    def do_show(self, arg):
        """
        Usage: show <class> <id> or <class>.show(<id>)
        Displays the string representation of a class instance of a given id.
        """

        argl = parse(arg)
        objdict = storage.all()

        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argl) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argl[0], argl[1]) not in objdict:
            print("** no instance found **")
        else:
            print(objdict["{}.{}".format(argl[0], argl[1])])

    def do_destroy(self, arg):
        """
        Usage: destroy <class> <id> or <class>.destroy(<id>)
        Deletes a class instance of a given id
        """

        argl = parse(arg)
        objdict = storage.all()

        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argl) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argl[0], argl[1]) not in objdict.keys():
            print("** no instance found **")
        else:
            del objdict["{}.{}".format(argl[0], argl[1])]
            storage.save()

    def do_all(self, arg):
        """
        Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects
        """

        argl = parse(arg)
        if len(argl) > 0 and argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objl = []
            for objct in storage.all().values():
                if len(argl) > 0 and argl[0] == objct.__class__.__name__:
                    objl.append(obj.__str__())
                elif len(argl) == 0:
                    objl.append(obj.__str__())
            print(objl)

    def do_count(self, arg):
        """
        Usage: count <class> or <class>.count()
        Retrieves the number of instances of a given class
        """

        argl = parse(arg)
        count = 0
        for objct in storage.all().values():
            if argl[0] == objct.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, arg):
        """
        Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary
        """

        argl = parse(arg)
        objdict = storage.all()

        if len(argl) == 0:
            print("** class name missing **")
            return False
        if argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(argl) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(argl[0], argl[1]) not in objdict.keys():
            print("** no instance found **")
            return False
        if len(argl) == 2:
            print("** attribute name missing **")
            return False
        if len(argl) == 3:
            try:
                type(eval(argl[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(argl) == 4:
            objct = objdict["{}.{}".format(argl[0], argl[1])]
            if argl[2] in objct.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[argl[2]])
                objct.__dict__[argl[2]] = valtype(argl[3])
            else:
                objct.__dict__[argl[2]] = argl[3]
        elif type(eval(argl[2])) == dict:
            objct = objdict["{}.{}".format(argl[0], argl[1])]
            for key, value in eval(argl[2]).items():
                if (key in objct.__class__.__dict__.keys() and
                    type(objct.__class__.__dict__[key]) in {str, int, float}):
                    valtype = type(objct.__class__.__dict__[key])
                    objct.__dict__[key] = valtype(value)
                else:
                    objct.__dict__[key] = value
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
