"""
JoyJaunt Backend API テストスクリpt
新しく実装したAPIエンドポイントの動作確認用
"""

import requests
import json
from datetime import datetime

# APIのベースURL(環境に応じて変更)
BASE_URL = "http://localhost:5000"


def print_separator(title):
    """セクション区切り線を出力"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)


def test_check_realtime_danger():
    """リアルタイム危険度チェックのテスト"""
    print_separator("リアルタイム危険度チェック")

    test_cases = [
        {"country": "Japan", "city": "Tokyo"},
        {"country": "France", "city": "Paris"},
        {"country": "United States", "city": "New York"},
    ]

    for test_data in test_cases:
        print(f"\n📍 テスト: {test_data['city']}, {test_data['country']}")
        try:
            response = requests.post(
                f"{BASE_URL}/check_realtime_danger",
                json=test_data,
                timeout=15
            )

            if response.status_code == 200:
                data = response.json()
                print(f"✅ ステータス: 成功")
                print(f"   危険度: {'⚠️ 危険' if data['is_dangerous'] else '✓ 安全'}")
                print(
                    f"   スコア: {data['danger_score']} (基本: {data['base_score']}, ニュース調整: +{data['news_adjustment']})")
                print(f"   ニュース件数: {data['news_count']}件")
                if data.get('recent_news'):
                    print(f"   最新ニュース: {len(data['recent_news'])}件取得")
            else:
                print(f"❌ エラー: {response.status_code}")
                print(f"   {response.text}")

        except Exception as e:
            print(f"❌ 例外発生: {str(e)}")


def test_get_location_news():
    """場所別ニュース取得のテスト"""
    print_separator("場所別ニュース取得")

    test_data = {"country": "United Kingdom", "city": "London"}
    print(f"\n📰 テスト: {test_data['city']}, {test_data['country']}")

    try:
        response = requests.post(
            f"{BASE_URL}/get_location_news",
            json=test_data,
            timeout=15
        )

        if response.status_code == 200:
            data = response.json()
            print(f"✅ ステータス: 成功")
            print(f"   ニュース件数: {data['news_count']}件")

            for i, article in enumerate(data.get('articles', [])[:3], 1):
                print(f"\n   [{i}] {article['title']}")
                print(f"       ソース: {article['source']}")
                print(f"       日時: {article['publishedAt']}")
        else:
            print(f"❌ エラー: {response.status_code}")
            print(f"   {response.text}")

    except Exception as e:
        print(f"❌ 例外発生: {str(e)}")


def test_travel_info():
    """総合旅行情報取得のテスト"""
    print_separator("総合旅行情報取得")

    test_data = {"country": "Japan", "city": "Tokyo"}
    print(f"\n🌏 テスト: {test_data['city']}, {test_data['country']}")

    try:
        response = requests.post(
            f"{BASE_URL}/travel_info",
            json=test_data,
            timeout=15
        )

        if response.status_code == 200:
            data = response.json()
            print(f"✅ ステータス: 成功")

            # 危険度情報
            danger = data.get('danger', {})
            print(f"\n   🚨 危険度情報:")
            print(
                f"      判定: {'⚠️ 危険' if danger.get('is_dangerous') else '✓ 安全'}")
            print(f"      スコア: {danger.get('score')}")
            print(f"      ニュース件数: {danger.get('news_count')}件")

            # 天気情報
            weather = data.get('weather', [])
            if weather:
                print(f"\n   🌤️ 天気予報: {len(weather)}日分")
                for w in weather[:3]:
                    print(
                        f"      {w['date']}: {w['temperature']}°C, {w['weather']}, 風速{w['wind_speed']}m/s")

            # ニュース
            news = data.get('recent_news', [])
            if news:
                print(f"\n   📰 最新ニュース: {len(news)}件")
                for article in news[:2]:
                    print(f"      - {article['title'][:50]}...")
        else:
            print(f"❌ エラー: {response.status_code}")
            print(f"   {response.text}")

    except Exception as e:
        print(f"❌ 例外発生: {str(e)}")


def test_weather_forecast():
    """天気予報取得のテスト"""
    print_separator("天気予報取得")

    cities = ["Tokyo", "Paris", "New York"]

    for city in cities:
        print(f"\n🌤️ テスト: {city}")
        try:
            response = requests.get(
                f"{BASE_URL}/weather_forecast_for_travel_plan",
                params={"city": city},
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                forecast = data.get('forecast', [])
                print(f"✅ ステータス: 成功")
                print(f"   予報日数: {len(forecast)}日分")
                if forecast:
                    first = forecast[0]
                    print(
                        f"   {first['date']}: {first['temperature']}°C, {first['weather']}")
            else:
                print(f"❌ エラー: {response.status_code}")

        except Exception as e:
            print(f"❌ 例外発生: {str(e)}")


def test_countries_and_cities():
    """国・都市情報取得のテスト"""
    print_separator("国・都市情報取得")

    try:
        # 国一覧
        print("\n🌍 国一覧取得:")
        response = requests.get(f"{BASE_URL}/countries")
        if response.status_code == 200:
            countries = response.json()
            print(f"✅ {len(countries)}カ国取得")
            print(f"   例: {countries[0]['name']} ({countries[0]['code']})")

        # 都市一覧(日本)
        print("\n🏙️ 都市一覧取得(日本):")
        response = requests.get(
            f"{BASE_URL}/get_cities_by_country?country_code=JPN")
        if response.status_code == 200:
            cities = response.json()
            print(f"✅ {len(cities)}都市取得")
            print(f"   例: {', '.join(cities[:5])}")

    except Exception as e:
        print(f"❌ 例外発生: {str(e)}")


def main():
    """メイン実行関数"""
    print("\n" + "🚀"*30)
    print("  JoyJaunt Backend API テスト開始")
    print("  サーバー: " + BASE_URL)
    print("  実行時刻: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("🚀"*30)

    # サーバー接続確認
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print(f"\n✅ サーバー接続成功!")
        else:
            print(f"\n⚠️ サーバー応答異常: {response.status_code}")
            return
    except Exception as e:
        print(f"\n❌ サーバーに接続できません: {str(e)}")
        print("   バックエンドサーバーが起動しているか確認してください。")
        return

    # 各テストを実行
    test_countries_and_cities()
    test_weather_forecast()
    test_check_realtime_danger()
    test_get_location_news()
    test_travel_info()

    print("\n" + "🎉"*30)
    print("  テスト完了!")
    print("🎉"*30 + "\n")


if __name__ == "__main__":
    main()
