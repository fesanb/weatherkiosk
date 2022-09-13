#!/usr/bin/python

import requests
import json

from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QHBoxLayout, QVBoxLayout, QPushButton, QFrame, QGridLayout
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer


url = 'https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=59.96&lon=10.74'
headers = {'user-agent': 'weatherkiosk/0.1 stefan@bahrawy.net'}
response = requests.get(url, headers=headers)

rdata = response.text
jdata = json.loads(rdata)

# print(type(jdata))
# print(jdata)

# print(jdata['properties']['meta'])

# print(jdata['properties']['timeseries'][1])




# print(jdata['properties']['timeseries'][1]['time'])
# print(jdata['properties']['timeseries'][1]['data']['instant']['details']['air_temperature'])
# print(jdata['properties']['timeseries'][1]['data']['instant']['details']['wind_speed'])
# print(jdata['properties']['timeseries'][1]['data']['next_1_hours']['summary']['symbol_code'])
# print(jdata['properties']['timeseries'][1]['data']['next_1_hours']['details']['precipitation_amount'])

times = 24
ts = 0

while ts < times:
    path_time = jdata['properties']['timeseries'][ts]['time']
    path_temp = jdata['properties']['timeseries'][ts]['data']['instant']['details']['air_temperature']
    path_wind = jdata['properties']['timeseries'][ts]['data']['instant']['details']['wind_speed']
    path_rain = jdata['properties']['timeseries'][ts]['data']['next_1_hours']['details']['precipitation_amount']
    path_symbol = jdata['properties']['timeseries'][ts]['data']['next_1_hours']['summary']['symbol_code']

    print(path_time, path_temp, path_temp, path_wind, path_rain, path_symbol)
    ts += 1


class App(QWidget):

	def __init__(self, parent=None):
		super(App, self).__init__(parent=parent)
		self.title = "WFS - Weather Forecast Station"
		self.setWindowIcon(QIcon("img/drawing.svg.png"))
		self.setWindowTitle(self.title)
		self.setStyleSheet("color: white; background-color: black;")

		if ps is True:
			self.showFullScreen()
		else:
			self.left = 0
			self.top = 0
			self.width = 720
			self.height = 480
			self.setGeometry(self.left, self.top, self.width, self.height)

		self.initUI()


def initUI(self):
    path = str(Path(__file__).parent.absolute())

    self.O1 = QVBoxLayout(self)
    self.mainContainer = QHBoxLayout(self)
    self.windContainer = QVBoxLayout(self)

    try:  # Wind box

        self.windBox = QHBoxLayout()
        self.windFrame = QFrame(self)
        self.wind_VL = QVBoxLayout(self.windFrame)
        self.windL = QLabel(fetch_wind.wind, self.windFrame)
        img = path + "/img/wc_wind.png"
        self.windL.setStyleSheet("background-image: url({}); "
                                 "background-repeat: no-repeat; "
                                 "background-position: center".format(img))
        self.windL.setAlignment(Qt.AlignCenter)
        self.windL.setMinimumHeight(200)
        self.windL.setFont(QFont('Arial', 50))
        self.wind_VL.addWidget(self.windL)
        self.windBox.addWidget(self.windFrame)

        self.meanFrame = QFrame(self)
        self.mean_VL = QVBoxLayout(self.meanFrame)
        self.meanL = QLabel(str(fetch_mean.meanwind), self.meanFrame)
        img = path + "/img/wc_mean.png"
        self.meanL.setStyleSheet("background-image: url({}); "
                                 "background-repeat: no-repeat; "
                                 "background-position: center".format(img))
        self.meanL.setAlignment(Qt.AlignCenter)
        self.meanL.setMinimumHeight(200)
        self.meanL.setFont(QFont('Arial', 50))
        self.mean_VL.addWidget(self.meanL)
        self.windBox.addWidget(self.meanFrame)

        self.windContainer.addLayout(self.windBox)

    except Exception as e:
        filename = Path(__file__).name
        error_handle(e, filename)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	ex.show()