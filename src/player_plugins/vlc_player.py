from decorators.singleton import Singleton
import vlc

@Singleton
class VlcPlayer:
    def __init__(self):
        self.player = vlc.MediaPlayer()
        self.filepath = None
    
    def set_media(self, filepath):
        if(self.filepath == None or self.filepath != filepath):
            media = vlc.Media(filepath)
            self.player.set_media(media)
            self.filepath = filepath
    
    def get_stats(self):
        data = {}
        data['is_playing'] = not not self.player.is_playing()
        data['is_mute'] = not not self.player.audio_get_mute()
        data['total_time'] = max(0, self.player.get_length())
        data['current_time'] = max(0, self.player.get_time())
        return data

    def subscribe_to_vlc_events(self, callback_fn):
        mp_em = self.player.event_manager()
        mp_em.event_attach(vlc.EventType.MediaPlayerPaused, callback_fn)
        mp_em.event_attach(vlc.EventType.MediaPlayerPlaying, callback_fn)
        mp_em.event_attach(vlc.EventType.MediaPlayerMuted, callback_fn)
        mp_em.event_attach(vlc.EventType.MediaPlayerUnmuted, callback_fn)
        mp_em.event_attach(vlc.EventType.MediaPlayerLengthChanged, callback_fn)
        mp_em.event_attach(vlc.EventType.MediaPlayerTimeChanged, callback_fn)

    def play(self):
            self.player.play()
    
    def pause(self):
        if(self.player.can_pause):
            self.player.pause()

    def stop(self):
            self.player.stop()