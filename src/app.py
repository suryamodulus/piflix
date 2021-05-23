from flask import Flask, request, render_template, jsonify
from os import makedirs, path
import glob
import base64
import pathlib
from werkzeug.utils import secure_filename
from xplayer import XPlayer
import vlc

app = Flask(__name__)
app.config.from_pyfile('config.py')

player = XPlayer.get_player(app.config['PLAYER_PLUGIN'])

# Try creating media folder if it doesn't exist
try:
    makedirs(app.config['MEDIA_FOLDER'])
except OSError:
    pass

def allowed_file(filename):
    file_extension = pathlib.Path(filename).suffix
    return file_ext and file_ext in app.config['ALLOWED_MEDIA_EXTENSIONS']
    

@app.route('/', methods=['GET'])
def index():
    media_files = [{"name": path.basename(x), "base64url_encoded_name": base64.urlsafe_b64encode(path.basename(x).encode('utf-8')).decode('utf-8')} for x in glob.glob(f"{app.config['MEDIA_FOLDER']}/*.mp4")]
    return render_template('index.html', media_files = media_files, allowed_media_extensions = app.config['ALLOWED_MEDIA_EXTENSIONS'])

@app.route('/add-media/upload', methods=['POST'])
def upload_media_file():
    if request.method == 'POST':
        if len(request.files) == 0:
          return jsonify(
              error="No files in request"
            ), 400
        for i in request.files:
            file = request.files[i]
            try:
                if allowed_file(file.filename):
                    print(file.filename)
                    filename = secure_filename(file.filename)
                    print(filename)
                    file.save(path.join(app.config['MEDIA_FOLDER'], filename))
                    return jsonify(
                        message="ok"
                    ), 201
            except:
                pass
        return jsonify(
              error="Upload Failed"
            ), 400

@app.route('/watch/<string:base64url_encoded_name>', methods=['GET'])
def watch_media(base64url_encoded_name):
    filename = base64.urlsafe_b64decode(base64url_encoded_name).decode("utf-8")
    player.add_file(path.join(app.config['MEDIA_FOLDER'], filename))
    return render_template('watch.html', filename = filename)

@app.route('/player/<string:action>', methods=['POST'])
def player_action(action):
    if(action == 'play'):
        player.play()
    elif(action == 'pause'):
        player.pause()
    elif(action == 'stop'):
        player.stop()
    return "Ok"

if __name__ == "__main__":
    app.run()