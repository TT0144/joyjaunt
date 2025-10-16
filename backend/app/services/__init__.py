"""
Services package
"""
from app.services.weather_service import get_weather_forecast, get_current_weather
from app.services.news_service import get_news_by_location, get_general_news
from app.services.danger_service import calculate_danger_level, get_danger_level_description

__all__ = [
    'get_weather_forecast',
    'get_current_weather',
    'get_news_by_location',
    'get_general_news',
    'calculate_danger_level',
    'get_danger_level_description'
]
