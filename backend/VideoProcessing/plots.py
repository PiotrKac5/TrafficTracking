from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import ticker


def generate_plots(duration='Yesterday'):
    curr_datetime = datetime.now().date()
    today = curr_datetime.strftime("%d/%m/%Y")

    df = pd.read_csv("sample_cars_data.csv")
    df['date'] = pd.to_datetime(df['date'], format="%d/%m/%Y").dt.date

    df = df[(df['date'] < curr_datetime)]

    fig, ax = plt.subplots(figsize=(12, 6))

    if duration == 'Yesterday':
        yesterday = datetime.now().date() - timedelta(days=1)
        df = df[df['date'] == yesterday]
        ax.plot(df['time'], df['vehicles'])
        ax.xaxis.set_major_locator(ticker.MultipleLocator(12))
    elif duration == 'One Week':
        one_week = datetime.now().date() - timedelta(days=8)
        df = df[df['date'] >= one_week]
        df = df.groupby('date').agg({'vehicles':'mean'}).reset_index()

        ax.plot(df['date'], df['vehicles'])
        ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    else:
        one_month = datetime.now().date() - timedelta(days=31)
        df = df[df['date'] >= one_month]
        ax.plot(df['date'], df['vehicles'])
        df = df.groupby('date').agg({'vehicles': 'mean'}).reset_index()

        ax.plot(df['date'], df['vehicles'])
        ax.xaxis.set_major_locator(ticker.MultipleLocator(7))

    # plt.show()

    return fig, ax



generate_plots('One Week')
