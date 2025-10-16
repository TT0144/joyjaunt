"""
危険度評価サービス
"""
from app.services.news_service import get_news_by_location
import logging

logger = logging.getLogger(__name__)

# 一時的な危険度スコアデータ
DANGER_SCORE = {
    "Afghanistan": {"score": 4.8, "cities": {"Kabul": 4.9, "Kandahar": 4.8, "Herat": 4.7, "Mazar-i-Sharif": 4.6}},
    "Albania": {"score": 2.7, "cities": {"Tirana": 2.8, "Durrës": 2.7, "Vlorë": 2.6}},
    "Algeria": {"score": 3.2, "cities": {"Algiers": 3.4, "Oran": 3.2, "Constantine": 3.1}},
    "Andorra": {"score": 1.2, "cities": {"Andorra la Vella": 1.2, "Escaldes-Engordany": 1.1}},
    "Angola": {"score": 3.7, "cities": {"Luanda": 3.9, "Huambo": 3.7, "Lobito": 3.6}},
    "Antigua and Barbuda": {"score": 2.1, "cities": {"Saint John's": 2.2, "All Saints": 2.0}},
    "Argentina": {"score": 3.0, "cities": {"Buenos Aires": 3.2, "Córdoba": 3.0, "Rosario": 3.1}},
    "Armenia": {"score": 2.5, "cities": {"Yerevan": 2.6, "Gyumri": 2.5, "Vanadzor": 2.4}},
    "Australia": {"score": 1.8, "cities": {"Sydney": 1.9, "Melbourne": 1.8, "Brisbane": 1.7, "Perth": 1.6}},
    "Austria": {"score": 1.5, "cities": {"Vienna": 1.7, "Graz": 1.5, "Linz": 1.4}},
    "Azerbaijan": {"score": 2.6, "cities": {"Baku": 2.7, "Ganja": 2.6, "Sumqayit": 2.5}},
    "Bahamas": {"score": 2.4, "cities": {"Nassau": 2.6, "Freeport": 2.3}},
    "Bahrain": {"score": 2.0, "cities": {"Manama": 2.1, "Riffa": 1.9}},
    "Bangladesh": {"score": 3.4, "cities": {"Dhaka": 3.6, "Chittagong": 3.4, "Khulna": 3.3}},
    "Barbados": {"score": 2.2, "cities": {"Bridgetown": 2.3, "Speightstown": 2.1}},
    "Belarus": {"score": 2.4, "cities": {"Minsk": 2.5, "Gomel": 2.4, "Mogilev": 2.3}},
    "Belgium": {"score": 2.0, "cities": {"Brussels": 2.3, "Antwerp": 2.0, "Ghent": 1.9}},
    "Belize": {"score": 3.1, "cities": {"Belize City": 3.3, "Belmopan": 3.0}},
    "Benin": {"score": 3.3, "cities": {"Porto-Novo": 3.4, "Cotonou": 3.3}},
    "Bhutan": {"score": 1.8, "cities": {"Thimphu": 1.9, "Phuntsholing": 1.8}},
    "Bolivia": {"score": 3.2, "cities": {"La Paz": 3.3, "Santa Cruz": 3.2, "Cochabamba": 3.1}},
    "Bosnia and Herzegovina": {"score": 2.5, "cities": {"Sarajevo": 2.6, "Banja Luka": 2.5}},
    "Botswana": {"score": 2.4, "cities": {"Gaborone": 2.5, "Francistown": 2.4}},
    "Brazil": {"score": 4.0, "cities": {"São Paulo": 4.2, "Rio de Janeiro": 4.5, "Salvador": 4.0}},
    "Brunei": {"score": 1.5, "cities": {"Bandar Seri Begawan": 1.6, "Kuala Belait": 1.5}},
    "Bulgaria": {"score": 2.4, "cities": {"Sofia": 2.5, "Plovdiv": 2.4, "Varna": 2.3}},
    "Burkina Faso": {"score": 3.6, "cities": {"Ouagadougou": 3.7, "Bobo-Dioulasso": 3.6}},
    "Burundi": {"score": 3.8, "cities": {"Bujumbura": 3.9, "Gitega": 3.8}},
    "Cambodia": {"score": 3.0, "cities": {"Phnom Penh": 3.2, "Siem Reap": 2.9}},
    "Cameroon": {"score": 3.5, "cities": {"Yaoundé": 3.6, "Douala": 3.5}},
    "Canada": {"score": 1.5, "cities": {"Toronto": 1.8, "Vancouver": 1.6, "Montreal": 1.9}},
    "Chad": {"score": 4.0, "cities": {"N'Djamena": 4.1, "Moundou": 4.0}},
    "Chile": {"score": 2.4, "cities": {"Santiago": 2.6, "Valparaíso": 2.4}},
    "China": {"score": 2.5, "cities": {"Beijing": 2.8, "Shanghai": 2.6, "Guangzhou": 2.7}},
    "Colombia": {"score": 3.8, "cities": {"Bogotá": 3.9, "Medellín": 3.8, "Cali": 3.7}},
    "Costa Rica": {"score": 2.5, "cities": {"San José": 2.7, "Alajuela": 2.4}},
    "Croatia": {"score": 1.8, "cities": {"Zagreb": 1.9, "Split": 1.8}},
    "Cuba": {"score": 2.7, "cities": {"Havana": 2.8, "Santiago de Cuba": 2.7}},
    "Cyprus": {"score": 1.7, "cities": {"Nicosia": 1.8, "Limassol": 1.7}},
    "Czech Republic": {"score": 1.7, "cities": {"Prague": 1.9, "Brno": 1.7}},
    "Denmark": {"score": 1.3, "cities": {"Copenhagen": 1.5, "Aarhus": 1.3}},
    "Dominican Republic": {"score": 3.3, "cities": {"Santo Domingo": 3.5, "Santiago": 3.2}},
    "Ecuador": {"score": 3.1, "cities": {"Quito": 3.2, "Guayaquil": 3.1}},
    "Egypt": {"score": 3.3, "cities": {"Cairo": 3.5, "Alexandria": 3.3}},
    "El Salvador": {"score": 3.9, "cities": {"San Salvador": 4.0, "Santa Ana": 3.8}},
    "Estonia": {"score": 1.6, "cities": {"Tallinn": 1.7, "Tartu": 1.6}},
    "Ethiopia": {"score": 3.5, "cities": {"Addis Ababa": 3.6, "Dire Dawa": 3.5}},
    "Fiji": {"score": 2.2, "cities": {"Suva": 2.3, "Lautoka": 2.2}},
    "Finland": {"score": 1.2, "cities": {"Helsinki": 1.3, "Espoo": 1.2}},
    "France": {"score": 2.4, "cities": {"Paris": 2.8, "Marseille": 2.6, "Lyon": 2.3}},
    "Germany": {"score": 2.0, "cities": {"Berlin": 2.4, "Hamburg": 2.2, "Munich": 1.9}},
    "Ghana": {"score": 3.0, "cities": {"Accra": 3.2, "Kumasi": 3.0}},
    "Greece": {"score": 2.2, "cities": {"Athens": 2.4, "Thessaloniki": 2.2}},
    "Hungary": {"score": 2.0, "cities": {"Budapest": 2.2, "Debrecen": 1.9}},
    "Iceland": {"score": 1.1, "cities": {"Reykjavík": 1.2, "Kópavogur": 1.1}},
    "India": {"score": 3.2, "cities": {"Mumbai": 3.5, "Delhi": 3.7, "Bangalore": 3.0}},
    "Indonesia": {"score": 3.0, "cities": {"Jakarta": 3.3, "Surabaya": 3.0}},
    "Iran": {"score": 3.5, "cities": {"Tehran": 3.7, "Isfahan": 3.4}},
    "Iraq": {"score": 4.5, "cities": {"Baghdad": 4.7, "Basra": 4.4}},
    "Ireland": {"score": 1.6, "cities": {"Dublin": 1.8, "Cork": 1.5}},
    "Israel": {"score": 2.8, "cities": {"Jerusalem": 3.0, "Tel Aviv": 2.7}},
    "Italy": {"score": 2.3, "cities": {"Rome": 2.5, "Milan": 2.3, "Naples": 2.4}},
    "Japan": {"score": 1.2, "cities": {"Tokyo": 2.0, "Osaka": 5.0, "Hirakata": 4.1, "Higashiosaka": 5.0, "Yokohama": 1.5}},
    "Jordan": {"score": 2.5, "cities": {"Amman": 2.6, "Zarqa": 2.5}},
    "Kazakhstan": {"score": 2.4, "cities": {"Almaty": 2.5, "Nur-Sultan": 2.4}},
    "Kenya": {"score": 3.5, "cities": {"Nairobi": 3.7, "Mombasa": 3.4}},
    "Kuwait": {"score": 1.8, "cities": {"Kuwait City": 1.9, "Jahrah": 1.8}},
    "Latvia": {"score": 2.0, "cities": {"Riga": 2.1, "Daugavpils": 2.0}},
    "Lebanon": {"score": 3.3, "cities": {"Beirut": 3.5, "Tripoli": 3.2}},
    "Libya": {"score": 4.2, "cities": {"Tripoli": 4.3, "Benghazi": 4.2}},
    "Malaysia": {"score": 2.4, "cities": {"Kuala Lumpur": 2.6, "George Town": 2.3}},
    "Mexico": {"score": 3.8, "cities": {"Mexico City": 4.0, "Guadalajara": 3.7}},
    "Mongolia": {"score": 2.5, "cities": {"Ulaanbaatar": 2.6, "Erdenet": 2.4}},
    "Morocco": {"score": 2.7, "cities": {"Casablanca": 2.9, "Rabat": 2.6}},
    "Nepal": {"score": 2.8, "cities": {"Kathmandu": 3.0, "Pokhara": 2.7}},
    "Netherlands": {"score": 1.7, "cities": {"Amsterdam": 1.9, "Rotterdam": 1.7}},
    "New Zealand": {"score": 1.4, "cities": {"Auckland": 1.5, "Wellington": 1.4}},
    "Nigeria": {"score": 4.0, "cities": {"Lagos": 4.2, "Kano": 4.0}},
    "Norway": {"score": 1.2, "cities": {"Oslo": 1.3, "Bergen": 1.2, "Trondheim": 1.1}},
    "Oman": {"score": 1.7, "cities": {"Muscat": 1.8, "Salalah": 1.7}},
    "Pakistan": {"score": 4.0, "cities": {"Karachi": 4.2, "Lahore": 4.0, "Islamabad": 3.8}},
    "Panama": {"score": 2.8, "cities": {"Panama City": 3.0, "Colón": 2.8}},
    "Papua New Guinea": {"score": 3.5, "cities": {"Port Moresby": 3.7, "Lae": 3.4}},
    "Paraguay": {"score": 2.9, "cities": {"Asunción": 3.0, "Ciudad del Este": 2.9}},
    "Peru": {"score": 3.2, "cities": {"Lima": 3.4, "Arequipa": 3.1, "Trujillo": 3.2}},
    "Philippines": {"score": 3.3, "cities": {"Manila": 3.5, "Cebu": 3.2, "Davao": 3.3}},
    "Poland": {"score": 2.0, "cities": {"Warsaw": 2.2, "Kraków": 1.9, "Łódź": 2.0}},
    "Portugal": {"score": 1.8, "cities": {"Lisbon": 2.0, "Porto": 1.8}},
    "Qatar": {"score": 1.5, "cities": {"Doha": 1.6, "Al Wakrah": 1.5}},
    "Romania": {"score": 2.3, "cities": {"Bucharest": 2.5, "Cluj-Napoca": 2.2}},
    "Russia": {"score": 2.9, "cities": {"Moscow": 3.2, "Saint Petersburg": 3.0, "Novosibirsk": 2.8}},
    "Saudi Arabia": {"score": 2.2, "cities": {"Riyadh": 2.3, "Jeddah": 2.2, "Mecca": 2.1}},
    "Senegal": {"score": 3.0, "cities": {"Dakar": 3.1, "Touba": 3.0}},
    "Serbia": {"score": 2.4, "cities": {"Belgrade": 2.5, "Novi Sad": 2.3}},
    "Singapore": {"score": 1.2, "cities": {"Singapore": 1.2}},
    "Slovakia": {"score": 1.9, "cities": {"Bratislava": 2.0, "Košice": 1.9}},
    "Slovenia": {"score": 1.5, "cities": {"Ljubljana": 1.6, "Maribor": 1.5}},
    "Somalia": {"score": 4.8, "cities": {"Mogadishu": 4.9, "Hargeisa": 4.7}},
    "South Africa": {"score": 4.1, "cities": {"Johannesburg": 4.3, "Cape Town": 4.0, "Durban": 4.1}},
    "South Korea": {"score": 1.7, "cities": {"Seoul": 1.8, "Busan": 1.7, "Incheon": 1.7}},
    "Spain": {"score": 2.1, "cities": {"Madrid": 2.3, "Barcelona": 2.2, "Valencia": 2.0}},
    "Sri Lanka": {"score": 2.6, "cities": {"Colombo": 2.7, "Kandy": 2.5}},
    "Sudan": {"score": 4.3, "cities": {"Khartoum": 4.4, "Omdurman": 4.3}},
    "Sweden": {"score": 1.6, "cities": {"Stockholm": 1.7, "Gothenburg": 1.6, "Malmö": 1.8}},
    "Switzerland": {"score": 1.2, "cities": {"Zürich": 1.3, "Geneva": 1.2, "Basel": 1.2}},
    "Syria": {"score": 4.7, "cities": {"Damascus": 4.8, "Aleppo": 4.7}},
    "Taiwan": {"score": 1.8, "cities": {"Taipei": 1.9, "Kaohsiung": 1.8, "Taichung": 1.7}},
    "Tanzania": {"score": 3.2, "cities": {"Dar es Salaam": 3.4, "Dodoma": 3.1}},
    "Thailand": {"score": 2.5, "cities": {"Bangkok": 2.7, "Nonthaburi": 2.4, "Phuket": 2.3}},
    "Tunisia": {"score": 2.8, "cities": {"Tunis": 2.9, "Sfax": 2.7}},
    "Turkey": {"score": 2.7, "cities": {"Istanbul": 2.9, "Ankara": 2.6, "Izmir": 2.7}},
    "Uganda": {"score": 3.4, "cities": {"Kampala": 3.5, "Gulu": 3.3}},
    "Ukraine": {"score": 3.8, "cities": {"Kyiv": 3.9, "Kharkiv": 3.8, "Odesa": 3.7}},
    "United Arab Emirates": {"score": 1.6, "cities": {"Dubai": 1.7, "Abu Dhabi": 1.5, "Sharjah": 1.6}},
    "United Kingdom": {"score": 2.3, "cities": {"London": 2.8, "Manchester": 2.5, "Birmingham": 2.4}},
    "United States": {"score": 2.8, "cities": {"New York": 3.5, "Los Angeles": 3.0, "Chicago": 3.2}},
    "Uruguay": {"score": 2.4, "cities": {"Montevideo": 2.5, "Salto": 2.3}},
    "Uzbekistan": {"score": 2.6, "cities": {"Tashkent": 2.7, "Namangan": 2.6}},
    "Venezuela": {"score": 4.2, "cities": {"Caracas": 4.4, "Maracaibo": 4.1, "Valencia": 4.2}},
    "Vietnam": {"score": 2.4, "cities": {"Hanoi": 2.5, "Ho Chi Minh City": 2.4, "Da Nang": 2.3}},
    "Yemen": {"score": 4.6, "cities": {"Sanaa": 4.7, "Aden": 4.6}},
    "Zambia": {"score": 3.1, "cities": {"Lusaka": 3.2, "Kitwe": 3.0}},
    "Zimbabwe": {"score": 3.3, "cities": {"Harare": 3.4, "Bulawayo": 3.3}}
}


def get_travel_advisory_score(country_name, city_name=None):
    """
    国名と都市名から危険度スコアを取得する

    Args:
        country_name: 国名
        city_name: 都市名(オプション)

    Returns:
        float: 危険度スコア(None if not found)
    """
    country_data = DANGER_SCORE.get(country_name)

    if not country_data:
        return None

    # 都市データが存在する場合は都市のスコアを返す
    if city_name and "cities" in country_data and city_name in country_data["cities"]:
        return country_data["cities"][city_name]

    # 都市データがない場合は国のスコアを返す
    return country_data["score"]


def calculate_danger_level(country_name, city_name=None):
    """
    国と都市の危険度を計算
    1. 静的な危険度スコア
    2. リアルタイムニュース情報
    を組み合わせて判定

    Args:
        country_name: 国名
        city_name: 都市名(オプション)

    Returns:
        dict: 危険度情報
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


def get_danger_level_description(score):
    """
    危険度スコアに基づいて説明を返す

    Args:
        score: 危険度スコア

    Returns:
        str: 危険度の説明
    """
    if score < 2.0:
        return "Very Safe"
    elif score < 3.0:
        return "Safe"
    elif score < 4.0:
        return "Moderate"
    elif score < 4.5:
        return "Dangerous"
    else:
        return "Very Dangerous"
