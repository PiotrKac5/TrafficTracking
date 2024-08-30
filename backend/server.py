import base64
import threading
from queue import Queue

import cv2
import numpy as np
import redis
import wres
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import ctypes
import time

# Load the necessary Windows library
winmm = ctypes.WinDLL('winmm')

# Define the timeBeginPeriod function
timeBeginPeriod = winmm.timeBeginPeriod
timeBeginPeriod.argtypes = [ctypes.c_uint]
timeBeginPeriod.restype = ctypes.c_uint

# Define the timeEndPeriod function
timeEndPeriod = winmm.timeEndPeriod
timeEndPeriod.argtypes = [ctypes.c_uint]
timeEndPeriod.restype = ctypes.c_uint


def set_timer_resolution(period_ms):
    """
    Set the system timer resolution.
    :param period_ms: Timer period in milliseconds.
    """
    if period_ms < 1:
        raise ValueError("Period must be at least 1 millisecond")

    timeBeginPeriod(period_ms)


def restore_timer_resolution():
    """
    Restore the default system timer resolution.
    """
    # Typically, 15 ms is the default period on many systems.
    timeEndPeriod(15)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
r = redis.Redis(host='localhost', port=6379, db=0)

q = Queue() # queue for frames


# @lru_cache(maxsize=None)
def redis_listener():
    pubsub = r.pubsub()
    pubsub.subscribe('video')

    for message in pubsub.listen():
        if message and message['type'] == 'message': # Check if it is an actual message
            frame =  message['data'].decode('utf-8')
            q.put(frame)


def generate_frames():
    while True:
        while q.empty():
            time.sleep(0.05)
        frame = q.get()
        # image_data = base64.b64decode(frame)
        #
        # # 2. Convert the bytes to a numpy array
        # nparr = np.frombuffer(image_data, np.uint8)
        # print("testing===============================================================================================")
        # # 3. Decode the image array back into an OpenCV image (BGR format)
        # img_decoded = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        # cv2.imshow('Test', img_decoded)
        # cv2.waitKey(1)
        yield frame


@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('request_frame')
def handle_frame_request():
    # c_time = 0
    # det_time = 0
    start_time = round(time.time() * 1000.0)
    frame_counter = 0
    for frame in generate_frames():
        # with wres.set_resolution(10000):  # ensures precision of 1ms on Windows system
        #     c_time = round(time.time() * 1000.0)
        # socketio.emit('new_frame', frame)
        # socketio.sleep(0)
        # with wres.set_resolution(10000):  # ensures precision of 1ms on Windows system
        #     det_time = round(time.time() * 1000.0)
        #     print(det_time-c_time, "weird ==========================================================================")
        if frame_counter == 0:
            start_time = round(time.time() * 1000.0)
        frame_counter += 1
        socketio.emit('new_frame', frame)
        with wres.set_resolution(10000):  # ensures precision of 1ms on Windows system
            c_time = round(time.time() * 1000.0)
        if c_time-start_time > frame_counter * 40:
            socketio.sleep(0)
        else:
            wait_time = frame_counter * 40 - (c_time-start_time)
            socketio.sleep(wait_time/1000.0)

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')




if __name__ == '__main__':
    set_timer_resolution(1)
    try:
        thread = threading.Thread(target=redis_listener)
        thread.daemon = True
        thread.start()

        socketio.run(app, host='0.0.0.0', port=5000, debug=True)
    finally:
        restore_timer_resolution()