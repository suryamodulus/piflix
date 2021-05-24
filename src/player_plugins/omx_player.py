from decorators.singleton import Singleton
import vlc

@Singleton
class OmxPlayer:
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

    def play(self):
            self.player.play()
    
    def pause(self):
        if(self.player.can_pause):
            self.player.pause()

    def stop(self):
        self.player.stop()