# API エンドポイント更新ガイド

## ✅ 更新完了

フロントエンドとバックエンドのAPIエンドポイントを新しいBlueprint構造に対応させました。

## 📋 変更されたエンドポイント一覧

### 🔐 認証エンドポイント (Auth)
| 旧エンドポイント | 新エンドポイント |
|----------------|----------------|
| `/register` | `/api/auth/register` |
| `/login` | `/api/auth/login` |
| `/get_user_info` | `/api/auth/user-info` |
| `/refresh` | `/api/auth/refresh` |

### 🌍 地域エンドポイント (Location)
| 旧エンドポイント | 新エンドポイント |
|----------------|----------------|
| `/countries` | `/api/location/countries` |
| `/get_cities_by_country` | `/api/location/cities` |
| `/get_city_by_country/<code>` | `/api/location/cities/<code>` |

### 🌤️ 天気エンドポイント (Weather)
| 旧エンドポイント | 新エンドポイント |
|----------------|----------------|
| `/weather_forecast` | `/api/weather/weather_forecast` |
| `/weather_forecast_for_user` | `/api/weather/weather_forecast_for_user` |
| `/weather_forecast_for_travel_plan` | `/api/weather/weather_forecast_for_travel_plan` |

### 📰 ニュースエンドポイント (News)
| 旧エンドポイント | 新エンドポイント |
|----------------|----------------|
| `/get_location_news` | `/api/news/location_news` |

### ⚠️ 危険度エンドポイント (Danger)
| 旧エンドポイント | 新エンドポイント |
|----------------|----------------|
| `/check_realtime_danger` | `/api/danger/check_realtime_danger` |
| `/travel_info` | `/api/danger/travel_info` |

### 🏥 システムエンドポイント
| エンドポイント | 説明 |
|--------------|------|
| `/health` | ヘルスチェック |
| `/` | API情報 |

## 📝 更新されたファイル

### フロントエンド
1. **`frontend/src/services/api.js`**
   - 全てのAPI呼び出し関数を新エンドポイントに更新
   - `getCountries()`, `registerUser()`, `loginUser()`, `checkRealtimeDanger()`など

2. **`frontend/src/pages/Danger/Dang.js`**
   - ハードコードされたURLを削除
   - `api.js`の`checkRealtimeDanger()`関数を使用するように変更

### バックエンド
1. **`backend/app/routes/auth.py`**
   - Blueprint定義から重複する`url_prefix`を削除

2. **`backend/app/routes/location.py`**
   - Blueprint定義から重複する`url_prefix`を削除

## 🔧 技術的な変更

### Blueprint URL構造
```python
# app/__init__.py で登録
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(location_bp, url_prefix='/api/location')
app.register_blueprint(weather_bp, url_prefix='/api/weather')
app.register_blueprint(news_bp, url_prefix='/api/news')
app.register_blueprint(danger_bp, url_prefix='/api/danger')
```

### フロントエンドAPI呼び出し例
```javascript
// 旧バージョン
fetch('http://localhost:5000/register', { ... })

// 新バージョン (api.js使用)
import { registerUser } from './services/api';
registerUser(userData)
```

## ✨ メリット

1. **明確なURL構造**: `/api/<カテゴリ>/<アクション>`
2. **バージョニング対応**: 将来的に`/api/v2`などに拡張可能
3. **保守性向上**: 機能ごとにエンドポイントが整理
4. **統一されたAPI呼び出し**: `services/api.js`で一元管理
5. **エラーハンドリング**: APIError クラスで統一的なエラー処理

## 🚀 動作確認

バックエンドサーバーを起動して、ルートエンドポイントを確認:

```bash
cd backend
python app.py
```

ブラウザで http://localhost:5000/ にアクセスすると、利用可能なエンドポイント一覧が表示されます:

```json
{
  "message": "Welcome to JoyJaunt API",
  "version": "2.0",
  "endpoints": {
    "auth": "/api/auth",
    "location": "/api/location",
    "weather": "/api/weather",
    "news": "/api/news",
    "danger": "/api/danger"
  }
}
```

## 📌 注意事項

- 既存のローカルストレージのトークンは引き続き使用可能
- API_URL設定(`frontend/src/services/config.js`)は変更不要
- すべてのエンドポイントでCORS設定が有効
- 認証が必要なエンドポイントでは引き続き`Authorization: Bearer <token>`ヘッダーを使用

## 🔄 互換性

- ✅ フロントエンドとバックエンド間の互換性確認済み
- ✅ 既存の認証フローは変更なし
- ✅ JWTトークンの形式は変更なし
- ✅ レスポンスデータの構造は変更なし
