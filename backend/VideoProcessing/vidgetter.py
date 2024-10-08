import multiprocessing
import platform
import subprocess
import time
import requests
import os
import m3u8
from moviepy.editor import *

def get_videos(start_id:int=0) -> None:
    """
    Downloads current video from: https://go.toya.net.pl/25-kamery/14022-krakow/444414022167-zbigniewa-herberta-trasa-lagiewnicka/play
    as many 2-seconds videos.
    Next, it converts them to mp4 files and saves in curr_vid folder
    start_id is id of first file (must be in range <0, 99>)
    (It downloads 50 2-seconds videos)
    """


    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                      "AppleWebKit/537.11 (KHTML, like Gecko) "
                      "Chrome/23.0.1271.64 Safari/537.11",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
        "Accept-Encoding": "none",
        "Accept-Language": "en-US,en;q=0.8",
        "Connection": "keep-alive",
    }

    i = start_id

    for i in range(start_id, start_id+50):
        i %= 100

        url = "https://cdn-13-go.toya.net.pl/kamery/krak_herbertalagiewnicka_0"

        x = f"{i}"
        for _ in range(2, len(x), -1):
            url += "0"
        url += x
        url += ".ts"

        ts_path = f"curr_vid/v{i}.ts"
        mp4_path = f"curr_vid/v{i}.mp4"

        with open(ts_path, 'wb') as f:
            r = requests.get(url, headers=headers)
            f.write(r.content)

        if platform.system() == "Windows":
            subprocess.run(['ffmpeg', '-y', '-i', ts_path, '-c', 'copy', mp4_path], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, shell=True)
        else:
            subprocess.run(['ffmpeg', '-y', '-i', ts_path, '-c', 'copy', mp4_path])
        os.remove(ts_path)

        with open(f"curr_vid/v{i}.txt", 'a') as f: #to show to other process running in parallel that mp4 file is ready
            f.write("File ready")

        print(f"Ts file {i} converted")

    return None


def get_starting_point() -> int:
    """
    Returns the id of first ts file to be downloaded
    """

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                      "AppleWebKit/537.11 (KHTML, like Gecko) "
                      "Chrome/23.0.1271.64 Safari/537.11",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
        "Accept-Encoding": "none",
        "Accept-Language": "en-US,en;q=0.8",
        "Connection": "keep-alive",
    }

    url = "https://cdn-14-go.toya.net.pl/kamery/krak_herbertalagiewnicka.m3u8"

    r = requests.get(url, headers=headers)
    playlist = m3u8.loads(r.text)

    start_id = int(playlist.data['segments'][0]['uri'][-5:-3])

    return start_id


def getting_live_videos(q:multiprocessing.Queue) -> None:
    """
    Ensures downloading, converting and connecting live-time video without any loss.
    """

    start_id = get_starting_point()
    q.put(start_id)

    last_download_time = time.time() - 50 * 2.2
    while True:
        last_download_time += 50 * 2.2
        get_videos(start_id=start_id)

        curr_time = time.time()
        if curr_time < last_download_time + 47 * 2.2: # to ensure non-stop video
            time.sleep(last_download_time + 47 * 2.2 - curr_time)

        start_id += 50
        start_id %= 100

if __name__ == '__main__':
    q = multiprocessing.Manager().Queue()
    getting_live_videos(q)