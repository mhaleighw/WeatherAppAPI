from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QLabel, QVBoxLayout
from api_key import my_key
import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class Home(QWidget):
    def __init__(self):
        super().__init__()
        self.settings()
        self.initUI()
        self.api_key = my_key
        self.submit.clicked.connect(self.search_click)

    def settings(self):
        self.setWindowTitle("OpenWeatherAPI")
        self.setGeometry(270, 400, 650, 700)

    def initUI(self):
        self.title = QLabel("OpenWeatherAPI")
        self.title.setFont(QFont("Montserrat", 50, QFont.Bold))
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Location: ")

        self.output = QLabel("Weather Information: ")
        self.output.setFont(QFont("Montserrat", 22, QFont.Bold))
        self.submit = QPushButton("Search")

        self.master = QVBoxLayout()
        self.master.addWidget(self.title, alignment=Qt.AlignCenter)
        self.master.addWidget(self.input_box)
        self.master.addWidget(self.output)
        self.master.addWidget(self.submit)


        self.setLayout(self.master)

        # styling of the GUI
        self.setStyleSheet("""
            QWidget {
                background-color: #FFF5E1; /* cream */
            }

            QLabel {
                color: #FF6969; /* strawberry */
            }

            QLabel#output {
                color: #0C1844;
                font-size: 35px; /* Increase font size here */
                border: 1px solid #FF6969; /* strawberry */
                padding: 10px;
                background-color: #FF6969; /* pink */
                border-radius: 5px;
            }

            QLineEdit {
                background-color: #FFF5E1; /* cream */
                color: #C80036; /* mauve */
                border: 1px solid #FF6969;
                padding: 5px;
                border-radius: 8px;
                font-size: 14px;
            }

            QPushButton {
                background-color: #FF6969; /* strawberry */
                color: white;
                border: 1px solid #C80036;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }

            QPushButton:hover {
                background-color: #C80036; /* deep red */
                color: #FFF5E1; /* cream */
            }

            QPushButton:pressed {
                background-color: #990024; /* darker red */
            }
        """)





    def search_click(self):
        self.results = self.get_weather(self.api_key, self.input_box.text())
        self.output.setText(self.results)




    def get_weather(self, api_key, city, country=""):
        base_url = "https://api.openweathermap.org/data/2.5/weather"
        params = {'q': f'{city}, {country}', 'appid': api_key}

        try:
            res = requests.get(base_url, params=params)
            data = res.json()

            if res.status_code == 200:
                city_name = data['name']
                country_code = data['sys']['country']

                temperature_kelvin = data['main']['temp']
                temperature_fahrenheit = (temperature_kelvin - 273.15) * 9/5 + 32

                weather_description = data['weather'][0]['description']
                humidity = data['main']['humidity']
                wind_speed = data['wind']['speed']
                wind_direction = data['wind']['deg']

                weather_info = (f"Weather in {city_name}, {country_code}:\n"
                                f"Temperature: {temperature_fahrenheit:.2f}°F\n"
                                f"Description: {weather_description}\n"
                                f"Humidity: {humidity}%\n"
                                f"Wind Speed: {wind_speed} m/s, Direction: {wind_direction}°")

                return weather_info
            else:
                return f"Error: {data['message']}"
        except Exception as e:
            return f"An error occurred: {e}"








if __name__ == "__main__":
    app = QApplication([])
    main = Home()
    main.show()
    app.exec_()