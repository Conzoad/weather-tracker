import requests
from pymongo import MongoClient
import schedule
import time
from datetime import datetime

# Настройки
API_KEY = '850f5e3cbceb1a61780f15f5e2d6c87e'
CITY = 'London'
MONGO_URI = 'mongodb://localhost:27017/'
DB_NAME = 'weather_db'
COLLECTION_NAME = 'weather_data'

# Подключение к MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def fetch_and_store_weather():
    url = f'http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()
    
    weather_record = {
        'city': CITY,
        'temperature': data['main']['temp'],
        'humidity': data['main']['humidity'],
        'timestamp': datetime.now()
    }
    
    collection.insert_one(weather_record)
    print(f"Данные сохранены: {weather_record}")

# Планирование задачи
schedule.every(30).minutes.do(fetch_and_store_weather)

if __name__ == '__main__':
    fetch_and_store_weather()  # Первоначальный запуск
    while True:
        schedule.run_pending()
        time.sleep(1)
