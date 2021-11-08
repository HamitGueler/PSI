from AdvisorSystem import AdvisorSystem
from YamlReader import YamlReader
import sys

if __name__ == "__main__":

    if len(sys.argv) == 2:
        yaml_reader = YamlReader(sys.argv[1])
        yaml_data = yaml_reader.read_yaml()
        if yaml_data:
            yaml_bool, missing_list = yaml_reader.validate_yaml(yaml_data)

            if yaml_bool:
                test_system = AdvisorSystem(yaml_data)
                result = test_system.test_file_created()
                print("Result: " + str(result))
            elif not yaml_bool:
                missing_err = (
                    "ERROR: Following Settings are missing in the Yaml-File:\n"
                )

                if missing_list[0] == 1:
                    missing_err += "[When][with_name]\n"
                if missing_list[1] == 1:
                    missing_err += "[When][in_directory]\n"
                if missing_list[2] == 1:
                    missing_err += "[Then][file_count]\n"
                if missing_list[3] == 1:
                    missing_err += "[Then][in_directory]\n"

                print(missing_err)
        elif not yaml_data:
            print("Error: Could not get the Data from Yaml-File")
    elif len(sys.argv) != 2:
        print("ERROR: Example:\npython.py ./Main.py <Path/Yaml-File>")
