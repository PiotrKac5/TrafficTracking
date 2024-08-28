from saver import save_counter
from tracker import track
from vidgetter import getting_live_videos
from multiprocessing import Pool, Manager
from publisher import publish_to_redis


def run():

    with Pool() as pool:
        q = Manager().Queue()
        p = Manager().Queue()
        k = Manager().Queue()
        res1 = pool.apply_async(getting_live_videos, args=(k,))
        res2 = pool.apply_async(track, args=(q, p, k))
        res3 = pool.apply_async(save_counter, args=(q,))
        res4 = pool.apply_async(publish_to_redis, args=(p,))
        res1.get()
        res2.get()
        res3.get()
        res4.get()

        pool.close()


if __name__ == "__main__":
    run()