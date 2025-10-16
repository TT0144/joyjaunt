"""
ニュース取得ルート
"""
from flask import Blueprint, request, jsonify
from app.services.news_service import get_news_by_location, get_general_news
import logging

logger = logging.getLogger(__name__)
news_bp = Blueprint('news', __name__)


@news_bp.route('/location_news', methods=['POST'])
def get_location_news():
    """
    指定された場所の最新ニュースを取得
    """
    try:
        data = request.json
        country_name = data.get('country', '').strip()
        city_name = data.get('city', '').strip()

        if not country_name:
            return jsonify({'error': 'Country name is required'}), 400

        news_articles = get_news_by_location(country_name, city_name)

        return jsonify({
            'country': country_name,
            'city': city_name,
            'news_count': len(news_articles),
            'articles': news_articles
        }), 200

    except Exception as e:
        logger.error(f"ニュース取得エラー: {str(e)}")
        return jsonify({'error': 'An error occurred', 'details': str(e)}), 500


@news_bp.route('/general_news', methods=['POST'])
def get_general_location_news():
    """
    指定された場所の一般ニュースを取得
    """
    try:
        data = request.json
        country_name = data.get('country', '').strip()
        city_name = data.get('city', '').strip()
        days = data.get('days', 7)

        if not country_name:
            return jsonify({'error': 'Country name is required'}), 400

        news_articles = get_general_news(country_name, city_name, days)

        return jsonify({
            'country': country_name,
            'city': city_name,
            'news_count': len(news_articles),
            'articles': news_articles
        }), 200

    except Exception as e:
        logger.error(f"一般ニュース取得エラー: {str(e)}")
        return jsonify({'error': 'An error occurred', 'details': str(e)}), 500
