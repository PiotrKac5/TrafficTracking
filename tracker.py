from ultralytics import YOLO
import numpy as np
import cv2
import cvzone
from sort import *




def track(path:str):
    model = YOLO("Yolo-Weights/yolov10l.pt") # you can change version of YOLO model here (for example to v10n -> nano)
    cap = cv2.VideoCapture(path)

    classNames = [
        "person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
        "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
        "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
        "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
        "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
        "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
        "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
        "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
        "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
        "teddy bear", "hair drier", "toothbrush"
    ]

    tracker = Sort(max_age=500, min_hits=5, iou_threshold=0.3) # max_age is so large, because in case of traffic cars will be moving slowly

    totalCount = set()

    car_mask = cv2.imread("masks/car_mask.png")

    limits = [[20, 393, 126, 450], [341, 345, 501, 272], [410, 476, 666, 592], [693, 230, 905, 307],
              [1092, 358, 1027, 450], [1141, 274, 1092, 317], [1150, 608, 1208, 703]]

    while True:
        succes, img = cap.read()
        if not succes:
            break

        imgRegionCars = cv2.bitwise_and(img, car_mask)

        results = model(imgRegionCars, stream=True)

        detections = np.empty((0, 5))
        for r in results:
            boxes = r.boxes
            for box in boxes:
                # Bounding Box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                # Confidence
                conf = round(float(box.conf[0]), 2)
                # Class name
                cls = box.cls[0]
                currClass = classNames[int(cls)]

                if (currClass == "car" or currClass == "truck" or currClass == "motorbike" or currClass == "bus" or currClass == "train"
                        or currClass == "person" and conf > 0.3):
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cvzone.putTextRect(img=img, text=f"{currClass} {conf}", pos=(max(0, x1), max(35, y1-20)), scale=0.7, thickness=1, offset=3)

                    currArray = np.array([x1, y1, x2, y2, conf])
                    detections = np.vstack((detections, currArray))

        resultsTracker = tracker.update(dets=detections)
        for limit in limits:
            cv2.line(img, (limit[0], limit[1]), (limit[2], limit[3]), (0, 0, 255), 5)

        for res in resultsTracker:
            x1, y1, x2, y2, ID = res
            w, h = x2 - x1, y2 - y1
            cx, cy = int(x1 + w // 2), int(y1 + h // 2)
            cv2.circle(img, (cx, cy), 10, (0, 255, 255), cv2.FILLED)




        cv2.imshow('Tracking', img)
        cv2.waitKey(1)


track("videos_to_detect/video0.mp4")