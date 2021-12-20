import pandas as pd
import mpl_finance
import matplotlib.ticker as ticker
import data_manager

def draw_chart(self, chart_interval='1일'):
    interval = {
        "1일": "day", "12시간": "hour12", "6시간": "hour6", "1시간": "hour"
    }[chart_interval]

    df = data_manager.get_price(interval)
    df = df[-90:-1]

    self.ax = self.fig.subplots()
    day_list = []
    name_list = []

    if interval == 'day':
        for i, day in enumerate(df.index):
            if day.dayofweek == 0 and day.week % 2 == 0:
                day_list.append(i)
                name_list.append(day.strftime('%m-%d'))
    elif interval == 'hour12':
        for i, day in enumerate(df.index):
            if day.dayofweek == 0 and day.hour == 0:
                day_list.append(i)
                name_list.append(day.strftime('%m-%d'))
    elif interval == 'hour6':
        for i, day in enumerate(df.index):
            if day.day % 3 == 1 and day.hour == 0:
                day_list.append(i)
                name_list.append(day.strftime('%m-%d'))

    elif interval == 'hour':
        for i, day in enumerate(df.index):
            if day.hour % 12 == 6:
                day_list.append(i)
                name_list.append(day.strftime('%m-%d.%H'))

    self.ax.xaxis.set_major_locator(ticker.FixedLocator(day_list))
    self.ax.xaxis.set_major_formatter(ticker.FixedFormatter(name_list))

    mpl_finance.candlestick2_ohlc(self.ax, df['open'], df['high'], df['low'], df['close'], width=0.5, colorup='r', colordown='b')
