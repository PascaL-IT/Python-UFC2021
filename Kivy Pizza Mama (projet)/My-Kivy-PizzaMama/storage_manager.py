#Storage Manager to load and save the data
import json


class StorageManager:

    FILENAME_JSON_EXT = ".json"

    """
        Check filename contains correct file extension
        See https://docs.python.org/3/library/exceptions.html
    """
    def check_filename(self, filename : str):
        if not filename.endswith(self.FILENAME_JSON_EXT):
            raise ValueError('Invalid file extension', 'Expecting ' + self.FILENAME_JSON_EXT)

    """ Get deserialise data from a JSON file """
    def get_data(self, filename):
        self.check_filename(filename)
        file = None
        try:
            file = open(filename, "r")
        except IOError as ioex:
            print(f"IOError: errno={ioex.errno} , message={ioex.strerror} , ioex={ ioex }")
            return ""
        else:
            data_json = file.read()
        finally:                       # https://www.python.org/dev/peps/pep-0341/
            if file:
                file.close()
        print("get_data: "+str(data_json))
        return json.loads(data_json)   # deserialise : json str -> python obj

    """ Save data into a JSON file """
    def store_data(self, filename, data):
        self.check_filename(filename)
        str_data = json.dumps(data)    # serialise : python obj -> json str
        with open(filename, "w") as file :
            file.write(str_data)
        file.close()
        print("store_data: " + str(str_data))

