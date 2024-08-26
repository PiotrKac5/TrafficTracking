import multiprocessing

from saver import save_counter
from tracker import track
from vidgetter import getting_live_videos
from multiprocessing import Pool, Manager
# from server import run_server


def run(p:multiprocessing.Queue):

    with Pool() as pool:
        # run_server()
        q = Manager().Queue()
        # res1 = pool.apply_async(getting_live_videos)
        res2 = pool.apply_async(track, args=(q,p,))
        res3 = pool.apply_async(save_counter, args=(q,))
        # res1.get()
        res2.get()
        res3.get()

        pool.close()


if __name__ == "__main__":
    run()