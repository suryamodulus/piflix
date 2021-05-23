from player_plugins.vlc import VlcPlayer
from player_plugins.omxplayer import OmxPlayer
from decorators.singleton import Singleton


@Singleton
class XPlayer(object):
    @staticmethod
    def get_player(player_plugin):
        if(player_plugin == 'vlc'):
            return VlcPlayer()
        elif (player_plugin == 'omxplayer'):
            return OmxPlayer()
        else:
            raise Exception('Player Plugin Not Found')


