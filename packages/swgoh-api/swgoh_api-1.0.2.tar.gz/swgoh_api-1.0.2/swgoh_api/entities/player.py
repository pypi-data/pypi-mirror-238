import os
import ujson as json
from .unit import Unit



class Player(object):
    def __init__(self, data):
        self.id = data["data"]["ally_code"]
        self.name = data["data"]["name"]
        self.units = self.__create_units(data["units"])
        self.__data = data

    @staticmethod
    def __create_units(data):
        return [Unit(u["data"]) for u in data]

    def get_unit(self, unit_id):
        for u in self.units:
            if unit_id == u.id:
                return u
        return None

    def get_unit_with_cond(self, unit_name, require):
        for u in self.units:
            if unit_name == u.name:
                return u if u.check_requirement(require) else None
        return None

    def save(self, path="."):
        os.makedirs(path, exist_ok=True)
        with open(f"{path}/{self.name}.json", "w") as f:
            json.dump(self.__data, f, indent=2)
