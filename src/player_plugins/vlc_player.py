from decorators.singleton import Singleton
import vlc

@Singleton
class VlcPlayer:
    def __init__(self):
        self.player = vlc.MediaPlayer()
        self.filepath = ''
    
    def set_media(self, filepath):
        if(self.player.is_playing()):
            if(self.filepath and self.filepath == filepath):
                return
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

    def play(self):
            self.player.play()
    
    def pause(self):
        if(self.player.can_pause):
            self.player.pause()

    def stop(self):
            self.player.stop()