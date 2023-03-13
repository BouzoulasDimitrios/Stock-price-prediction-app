from PyQt5 import  QtGui, QtWidgets
from PyQt5.QtWidgets import *
from general_functinos import stock_prediction_functions as spf
from model import LSTM
import torch
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


input_dim = 1
hidden_dim = 16
num_layers = 3
output_dim = 1
saved_model_path = "predict_stock_price_weights"

model = LSTM(input_dim=input_dim, hidden_dim=hidden_dim, output_dim=output_dim, num_layers=num_layers)
model.load_state_dict(torch.load(saved_model_path))

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(500, 500, 500, 300)
        self.setWindowTitle("Stock price predictor.")
        self.initUI()

    def initUI(self):
        self.label = QtWidgets.QLabel(self)
        self.label.setText("Enter a stock ticker.")
        self.label.adjustSize()
        self.update_label()

        self.prediction_button = QtWidgets.QPushButton(self)
        self.prediction_button.setText('Predict')
        self.prediction_button.move(70,150)
        self.prediction_button.clicked.connect(self.clicked)
        
        self.textbox = QLineEdit(self)
        self.textbox.move(80, 80)
        self.textbox.resize(80,30)
    
        self.graph = QtWidgets.QLabel(self)
        self.graph.setPixmap(QtGui.QPixmap("empty_graph.png"))
        self.graph.move(230,40)
        self.graph.resize(200,200)
        self.graph.setScaledContents(True)

        with open('dark.qss', 'r') as f:
            self.setStyleSheet(f.read())

        self.graph.show() 


    def clicked(self):

        ticker = self.textbox.text().strip()
        self.textbox.clear()

        if(not ticker):
            self.update_label()
            self.graph.setPixmap(QtGui.QPixmap("empty_graph.png"))
            return

        closing_price = spf.make_prediciton_for_ticker(ticker, model)
        message = self.generate_label_content(ticker, closing_price) 

        self.label.setText(message)
        self.label.adjustSize()
        self.label.setAlignment(Qt.AlignCenter)

        self.update_label(message)


    def update_label(self, output_message = "Please, enter a stock ticker."):

        self.label.adjustSize()
        self.label.setText(output_message)
        self.label.adjustSize()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.move(int(250 - self.label.width()/2), 250)


    def generate_label_content(self, inputed_ticker, closing_price = 0):

        if(closing_price):
            self.graph.setPixmap(QtGui.QPixmap("prediction_graph.png"))
            return  ( "next closing price for $" + str(inputed_ticker).upper() + " = " + str(closing_price) )        

        self.graph.setPixmap(QtGui.QPixmap("empty_graph.png"))
        return "No data was found.\nPlease give another stock ticker."
    

def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())

window()