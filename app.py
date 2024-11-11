from flask import Flask, render_template
from pymongo import MongoClient
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime, timedelta

app = Flask(__name__)

# Подключение к MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['weather_db']
collection = db['weather_data']

@app.route('/')
def index():
    # Получение данных за последний день
    today = datetime.now()
    start = today - timedelta(days=1)
    data = list(collection.find({'timestamp': {'$gte': start, '$lte': today}}))

    # Подготовка данных для графика
    times = [record['timestamp'] for record in data]
    temperatures = [record['temperature'] for record in data]

    # Построение графика
    plt.figure(figsize=(10,5))
    plt.plot(times, temperatures, marker='o')
    plt.title('Температура за последние 24 часа')
    plt.xlabel('Время')
    plt.ylabel('Температура (°C)')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Сохранение графика в буфер
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_png = buf.getvalue()
    buf.close()

    # Кодирование изображения
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')

    return render_template('index.html', graph=graph)

if __name__ == '__main__':
    app.run(debug=True)
