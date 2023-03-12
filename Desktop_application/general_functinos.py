import yfinance as yf
# import fix_yahoo_finance as yf 
import pandas as pd
import datetime
from sklearn.preprocessing import MinMaxScaler
import torch 
import numpy as np
import matplotlib.pyplot as plt

class stock_prediction_functions():

    def get_stock_data(ticker: str, start_date: str, end_date: str):
        '''
            takes in stock name: "AAPL"
            starting date : '2010-01-01'
            ending date : '2015-01-01'
        '''
        data = yf.download(ticker, start_date, end_date, progress=False, show_errors=False) 
        return data
    

    def get_stock_data_for_prediction(ticker: str):
        '''
            returns a dataframe of the past 20 closing prices
            or an empty dataframe if nothing's found.
        '''
        days = 28
        price = []
        while (len(price)<20):
            today = datetime.datetime.now()
            d = datetime.timedelta(days = days)
            date = today - d
            prices = stock_prediction_functions.get_stock_data(ticker, date, datetime.datetime.now())
            price = prices[['Close']]
            if(price.empty):
                return pd.DataFrame({'A' : []})
            days +=1 

        return price


    def make_prediction(prediction_data, model_used):
        scaler = MinMaxScaler(feature_range=(-1, 1))
        prediction_data = scaler.fit_transform(prediction_data.values.reshape(-1,1))
        data = np.array(prediction_data)
        past_20_days =torch.from_numpy(data).type(torch.Tensor) 
        past_20_days = past_20_days.unsqueeze(dim=0)
        
        # make prediction
        y_load = model_used(past_20_days)

        # reverse the transformation done by the scaler.
        actuals = pd.DataFrame(scaler.inverse_transform(y_load.detach().numpy()))
        return actuals[0][0]
    

    def make_n_save_graph(prediciton_data, prediction):
        '''
            makes and saves a graph consisting of 21 closing prices,
            the 20 values used in order to make the prediciton and
            the one predicted value
        '''

        prediction = {'Close': prediction}
        prediciton_data = prediciton_data.append(prediction,ignore_index=True)

        plt.style.use('dark_background')
        plt.rcParams.update({'font.size': 20})
        plt.title("20 days + 1 predicted")
        plt.plot(range(len(prediciton_data)), prediciton_data, '-', color = 'yellow')
        plt.savefig('prediction_graph.png')
        plt.clf()


    def make_prediciton_for_ticker(ticker: str, model):

        pred_data   = stock_prediction_functions.get_stock_data_for_prediction(ticker)

        if(pred_data.empty):
            return
        
        prediction  = stock_prediction_functions.make_prediction(pred_data['Close'], model)
        stock_prediction_functions.make_n_save_graph(pred_data, prediction)
        return prediction


        