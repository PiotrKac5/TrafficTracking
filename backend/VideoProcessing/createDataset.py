import multiprocessing
import os
import time
from multiprocessing import Pool, Manager
from vidgetter import getting_live_videos
from ultralytics import YOLO
import cv2
import random


def create(q:multiprocessing.Queue):

    model = YOLO("Yolo-Weights/yolov10x.pt") # creating dataset based on prediction of biggest and most accurate model

    classNames = model.names

    while q.empty():
        time.sleep(1)
    ID = q.get()
    img_id = 0

    while img_id < 5000:
        path = f"curr_vid/v{ID}.ts"
        print(ID, "---------------------------------------------------------------------------------------------------")
        while not os.path.exists(path):
            time.sleep(1)

        car_mask = cv2.imread("masks/car_mask.png")
        cap = cv2.VideoCapture(path)

        frame_nr = random.randint(0, int(2.2*25))
        success, img = cap.read()
        counter = 0
        while counter < frame_nr:
            success, wimg = cap.read()
            if not success:
                break
            img = wimg
            counter += 1

        height, width, channels = img.shape

        rand_val = random.random()
        if rand_val < 0.75:
            which_set = "train"
        elif rand_val > 0.85:
            which_set = "test"
        else:
            which_set = "valid"

        img_path = f"CustomDataset/{which_set}/images/img{img_id}.jpg"
        img = cv2.bitwise_and(img, car_mask)
        write_img = cv2.imwrite(img_path, img)

        results = model(img, stream=True)
        with open(f"CustomDataset/{which_set}/labels/img{img_id}.txt", mode="w") as f:
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    # Bounding Box
                    x1, y1, x2, y2 = box.xyxy[0]
                    w, h = x2 - x1, y2 - y1
                    cx, cy = int(x1 + w // 2), int(y1 + h // 2)
                    # Confidence
                    conf = round(float(box.conf[0]), 2)
                    # Class name
                    cls = box.cls[0]
                    currClass = classNames[int(cls)]
                    objects = ["car", "truck", "motorbike", "bus"]
                    if currClass in objects and conf > 0.3:
                        idx = objects.index(currClass)
                        f.write(f"{idx} {cx/width} {cy/height} {w/width} {h/height}\n")

        print(f"Img and label {img_id} created")
        img_id += 1

        time.sleep(30) # to make each frame different from another

        ID += 12 # to make each frame different from another
        ID %= 100



if __name__ == "__main__":
    with Pool() as pool:
        q = Manager().Queue()
        res1 = pool.apply_async(getting_live_videos, args=(q,))
        res2 = pool.apply_async(create, args=(q,))
        res1.get()
        res2.get()

        pool.close()
