import eventlet
eventlet.monkey_patch()
import io
import threading
from queue import Queue
from VideoProcessing.plots import generate_plots
import cv2
import redis
from flask import Flask, render_template, send_file, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import ctypes
import time
import platform
from matplotlib import pyplot as plt


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
r = redis.Redis(host='redis', port=6379, db=0)
# r = redis.Redis(host='localhost', port=6379, db=0)
CORS(app, resources={r"/*": {"origins": "*"}})


q = Queue() # queue for frames


def redis_listener():
    pubsub = r.pubsub()
    pubsub.subscribe('video')

    for message in pubsub.listen():
        if message and message['type'] == 'message': # Check if it is an actual message
            frame = message['data'].decode('utf-8')
            q.put(frame)


def generate_frames():
    while True:
        while q.empty():
            time.sleep(0.05)
        frame = q.get()
        yield frame


@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('request_frame')
def handle_frame_request():
    for frame in generate_frames():
        socketio.emit('new_frame', frame)
        socketio.sleep(0)

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@app.route('/plots/<duration>', methods=['GET'])
def plot(duration):
    print(f"Received duration: {duration}")
    # Generate a plot
    fig, ax = generate_plots(duration=duration)
    ax.set_title('Tracking stats', fontsize=20, fontweight='bold', color='#D9D9D9')
    # Save plot to a bytes buffer
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)  # Close the figure to free memory

    # Send the image to the client
    return send_file(buf, mimetype='image/png')


if __name__ == '__main__':
    thread = threading.Thread(target=redis_listener)
    thread.daemon = True
    thread.start()

    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
    # socketio.run(app, host='localhost', port=5000, debug=True)
