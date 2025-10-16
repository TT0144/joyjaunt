"""
危険度評価ルート
"""
from flask import Blueprint, request, jsonify
from app.services.danger_service import calculate_danger_level, get_danger_level_description
from app.services.weather_service import get_weather_forecast
from app.services.geocoding_service import get_location_from_coordinates
from app.models import Country
import logging

logger = logging.getLogger(__name__)
danger_bp = Blueprint('danger', __name__)


@danger_bp.route('/check_realtime_danger', methods=['POST'])
def check_realtime_danger():
    """
    リアルタイム危険度チェック
    静的スコア + ニュース情報で総合判定
    """
    try:
        data = request.json
        country_name = data.get('country', '').strip()
        city_name = data.get('city', '').strip()

        if not country_name:
            return jsonify({'error': 'Country name is required'}), 400

        # 国の存在確認
        country = Country.query.filter_by(Name=country_name).first()
        if not country:
            return jsonify({'error': f'Country "{country_name}" not found'}), 404

        # 総合的な危険度を計算
        danger_info = calculate_danger_level(country_name, city_name)

        return jsonify({
            'is_dangerous': danger_info['is_dangerous'],
            'danger_score': danger_info['score'],
            'base_score': danger_info['base_score'],
            'news_count': danger_info['news_count'],
            'news_adjustment': danger_info['news_adjustment'],
            'danger_level': get_danger_level_description(danger_info['score']),
            'country': country_name,
            'city': city_name if city_name else None,
            'recent_news': danger_info['recent_news']
        }), 200

    except Exception as e:
        logger.error(f"危険度チェックエラー: {str(e)}")
        return jsonify({'error': 'An error occurred', 'details': str(e)}), 500


@danger_bp.route('/travel_info', methods=['POST'])
def get_travel_info():
    """
    総合的な旅行情報を取得
    危険度、天気予報、ニュースをまとめて返す
    """
    try:
        data = request.json
        country_name = data.get('country', '').strip()
        city_name = data.get('city', '').strip()

        if not country_name:
            return jsonify({'error': 'Country name is required'}), 400

        # 危険度情報を取得
        danger_info = calculate_danger_level(country_name, city_name)

        # 天気予報を取得
        weather_data = None
        if city_name:
            weather_data = get_weather_forecast(city_name)

        return jsonify({
            'country': country_name,
            'city': city_name,
            'danger': {
                'is_dangerous': danger_info['is_dangerous'],
                'score': danger_info['score'],
                'base_score': danger_info['base_score'],
                'news_count': danger_info['news_count'],
                'danger_level': get_danger_level_description(danger_info['score'])
            },
            'weather': weather_data,
            'recent_news': danger_info['recent_news'][:3]  # 最新3件のみ
        }), 200

    except Exception as e:
        logger.error(f"旅行情報取得エラー: {str(e)}")
        return jsonify({'error': 'An error occurred', 'details': str(e)}), 500


@danger_bp.route('/check_danger_by_location', methods=['POST'])
def check_danger_by_location():
    """
    位置情報（緯度経度）から危険度をチェック
    1. 緯度経度から都市・国を特定
    2. その場所の危険度を計算して返す
    """
    try:
        data = request.json
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        # バリデーション
        if latitude is None or longitude is None:
            return jsonify({
                'error': 'Latitude and longitude are required',
                'details': 'Please provide both latitude and longitude'
            }), 400

        # 緯度経度の範囲チェック
        try:
            lat = float(latitude)
            lon = float(longitude)
            if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                raise ValueError("Invalid coordinates")
        except (ValueError, TypeError):
            return jsonify({
                'error': 'Invalid coordinates',
                'details': 'Latitude must be between -90 and 90, longitude between -180 and 180'
            }), 400

        logger.info(f"位置情報ベース危険度チェック: lat={lat}, lon={lon}")

        # 逆ジオコーディング: 緯度経度から都市・国を取得
        location_info = get_location_from_coordinates(lat, lon)

        if not location_info:
            return jsonify({
                'error': 'Could not determine location',
                'details': 'Unable to identify city/country from coordinates',
                'latitude': lat,
                'longitude': lon
            }), 404

        city_name = location_info.get('city', '')
        country_code = location_info.get('country_code', '')

        # 国名を取得（データベースから、または逆ジオコーディング結果から）
        country_name = location_info.get('country', '')

        # データベースで国名を検証・取得
        country = Country.query.filter_by(CODE=country_code).first()
        if country:
            country_name = country.NAME

        logger.info(f"特定された位置: {city_name}, {country_name} ({country_code})")

        # 危険度を計算
        danger_info = calculate_danger_level(country_name, city_name)

        # 天気情報も取得（オプション）
        weather_data = None
        if city_name:
            try:
                weather_data = get_weather_forecast(city_name)
            except Exception as weather_error:
                logger.warning(f"天気情報取得失敗: {str(weather_error)}")

        return jsonify({
            'location': {
                'city': city_name,
                'country': country_name,
                'country_code': country_code,
                'state': location_info.get('state', ''),
                'latitude': lat,
                'longitude': lon
            },
            'danger': {
                'is_dangerous': danger_info['is_dangerous'],
                'danger_score': danger_info['score'],
                'base_score': danger_info['base_score'],
                'news_count': danger_info['news_count'],
                'news_adjustment': danger_info['news_adjustment'],
                'danger_level': get_danger_level_description(danger_info['score']),
                'recent_news': danger_info['recent_news'][:5]  # 最新5件
            },
            'weather': weather_data[:3] if weather_data else None  # 3日分の天気
        }), 200

    except Exception as e:
        logger.error(f"位置情報ベース危険度チェックエラー: {str(e)}")
        return jsonify({
            'error': 'An error occurred',
            'details': str(e)
        }), 500
