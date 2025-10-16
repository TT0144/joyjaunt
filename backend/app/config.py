"""
アプリケーション設定
"""
import os
from datetime import timedelta
from dotenv import load_dotenv

# .envファイルを読み込む
load_dotenv()


class Config:
    """基本設定"""
    # Flask設定
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')

    # JWT設定
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default_jwt_secret_key')
    JWT_TOKEN_LOCATION = ['headers']
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1)

    # データベース設定
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'mysql+pymysql://dbuser:ecc@db:3306/Joy'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # CORS設定
    CORS_ORIGINS = ["http://localhost:3001", "http://localhost:3000"]
    CORS_SUPPORTS_CREDENTIALS = True

    # 外部API設定
    NEWS_API_KEY = os.getenv('NEWS_API_KEY')
    TRAVEL_ADVISORY_API_KEY = os.getenv('TRAVEL_ADVISORY_API_KEY')
    OPEN_WEATHER_API_KEY = os.getenv('OPEN_WEATHER_API_KEY')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

    # API URL
    NEWS_API_URL = 'https://newsapi.org/v2/everything'
    TRAVEL_ADVISORY_API_URL = 'https://www.travel-advisory.info/api'
    OPEN_WEATHER_API_URL = 'https://api.openweathermap.org/data/2.5'


class DevelopmentConfig(Config):
    """開発環境設定"""
    DEBUG = True


class ProductionConfig(Config):
    """本番環境設定"""
    DEBUG = False


# 環境に応じた設定を取得
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
