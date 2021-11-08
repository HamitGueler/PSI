import os

"""A simple class which is to create a specific file in a selected directory.  If there are other specific tests, 
e.g. "delete_file" etc. The function for this could be written in this class and used by the TestSystem class. The 
idea is to have classes for specific test purposes, which are then used and performed by the TestSystem class. """


class FileCreator:
    def create_file(self, directory, file_name):
        try:
            path = self.create_valid_path(directory) + file_name

            with open(path, "w") as file:
                file.write("FILE CREATED")
            return True
        except FileNotFoundError as e:
            print(e)
            return False
        except FileExistsError as e:
            return False
        except IOError as e:
            print(e)
            return False

    # function could be improved, but for this purpose it should be enough
    def create_valid_path(self, file_path):
        if file_path.startswith("/"):
            file_path = "." + file_path

        file_path = os.path.abspath(file_path)
        return file_path + "/"
