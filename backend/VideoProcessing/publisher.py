import base64
import multiprocessing
import cv2
import redis

r = redis.Redis(host='redis', port=6379, db=0)
# r = redis.Redis(host='localhost', port=6379, db=0)

def publish_to_redis(q: multiprocessing.Queue):
    while True:
        while not q.empty():
            img = q.get()
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 60] # to reduce CPU-usage
            ret, buffer = cv2.imencode('.jpg', img, encode_param)
            frame = base64.b64encode(buffer).decode('utf-8')
            r.publish('video', frame)
            print("Published frame")