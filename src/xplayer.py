from player_plugins.vlc import VlcPlayer
from player_plugins.omxplayer import OmxPlayer

class XPlayer:
    @staticmethod
    def get_player(player_plugin):
        if(player_plugin == 'vlc'):
            return VlcPlayer()
        elif (player_plugin == 'omxplayer'):
            return OmxPlayer()
        else:
            raise Exception('Player Plugin Not Found')


