import csv
import multiprocessing
import time
from datetime import datetime


def get_and_reset_counter(totalCount: set, q: multiprocessing.Queue) -> int:
    """
    Returns the number of vehicles_IDs currently in totalCount and clears it.
    :param totalCount: Set of vehicles_IDs seens up to 15min ago
    :return: Number of elements in totalCount
    """

    counted = len(totalCount)
    totalCount.clear()
    q.put(totalCount)
    return counted


def write_to_csv(veh_num: int, curr_date: str, curr_time:str) -> None:
    """
    Writes to "data.csv" number of vehicles from 15 minutes before current date and time.
    :param veh_num: Number of vehicles
    :param curr_date: Current date
    :param curr_time: Current time
    """

    with open("data.csv", newline='', mode="a") as f:
        fieldnames = [
            "date",
            "time",
            "vehicles",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow({"date": curr_date, "time":curr_time, "vehicles": veh_num})
        f.close()


def save_counter(q: multiprocessing.Queue) -> None:
    """
    Saves number of vehicles every 15 minutes to "data.csv" and zeroes it.
    "data.csv" file is cleared at every restart of application.
    """

    with open("data.csv", newline='', mode="w") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "time", "vehicles"])
        writer.writeheader()
        f.close()

    while True:
        curr_datetime = datetime.now()
        curr_min = int(curr_datetime.strftime("%M"))

        while curr_min % 15 != 0:  # ensures saving counted vehicles once every 15 minutes
            time.sleep(1)
            curr_datetime = datetime.now()
            curr_min = int(curr_datetime.strftime("%M"))

        curr_date = curr_datetime.strftime("%d/%m/%Y")
        curr_time = curr_datetime.strftime("%H:%M")

        totalCount = q.get()
        while not q.empty():
            totalCount = q.get()
        veh_num = get_and_reset_counter(totalCount=totalCount, q=q)

        write_to_csv(veh_num=veh_num, curr_date=curr_date, curr_time=curr_time)
        time.sleep(60)
