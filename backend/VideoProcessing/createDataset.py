import multiprocessing
import os
import time
from multiprocessing import Pool, Manager
from vidgetter import getting_live_videos, get_starting_point
from ultralytics import YOLO
import cv2
import random


def create(q:multiprocessing.Queue):

    model = YOLO("Yolo-Weights/yolov10x.pt") # creating dataset based on prediction of biggest and most accurate model

    while q.empty():
        time.sleep(1)
    ID = q.get()
    img_id = 0

    while True:
        path = f"curr_vid/v{ID}.ts"
        print(ID, "---------------------------------------------------------------------------------------------------")
        while not os.path.exists(path):
            time.sleep(1)

        cap = cv2.VideoCapture(path)

        while img_id < 200000:
            success, img = cap.read()
            if not success:
                break

            rand_val = random.random()
            if rand_val < 0.75:
                which_set = "train"
            elif rand_val > 0.85:
                which_set = "test"
            else:
                which_set = "valid"


            results = model(img, stream=True)

if __name__ == "__main__":
    with Pool() as pool:
        q = Manager().Queue()
        res1 = pool.apply_async(getting_live_videos, args=(q,))
        res2 = pool.apply_async(create, args=(q,))
        res1.get()
        res2.get()

        pool.close()