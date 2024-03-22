import json

class CreateJson:
    def __init__(self, dict, output_path):
        self.__json_string = json.dumps(dict)
        with open(output_path, 'w') as file_json:
            file_json.write(self.__json_string)