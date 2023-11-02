from .utils.singleton import singleton
from .utils.image import save_image
from .loaders.guild_loader import GuildLocalLoader, GuildRemoteLoader
from .loaders.player_loader import PlayerLocalLoader, PlayerRemoteLoader
from .loaders.unit_loader import UnitRemoteLoader
from .loaders.image_loader import ImageRemoteLoader


@singleton
class SwgohAPI(object):
    '''
    API for getting different usefull data from swgoh.gg
    '''
    def __init__(self):
        self.__local_guild_loader = GuildLocalLoader()
        self.__remote_guild_loader = GuildRemoteLoader()
        self.__local_player_loader = PlayerLocalLoader()
        self.__remote_player_loader = PlayerRemoteLoader()
        self.__unit_loader = UnitRemoteLoader()
        self.__image_loader = ImageRemoteLoader()

    def load_guild_from_cache(self, guild_name, path="."):
        '''Load data from local storage and create Guild object'''
        return self.__local_guild_loader.load(path, guild_name)

    def load_guild_from_url(self, guild_id):
        '''Get data from swgoh.gg and create Guild object'''
        return self.__remote_guild_loader.load(guild_id)

    def load_player_from_cache(self, player_name, path="."):
        '''Load data from local storage and create Player object'''
        return self.__local_player_loader.load(path, player_name)

    def load_player_from_url(self, ally_code):
        '''Get data from swgoh.gg and create Player object'''
        return self.__remote_player_loader.load(ally_code)

    def load_unit_from_url(self, ally_code, unit_name):
        '''Get data from swgoh.gg and create Unit object (of giving player)'''
        return self.__unit_loader.load(ally_code, unit_name)

    def save_unit_image(self, unit_name, path=".", filename=None):
        '''Download icon of unit from swgoh.gg and save it in local storage'''
        data = self.__image_loader.load(unit_name)
        if data:
            if not filename:
                filename = f"{unit_name}.png"
            save_image(data, path, filename)
        return data is not None
