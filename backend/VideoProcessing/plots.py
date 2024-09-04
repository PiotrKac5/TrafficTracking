from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import pandas as pd

def generate_plots(duration=None):
    curr_datetime = datetime.now().date()
    today = curr_datetime.strftime("%d/%m/%Y")

    df = pd.read_csv("sample_cars_data.csv")
    df['date'] = pd.to_datetime(df['date'], format="%d/%m/%Y").dt.date

    df = df[(df['date'] < curr_datetime)]

    if duration == 'Yesterday':
        yesterday = datetime.now().date() - timedelta(days=1)
        df = df[df['date'] == yesterday]
    elif duration == 'One Week':
        one_week = datetime.now().date() - timedelta(days=8)
        df = df[df['date'] >= one_week]
    else:
        one_month = datetime.now().date() - timedelta(days=31)
        df = df[df['date'] >= one_month]

    print(df.describe())



generate_plots('One Month')
