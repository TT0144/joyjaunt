"""
JoyJaunt バックエンドアプリケーション エントリーポイント

モジュール化されたBlueprint構造:
- app/__init__.py: アプリケーションファクトリ
- app/config.py: 設定管理
- app/extensions.py: Flask拡張機能
- app/models/: データベースモデル
- app/routes/: エンドポイント(Blueprint)
- app/services/: ビジネスロジック
"""
import os
from dotenv import load_dotenv
from app import create_app
from app.extensions import db

# 環境変数をロード
load_dotenv()

# 環境に応じてアプリケーションを作成
config_name = os.getenv('FLASK_ENV', 'development')
app = create_app(config_name)

# データベースコンテキストでモデルをインポート
with app.app_context():
    from app.models import User, Country, City


if __name__ == '__main__':
    # 開発サーバーを起動
    app.run(
        host=os.getenv('FLASK_HOST', '0.0.0.0'),
        port=int(os.getenv('FLASK_PORT', 5000)),
        debug=(config_name == 'development')
    )
