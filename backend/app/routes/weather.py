"""
天気予報ルート
"""
from flask import Blueprint, request, jsonify
from app.services.weather_service import get_weather_forecast, get_current_weather
from app.models import User, db
import logging

logger = logging.getLogger(__name__)
weather_bp = Blueprint('weather', __name__)


@weather_bp.route('/weather_forecast', methods=['GET'])
def weather_forecast():
    """天気予報を取得"""
    try:
        city = request.args.get('city', default='Tokyo', type=str)
        logger.info(f"天気予報リクエスト - 都市: {city}")

        forecast_data = get_weather_forecast(city)

        if not forecast_data:
            logger.warning(f"天気データが取得できませんでした: {city}")
            return jsonify({"error": "Could not fetch weather forecast"}), 500

        logger.info(f"天気予報取得成功: {city}, {len(forecast_data)}日分")
        return jsonify({"forecast": forecast_data}), 200

    except Exception as e:
        logger.error(f"天気予報エラー: {str(e)}")
        return jsonify({"error": "An error occurred", "details": str(e)}), 500


@weather_bp.route('/weather_forecast_for_user', methods=['GET'])
def weather_forecast_for_user():
    """ユーザーの居住国に基づいて天気予報を取得"""
    try:
        email = request.args.get('email')
        if not email:
            logger.warning("Emailが指定されていません")
            return jsonify({"error": "Email is required"}), 400

        user = User.query.filter_by(EMAIL=email).first()
        if not user:
            logger.warning(f"ユーザーが見つかりません: {email}")
            return jsonify({"error": "User not found"}), 404

        # ユーザーの国コードから国名を取得
        from app.models import Country
        country = Country.query.filter_by(CODE=user.COUNTRY_Code).first()
        if not country:
            logger.warning(f"国が見つかりません: {user.COUNTRY_Code}")
            return jsonify({"error": "Country not found"}), 404

        logger.info(f"ユーザーの天気予報リクエスト - Email: {email}, 国: {country.NAME}")

        forecast_data = get_weather_forecast(country.NAME)

        if not forecast_data:
            logger.warning(f"天気データが取得できませんでした: {country.NAME}")
            return jsonify({"error": "Could not fetch weather forecast"}), 500

        logger.info(f"天気予報取得成功: {country.NAME}, {len(forecast_data)}日分")
        return jsonify({
            "country": country.NAME,
            "forecast": forecast_data
        }), 200

    except Exception as e:
        logger.error(f"ユーザー天気予報エラー: {str(e)}")
        return jsonify({"error": "An error occurred", "details": str(e)}), 500


@weather_bp.route('/weather_forecast_for_travel_plan', methods=['GET'])
def weather_forecast_for_travel_plan():
    """旅行計画のための天気予報を取得"""
    try:
        city = request.args.get('city', default='Tokyo', type=str)
        logger.info(f"天気予報リクエスト - 都市: {city}")

        forecast_data = get_weather_forecast(city)

        if not forecast_data:
            logger.warning(f"天気データが取得できませんでした: {city}")
            return jsonify({"error": "Could not fetch weather forecast"}), 500

        logger.info(f"天気予報取得成功: {city}, {len(forecast_data)}日分")
        return jsonify({"forecast": forecast_data}), 200

    except Exception as e:
        logger.error(f"天気予報エラー: {str(e)}")
        return jsonify({"error": "An error occurred", "details": str(e)}), 500


@weather_bp.route('/current_weather', methods=['GET'])
def current_weather():
    """現在の天気を取得"""
    try:
        city = request.args.get('city', default='Tokyo', type=str)
        logger.info(f"現在の天気リクエスト - 都市: {city}")

        weather_data = get_current_weather(city)

        if not weather_data:
            logger.warning(f"天気データが取得できませんでした: {city}")
            return jsonify({"error": "Could not fetch current weather"}), 500

        logger.info(f"現在の天気取得成功: {city}")
        return jsonify(weather_data), 200

    except Exception as e:
        logger.error(f"現在の天気エラー: {str(e)}")
        return jsonify({"error": "An error occurred", "details": str(e)}), 500
