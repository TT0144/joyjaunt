from datetime import datetime, timedelta
from flask import Flask, Blueprint, jsonify, request
from flask_sqlalchemy import SQLAlchemy  # type: ignore
from flask_bcrypt import Bcrypt  # type: ignore
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token  # type: ignore
from flask_cors import CORS  # type: ignore
import requests
from sqlalchemy.exc import SQLAlchemyError
from flask_migrate import Migrate  # type: ignore
from dotenv import load_dotenv
import os
import logging

# .envファイルを読み込む
load_dotenv()

# ロギング設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
auth_bp = Blueprint('auth', __name__)

# 環境変数から設定を読み込む
app.config['JWT_SECRET_KEY'] = os.getenv(
    'JWT_SECRET_KEY', 'default_jwt_secret_key')
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 300  # アクセストークンの有効期限(5分)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 86400  # リフレッシュトークンの有効期限(24時間)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://dbuser:ecc@db:3306/Joy'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

# CORS設定を明示的に指定
CORS(app, resources={
     r"/*": {"origins": ["http://localhost:3001", "http://localhost:3000"]}},
     supports_credentials=True)

# API キーを環境変数から取得
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
TRAVEL_ADVISORY_API_KEY = os.getenv('TRAVEL_ADVISORY_API_KEY')
OPEN_WEATHER_API_KEY = os.getenv('OPEN_WEATHER_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# API URL定数
OPEN_WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/forecast"
NEWS_API_URL = "https://newsapi.org/v2/everything"


@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    try:
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user)
        print(request.headers.get('Authorization'))  # トークンをログに出力
        return jsonify(access_token=new_access_token), 200

    except Exception as e:
        return jsonify({"error": "Token refresh failed", "details": str(e)}), 401


OPEN_WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/forecast"
TRAVEL_ADVISORY_API_URL = "https://www.travel-advisory.info/api"

# Userモデル


class User(db.Model):
    __tablename__ = 'USER'
    USER_NO = db.Column(db.String(8), primary_key=True, nullable=False)
    EMAIL = db.Column(db.String(50), nullable=False, unique=True)
    PW = db.Column(db.String(255), nullable=False)
    COUNTRY_Code = db.Column(db.String(3), nullable=False)
    PASSPORTEXPIRY = db.Column(db.Date)
    LANGUAGE_NO = db.Column(db.String(10), nullable=False)

    # ユーザー番号生成メソッド
    @staticmethod
    def generate_user_no():
        count = db.session.query(db.func.count(User.USER_NO)).scalar()
        next_id = count + 1
        return f'U{next_id:07d}'  # U0000001 の形式で返す


class City(db.Model):
    __tablename__ = 'city'
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(35), nullable=False)
    CountryCode = db.Column(db.String(3), db.ForeignKey(
        'country.Code'), nullable=False)


class Country(db.Model):
    __tablename__ = 'country'
    Code = db.Column(db.String(3), primary_key=True)
    Name = db.Column(db.String(52), nullable=False)
    Continent = db.Column(db.Enum('Asia', 'Europe', 'North America',
                          'Africa', 'Oceania', 'Antarctica', 'South America'), nullable=False)


@app.route('/')
def home():
    return jsonify({"message": "Flask backend is running!"})


@app.route('/get_cities_by_country', methods=['GET'])
def get_cities_by_country():
    country_code = request.args.get('country_code')

    if not country_code:
        return jsonify({'error': 'Country code is required'}), 400

    cities = City.query.filter_by(CountryCode=country_code).all()
    city_names = [city.Name for city in cities]

    return jsonify(city_names)


@app.route('/get_city_by_country/<country_code>', methods=['GET'])
def get_city_by_country(country_code):
    cities = City.query.filter_by(CountryCode=country_code).all()
    city_data = [{'ID': city.ID, 'Name': city.Name} for city in cities]
    return jsonify(city_data)


@app.route('/countries', methods=['GET'])
def get_countries():
    countries = Country.query.all()
    return jsonify([{'code': c.Code, 'name': c.Name} for c in countries])


@app.route('/register', methods=['POST'])
def register():
    try:

        # JSONデータを取得
        data = request.get_json()

        # 必要な処理を実行
        email = data['email']
        password = data['password']
        country_code = data['country_code']
        passport_expiry = data['passport_expiry']

        data = request.json
        email = data.get('email')
        password = data.get('password')
        country_code = data.get('country_code')
        passport_expiry_str = data.get('passport_expiry')

        if not email or not password or not country_code or not passport_expiry_str:
            raise ValueError("Missing required fields")

        # 日付の変換
        if passport_expiry_str.endswith("Z"):
            passport_expiry_str = passport_expiry_str.replace("Z", "+00:00")

        # passport_expiryのパース
        passport_expiry = datetime.fromisoformat(passport_expiry_str)

        language_no = data.get('language_no', 'ja')  # デフォルトで日本語

        # パスワードをハッシュ化
        hashed_password = bcrypt.generate_password_hash(
            password).decode('utf-8')

        # ユーザー番号を生成
        user_no = User.generate_user_no()

        # 新しいユーザーを作成
        new_user = User(
            USER_NO=user_no,
            EMAIL=email,
            PW=hashed_password,
            COUNTRY_Code=country_code,
            PASSPORTEXPIRY=passport_expiry,
            LANGUAGE_NO=language_no
        )

        # データベースに保存
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "Registration successful"}), 200

    except SQLAlchemyError as e:
        db.session.rollback()  # エラー発生時にロールバック
        print(f"SQLAlchemy error: {str(e)}")  # エラーログ出力
        return jsonify({"error": "Database error", "details": str(e)}), 500
    except ValueError as e:
        return jsonify({"error": "Invalid data", "details": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        print(f"Unexpected error: {str(e)}")  # エラーログ出力
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500


# ログインエンドポイント


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # ユーザー情報をデータベースから取得
    user = User.query.filter_by(EMAIL=email).first()

    if user and bcrypt.check_password_hash(user.PW, password):
        # JWTトークンを作成
        access_token = create_access_token(identity=user.USER_NO)

        # パスポート有効期限をフォーマット (Noneの場合はそのまま返す)
        passport_expiry = user.PASSPORTEXPIRY.strftime(
            '%Y-%m-%d') if user.PASSPORTEXPIRY else None

        # レスポンスデータに必要な情報を含める
        return jsonify({
            "access_token": access_token,
            "passportExpiry": passport_expiry,
            "country": user.COUNTRY_Code
        }), 200
    else:
        return jsonify({"error": "Invalid email or password"}), 401


@app.route('/get_user_info', methods=['GET'])
@jwt_required()  # JWTトークンが必要
def get_user_info():
    # トークンから現在のユーザー番号を取得
    current_user_no = get_jwt_identity()

    # ユーザー情報をデータベースから取得
    user = User.query.filter_by(USER_NO=current_user_no).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    # ユーザーの国コードから都市情報を取得
    cities = City.query.filter_by(CountryCode=user.COUNTRY_Code).all()

    # 都市名をリストに変換
    city_names = [city.Name for city in cities]

    # パスポート有効期限をISO形式の文字列に変換
    passport_expiry = user.PASSPORTEXPIRY.isoformat() if user.PASSPORTEXPIRY else None

    # 必要な情報をレスポンスに含めて返す
    return jsonify({
        "email": user.EMAIL,
        "country_code": user.COUNTRY_Code,
        "passport_expiry": passport_expiry,
        "cities": city_names  # 都市名のリストを追加
    }), 200


def get_news_by_location(country_name, city_name=None):
    """
    指定された場所(国・都市)の危険に関するニュースを取得
    過去1週間以内のニュースを検索
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
            'apiKey': NEWS_API_KEY
        }

        logger.info(f"ニュース検索: {location_query}")
        response = requests.get(NEWS_API_URL, params=params, timeout=10)

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


def calculate_danger_level(country_name, city_name=None):
    """
    危険度を総合的に判定
    1. 静的な危険度スコア
    2. リアルタイムニュース情報
    を組み合わせて判定
    """
    # 基本スコアを取得
    base_score = get_travel_advisory_score(country_name, city_name)

    if base_score is None:
        base_score = 2.5  # デフォルト値

    # ニュース情報を取得
    news_articles = get_news_by_location(country_name, city_name)

    # ニュース件数に応じてスコアを調整
    news_count = len(news_articles)
    news_adjustment = min(news_count * 0.2, 1.0)  # 最大+1.0まで

    # 最終スコアを計算
    final_score = base_score + news_adjustment

    return {
        'score': round(final_score, 2),
        'base_score': base_score,
        'news_count': news_count,
        'news_adjustment': round(news_adjustment, 2),
        'is_dangerous': final_score >= 4.0,
        'recent_news': news_articles
    }

# 保護されたエンドポイントの例

# 旧バージョン(座標ベース)は削除 - Webアプリでは手動選択に統一


# 一時的な危険度スコアデータ
DANGER_SCORE = {
    "Afghanistan": {
        "score": 4.8,
        "cities": {"Kabul": 4.9, "Kandahar": 4.8, "Herat": 4.7, "Mazar-i-Sharif": 4.6}
    },
    "Albania": {
        "score": 2.7,
        "cities": {"Tirana": 2.8, "Durrës": 2.7, "Vlorë": 2.6}
    },
    "Algeria": {
        "score": 3.2,
        "cities": {"Algiers": 3.4, "Oran": 3.2, "Constantine": 3.1}
    },
    "Andorra": {
        "score": 1.2,
        "cities": {"Andorra la Vella": 1.2, "Escaldes-Engordany": 1.1}
    },
    "Angola": {
        "score": 3.7,
        "cities": {"Luanda": 3.9, "Huambo": 3.7, "Lobito": 3.6}
    },
    "Antigua and Barbuda": {
        "score": 2.1,
        "cities": {"Saint John's": 2.2, "All Saints": 2.0}
    },
    "Argentina": {
        "score": 3.0,
        "cities": {"Buenos Aires": 3.2, "Córdoba": 3.0, "Rosario": 3.1}
    },
    "Armenia": {
        "score": 2.5,
        "cities": {"Yerevan": 2.6, "Gyumri": 2.5, "Vanadzor": 2.4}
    },
    "Australia": {
        "score": 1.8,
        "cities": {"Sydney": 1.9, "Melbourne": 1.8, "Brisbane": 1.7, "Perth": 1.6}
    },
    "Austria": {
        "score": 1.5,
        "cities": {"Vienna": 1.7, "Graz": 1.5, "Linz": 1.4}
    },
    "Azerbaijan": {
        "score": 2.6,
        "cities": {"Baku": 2.7, "Ganja": 2.6, "Sumqayit": 2.5}
    },
    "Bahamas": {
        "score": 2.4,
        "cities": {"Nassau": 2.6, "Freeport": 2.3}
    },
    "Bahrain": {
        "score": 2.0,
        "cities": {"Manama": 2.1, "Riffa": 1.9}
    },
    "Bangladesh": {
        "score": 3.4,
        "cities": {"Dhaka": 3.6, "Chittagong": 3.4, "Khulna": 3.3}
    },
    "Barbados": {
        "score": 2.2,
        "cities": {"Bridgetown": 2.3, "Speightstown": 2.1}
    },
    "Belarus": {
        "score": 2.4,
        "cities": {"Minsk": 2.5, "Gomel": 2.4, "Mogilev": 2.3}
    },
    "Belgium": {
        "score": 2.0,
        "cities": {"Brussels": 2.3, "Antwerp": 2.0, "Ghent": 1.9}
    },
    "Belize": {
        "score": 3.1,
        "cities": {"Belize City": 3.3, "Belmopan": 3.0}
    },
    "Benin": {
        "score": 3.3,
        "cities": {"Porto-Novo": 3.4, "Cotonou": 3.3}
    },
    "Bhutan": {
        "score": 1.8,
        "cities": {"Thimphu": 1.9, "Phuntsholing": 1.8}
    },
    "Bolivia": {
        "score": 3.2,
        "cities": {"La Paz": 3.3, "Santa Cruz": 3.2, "Cochabamba": 3.1}
    },
    "Bosnia and Herzegovina": {
        "score": 2.5,
        "cities": {"Sarajevo": 2.6, "Banja Luka": 2.5}
    },
    "Botswana": {
        "score": 2.4,
        "cities": {"Gaborone": 2.5, "Francistown": 2.4}
    },
    "Brazil": {
        "score": 4.0,
        "cities": {"São Paulo": 4.2, "Rio de Janeiro": 4.5, "Salvador": 4.0}
    },
    "Brunei": {
        "score": 1.5,
        "cities": {"Bandar Seri Begawan": 1.6, "Kuala Belait": 1.5}
    },
    "Bulgaria": {
        "score": 2.4,
        "cities": {"Sofia": 2.5, "Plovdiv": 2.4, "Varna": 2.3}
    },
    "Burkina Faso": {
        "score": 3.6,
        "cities": {"Ouagadougou": 3.7, "Bobo-Dioulasso": 3.6}
    },
    "Burundi": {
        "score": 3.8,
        "cities": {"Bujumbura": 3.9, "Gitega": 3.8}
    },
    "Cambodia": {
        "score": 3.0,
        "cities": {"Phnom Penh": 3.2, "Siem Reap": 2.9}
    },
    "Cameroon": {
        "score": 3.5,
        "cities": {"Yaoundé": 3.6, "Douala": 3.5}
    },
    "Canada": {
        "score": 1.5,
        "cities": {"Toronto": 1.8, "Vancouver": 1.6, "Montreal": 1.9}
    },
    "Chad": {
        "score": 4.0,
        "cities": {"N'Djamena": 4.1, "Moundou": 4.0}
    },
    "Chile": {
        "score": 2.4,
        "cities": {"Santiago": 2.6, "Valparaíso": 2.4}
    },
    "China": {
        "score": 2.5,
        "cities": {"Beijing": 2.8, "Shanghai": 2.6, "Guangzhou": 2.7}
    },
    "Colombia": {
        "score": 3.8,
        "cities": {"Bogotá": 3.9, "Medellín": 3.8, "Cali": 3.7}
    },
    "Costa Rica": {
        "score": 2.5,
        "cities": {"San José": 2.7, "Alajuela": 2.4}
    },
    "Croatia": {
        "score": 1.8,
        "cities": {"Zagreb": 1.9, "Split": 1.8}
    },
    "Cuba": {
        "score": 2.7,
        "cities": {"Havana": 2.8, "Santiago de Cuba": 2.7}
    },
    "Cyprus": {
        "score": 1.7,
        "cities": {"Nicosia": 1.8, "Limassol": 1.7}
    },
    "Czech Republic": {
        "score": 1.7,
        "cities": {"Prague": 1.9, "Brno": 1.7}
    },
    "Denmark": {
        "score": 1.3,
        "cities": {"Copenhagen": 1.5, "Aarhus": 1.3}
    },
    "Dominican Republic": {
        "score": 3.3,
        "cities": {"Santo Domingo": 3.5, "Santiago": 3.2}
    },
    "Ecuador": {
        "score": 3.1,
        "cities": {"Quito": 3.2, "Guayaquil": 3.1}
    },
    "Egypt": {
        "score": 3.3,
        "cities": {"Cairo": 3.5, "Alexandria": 3.3}
    },
    "El Salvador": {
        "score": 3.9,
        "cities": {"San Salvador": 4.0, "Santa Ana": 3.8}
    },
    "Estonia": {
        "score": 1.6,
        "cities": {"Tallinn": 1.7, "Tartu": 1.6}
    },
    "Ethiopia": {
        "score": 3.5,
        "cities": {"Addis Ababa": 3.6, "Dire Dawa": 3.5}
    },
    "Fiji": {
        "score": 2.2,
        "cities": {"Suva": 2.3, "Lautoka": 2.2}
    },
    "Finland": {
        "score": 1.2,
        "cities": {"Helsinki": 1.3, "Espoo": 1.2}
    },
    "France": {
        "score": 2.4,
        "cities": {"Paris": 2.8, "Marseille": 2.6, "Lyon": 2.3}
    },
    "Germany": {
        "score": 2.0,
        "cities": {"Berlin": 2.4, "Hamburg": 2.2, "Munich": 1.9}
    },
    "Ghana": {
        "score": 3.0,
        "cities": {"Accra": 3.2, "Kumasi": 3.0}
    },
    "Greece": {
        "score": 2.2,
        "cities": {"Athens": 2.4, "Thessaloniki": 2.2}
    },
    "Hungary": {
        "score": 2.0,
        "cities": {"Budapest": 2.2, "Debrecen": 1.9}
    },
    "Iceland": {
        "score": 1.1,
        "cities": {"Reykjavík": 1.2, "Kópavogur": 1.1}
    },
    "India": {
        "score": 3.2,
        "cities": {"Mumbai": 3.5, "Delhi": 3.7, "Bangalore": 3.0}
    },
    "Indonesia": {
        "score": 3.0,
        "cities": {"Jakarta": 3.3, "Surabaya": 3.0}
    },
    "Iran": {
        "score": 3.5,
        "cities": {"Tehran": 3.7, "Isfahan": 3.4}
    },
    "Iraq": {
        "score": 4.5,
        "cities": {"Baghdad": 4.7, "Basra": 4.4}
    },
    "Ireland": {
        "score": 1.6,
        "cities": {"Dublin": 1.8, "Cork": 1.5}
    },
    "Israel": {
        "score": 2.8,
        "cities": {"Jerusalem": 3.0, "Tel Aviv": 2.7}
    },
    "Italy": {
        "score": 2.3,
        "cities": {"Rome": 2.5, "Milan": 2.3, "Naples": 2.4}
    },
    "Japan": {
        "score": 1.2,
        "cities": {"Tokyo": 2.0, "Osaka": 5.0, "Hirakata": 4.1, "Higashiosaka": 5.0, "Yokohama": 1.5}
    },
    "Jordan": {
        "score": 2.5,
        "cities": {"Amman": 2.6, "Zarqa": 2.5}
    },
    "Kazakhstan": {
        "score": 2.4,
        "cities": {"Almaty": 2.5, "Nur-Sultan": 2.4}
    },
    "Kenya": {
        "score": 3.5,
        "cities": {"Nairobi": 3.7, "Mombasa": 3.4}
    },
    "Kuwait": {
        "score": 1.8,
        "cities": {"Kuwait City": 1.9, "Jahrah": 1.8}
    },
    "Latvia": {
        "score": 2.0,
        "cities": {"Riga": 2.1, "Daugavpils": 2.0}
    },
    "Lebanon": {
        "score": 3.3,
        "cities": {"Beirut": 3.5, "Tripoli": 3.2}
    },
    "Libya": {
        "score": 4.2,
        "cities": {"Tripoli": 4.3, "Benghazi": 4.2}
    },
    "Malaysia": {
        "score": 2.4,
        "cities": {"Kuala Lumpur": 2.6, "George Town": 2.3}
    },
    "Mexico": {
        "score": 3.8,
        "cities": {"Mexico City": 4.0, "Guadalajara": 3.7}
    },
    "Mongolia": {
        "score": 2.5,
        "cities": {"Ulaanbaatar": 2.6, "Erdenet": 2.4}
    },
    "Morocco": {
        "score": 2.7,
        "cities": {"Casablanca": 2.9, "Rabat": 2.6}
    },
    "Nepal": {
        "score": 2.8,
        "cities": {"Kathmandu": 3.0, "Pokhara": 2.7}
    },
    "Netherlands": {
        "score": 1.7,
        "cities": {"Amsterdam": 1.9, "Rotterdam": 1.7}
    },
    "New Zealand": {
        "score": 1.4,
        "cities": {"Auckland": 1.5, "Wellington": 1.4}
    },
    "Nigeria": {
        "score": 4.0,
        "cities": {"Lagos": 4.2, "Kano": 4.0}
    },
    "Norway": {
        "score": 1.2,
        "cities": {"Oslo": 1.3, "Bergen": 1.2, "Trondheim": 1.1}
    },
    "Oman": {
        "score": 1.7,
        "cities": {"Muscat": 1.8, "Salalah": 1.7}
    },
    "Pakistan": {
        "score": 4.0,
        "cities": {"Karachi": 4.2, "Lahore": 4.0, "Islamabad": 3.8}
    },
    "Panama": {
        "score": 2.8,
        "cities": {"Panama City": 3.0, "Colón": 2.8}
    },
    "Papua New Guinea": {
        "score": 3.5,
        "cities": {"Port Moresby": 3.7, "Lae": 3.4}
    },
    "Paraguay": {
        "score": 2.9,
        "cities": {"Asunción": 3.0, "Ciudad del Este": 2.9}
    },
    "Peru": {
        "score": 3.2,
        "cities": {"Lima": 3.4, "Arequipa": 3.1, "Trujillo": 3.2}
    },
    "Philippines": {
        "score": 3.3,
        "cities": {"Manila": 3.5, "Cebu": 3.2, "Davao": 3.3}
    },
    "Poland": {
        "score": 2.0,
        "cities": {"Warsaw": 2.2, "Kraków": 1.9, "Łódź": 2.0}
    },
    "Portugal": {
        "score": 1.8,
        "cities": {"Lisbon": 2.0, "Porto": 1.8}
    },
    "Qatar": {
        "score": 1.5,
        "cities": {"Doha": 1.6, "Al Wakrah": 1.5}
    },
    "Romania": {
        "score": 2.3,
        "cities": {"Bucharest": 2.5, "Cluj-Napoca": 2.2}
    },
    "Russia": {
        "score": 2.9,
        "cities": {"Moscow": 3.2, "Saint Petersburg": 3.0, "Novosibirsk": 2.8}
    },
    "Saudi Arabia": {
        "score": 2.2,
        "cities": {"Riyadh": 2.3, "Jeddah": 2.2, "Mecca": 2.1}
    },
    "Senegal": {
        "score": 3.0,
        "cities": {"Dakar": 3.1, "Touba": 3.0}
    },
    "Serbia": {
        "score": 2.4,
        "cities": {"Belgrade": 2.5, "Novi Sad": 2.3}
    },
    "Singapore": {
        "score": 1.2,
        "cities": {"Singapore": 1.2}
    },
    "Slovakia": {
        "score": 1.9,
        "cities": {"Bratislava": 2.0, "Košice": 1.9}
    },
    "Slovenia": {
        "score": 1.5,
        "cities": {"Ljubljana": 1.6, "Maribor": 1.5}
    },
    "Somalia": {
        "score": 4.8,
        "cities": {"Mogadishu": 4.9, "Hargeisa": 4.7}
    },
    "South Africa": {
        "score": 4.1,
        "cities": {"Johannesburg": 4.3, "Cape Town": 4.0, "Durban": 4.1}
    },
    "South Korea": {
        "score": 1.7,
        "cities": {"Seoul": 1.8, "Busan": 1.7, "Incheon": 1.7}
    },
    "Spain": {
        "score": 2.1,
        "cities": {"Madrid": 2.3, "Barcelona": 2.2, "Valencia": 2.0}
    },
    "Sri Lanka": {
        "score": 2.6,
        "cities": {"Colombo": 2.7, "Kandy": 2.5}
    },
    "Sudan": {
        "score": 4.3,
        "cities": {"Khartoum": 4.4, "Omdurman": 4.3}
    },
    "Sweden": {
        "score": 1.6,
        "cities": {"Stockholm": 1.7, "Gothenburg": 1.6, "Malmö": 1.8}
    },
    "Switzerland": {
        "score": 1.2,
        "cities": {"Zürich": 1.3, "Geneva": 1.2, "Basel": 1.2}
    },
    "Syria": {
        "score": 4.7,
        "cities": {"Damascus": 4.8, "Aleppo": 4.7}
    },
    "Taiwan": {
        "score": 1.8,
        "cities": {"Taipei": 1.9, "Kaohsiung": 1.8, "Taichung": 1.7}
    },
    "Tanzania": {
        "score": 3.2,
        "cities": {"Dar es Salaam": 3.4, "Dodoma": 3.1}
    },
    "Thailand": {
        "score": 2.5,
        "cities": {"Bangkok": 2.7, "Nonthaburi": 2.4, "Phuket": 2.3}
    },
    "Tunisia": {
        "score": 2.8,
        "cities": {"Tunis": 2.9, "Sfax": 2.7}
    },
    "Turkey": {
        "score": 2.7,
        "cities": {"Istanbul": 2.9, "Ankara": 2.6, "Izmir": 2.7}
    },
    "Uganda": {
        "score": 3.4,
        "cities": {"Kampala": 3.5, "Gulu": 3.3}
    },
    "Ukraine": {
        "score": 3.8,
        "cities": {"Kyiv": 3.9, "Kharkiv": 3.8, "Odesa": 3.7}
    },
    "United Arab Emirates": {
        "score": 1.6,
        "cities": {"Dubai": 1.7, "Abu Dhabi": 1.5, "Sharjah": 1.6}
    },
    "United Kingdom": {
        "score": 2.3,
        "cities": {"London": 2.8, "Manchester": 2.5, "Birmingham": 2.4}
    },
    "United States": {
        "score": 2.8,
        "cities": {"New York": 3.5, "Los Angeles": 3.0, "Chicago": 3.2}
    },
    "Uruguay": {
        "score": 2.4,
        "cities": {"Montevideo": 2.5, "Salto": 2.3}
    },
    "Uzbekistan": {
        "score": 2.6,
        "cities": {"Tashkent": 2.7, "Namangan": 2.6}
    },
    "Venezuela": {
        "score": 4.2,
        "cities": {"Caracas": 4.4, "Maracaibo": 4.1, "Valencia": 4.2}
    },
    "Vietnam": {
        "score": 2.4,
        "cities": {"Hanoi": 2.5, "Ho Chi Minh City": 2.4, "Da Nang": 2.3}
    },
    "Yemen": {
        "score": 4.6,
        "cities": {"Sanaa": 4.7, "Aden": 4.6}
    },
    "Zambia": {
        "score": 3.1,
        "cities": {"Lusaka": 3.2, "Kitwe": 3.0}
    },
    "Zimbabwe": {
        "score": 3.3,
        "cities": {"Harare": 3.4, "Bulawayo": 3.3}
    }
}


def get_travel_advisory_score(country_name, city_name=None):
    """
    国名と都市名から危険度スコアを取得する
    """
    country_data = DANGER_SCORE.get(country_name)

    if not country_data:
        return None

    # 都市データが存在する場合は都市のスコアを返す
    if city_name and "cities" in country_data and city_name in country_data["cities"]:
        return country_data["cities"][city_name]

    # 都市データがない場合は国のスコアを返す
    return country_data["score"]


@app.route('/check_realtime_danger', methods=['POST'])
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
            'country': country_name,
            'city': city_name if city_name else None,
            'recent_news': danger_info['recent_news']
        }), 200

    except Exception as e:
        logger.error(f"危険度チェックエラー: {str(e)}")
        return jsonify({'error': 'An error occurred', 'details': str(e)}), 500


@app.route('/get_location_news', methods=['POST'])
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


def get_weather_forecast(city_name):
    """OpenWeather APIを使って天気予報を取得"""
    try:
        params = {
            "q": city_name,
            "appid": OPEN_WEATHER_API_KEY,
            "units": "metric",
            "lang": "ja",
            "cnt": 40  # 最大40件(5日分、3時間ごとのデータ)
        }
        response = requests.get(OPEN_WEATHER_API_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            # 12:00のデータだけを抽出して日ごとの天気を整理
            forecast_data = []
            for item in data["list"]:
                if "12:00:00" in item["dt_txt"]:  # 12:00のデータを取得
                    weather_icon = item["weather"][0]["icon"]
                    icon_url = f"http://openweathermap.org/img/wn/{weather_icon}@2x.png"
                    # 日付をフォーマット
                    date_formatted = datetime.strptime(
                        item["dt_txt"], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
                    forecast_data.append({
                        "date": date_formatted,
                        "temperature": item["main"]["temp"],
                        "weather": item["weather"][0]["description"],
                        "wind_speed": item["wind"]["speed"],
                        "icon_url": icon_url
                    })
            return forecast_data
        else:
            return None
    except requests.exceptions.RequestException as e:
        print("Error fetching weather forecast:", e)
        return None


@app.route('/weather_forecast', methods=['POST'])
def weather_forecast():
    """指定された都市の天気予報を取得"""
    try:
        data = request.json
        city = data.get('city')
        if not city:
            return jsonify({"error": "City name is required"}), 400

        forecast_data = get_weather_forecast(city)
        if not forecast_data:
            return jsonify({"error": "Could not fetch weather forecast"}), 500

        return jsonify({"forecast": forecast_data}), 200
    except Exception as e:
        return jsonify({"error": "An error occurred", "details": str(e)}), 500


@app.route('/weather_forecast_for_user', methods=['GET'])
def weather_forecast_for_user():
    """ユーザーの国に基づいた天気予報を取得"""
    try:
        # ユーザー番号を取得
        user_no = request.args.get('user_no')
        if not user_no:
            return jsonify({"error": "User number is required"}), 400

        # データベースからユーザー情報を取得
        user = User.query.filter_by(USER_NO=user_no).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        # 国名を取得
        country = Country.query.filter_by(Code=user.COUNTRY_Code).first()
        if not country:
            return jsonify({"error": "Country not found"}), 404

        # 天気予報を取得
        forecast_data = get_weather_forecast(country.Name)
        if not forecast_data:
            return jsonify({"error": "Could not fetch weather forecast"}), 500

        return jsonify({"forecast": forecast_data}), 200
    except Exception as e:
        return jsonify({"error": "An error occurred", "details": str(e)}), 500


@app.route('/weather_forecast_for_travel_plan', methods=['GET'])
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


@app.route('/travel_info', methods=['POST'])
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
                'news_count': danger_info['news_count']
            },
            'weather': weather_data,
            'recent_news': danger_info['recent_news'][:3]  # 最新3件のみ
        }), 200

    except Exception as e:
        logger.error(f"旅行情報取得エラー: {str(e)}")
        return jsonify({'error': 'An error occurred', 'details': str(e)}), 500


@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    """保護されたエンドポイント例"""
    current_user = get_jwt_identity()
    return jsonify({
        "message": "Access granted to protected route",
        "user": current_user
    }), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
