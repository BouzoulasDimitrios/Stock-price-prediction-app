# Stock-price-prediction-app

<p align = "center">
<img src="./images/stock_graph.jpg" alt="ROS 2 Humble logo" style="width:50%;"/>
</p>

# Summary

The model used is an LSTM neural network. The aim was to create a model <br> 
that's able to predict the closing price of a given stock one day into the future.<br> 
In order to do this, the model takes as input the last 20 closing prices of the given stock. <br>
The data used to train the model consists of the stocks that are part of the S&P500 stock index fund,<br> 
meaning that the model is primarily adjusted for 'blue chip' stocks that don't tend to have <br>
large price fluctuations.

# Installation

In order to install all the required dependencies run:

    ~/$ git clone https://github.com/BouzoulasDimitrios/Stock-price-prediction-app.git
    ~/$ cd Stock-price-prediction-app/
    ~/Stock_price_prediction_app$ pip install -r requirements.txt

In order to run the desktop application:

    ~/Stock_price_prediction_app$ cd Desktop_application/
    ~/Stock_price_prediction_app/Desktop_application$ python3 main.py 


# Demo

<p align = "center">
<img src="./images/demo.gif" alt="ROS 2 Humble logo" style="width:65%;"/>
</p>

