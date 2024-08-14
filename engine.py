import os
from tracker import track
from vidgetter import get_videos, connect_vid, get_starting_point
import time
from multiprocessing import Pool

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
        connect_vid(start_id=start_id, ID=ID) # this can be working on another thread in parallel to ensure continuous video

        f = open(f"videos_to_detect/ready{ID}.txt", "a")
        f.write(f"File {ID} ready for processing\n")
        f.close()
        # track(f"videos_to_detect/video{ID}.mp4")

        curr_time = time.time()
        if curr_time < last_download_time + 50 * 2.2:
            time.sleep(last_download_time + 50 * 2.2 - curr_time)

        start_id += 50
        if start_id >= 100:
            start_id -= 100

        ID += 1
        if ID == 10:
            ID = 0
            break # uncomment only when you do not want program to run endlessly



def run():

    with Pool() as pool:
        res1 = pool.apply_async(getting_live_videos)
        res2 = pool.apply_async(track)
        res1.get()
        res2.get()

        pool.close()



run()

# getting_live_videos()