"""
Flask アプリケーションファクトリ
"""
import os
import logging
from flask import Flask
from flask_cors import CORS

from app.extensions import db, bcrypt, jwt, migrate
from app.config import Config, DevelopmentConfig, ProductionConfig


def create_app(config_name='development'):
    """
    Flaskアプリケーションを作成するファクトリ関数

    Args:
        config_name: 設定名('development' or 'production')

    Returns:
        Flask: 設定済みのFlaskアプリケーション
    """
    app = Flask(__name__)

    # 設定をロード
    if config_name == 'production':
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    # ロギング設定
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # 拡張機能を初期化
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # CORS設定
    CORS(app,
         resources={r"/*": {"origins": app.config['CORS_ALLOWED_ORIGINS']}},
         supports_credentials=True)

    # Blueprintを登録
    from app.routes import auth_bp, location_bp, weather_bp, news_bp, danger_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(location_bp, url_prefix='/api/location')
    app.register_blueprint(weather_bp, url_prefix='/api/weather')
    app.register_blueprint(news_bp, url_prefix='/api/news')
    app.register_blueprint(danger_bp, url_prefix='/api/danger')

    # ヘルスチェックエンドポイント
    @app.route('/health', methods=['GET'])
    def health_check():
        return {'status': 'OK', 'message': 'JoyJaunt API is running'}, 200

    # ルートエンドポイント
    @app.route('/', methods=['GET'])
    def index():
        return {
            'message': 'Welcome to JoyJaunt API',
            'version': '2.0',
            'endpoints': {
                'auth': '/api/auth',
                'location': '/api/location',
                'weather': '/api/weather',
                'news': '/api/news',
                'danger': '/api/danger'
            }
        }, 200

    return app
