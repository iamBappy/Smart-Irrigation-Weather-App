import sys
import requests 
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt

class Wapp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label= QLabel("Enter city name: ", self)
        self.city_input= QLineEdit(self)
        self.get_weather_button= QPushButton("Get Weather", self)
        self.temperature_label= QLabel( self)
        self.emoji_label= QLabel(self)
        self.description_label= QLabel( self)
        self.UI()

    def UI(self):
        self.setWindowTitle("Smart Irrigation Weather App")
        
        vbox=QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""
          QLabel#city_label {
          font-size: 35px;
                    }
          QLineEdit#city_input{
            font-size: 25px;}
          QPushButton#get_weather_button{
            font-size: 25px;
             font-weight: bold;}
            QLabel#temperature_label{
             font-size: 70px;}
            QLabel#emoji_label{
             font-size: 70px;
             font-family: Segoe UI emoji;}
             QLabel#description_label{
             font-size: 40px;}     
                         """)
        self.get_weather_button.clicked.connect(self.get_weather)
    
    def get_weather(self):
        api_key= "381ddd01706435a141fdc7ade46dda81"
        city=self.city_input.text()
        url= f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        
        try:   
           response= requests.get(url)
           response.raise_for_status()
           data= response.json()
           if data["cod"]== 200:
               self.display_weather(data)
        except requests.exceptions.HTTPError as http_error:
           match response.status_code:
              case 400:
                 self.display_error("Bad request\nPlease check your input")
              case 401:
                 self.display_error("Unauthorized\nInvalid API key")
              case 403:
                 self.display_error("Forbidden\nAccess denied")
              case 404:
                 self.display_error("Not found\nCity not found")
              case 500:
                 self.display_error("Internal server error\nPlease try again later")
              case 502:
                 self.display_error("Bad Gateway\nInvalid response from the server")
              case 503:
                 self.display_error("Service unavailable\nServer is down")
              case 504:
                 self.display_error("Gateway Timeout\nNo response from the server")
              case _:
                 self.display_error(f"HTTP  error occured\n{http_error}")
        except requests.exceptions.ConnectionError:
           self.display_error("Connection Error:\nCheck your internet connection")
        except requests.exceptions.Timeout:
           self.display_error("Timeout Error:\nThe request timed out")
        except requests.exceptions.TooManyRedirects:
           self.display_error("Too many redirects:\nCheck the url")
        except requests.exceptions.RequestException as any_error:
           self.display_error(f"Request Error:\n{any_error}")
    

    def display_error(self, message):
      self.temperature_label.setStyleSheet("font-size: 30px;")
      self.temperature_label.setText(message)
      self.emoji_label.clear()
      self.description_label.clear()

    def display_weather(self, data):
      self.temperature_label.setStyleSheet("font-size: 70px;")
      temp_k=data["main"]["temp"]
      temp_c=temp_k - 273.15 
      w_description=data["weather"][0]["description"]
      self.temperature_label.setText(f"{temp_c:.0f}°C")
      self.description_label.setText(w_description)
      w_id=data["weather"][0]["id"]
      self.emoji_label.setText(self.get_weather_emoji(w_id))

    @staticmethod
    def get_weather_emoji(w_id):
       if 200 <= w_id <=232:
          return "⛈️"
       elif 300 <= w_id <= 321:
          return "🌦️"
       elif 500 <= w_id <= 531:
          return "☔"
       elif 600 <= w_id <= 622:
          return "❄️"
       elif 701 <= w_id <= 741:
          return "🌫️"
       elif w_id== 762:
          return "🌋"
       elif w_id== 771:
          return "💨"
       elif w_id== 781:
          return "🌪️"
       elif w_id== 800:
          return "☀️\n May need irrigation"
       elif 801 <= w_id <= 804:
          return "☁️"
       else:
          return ""
       
       

if __name__=="__main__":
    app=QApplication(sys.argv)
    w_app=Wapp()
    w_app.show()
    sys.exit(app.exec_())


