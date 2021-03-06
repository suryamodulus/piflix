from flask import Flask, request, render_template, jsonify, json, g
from flask_socketio import SocketIO, send, emit
from os import makedirs, path
import glob
import base64
import pathlib
from werkzeug.utils import secure_filename
from utils import check_media_folder_path, check_allowed_extensions
from xplayer import init_player

app = Flask(__name__)
app.config.from_pyfile('config.py')

# Initialize Socket.io
socketio = SocketIO(app)
socketio_clients = 0

# Validate media folder path
check_media_folder_path(app.config['MEDIA_FOLDER_PATH'])

# Initalize player plugin
player = init_player(app.config['PLAYER_PLUGIN'])


def vlc_events_consumer(event):
    global socketio_clients
    if(socketio_clients > 0):
        data = player.get_stats()
        data = json.dumps(data)
        socketio.emit('player_stats',data, json=True)

@socketio.on("connect")
def socket_connect():
    global socketio_clients
    if(socketio_clients < 1):
        player.subscribe_to_vlc_events(vlc_events_consumer)
    socketio_clients += 1

@socketio.on("disconnect")
def socket_disconnect():
    global socketio_clients
    socketio_clients -= 1

@app.route('/', methods=['GET'])
def index():
    media_files = [{"name": path.basename(x), "base64url_encoded_name": base64.urlsafe_b64encode(path.basename(x).encode('utf-8')).decode('utf-8')} for x in glob.glob(f"{app.config['MEDIA_FOLDER_PATH']}/*.mp4")]
    return render_template('index.html', media_files = media_files, allowed_media_extensions = app.config['ALLOWED_MEDIA_EXTENSIONS'])

@app.route('/add-media/upload', methods=['POST'])
def upload_media_file():
    if len(request.files) == 0:
        return jsonify(
            error="No files in request"
        ), 400
    success_uploads = []
    failed_uploads = []
    for i in request.files:
        file = request.files[i]
        try:
            # Validate file extension
            check_allowed_extensions(file.filename, app.config['ALLOWED_MEDIA_EXTENSIONS'])
            filename = secure_filename(file.filename)
            file.save(path.join(app.config['MEDIA_FOLDER_PATH'], filename))
            success_uploads.append(file.filename)
        except:
            failed_uploads.append(file.filename)
            pass
    if(len(success_uploads) > 0):
        return jsonify(message="Uploads Result", success_uploads = success_uploads, failed_uploads = failed_uploads), 200
    else:
        return jsonify(message="Uploads Failed", success_uploads = success_uploads, failed_uploads = failed_uploads), 400


@app.route('/watch/<string:base64url_encoded_name>', methods=['GET'])
def watch_media(base64url_encoded_name):
    filename = base64.urlsafe_b64decode(base64url_encoded_name).decode("utf-8")
    player.set_media(path.join(app.config['MEDIA_FOLDER_PATH'], filename))
    stats = player.get_stats()
    return render_template('watch.html', filename = filename, stats = stats)

@app.route('/player/stats', methods=['GET'])
def player_stats():
    data = player.get_stats()
    return jsonify(data=data)

@app.route('/player/controller', methods=['POST'])
def player_action():
    data = request.json
    # print("Id of player : {}".format(str(id(player))))
    if(data['action'] == 'play'):
        player.play()
    elif(data['action'] == 'pause'):
        player.pause()
    elif(data['action'] == 'stop'):
        player.stop()
    data = player.get_stats()
    return jsonify(data=data)

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5050)