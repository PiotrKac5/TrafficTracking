import requests
import subprocess
import os

def get_videos(start_id:int=0) -> None:
    """
    Downloads current video from: https://go.toya.net.pl/25-kamery/14022-krakow/444414022176-centrum-kongresowe-ice/play
    as many 2seconds videos.
    Next, it converts them to mp4 files and saves in curr_vid folder
    start_id is id of first file (must be in range <0, 99>)
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

    for _ in range(100):
        url = "https://cdn-13-go.toya.net.pl/kamery/krak_centrumkongresowe_0"

        x = f"{i}"
        for _ in range(2, len(x), -1):
            url += "0"
        url += x
        url += ".ts"

        with open(f"curr_vid/v{i}.ts", 'wb') as f:
            r = requests.get(url, headers=headers)
            f.write(r.content)
            subprocess.run(['ffmpeg', '-i', f'curr_vid/v{i}.ts', f'curr_vid/v{i}.mp4'])

        os.remove(f"curr_vid/v{i}.ts")

        print(f"Ts file {i} converted")

        i += 1
        if i == 100:
            i = 0

    return None


get_videos(0)