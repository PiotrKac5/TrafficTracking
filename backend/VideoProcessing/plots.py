from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import ticker


def generate_plots(duration='Yesterday'):
    """
    Generates plots based on data.csv file
    :param duration: Sets time range from data.csv file
    :return: plot in format fig, ax
    """
    curr_datetime = datetime.now().date()
    today = curr_datetime.strftime("%d/%m/%Y")

    df = pd.read_csv("VideoProcessing/sample_cars_data.csv")
    df['date'] = pd.to_datetime(df['date'], format="%d/%m/%Y").dt.date

    df = df[(df['date'] < curr_datetime)]

    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(16, 8))

    fig.set_facecolor('#1F1F1F')
    ax.set_facecolor('#1F1F1F')
    ax.grid(True, color='#FFFFFF', linestyle='--', linewidth=0.7)
    ax.set_ylabel('Number of vehicles', color='#FFFFFF', fontsize=12)
    ax.tick_params(axis='both', labelcolor='#FFFFFF', color='#FFFFFF')
    # ax.tick_params(axis='y', color='#FFFFFF')


    if duration == 'Yesterday':
        yesterday = datetime.now().date() - timedelta(days=1)
        df = df[df['date'] == yesterday]
        ax.plot(df['time'], df['vehicles'], color='#FFA500')
        ax.xaxis.set_major_locator(ticker.MultipleLocator(12))
    elif duration == 'OneWeek':
        one_week = datetime.now().date() - timedelta(days=8)
        df = df[df['date'] >= one_week]
        df = df.groupby('date').agg({'vehicles':'sum'}).reset_index()

        ax.plot(df['date'], df['vehicles'], color='#FFA500')
        # ax.xaxis.set_major_locator(ticker.MultipleLocator(1))

    else:
        one_month = datetime.now().date() - timedelta(days=31)
        df = df[df['date'] >= one_month]
        df = df.groupby('date').agg({'vehicles': 'sum'}).reset_index()

        ax.plot(df['date'], df['vehicles'], color='#FFA500')
        # ax.xaxis.set_major_locator(ticker.MultipleLocator(7))

    # plt.show()

    return fig, ax
