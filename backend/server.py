import multiprocessing
import time
import cv2
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import base64

q = multiprocessing.Queue()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

def generate_frames():
    while True:
        while q.empty():
            time.sleep(1)
        frame = q.get()
        # Encode the frame in JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = base64.b64encode(buffer).decode('utf-8')
        yield frame

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('request_frame')
def handle_frame_request():
    for frame in generate_frames():
        socketio.emit('new_frame', frame)
        socketio.sleep(0)  # Adjust sleep to control the frame rate
        # cv2.waitKey(20)
@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

def run_server(q1: multiprocessing.Queue):
    q = q1
    print("niby kurwa działa")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)