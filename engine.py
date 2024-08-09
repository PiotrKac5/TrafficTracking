import os

from vidgetter import get_videos, connect_vid, get_starting_point
import time

def getting_live_videos() -> None:
    last_download_time = time.time()
    start_id = get_starting_point()
    # print(start_id)
    ID = 0
    while True:
        if os.path.exists(f"videos_to_detect/video{ID}.mp4"):
            os.remove(f"videos_to_detect/video{ID}.mp4")

        last_download_time = time.time()
        get_videos(start_id=start_id)
        connect_vid(start_id=start_id, ID=ID) #this has to be on another thread working in parallel to ensure continuous video

        curr_time = time.time()
        while curr_time < last_download_time + 50 * 2.2:
            time.sleep(last_download_time-curr_time)
            curr_time = time.time()

        start_id += 50
        if start_id >= 100:
            start_id -= 100

        ID += 1
        if ID == 10:
            ID = 0
            break # uncomment only when you do not want program to run endlessly



getting_live_videos()