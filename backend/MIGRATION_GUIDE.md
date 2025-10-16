# JoyJaunt Backend - Modular Structure

## 📁 新しいフォルダ構造

```
backend/
├── app_new.py              # 新しいエントリーポイント(app.pyの代わりに使用)
├── app.py                  # 旧バージョン(962行の巨大ファイル - 削除推奨)
├── db_init.py              # データベース初期化スクリプト
├── requirements.txt        # Python依存関係
├── Dockerfile             
├── package.json           
│
└── app/                    # アプリケーションパッケージ
    ├── __init__.py         # アプリケーションファクトリ(create_app)
    ├── config.py           # 環境設定(Development/Production)
    ├── extensions.py       # Flask拡張機能(db, bcrypt, jwt, migrate)
    │
    ├── models/             # データベースモデル
    │   ├── __init__.py     # モデルパッケージ
    │   ├── user.py         # Userモデル
    │   └── location.py     # Country, Cityモデル
    │
    ├── routes/             # APIエンドポイント(Blueprint)
    │   ├── __init__.py     # ルートパッケージ
    │   ├── auth.py         # 認証エンドポイント
    │   ├── location.py     # 地域エンドポイント
    │   ├── weather.py      # 天気エンドポイント
    │   ├── news.py         # ニュースエンドポイント
    │   └── danger.py       # 危険度エンドポイント
    │
    └── services/           # ビジネスロジック
        ├── __init__.py     # サービスパッケージ
        ├── weather_service.py   # 天気予報API統合
        ├── news_service.py      # ニュースAPI統合
        └── danger_service.py    # 危険度計算ロジック
```

## 🔄 移行手順

### 1. 古いapp.pyをバックアップ
```bash
cd backend
mv app.py app_old.py
mv app_new.py app.py
```

### 2. データベースマイグレーション
```bash
# 既存のマイグレーションを確認
flask db current

# 必要に応じて新しいマイグレーションを作成
flask db migrate -m "Modular structure migration"

# マイグレーションを適用
flask db upgrade
```

### 3. アプリケーションを起動
```bash
python app.py
```

## 📋 エンドポイント一覧

### 認証 (auth_bp) - `/api/auth`
- `POST /api/auth/register` - ユーザー登録
- `POST /api/auth/login` - ログイン
- `GET /api/auth/user-info` - ユーザー情報取得
- `POST /api/auth/refresh` - トークン更新

### 地域 (location_bp) - `/api/location`
- `GET /api/location/countries` - 国一覧取得
- `GET /api/location/countries/<code>/cities` - 国の都市一覧
- `GET /api/location/cities/<code>` - 特定都市の情報

### 天気 (weather_bp) - `/api/weather`
- `GET /api/weather/weather_forecast` - 天気予報取得
- `GET /api/weather/weather_forecast_for_user` - ユーザーの国の天気
- `GET /api/weather/weather_forecast_for_travel_plan` - 旅行計画用天気
- `GET /api/weather/current_weather` - 現在の天気

### ニュース (news_bp) - `/api/news`
- `POST /api/news/location_news` - 地域のニュース取得
- `POST /api/news/general_news` - 一般ニュース取得

### 危険度 (danger_bp) - `/api/danger`
- `POST /api/danger/check_realtime_danger` - リアルタイム危険度チェック
- `POST /api/danger/travel_info` - 総合旅行情報取得

### システム
- `GET /health` - ヘルスチェック
- `GET /` - API情報

## ⚙️ 環境変数(.env)

```env
# Flask設定
FLASK_ENV=development
FLASK_HOST=0.0.0.0
FLASK_PORT=5000

# JWT設定
JWT_SECRET_KEY=your_secret_key_here

# データベース
SQLALCHEMY_DATABASE_URI=mysql+pymysql://dbuser:ecc@db:3306/Joy

# 外部API
NEWS_API_KEY=your_news_api_key
OPEN_WEATHER_API_KEY=your_openweather_api_key
TRAVEL_ADVISORY_API_KEY=your_travel_advisory_api_key
```

## 📊 統計

| 項目 | 旧構造 | 新構造 |
|------|--------|--------|
| ファイル数 | 1 (app.py) | 15+ ファイル |
| 行数 | 962行 | 平均50-150行/ファイル |
| Blueprint数 | 0 | 5 |
| サービス層 | なし | 3サービス |
| 保守性 | 低 | 高 ✅ |
| テスト容易性 | 低 | 高 ✅ |
| 拡張性 | 低 | 高 ✅ |

## 🎯 主な改善点

1. **関心の分離**: モデル、ルート、ビジネスロジックが分離
2. **Blueprint使用**: URLプレフィックスで機能を整理
3. **サービス層**: API統合ロジックを再利用可能に
4. **設定管理**: 環境別設定(Development/Production)
5. **ファクトリパターン**: テストとデプロイが容易
6. **パッケージ化**: Pythonのベストプラクティスに準拠

## ⚠️ 注意事項

- 元の`app.py`は`app_old.py`として保存することを推奨
- フロントエンドのAPIエンドポイントURLを更新する必要があります
  - 例: `/register` → `/api/auth/register`
- Docker Composeを使用している場合、コンテナを再ビルドしてください

## 🔧 トラブルシューティング

### Import Errorが発生する場合
```bash
# PYTHONPATH を設定
export PYTHONPATH="${PYTHONPATH}:/path/to/backend"
```

### データベース接続エラー
```bash
# マイグレーションをリセット
flask db downgrade base
flask db upgrade
```

### モジュールが見つからない
```bash
# 仮想環境を再作成
pip install -r requirements.txt
```
