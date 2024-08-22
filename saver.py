import csv
import time
from datetime import datetime
from tracker import get_and_reset_counter


def write_to_csv(veh_num:int, curr_date_time:str):
    with open("data.csv", mode="w") as f:
        fieldnames = [
            "date",
            "vehicles",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({"date":curr_date_time, "vehicles":veh_num})

def save_counter():
    while True:
        curr_datetime = datetime.now()
        curr_min = int(curr_datetime.strftime("%M"))

        while curr_min % 2 != 0: # ensures saving counted vehicles once every 15 minutes
            time.sleep(1)
            curr_datetime = datetime.now()
            curr_min = int(curr_datetime.strftime("%M"))

        curr_date_time = curr_datetime.strftime("%d/%m/%Y %H:%M")
        veh_num = get_and_reset_counter()
        write_to_csv(veh_num=veh_num, curr_date_time=curr_date_time)
        time.sleep(60)


save_counter()