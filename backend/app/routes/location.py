"""
国・都市関連のルート
"""
from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models import Country, City

location_bp = Blueprint('location', __name__)


@location_bp.route('/countries', methods=['GET'])
def get_countries():
    """全国リスト取得"""
    try:
        countries = Country.query.all()
        return jsonify([country.to_dict() for country in countries]), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch countries", "details": str(e)}), 500


@location_bp.route('/cities', methods=['GET'])
def get_cities_by_country():
    """国コードで都市リスト取得"""
    try:
        country_code = request.args.get('country_code')

        if not country_code:
            return jsonify({"error": "country_code parameter required"}), 400

        cities = City.query.filter_by(CountryCode=country_code).all()

        # 都市名のリストを返す
        city_names = [city.Name for city in cities]
        return jsonify(city_names), 200

    except Exception as e:
        return jsonify({"error": "Failed to fetch cities", "details": str(e)}), 500


@location_bp.route('/cities/<country_code>', methods=['GET'])
def get_city_by_country(country_code):
    """国コードで都市情報取得(詳細版)"""
    try:
        cities = City.query.filter_by(CountryCode=country_code).all()
        return jsonify([city.to_dict() for city in cities]), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch cities", "details": str(e)}), 500
