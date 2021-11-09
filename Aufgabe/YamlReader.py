import yaml

"""
Class to read yaml files and check their contents.
This class could check for different contents depending on the test purpose.
"""


class YamlReader:
    def __init__(self, file_path):
        self.__file_path = file_path

    def read_yaml(self):
        try:
            with open(self.__file_path, "r") as yaml_file:
                yaml_data = yaml.load(yaml_file, Loader=yaml.Loader)

            return yaml_data
        except yaml.YAMLError as e:
            print(e)
            return []
        except FileNotFoundError as e:
            print(e)
            return []
        except IOError as e:
            print(e)
            return []

    """
    Function checks if some necessary Keys are missing in the Yaml-File
    """

    def validate_yaml(self, yaml_data):
        missing_list = [0, 0, 0, 0]

        if yaml_data["When"] is None or yaml_data["Then"] is None:

            if yaml_data["When"] is None and yaml_data["Then"] is None:
                missing_list[0] = 1
                missing_list[1] = 1
                missing_list[2] = 1
                missing_list[3] = 1

            if yaml_data["When"] is not None and yaml_data["Then"] is None:
                missing_list[2] = 1
                missing_list[3] = 1

                if not "with_name" in yaml_data["When"]:
                    missing_list[0] = 1
                if not "in_directory" in yaml_data["When"]:
                    missing_list[1] = 1

            if yaml_data["When"] is None and yaml_data["Then"] is not None:
                missing_list[0] = 1
                missing_list[1] = 1

                if not "file_count" in yaml_data["Then"]:
                    missing_list[2] = 1
                if not "in_directory" in yaml_data["Then"]:
                    missing_list[3] = 1

            return False, missing_list

        elif (yaml_data["When"] is not None and len(yaml_data["When"]) < 2) or (
            yaml_data["Then"] is not None and len(yaml_data["Then"]) < 3
        ):
            if not "with_name" in yaml_data["When"]:
                missing_list[0] = 1
            if not "in_directory" in yaml_data["When"]:
                missing_list[1] = 1
            if not "file_count" in yaml_data["Then"]:
                missing_list[2] = 1
            if not "in_directory" in yaml_data["Then"]:
                missing_list[3] = 1

            return False, missing_list

        else:
            return True, missing_list
