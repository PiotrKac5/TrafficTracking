import csv
import multiprocessing
import time
from datetime import datetime

def get_and_reset_counter(totalCount:set, q:multiprocessing.Queue):
    counted = len(totalCount)
    totalCount.clear()
    q.put(totalCount)
    return counted


def write_to_csv(veh_num:int, curr_date_time:str):
    with open("data.csv", newline='', mode="a") as f:
        fieldnames = [
            "date",
            "vehicles",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow({"date":curr_date_time, "vehicles":veh_num})
        f.close()

def save_counter(q):
    with open("data.csv", newline='', mode="w") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "vehicles"])
        writer.writeheader()
        f.close()

    while True:
        curr_datetime = datetime.now()
        curr_min = int(curr_datetime.strftime("%M"))

        while curr_min % 15 != 0: # ensures saving counted vehicles once every 15 minutes
            time.sleep(1)
            curr_datetime = datetime.now()
            curr_min = int(curr_datetime.strftime("%M"))

        curr_date_time = curr_datetime.strftime("%d/%m/%Y %H:%M")

        totalCount = q.get()
        while not q.empty():
            totalCount = q.get()
        veh_num = get_and_reset_counter(totalCount=totalCount, q=q)

        write_to_csv(veh_num=veh_num, curr_date_time=curr_date_time)
        time.sleep(60)


# save_counter()