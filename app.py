from flask import Flask
from flask_restful import Api
from flask_pagedown import PageDown
from flask_socketio import SocketIO
import os

api = Api()
pagedown = PageDown()
socketio = SocketIO()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# Extensions
api.init_app(app)
pagedown.init_app(app)
socketio = SocketIO(app)  # Initialize Flask-SocketIO

from core import core
app.register_blueprint(core)

notes = {}
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('update_note')
def handle_update(data):
    note_id = data['id']
    content = data['content']
    notes[note_id] = content
    socketio.emit('note_updated', {'id': note_id, 'content': content})

if __name__ == '__main__':
    socketio.run(app, debug=True)
