class URLRequest(object):
    def __init__(self, url="http://api.swgoh.gg/"):
        self.url = url

    def handle_data(self, data, handler):
        return data.content

    def error(self):
        # raise Exception("Can't make request")
        pass


class GuildURLRequest(URLRequest):
    def __init__(self, guild_id):
        super().__init__()
        self.url += f"guild-profile/{guild_id}"

    def handle_data(self, data, handler):
        return data.json()["data"]


class PlayerURLRequest(URLRequest):
    def __init__(self, allycode):
        super().__init__()
        self.url += f"player/{allycode}"

    def handle_data(self, data, handler):
        return data.json()


class UnitURLRequest(URLRequest):
    def __init__(self, allycode, unitname):
        super().__init__()
        self.url += f"player/{allycode}"
        self.name = unitname

    def handle_data(self, data, handler):
        for u in data.json()["units"]:
            cur = u["data"]
            if cur["base_id"] == self.name:
                return cur
        return None


class ImageURLRequest(URLRequest):
    def __init__(self, unitname):
        super().__init__()
        self.url += "units"
        self.name = unitname

    def handle_data(self, data, handler):
        for u in data.json()["data"]:
            if u["base_id"] == self.name:
                new_req = URLRequest(u["image"])
                return handler._make_stream_request(new_req)
        return None
