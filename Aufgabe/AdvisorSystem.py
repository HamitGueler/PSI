import os
import re
import time
from FileCreator import FileCreator

"""
This class should use the fetched yaml-data and FileCreator class to execute the test description of the advisor. 
"""


class AdvisorSystem:
    def __init__(self, yaml_data):
        self.__yaml_data = yaml_data

    def test_file_created(self):
        file_creator = FileCreator()
        if (
            self.__yaml_data["When"]["in_directory"] is not None
            and self.__yaml_data["When"]["with_name"] is not None
            and self.__yaml_data["Then"]["file_count"] is not None
            and self.__yaml_data["Then"]["after"] is not None
            and self.__yaml_data["Then"]["in_directory"] is not None
        ):

            count_valid = re.search(
                "^[0-9]*\Z", str(self.__yaml_data["Then"]["file_count"])
            )

            if count_valid:
                create_bool = file_creator.create_file(
                    self.__yaml_data["When"]["in_directory"],
                    self.__yaml_data["When"]["with_name"],
                )
                if create_bool:
                    if "after" in self.__yaml_data["Then"]:
                        duration = self.calculate_duration()
                        if duration != -1:
                            try:
                                time.sleep(duration)
                            except OverflowError as e:
                                print(e)
                                return False
                        elif duration == -1:
                            return False

                    file_count = 0
                    path = file_creator.create_valid_path(
                        self.__yaml_data["Then"]["in_directory"]
                    )
                    for _ in os.listdir(path):
                        file_count += 1

                    if file_count != self.__yaml_data["Then"]["file_count"]:
                        return False
                    elif file_count == self.__yaml_data["Then"]["file_count"]:
                        return True
                elif not create_bool:
                    return False
            elif not count_valid:
                print("Error: Use for [Then][file_count] a valid Input")
                return False

        elif (
            self.__yaml_data["When"]["in_directory"] is None
            or self.__yaml_data["When"]["with_name"] is None
            or self.__yaml_data["Then"]["file_count"] is None
            or self.__yaml_data["Then"]["after"] is None
            or self.__yaml_data["Then"]["in_directory"] is None
        ):
            print("Error: Missing Values in the Yaml-File")
            return False

    """Since the example uses "s" for seconds, I was wondering if the consultant could provide more time 
    specifictaions. I have realized a rough idea, how one could approach something like that. Here the consultant has 
    the freedom to choose between hours, minutes or seconds. For this, he must specify either a "h", "m" or "s" to 
    his number in the setting "after". If he only enters a number, it will automatically be considered as seconds. If 
    he specifies a float value, it will be transformed to an Int. This was a 
    spontaneous decision, depending on how the system would develop, other or more specific settings could be 
    adopted."""

    def calculate_duration(self):
        duration = self.__yaml_data["Then"]["after"]
        if isinstance(duration, int):
            return abs(duration)

        elif isinstance(duration, float):
            return int(round(abs(duration)))

        elif isinstance(duration, str):
            # remove Spaces from String
            duration = "".join(duration.split())
            # search for invalid Inputs
            # example: a200m, 2s34h, 2sh
            # ^\d[.]{0,1}\d*[hms]\Z -> this regex-expression could be used, if we would allow floats
            regex_result = re.search("^\d*[hms]\Z", duration)
            if regex_result:
                if duration.endswith("s"):
                    seconds = "".join(duration.split("s"))
                    return int(float(seconds))

                elif duration.endswith("m"):
                    minutes = "".join(duration.split("m"))
                    return int(float(minutes)) * 60

                elif duration.endswith("h"):
                    hours = "".join(duration.split("h"))
                    return (int(float(hours)) * 60) * 60
                else:  # this "else" isn't reachable actually because of the regex-expression at the beginning
                    print(
                        "ERROR: Invalid Time specification.\n Valid Time specifications would be: s:seconds, "
                        "m:minutes, h:hours"
                    )
                    return -1
            elif not regex_result:
                print(
                    "ERROR: Invalid Time specification.\n Valid Time specifications would be: s:seconds, m:minutes, "
                    "h:hours"
                )
                return -1
