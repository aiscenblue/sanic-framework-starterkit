import pkgutil
import os
import re as regex


"""
    Description:: Initialize the blueprints inside in the root folder
    and sub folder
    
    Requirements:: all directories and sub directories must consist of __init__.py
    to be considered as a package. 
    
    :: param app = sanic module
    files are ignored if its not end with .py or __.py
    
    NOTE :: directories must not consist of __ in their name
    
"""


class Init:

    __app = None

    def __init__(self, app):

        """ save sanic app module """
        self.__app = app
        root_path = __path__

        """ register blueprint to the current path """
        self.register_blueprint(root_path)

        """ loop root path and get the sub directories """
        for path in root_path:
            self.directory_path(path=path)

    def directory_path(self, path):

        """ get all the list of files and directories """
        for file in os.listdir(path):

            """ prevent __pycache__ directory or any directory that has __ """
            if "__" not in file:

                """ get the full path directory """
                dir_file = path + '/' + file

                """ check is the path is a directory 
                    only directories are picked
                """
                if os.path.isdir(dir_file):

                    """ register blueprint on the directory """
                    self.register_blueprint(dir_file)

                    """ find sub directories on each directory found """
                    self.directory_path(path=dir_file)

    def register_blueprint(self, path):

        """ find all packages in the current path """
        for loader, name, is_pkg in pkgutil.walk_packages(path, prefix="", onerror=None):

            """ if module found load module and save all attributes in the module found """
            mod = loader.find_module(name).load_module(name)

            """ find the attribute method on each module """
            if hasattr(mod, 'method'):

                """ register to the blueprint if method attribute found """
                self.__app.blueprint(mod.method)

            else:

                """ prompt not found notification """
                print('{} has no module attribute method'.format(mod))


def get_file_name(file):
    name = regex.sub('(.)([A-Z][a-z]+)(\s\s+)', r'\1_\2', file)
    return os.path.basename(name).replace(".py", "")
