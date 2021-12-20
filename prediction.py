import numpy as np
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout

"""
    Original Code
    https://github.com/INVESTAR/StockAnalysisInPython/blob/master/09_Deep_Learning_Prediction/ch09_09_RNN_StockPrediction.py
    modified by s-jun
"""

def LSTM(df):
    raw_df = df

    def MinMaxScaler(data):
        """최솟값, 최댓값 이용해 0~1 값으로 변환"""
        numerator = data - np.min(data, 0)
        denominator = np.max(data, 0) - np.min(data, 0)
        return numerator / (denominator + 1e-7)

    dfx = raw_df[['open', 'high', 'low', 'close', 'volume']]
    dfx = MinMaxScaler(dfx)
    dfy = dfx[['close']]
    x = dfx.values.tolist()
    y = dfy.values.tolist()

    data_x = []
    data_y = []
    window_size = 10
    for i in range(len(y) - window_size):
        _x = x[i: i + window_size]
        _y = y[i + window_size]
        data_x.append(_x)
        data_y.append(_y)

    # 훈련용 데이터셋
    train_size = int(len(data_y) * 0.7)
    train_x = np.array(data_x[0:train_size])
    train_y = np.array(data_y[0:train_size])

    # 테스트용 데이터셋
    test_size = len(data_y) - train_size
    test_x = np.array(data_x[train_size:len(data_x)])
    test_y = np.array(data_y[train_size:len(data_y)])

    model = Sequential()
    model.add(LSTM(units=10, activation='relu', return_sequences=True, input_shape=(window_size, 5)))
    model.add(Dropout(0.1))
    model.add(LSTM(units=10, activation='relu'))
    model.add(Dropout(0.1))
    model.add(Dense(units=1))
    model.summary()

    model.compile(optimizer='adam', loss='mean_squared_error')  # 최적화도구: adam
    model.fit(train_x, train_y, epochs=50, batch_size=30)  # epochs : 학습횟수, batch_size: 훈련데이터 갯수
    pred_y = model.predict(test_x)

    predict_price_tommorow = (raw_df.close.iloc[-1] * pred_y[-1] / dfy.close.iloc[-1])[0]
    predict_price_today = (raw_df.close.iloc[-2] * pred_y[-2] / dfy.close.iloc[-2])[0]

    percentage = round(((predict_price_tommorow / predict_price_today - 1) * 100), 3)
    percentage = str(percentage) + '%'

    return df.index[-1], percentage
