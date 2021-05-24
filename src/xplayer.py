from player_plugins.vlc_player import VlcPlayer
from player_plugins.omx_player import OmxPlayer


def init_player(player_plugin):
    if(player_plugin == 'vlc'):
            return VlcPlayer.Instance()
    elif (player_plugin == 'omx'):
        return OmxPlayer.Instance()
    else:
        raise Exception('Player Plugin Not Found')


