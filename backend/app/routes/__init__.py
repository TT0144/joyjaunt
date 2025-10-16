"""
Routes package
"""
from app.routes.auth import auth_bp
from app.routes.location import location_bp
from app.routes.weather import weather_bp
from app.routes.news import news_bp
from app.routes.danger import danger_bp

__all__ = ['auth_bp', 'location_bp', 'weather_bp', 'news_bp', 'danger_bp']
