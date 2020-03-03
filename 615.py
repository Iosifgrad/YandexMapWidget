from PyQt5.QtWidgets import QApplication, QMainWindow, QMainWindow, QListView, QPushButton, QPushButton, QLineEdit, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5 import Qt, QtCore, uic
from PyQt5.QtCore import Qt
import sys, requests
from PIL import Image


class YandexMap(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('yandex_map.ui', self)
        self.initUI()

    def initUI(self):
        self.search_butt.clicked.connect(self.check_input)
    
    def check_input(self):
        self.delta = str(self.delta_input.text())
        self.find = self.address_input.text()
        self.search()

    def search(self):
        # функцию писал на коленке, можешь оптимизировать, если нужно. Имена виджетов оставь
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

        geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": self.find,
        "format": "json",
        }

        response = requests.get(geocoder_api_server, params=geocoder_params)
        find = response.json()
        find = ','.join(find['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split())

        geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": find,
        "format": "json"
        }

        response = requests.get(geocoder_api_server, params=geocoder_params)
        json_response = response.json()
        coords = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]['Point']['pos']

        map_params = {
        "ll": ','.join(coords.split()),
        "spn": ",".join([self.delta, self.delta]),
        "l": "map"
        }

        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)

        with open('map.png', "wb") as file:
            file.write(response.content)
        
        self.set_image()
    
    def set_image(self):
        pixmap = QPixmap('map.png')
        self.map.setPixmap(pixmap)
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            if self.delta:
                self.delta = str(float(self.delta) + 0.1)
        if event.key() == Qt.Key_PageDown:
            if self.delta:
                self.delta = str(float(self.delta) - 0.1)
                


app = QApplication(sys.argv)
ex = YandexMap()
ex.show()
sys.exit(app.exec_())