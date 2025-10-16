"""
位置情報サービス - 緯度経度から都市・国を特定
"""
import requests
from flask import current_app
import logging

logger = logging.getLogger(__name__)


def get_location_from_coordinates(latitude, longitude):
    """
    緯度経度から都市・国情報を取得（逆ジオコーディング）
    OpenWeather Geocoding APIを使用

    Args:
        latitude: 緯度
        longitude: 経度

    Returns:
        dict: {
            'city': 都市名,
            'country': 国名,
            'country_code': 国コード,
            'state': 州/地方名（オプション）
        }
    """
    try:
        api_key = current_app.config['OPEN_WEATHER_API_KEY']
        base_url = "http://api.openweathermap.org/geo/1.0/reverse"

        params = {
            'lat': latitude,
            'lon': longitude,
            'limit': 1,
            'appid': api_key
        }

        logger.info(f"逆ジオコーディング: lat={latitude}, lon={longitude}")
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        if not data or len(data) == 0:
            logger.warning("位置情報が見つかりませんでした")
            return None

        location = data[0]

        result = {
            'city': location.get('name', ''),
            'country': location.get('country', ''),
            'country_code': location.get('country', ''),
            'state': location.get('state', ''),
            'latitude': latitude,
            'longitude': longitude
        }

        logger.info(f"位置特定成功: {result['city']}, {result['country']}")
        return result

    except requests.exceptions.RequestException as e:
        logger.error(f"逆ジオコーディングエラー: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"位置情報取得エラー: {str(e)}")
        return None


def get_country_name_from_code(country_code):
    """
    国コードから国名を取得（データベースから）

    Args:
        country_code: ISO 3166-1 alpha-2 国コード (例: 'JP', 'US')

    Returns:
        str: 国名、見つからない場合はNone
    """
    from app.models import Country

    try:
        # 2文字コードを3文字コードに変換するマッピング（必要に応じて）
        # データベースが3文字コードを使用している場合
        country = Country.query.filter_by(CODE=country_code).first()

        if country:
            return country.NAME

        return None

    except Exception as e:
        logger.error(f"国名取得エラー: {str(e)}")
        return None


# 主要都市の緯度経度マッピング（フォールバック用）
MAJOR_CITIES = {
    'Tokyo': {'lat': 35.6762, 'lon': 139.6503, 'country': 'Japan'},
    'New York': {'lat': 40.7128, 'lon': -74.0060, 'country': 'United States'},
    'London': {'lat': 51.5074, 'lon': -0.1278, 'country': 'United Kingdom'},
    'Paris': {'lat': 48.8566, 'lon': 2.3522, 'country': 'France'},
    'Sydney': {'lat': -33.8688, 'lon': 151.2093, 'country': 'Australia'},
}


def find_nearest_city(latitude, longitude, max_distance_km=50):
    """
    緯度経度から最も近い主要都市を検索

    Args:
        latitude: 緯度
        longitude: 経度
        max_distance_km: 最大検索距離（km）

    Returns:
        str: 都市名、見つからない場合はNone
    """
    import math

    def calculate_distance(lat1, lon1, lat2, lon2):
        """2点間の距離を計算（Haversine formula）"""
        R = 6371  # 地球の半径（km）

        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)

        a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * \
            math.cos(lat2_rad) * math.sin(delta_lon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

        return R * c

    nearest_city = None
    min_distance = float('inf')

    for city_name, coords in MAJOR_CITIES.items():
        distance = calculate_distance(
            latitude, longitude,
            coords['lat'], coords['lon']
        )

        if distance < min_distance and distance <= max_distance_km:
            min_distance = distance
            nearest_city = city_name

    if nearest_city:
        logger.info(f"最寄り都市: {nearest_city} (距離: {min_distance:.2f}km)")

    return nearest_city
