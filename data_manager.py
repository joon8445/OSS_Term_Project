import pybithumb
import pandas as pd
import os
import prediction

def get_price(interval='day', view_all=False):
    price = pybithumb.get_ohlcv("BTC", interval=interval)
    if not view_all:
        if interval == 'hour6':
            if price.index[-1].hour % 6 != 0:
                price = price[:-1]

        elif interval == 'hour12':
            if price.index[-1].hour % 12 != 0:
                price = price[:-1]

        elif interval == 'day':
            if price.index[-1].hour != 0:
                price = price[:-1]
    return price

def update_predict(interval):
    time, percent = prediction.RNN(get_price(interval))
    pred_data = {'time': time, 'pred': percent}
    pred_data = pd.DataFrame([pred_data])
    file = f'./data/{interval}_predict.csv'
    if not os.path.exists(file):
        pred_data.to_csv(file, index=False, mode='w', encoding='utf-8-sig')
    else:
        pred_data.to_csv(file, index=False, mode='a', encoding='utf-8-sig', header=False)

def read_predict(chart_interval):
    interval = {
        "1일": "day", "12시간": "hour12", "6시간": "hour6", "1시간": "hour"
    }[chart_interval]
    try:
        df = pd.read_csv(f'./data/{interval}_predict.csv')
        predict = df.time.iloc[-1]
        predict+= ' 기준\n' + chart_interval +' 후 예측 : '
        predict+= df.pred.iloc[-1]
        return predict
    except:
        return 'prediction error'