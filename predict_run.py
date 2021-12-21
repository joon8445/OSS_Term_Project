import data_manager
import os
import pandas as pd

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


if __name__ == '__main__':
    interval_list = ['day', 'hour12', 'hour6', 'hour']

    for interval in interval_list:
        print(interval)
        df = data_manager.get_price(interval)
        pred_file = f'./data/{interval}_predict.csv'


        time = str(df.index[-1])

        if os.path.exists(pred_file):
            predict = pd.read_csv(pred_file)
            if predict.time.iloc[-1] == time:
                print('already predicted')
            else:
                print('predict yet')
                data_manager.update_predict(interval)
        else:
            print('predict yet')
            data_manager.update_predict(interval)
