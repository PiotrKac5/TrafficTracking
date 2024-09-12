import multiprocessing
import os
import time

from vidgetter import get_starting_point
import wres
from ultralytics import YOLO
import cv2
import cvzone
from sort import *
from publisher import publish_to_redis

def cross_product(v1, v2) -> int:
    """
    Returns cross product of two vectors (v1 and v2)
    """

    return v1[0] * v2[1] - v1[1] * v2[0]


def check_crossing(limits, cx: int, cy: int) -> (bool, int):
    """
    Checks whether object is in area of any segment, which is counted as crossing one.
    :param limits: array of 4-element arrays, in which are segment coordinates
    :param cx: middle x-coordinate of an object
    :param cy: middle y-coordinate of an object
    :return: True, limit if object crossed segment number "limit"; False if object did not cross any segments
    """

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


def track(q: multiprocessing.Queue, p:multiprocessing.Queue, k:multiprocessing.Queue, path: str="curr_vid/v0.mp4") -> None:
    """
    Reads mp4 files, detects objects in each frame in certain regions (not covered by mask) and shows result of it.
    It also counts all objects that are crossing segments defined in "limits" and shows it on screen.
    Number of vehicles is automatically zeroed after every 15 minutes (when minutes % 15 == 0) by other process.
    """

    # model = YOLO("Yolo-Weights/yolov10n.pt")  # you can change version of YOLO model here (for example to v10n -> nano)
    model = YOLO("runs/detect/yolov10n-customdataset/weights/best.pt") # model trained on custom dataset

    ID = 0
    while k.empty():
        time.sleep(1)
    ID = k.get()
    # k.close()

    classNames = model.names

    tracker = Sort(max_age=1000, min_hits=3,
                   iou_threshold=0.3)  # max_age is so large, because in case of traffic cars will be moving slowly

    car_mask = cv2.imread("masks/car_mask.png")

    limits = [[20, 393, 126, 450], [341, 345, 501, 272], [410, 476, 666, 592], [693, 230, 871, 291],
              [1027, 450, 1141, 298], [1150, 608, 1208, 703]]

    totalCount = set()
    q.put(totalCount)

    while True:
        curr_path = path[:10] + str(ID) + path[-4:]
        check_path = path[:10] + str(ID) + ".txt"

        while not os.path.exists(check_path):
            time.sleep(0.001)

        cap = cv2.VideoCapture(curr_path)

        path_to_remove = path[:10] + str((ID-1)%100) + path[-4:]
        cpath_to_remove = path[:10] + str((ID-1)%100) + ".txt"
        if os.path.exists(path_to_remove):
            os.remove(path_to_remove)
        if os.path.exists(cpath_to_remove):
            os.remove(cpath_to_remove)

        while True:
            with wres.set_resolution(10000): # ensures precision of 1ms on Windows system
                det_time = round(time.time() * 1000.0)
            success, img = cap.read()
            if not success:
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
                    if (currClass == "car" or currClass == "truck" or currClass == "motorbike" or currClass == "bus"
                            and conf > 0.3):
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cvzone.putTextRect(img=img, text=f"{currClass} {conf}", pos=(max(0, x1), max(35, y1 - 20)),
                                           scale=0.7, thickness=1, offset=3)

                        currArray = np.array([x1, y1, x2, y2, conf])
                        detections = np.vstack((detections, currArray))

            resultsTracker = tracker.update(dets=detections)
            for limit in limits:
                cv2.line(img, (limit[0], limit[1]), (limit[2], limit[3]), (0, 0, 255), 5)

            totalCount = q.get()

            for res in resultsTracker:
                x1, y1, x2, y2, obj_ID = res
                w, h = x2 - x1, y2 - y1
                cx, cy = int(x1 + w // 2), int(y1 + h // 2)
                cv2.circle(img, (cx, cy), 5, (0, 255, 255), cv2.FILLED)

                crossed, limit = check_crossing(limits=limits, cx=cx, cy=cy)
                if crossed:
                    dl = len(totalCount)
                    totalCount.add(obj_ID)
                    if dl < len(totalCount):
                        cv2.line(img, (limit[0], limit[1]), (limit[2], limit[3]), (0, 255, 0), 5)


            cv2.putText(img=img, text=str(len(totalCount)), org=(255, 100), color=(50, 50, 255), fontScale=5,
                        fontFace=cv2.FONT_HERSHEY_PLAIN, thickness=8)
            # cv2.imshow('Tracking', img) #shows frame

            p.put(img)

            q.put(totalCount)
            with wres.set_resolution(10000): # ensures precision of 1ms on Windows system
                c_time = round(time.time() * 1000.0)
                # cv2.waitKey(max(1, (40-(c_time-det_time))))

        print(f"Cars counted: {len(totalCount)}")

        ID += 1
        ID %= 100

if __name__ == "__main__": # added if you want to test only tracker and publisher without running whole app
    q = multiprocessing.Manager().Queue()
    p = multiprocessing.Manager().Queue()
    k = multiprocessing.Manager().Queue()
    with multiprocessing.Pool() as pool:
        print("Starting...")
        res2 = pool.apply_async(track, args=(q,p,k,))
        res1 = pool.apply_async(publish_to_redis, args=(p,))
        res2.get()
        res1.get()
        pool.close()