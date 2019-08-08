import json


class Config:
    # config
    def __init__(self, file, defaultConfig={}):
        self.__file = file
        try:
            # read config
            with open(self.__file, "r") as f:
                self.__config = json.load(f)
        except (OSError, json.decoder.JSONDecodeError):
            print("No config present. Create new.")
            # TODO find gateway
            self.__config = defaultConfig

    def save(self):
        try:
            self.__config
            with open(self.__file, "w") as f:
                json.dump(self.__config, f)
        except NameError:
            print("Config not loaded, not saving")

    def get(self, key, defaultValue=None):
        if key in self.__config:
            return self.__config[key]
        else:
            self.set(key, defaultValue)  # set default
            return defaultValue

    def set(self, key, value):
        self.__config[key] = value
        self.save()
