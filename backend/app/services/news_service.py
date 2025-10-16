"""
ニュース取得サービス
"""
import requests
from datetime import datetime, timedelta
from flask import current_app
import logging

logger = logging.getLogger(__name__)


def get_news_by_location(country_name, city_name=None):
    """
    指定された場所(国・都市)の危険に関するニュースを取得
    過去1週間以内のニュースを検索

    Args:
        country_name: 国名
        city_name: 都市名(オプション)

    Returns:
        list: ニュース記事のリスト
    """
    try:
        today = datetime.now()
        one_week_ago = today - timedelta(days=7)
        from_date = one_week_ago.strftime('%Y-%m-%d')

        # 検索キーワード: 犯罪、テロ、危険関連
        keywords = 'crime OR terrorism OR violence OR attack OR murder OR assault'

        # 都市が指定されている場合は都市名を含める
        location_query = f'"{city_name}" AND "{country_name}"' if city_name else f'"{country_name}"'

        # NewsAPIのパラメータ
        params = {
            'q': f'({keywords}) AND {location_query}',
            'from': from_date,
            'sortBy': 'publishedAt',
            'language': 'en',
            'pageSize': 10,
            'apiKey': current_app.config['NEWS_API_KEY']
        }

        logger.info(f"ニュース検索: {location_query}")
        response = requests.get(
            current_app.config['NEWS_API_URL'],
            params=params,
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])

            # 記事を整形して返す
            formatted_articles = []
            for article in articles[:5]:  # 最大5件
                formatted_articles.append({
                    'title': article.get('title', ''),
                    'description': article.get('description', ''),
                    'url': article.get('url', ''),
                    'publishedAt': article.get('publishedAt', ''),
                    'source': article.get('source', {}).get('name', '')
                })

            return formatted_articles
        else:
            logger.warning(f"NewsAPI エラー: {response.status_code}")
            return []

    except requests.exceptions.RequestException as e:
        logger.error(f"ニュース取得エラー: {str(e)}")
        return []
    except Exception as e:
        logger.error(f"予期しないエラー: {str(e)}")
        return []


def get_general_news(country_name, city_name=None, days=7):
    """
    一般的なニュースを取得(危険関連以外も含む)

    Args:
        country_name: 国名
        city_name: 都市名(オプション)
        days: 過去何日分のニュースを取得するか

    Returns:
        list: ニュース記事のリスト
    """
    try:
        today = datetime.now()
        from_date = (today - timedelta(days=days)).strftime('%Y-%m-%d')

        # 都市が指定されている場合は都市名を含める
        location_query = f'"{city_name}" AND "{country_name}"' if city_name else f'"{country_name}"'

        params = {
            'q': location_query,
            'from': from_date,
            'sortBy': 'publishedAt',
            'language': 'en',
            'pageSize': 10,
            'apiKey': current_app.config['NEWS_API_KEY']
        }

        logger.info(f"一般ニュース検索: {location_query}")
        response = requests.get(
            current_app.config['NEWS_API_URL'],
            params=params,
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])

            formatted_articles = []
            for article in articles[:10]:
                formatted_articles.append({
                    'title': article.get('title', ''),
                    'description': article.get('description', ''),
                    'url': article.get('url', ''),
                    'publishedAt': article.get('publishedAt', ''),
                    'source': article.get('source', {}).get('name', ''),
                    'urlToImage': article.get('urlToImage', '')
                })

            return formatted_articles
        else:
            logger.warning(f"NewsAPI エラー: {response.status_code}")
            return []

    except Exception as e:
        logger.error(f"一般ニュース取得エラー: {str(e)}")
        return []
