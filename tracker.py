from ultralytics import YOLO
import numpy as np
import cv2
import cvzone
from sort import *


def cross_product(v1, v2):
    return v1[0] * v2[1] - v1[1] * v2[0]


def check_crossing(limits, cx: int, cy: int):
    rec_size = 30
    # I assume that in limits always x1 < x2
    for limit in limits:
        x1, y1, x2, y2 = limit
        vec1, vec2, vec3, vec4 = (0, 0), (0, 0), (0, 0), (0, 0)
        vc1p, vc2p, vc3p, vc4p = (0, 0), (0, 0), (0, 0), (0, 0)
        if y1 > y2:
            vec1 = (x2 - rec_size) - (x1 - rec_size), (y2 - rec_size) - (y1 - rec_size)
            vc1p = (cx) - (x1 - rec_size), (cy) - (y1 - rec_size)
            vec2 = (x2 + rec_size) - (x2 - rec_size), (y2 + rec_size) - (y2 - rec_size)
            vc2p = (cx) - (x2 - rec_size), (cy) + (y2 - rec_size)
            vec3 = (x1 + rec_size) - (x2 + rec_size), (y1 + rec_size) - (y2 + rec_size)
            vc3p = (cx) - (x2 + rec_size), (cy) - (y2 + rec_size)
            vec4 = (x1 - rec_size) - (x1 + rec_size), (y1 - rec_size) - (y1 + rec_size)
            vc4p = (cx) - (x1 + rec_size), (cy) - (y1 + rec_size)
        else:
            vec1 = (x2 + rec_size) - (x1 + rec_size), (y2 - rec_size) - (y1 - rec_size)
            vc1p = (cx) - (x1 + rec_size), (cy) - (y1 - rec_size)
            vec2 = (x2 - rec_size) - (x2 + rec_size), (y2 + rec_size) - (y2 - rec_size)
            vc2p = (cx) - (x2 + rec_size), (cy) - (y2 - rec_size)
            vec3 = (x1 - rec_size) - (x2 - rec_size), (y1 + rec_size) - (y2 + rec_size)
            vc3p = (cx) - (x2 - rec_size), (cy) - (y2 + rec_size)
            vec4 = (x1 + rec_size) - (x1 - rec_size), (y1 + rec_size) - (y2 + rec_size)
            vc4p = (cx) - (x1 - rec_size), (cy) - (y2 + rec_size)

        if (cross_product(vec1, vc1p) > 0 and cross_product(vec2, vc2p) > 0 and cross_product(vec3, vc3p) > 0 and cross_product(vec4, vc4p) > 0 or
                cross_product(vec1, vc1p) < 0 and cross_product(vec2, vc2p) < 0 and cross_product(vec3, vc3p) < 0 and cross_product(vec4, vc4p) < 0):
            return True, limit

    return False, None


def track(path: str="videos_to_detect/video0.mp4"):
    model = YOLO("Yolo-Weights/yolov10x.pt")  # you can change version of YOLO model here (for example to v10n -> nano)

    ID = int(path[-5])

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

    tracker = Sort(max_age=500, min_hits=5,
                   iou_threshold=0.3)  # max_age is so large, because in case of traffic cars will be moving slowly

    totalCount = set()

    car_mask = cv2.imread("masks/car_mask.png")

    limits = [[20, 393, 126, 450], [341, 345, 501, 272], [410, 476, 666, 592], [693, 230, 871, 291],
              [1027, 450, 1092, 358], [1092, 317, 1141, 274], [1150, 608, 1208, 703]]

    while True:
        curr_path = path[:-5] + str(ID) + path[-4:]

        while not os.path.exists(f"videos_to_detect/ready{ID}.txt"):
            time.sleep(2)
            # print("File not detected")

        os.remove(f"videos_to_detect/ready{ID}.txt")

        cap = cv2.VideoCapture(curr_path)

        while True:
            succes, img = cap.read()
            if not succes:
                cv2.destroyAllWindows()
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
                            and conf > 0.3):
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cvzone.putTextRect(img=img, text=f"{currClass} {conf}", pos=(max(0, x1), max(35, y1 - 20)),
                                           scale=0.7, thickness=1, offset=3)

                        currArray = np.array([x1, y1, x2, y2, conf])
                        detections = np.vstack((detections, currArray))

            resultsTracker = tracker.update(dets=detections)
            for limit in limits:
                cv2.line(img, (limit[0], limit[1]), (limit[2], limit[3]), (0, 0, 255), 5)

            for res in resultsTracker:
                x1, y1, x2, y2, obj_ID = res
                w, h = x2 - x1, y2 - y1
                cx, cy = int(x1 + w // 2), int(y1 + h // 2)
                cv2.circle(img, (cx, cy), 10, (0, 255, 255), cv2.FILLED)

                crossed, limit = check_crossing(limits=limits, cx=cx, cy=cy)
                if crossed:
                    dl = len(totalCount)
                    totalCount.add(obj_ID)
                    if dl < len(totalCount):
                        cv2.line(img, (limit[0], limit[1]), (limit[2], limit[3]), (0, 255, 0), 5)


            cv2.putText(img=img, text=str(len(totalCount)), org=(255, 100), color=(50, 50, 255), fontScale=5,
                        fontFace=cv2.FONT_HERSHEY_PLAIN, thickness=8)
            cv2.imshow('Tracking', img)
            cv2.waitKey(20)

        print(f"Cars counted: {len(totalCount)}")
        # break
        ID += 1
        if ID == 10:
            ID = 0

# track("videos_to_detect/video0.mp4")
# print(is_file_in_use("videos_to_detect/video0.mp4"))