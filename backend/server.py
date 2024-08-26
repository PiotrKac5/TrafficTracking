import threading
import time
from queue import Queue
import redis
import cv2
import wres
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import base64

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
r = redis.Redis(host='localhost', port=6379, db=0)

q = Queue() #queue for frames

def redis_listener():
    pubsub = r.pubsub()
    pubsub.subscribe('video')

    for message in pubsub.listen():
        if message and message['type'] == 'message': # Check if it is an actual message
            frame = message['data'].decode('utf-8')
            q.put(frame)
            # print("Frame GOT ==============================================================================")

def generate_frames():
    while True:
        # while q.empty():
        #     with wres.set_resolution(10000): # ensures precision of 1ms on Windows system
        #         time.sleep(0.001)
        frame = q.get()
        # Encode the frame in JPEG format
        # ret, buffer = cv2.imencode('.jpg', frame)
        # frame = base64.b64encode(buffer).decode('utf-8')
        yield frame


@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('request_frame')
def handle_frame_request():
    for frame in generate_frames():
        socketio.emit('new_frame', frame)
        with wres.set_resolution(1000000):  # ensures precision of 1ms on Windows system
        #     c_time = round(time.time() * 1000.0)
            socketio.sleep(0)  # Adjust sleep to control the frame rate
        # cv2.waitKey(20)

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')




if __name__ == '__main__':
    thread = threading.Thread(target=redis_listener)
    thread.daemon = True
    thread.start()

    socketio.run(app, host='0.0.0.0', port=5000, debug=True)