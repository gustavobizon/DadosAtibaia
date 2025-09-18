import requests
import os
from datetime import datetime

# ---- CONFIGURAÇÕES ----
WEATHER_API_KEY = os.getenv("9ac74d5ccb01496a836200425251709")  # Chave do WeatherAPI
THINGSBOARD_TOKEN = os.getenv("TPG2CFH6bXIPCFcnQdMy")  # Token do device no ThingsBoard
LAT = "-23.1165"  # Latitude de Atibaia
LON = "-46.5500"  # Longitude de Atibaia

# Endpoints
WEATHER_URL = f"http://api.weatherapi.com/v1/current.json?key=9ac74d5ccb01496a836200425251709&q=Atibaia"
THINGSBOARD_URL = f"https://thingsboard.cloud/api/v1/TPG2CFH6bXIPCFcnQdMy/telemetry"

def get_weather():
    """Busca dados do WeatherAPI"""
    try:
        response = requests.get(WEATHER_URL)
        data = response.json()

        # Pegando temperatura e umidade
        temp_c = data["current"]["temp_c"]
        humidity = data["current"]["humidity"]

        print(f"[{datetime.now()}] Temperatura: {temp_c}°C | Umidade: {humidity}%")
        return temp_c, humidity
    except Exception as e:
        print("Erro ao obter dados do WeatherAPI:", e)
        return None, None

def send_to_thingsboard(temp, humidity):
    """Envia temperatura e umidade para o ThingsBoard"""
    try:
        payload = {
            "temperature": temp,
            "humidity": humidity
        }
        r = requests.post(THINGSBOARD_URL, json=payload)
        if r.status_code == 200:
            print("Dados enviados com sucesso!")
        else:
            print("Falha ao enviar dados:", r.text)
    except Exception as e:
        print("Erro ao enviar para o ThingsBoard:", e)

def main():
    temp, humidity = get_weather()
    if temp is not None and humidity is not None:
        send_to_thingsboard(temp, humidity)

if __name__ == "__main__":
    main()
