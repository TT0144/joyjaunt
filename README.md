# JoyJaunt - 旅行安全情報Webアプリケーション

第3回チーム開発プロジェクト

旅行者向けの安全情報・天気予報を提供するWebアプリケーションです。

## 🌟 主な機能

- **リアルタイム危険度判定**: 静的データ + 最新ニュースで総合判定
- **天気予報**: 5日間の詳細な天気予報
- **ニュース取得**: 指定場所の安全関連ニュース
- **ユーザー認証**: JWT認証によるセキュアなログイン
- **パスポート・ビザ情報**: 有効期限チェック機能

## 🛠️ 技術スタック

### バックエンド
- Python 3.x
- Flask
- MySQL 8.0
- SQLAlchemy
- JWT認証

### フロントエンド
- React
- React Router
- Tailwind CSS

### インフラ
- Docker & Docker Compose

## 📋 前提条件

- Docker Desktop がインストールされていること
- Git がインストールされていること

## 🚀 セットアップ手順

### 1. リポジトリのクローン

```bash
git clone https://github.com/TT0144/joyjaunt.git
cd joyjaunt
```

### 2. 環境変数の設定

#### バックエンド環境変数

```bash
# backend/.env.example を backend/.env にコピー
cp backend/.env.example backend/.env
```

`backend/.env` を編集して、以下の値を設定:

```env
# セキュリティキー(ランダムな文字列を生成してください)
SECRET_KEY=your_random_secret_key_here
JWT_SECRET_KEY=your_random_jwt_secret_key_here

# 外部APIキー(各サービスで取得してください)
NEWS_API_KEY=your_newsapi_key_here
OPEN_WEATHER_API_KEY=your_openweather_key_here
TRAVEL_ADVISORY_API_KEY=your_travel_advisory_key_here

# データベース設定(必要に応じて変更)
DB_NAME=Joy
DB_USER=dbuser
DB_PASSWORD=your_secure_password_here
DB_ROOT_PASSWORD=your_secure_root_password_here
```

#### フロントエンド環境変数

```bash
# frontend/.env.example を frontend/.env にコピー
cp frontend/.env.example frontend/.env
```

`frontend/.env` を編集:

```env
# 開発環境
REACT_APP_API_URL=http://localhost:5000

# 本番環境の場合
# REACT_APP_API_URL=https://your-api-domain.com
```

### 3. APIキーの取得

以下のサービスでAPIキーを取得してください:

1. **NewsAPI**: https://newsapi.org/
   - 無料プラン: 1日100リクエストまで
   
2. **OpenWeather**: https://openweathermap.org/api
   - 無料プラン: 1分60リクエストまで

3. **Travel Advisory API**: https://www.travel-advisory.info/api
   - APIキーが必要な場合があります

### 4. Dockerでアプリケーションを起動

#### ⚡ クイックスタート（推奨）

```powershell
# PowerShellスクリプトで高速起動
.\docker-start.ps1
```

起動オプション:
- **[1] 高速起動** - キャッシュ利用で10-30秒で起動 (推奨)
- **[2] クリーンビルド** - 依存関係変更時に使用 (1-2分)
- **[3] 停止のみ** - コンテナを停止
- **[4] システムクリーンアップ** - 完全リセット

#### 📝 従来の方法

```bash
# 高速起動（キャッシュ利用）
docker-compose up -d --build

# クリーンビルド（初回または依存関係変更時）
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

#### 🎯 起動時間の目安

| 起動方法 | 所要時間 | 使用タイミング |
|---------|---------|--------------|
| 高速起動 | 10-30秒 | 通常の開発作業 |
| クリーンビルド | 1-2分 | 依存関係の変更後 |
| 初回ビルド | 1-2分 | プロジェクト初回セットアップ |

💡 **最適化の詳細**: [DOCKER_OPTIMIZATION.md](DOCKER_OPTIMIZATION.md) を参照

### 5. データベースの初期化

初回起動時のみ、データベースのマイグレーションを実行:

```bash
# バックエンドコンテナに接続
docker exec -it backend bash

# マイグレーション実行
flask db upgrade

# コンテナから抜ける
exit
```

### 6. アプリケーションへのアクセス

- **フロントエンド**: http://localhost:3001
- **バックエンドAPI**: http://localhost:5000
- **MySQL**: localhost:3307

## 📖 API ドキュメント

詳細なAPIドキュメントは [backend/API_DOCUMENTATION.md](backend/API_DOCUMENTATION.md) を参照してください。

## 🔒 セキュリティ

### 重要な注意事項

1. **`.env` ファイルは Git にコミットしないでください**
   - `.gitignore` に含まれています
   - 代わりに `.env.example` を更新してください

2. **本番環境では強力なパスワードを使用してください**
   - SECRET_KEY と JWT_SECRET_KEY は長くランダムな文字列にする
   - データベースパスワードも強力なものに変更する

3. **APIキーは外部に公開しないでください**

### セキュアな SECRET_KEY の生成方法

Python で生成:

```python
import secrets
print(secrets.token_urlsafe(32))
```

または:

```bash
# Linux/Mac
openssl rand -base64 32

# PowerShell (Windows)
[Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Maximum 256 }))
```

## 🧪 テスト

APIのテストスクリプトを実行:

```bash
cd backend
python test_api.py
```

## 📁 プロジェクト構造

```
joyjaunt/
├── backend/
│   ├── app.py              # メインアプリケーション
│   ├── requirements.txt    # Python依存パッケージ
│   ├── .env.example        # 環境変数テンプレート
│   ├── .env                # 環境変数(Git除外)
│   └── API_DOCUMENTATION.md # APIドキュメント
├── frontend/
│   ├── src/
│   │   ├── config.js       # API設定
│   │   └── ...
│   ├── .env.example        # 環境変数テンプレート
│   └── .env                # 環境変数(Git除外)
├── docker-compose.yml      # Docker設定
├── .gitignore             # Git除外ファイル
└── README.md              # このファイル
```

## 🐛 トラブルシューティング

### ポートが既に使用されている

```bash
# 使用中のポートを確認
netstat -ano | findstr :5000
netstat -ano | findstr :3001
netstat -ano | findstr :3307

# Dockerコンテナを停止
docker-compose down
```

### データベース接続エラー

```bash
# コンテナの状態確認
docker-compose ps

# ログ確認
docker-compose logs db
docker-compose logs backend

# データベースのリセット
docker-compose down -v
docker-compose up --build
```

### API キーエラー

- `.env` ファイルが正しく作成されているか確認
- APIキーが正しく設定されているか確認
- コンテナを再起動: `docker-compose restart backend`

## 🤝 コントリビューション

1. このリポジトリをフォーク
2. 新しいブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## 📝 ライセンス

このプロジェクトは MIT ライセンスの下で公開されています。

## 👥 開発チーム

第3回チーム開発プロジェクト

## 📞 サポート

問題が発生した場合は、GitHub Issues でお知らせください。

---

**注意**: このアプリケーションは教育目的で開発されました。本番環境で使用する場合は、追加のセキュリティ対策を実施してください。
