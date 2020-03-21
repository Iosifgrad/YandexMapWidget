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
        self.sub()
        self.search()

    def sub(self):
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": self.find,
        "format": "json"}

        response = requests.get(geocoder_api_server, params=geocoder_params)
        json_response = response.json()
        self.coords = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]['Point']['pos']

    def search(self):
        map_params = {
        "ll": ','.join(self.coords.split()),
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
                self.delta = str(float(self.delta) + 0.05)
                self.search()
                print(self.delta)
        if event.key() == Qt.Key_PageDown:
            if self.delta:
                self.delta = str(float(self.delta) - 0.05)
                self.search()
                print(self.delta)
        if event.key() == Qt.Key_Up:
            self.coords = [str(float(self.coords[0]) - 1), self.coords[1]]
            self.search()



app = QApplication(sys.argv)
ex = YandexMap()
ex.show()
sys.exit(app.exec_())