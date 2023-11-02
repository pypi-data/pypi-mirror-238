class Unit(object):
    UNIT = 0
    SHEEP = 1

    def __init__(self, data):
        self.id = data["base_id"]
        self.name = data["name"]
        self.gear_level = data["gear_level"]
        self.galactic_power = data["power"]
        self.stars = data["rarity"]
        self.relic = data["relic_tier"] - 2
        self.kind = Unit.UNIT if data["combat_type"] == 1 else Unit.SHEEP
        self.omicrons = 0
        self.max_omicrons = 0
        for ability in data["ability_data"]:
            if ability["is_omicron"]:
                self.max_omicrons += 1
            if ability["has_omicron_learned"]:
                self.omicrons += 1

    def check_requirement(self, req):
        for key in req.require:
            if hasattr(self, key):
                val = self.__getattribute__(key)
                if val < req.require[key]:
                    return False
        return True
