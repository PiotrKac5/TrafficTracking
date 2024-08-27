import threading
# from functools import lru_cache
# import asyncio
from queue import Queue
import redis
# import cv2
import wres
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
# import base64
import ctypes
import time

# # Load the necessary Windows library
# winmm = ctypes.WinDLL('winmm')
#
# # Define the timeBeginPeriod function
# timeBeginPeriod = winmm.timeBeginPeriod
# timeBeginPeriod.argtypes = [ctypes.c_uint]
# timeBeginPeriod.restype = ctypes.c_uint
#
# # Define the timeEndPeriod function
# timeEndPeriod = winmm.timeEndPeriod
# timeEndPeriod.argtypes = [ctypes.c_uint]
# timeEndPeriod.restype = ctypes.c_uint
#
#
# def set_timer_resolution(period_ms):
#     """
#     Set the system timer resolution.
#     :param period_ms: Timer period in milliseconds.
#     """
#     if period_ms < 1:
#         raise ValueError("Period must be at least 1 millisecond")
#
#     timeBeginPeriod(period_ms)
#
#
# def restore_timer_resolution():
#     """
#     Restore the default system timer resolution.
#     """
#     # Typically, 15 ms is the default period on many systems.
#     timeEndPeriod(15)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
r = redis.Redis(host='localhost', port=6379, db=0)

q = Queue() # queue for frames


# @lru_cache(maxsize=None)
def redis_listener():
    pubsub = r.pubsub()
    pubsub.subscribe('video')

    # waited = False
    # with wres.set_resolution(10000):  # ensures precision of 1ms on Windows system
    #     c_time = round(time.time() * 1000.0)
    #     det_time = c_time

    for message in pubsub.listen():
        if message and message['type'] == 'message': # Check if it is an actual message
            with wres.set_resolution(10000):  # ensures precision of 1ms on Windows system
                det_time = round(time.time() * 1000.0)
            frame =  message['data'].decode('utf-8')
            # frame = message['data']
            q.put(frame)
            with wres.set_resolution(10000):  # ensures precision of 1ms on Windows system
                c_time = round(time.time() * 1000.0)
            # print(det_time-c_time, " eh ==================================================================================")


def generate_frames():
    while True:
        frame = q.get()
        yield frame


@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('request_frame')
def handle_frame_request():
    c_time = 0
    det_time = 0
    for frame in generate_frames():
        with wres.set_resolution(10000):  # ensures precision of 1ms on Windows system
            c_time = round(time.time() * 1000.0)
        socketio.sleep((max(0, (30-(c_time-det_time))/1000.0)))
        with wres.set_resolution(10000):  # ensures precision of 1ms on Windows system
            det_time2 = round(time.time() * 1000.0)
        socketio.emit('new_frame', frame)
        with wres.set_resolution(10000):  # ensures precision of 1ms on Windows system
            c_time2 = round(time.time() * 1000.0)
        # print(det_time2-c_time2, " weird ============================================================================")
        with wres.set_resolution(10000):  # ensures precision of 1ms on Windows system
            det_time = round(time.time() * 1000.0)
            # socketio.sleep(0)
            # socketio.sleep(max(0,(30-(c_time-det_time))/1000.0) ) # Adjust sleep to control the frame rate
            # cv2.waitKey(max(1, 40-(c_time-det_time)))

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')




if __name__ == '__main__':
    # set_timer_resolution(1)
    try:
        thread = threading.Thread(target=redis_listener)
        thread.daemon = True
        thread.start()

        socketio.run(app, host='0.0.0.0', port=5000, debug=True)
    finally:
        restore_timer_resolution()