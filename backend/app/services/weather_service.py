"""
天気予報サービス
"""
import requests
from datetime import datetime, timedelta
from flask import current_app


def get_weather_forecast(city_name, days=7):
    """
    OpenWeather APIを使用して天気予報を取得

    Args:
        city_name: 都市名
        days: 取得する日数(デフォルト7日)

    Returns:
        list: 天気予報データのリスト
    """
    try:
        api_key = current_app.config['OPEN_WEATHER_API_KEY']
        base_url = current_app.config['OPEN_WEATHER_API_URL']

        # 現在の天気を取得して座標を取得
        current_weather_url = f"{base_url}/weather"
        params = {
            'q': city_name,
            'appid': api_key,
            'units': 'metric',
            'lang': 'ja'
        }

        response = requests.get(current_weather_url, params=params, timeout=10)
        response.raise_for_status()
        current_data = response.json()

        # 座標を取得
        lat = current_data['coord']['lat']
        lon = current_data['coord']['lon']

        # One Call APIで詳細な予報を取得
        forecast_url = f"{base_url}/onecall"
        forecast_params = {
            'lat': lat,
            'lon': lon,
            'appid': api_key,
            'units': 'metric',
            'lang': 'ja',
            'exclude': 'minutely,hourly,alerts'
        }

        forecast_response = requests.get(
            forecast_url, params=forecast_params, timeout=10)
        forecast_response.raise_for_status()
        forecast_data = forecast_response.json()

        # データを整形
        formatted_forecast = []
        for i, day in enumerate(forecast_data.get('daily', [])[:days]):
            date = datetime.fromtimestamp(day['dt'])
            formatted_forecast.append({
                'date': date.strftime('%Y-%m-%d'),
                'day_of_week': date.strftime('%A'),
                'temperature': round(day['temp']['day'], 1),
                'temp_min': round(day['temp']['min'], 1),
                'temp_max': round(day['temp']['max'], 1),
                'weather': day['weather'][0]['description'],
                'weather_main': day['weather'][0]['main'],
                'humidity': day['humidity'],
                'wind_speed': day['wind_speed'],
                'pop': day.get('pop', 0) * 100  # 降水確率(%)
            })

        return formatted_forecast

    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"Weather API error: {str(e)}")
        return None
    except Exception as e:
        current_app.logger.error(f"Weather forecast error: {str(e)}")
        return None


def get_current_weather(city_name):
    """
    現在の天気を取得

    Args:
        city_name: 都市名

    Returns:
        dict: 現在の天気データ
    """
    try:
        api_key = current_app.config['OPEN_WEATHER_API_KEY']
        base_url = current_app.config['OPEN_WEATHER_API_URL']

        url = f"{base_url}/weather"
        params = {
            'q': city_name,
            'appid': api_key,
            'units': 'metric',
            'lang': 'ja'
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        return {
            'temperature': round(data['main']['temp'], 1),
            'feels_like': round(data['main']['feels_like'], 1),
            'temp_min': round(data['main']['temp_min'], 1),
            'temp_max': round(data['main']['temp_max'], 1),
            'humidity': data['main']['humidity'],
            'weather': data['weather'][0]['description'],
            'weather_main': data['weather'][0]['main'],
            'wind_speed': data['wind']['speed'],
            'city_name': data['name']
        }

    except Exception as e:
        current_app.logger.error(f"Current weather error: {str(e)}")
        return None
