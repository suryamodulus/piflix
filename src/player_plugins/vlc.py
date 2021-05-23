import vlc

class VlcPlayer:
    def __init__(self):
        self.player = ''
    
    def add_file(self, filepath):
        self.player = vlc.MediaPlayer(filepath)

    def play(self):
        if(self.player):
            self.player.play()
    
    def pause(self):
        if(self.player):
            self.player.pause()
    def stop(self):
        if(self.player):
            self.player.stop()