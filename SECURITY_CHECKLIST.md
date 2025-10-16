# セキュリティチェックリスト

このドキュメントは、JoyJauntプロジェクトをGitにコミットする前のセキュリティチェックリストです。

## ✅ 完了済みのセキュリティ対策

### 1. 環境変数の分離
- [x] `.env.example` ファイルを作成(機密情報を除外)
- [x] 実際の `.env` ファイルを `.gitignore` に追加
- [x] backend/.env.example を作成
- [x] frontend/.env.example を作成

### 2. .gitignore の設定
- [x] ルート `.gitignore` を作成
- [x] `.env` ファイルを除外
- [x] データベースファイル(`db_data/`)を除外
- [x] ログファイルを除外
- [x] APIキー・証明書ファイルを除外
- [x] `__pycache__/` を除外
- [x] `node_modules/` を除外

### 3. docker-compose.yml の環境変数化
- [x] データベース認証情報を環境変数に変更
- [x] env_file ディレクティブを追加
- [x] デフォルト値の設定

### 4. フロントエンドのAPI URL管理
- [x] ハードコードされたAPI URLを削除
- [x] `config.js` ファイルを作成
- [x] 環境変数 `REACT_APP_API_URL` を使用
- [x] 全コンポーネントを更新:
  - [x] Home.js
  - [x] tour.jsx
  - [x] LoginSignup.jsx
  - [x] Weather.js

### 5. ドキュメント整備
- [x] README.md を更新(セットアップ手順を詳細化)
- [x] セキュリティ注意事項を追加
- [x] SECRET_KEY生成方法を記載
- [x] API_DOCUMENTATION.md を作成

## ⚠️ Gitコミット前の最終チェック

### コミットしてはいけないファイル

```
❌ backend/.env                    # 実際のAPIキーを含む
❌ frontend/.env                   # 実際のAPI URLを含む
❌ backend/db_data/                # データベースファイル
❌ backend/__pycache__/            # Pythonキャッシュ
❌ frontend/node_modules/          # Node.jsパッケージ
❌ *.log                           # ログファイル
❌ secrets/                        # 機密情報フォルダ
❌ *.key, *.pem, *.crt             # 証明書ファイル
```

### コミットすべきファイル

```
✅ backend/.env.example            # テンプレート
✅ frontend/.env.example           # テンプレート
✅ .gitignore                      # Git除外設定
✅ docker-compose.yml              # 環境変数対応版
✅ backend/app.py                  # ソースコード
✅ frontend/src/**/*.js(x)         # ソースコード
✅ README.md                       # ドキュメント
✅ backend/API_DOCUMENTATION.md    # APIドキュメント
```

## 🔍 コミット前の確認コマンド

### 1. 機密情報が含まれていないか確認

```bash
# .envファイルがステージングされていないか確認
git status

# 除外されるべきファイルを確認
git ls-files --others --ignored --exclude-standard
```

### 2. .envファイルの確認

```bash
# .envが除外されているか確認
git check-ignore backend/.env
git check-ignore frontend/.env

# 出力があれば除外されている(正常)
```

### 3. APIキーが含まれていないか検索

```bash
# コミット対象のファイルにAPIキーがないか確認
git diff --cached | grep -i "api_key\|secret_key\|password"

# 何も出力されなければOK
```

### 4. .env.exampleの確認

```bash
# .env.exampleに実際の値が含まれていないか確認
cat backend/.env.example
cat frontend/.env.example

# "your_*_here" のようなプレースホルダーのみであることを確認
```

## 🚨 もし機密情報をコミットしてしまった場合

### 即座に実行すべきこと

1. **リモートにプッシュ前の場合**
```bash
# 最新のコミットを取り消し
git reset --soft HEAD~1

# 修正してから再コミット
git add .
git commit -m "Fixed: Remove sensitive data"
```

2. **リモートにプッシュ済みの場合**
```bash
# !!注意: 履歴を書き換えるため、チームメンバーに通知すること!!

# 機密情報を含むファイルを履歴から完全削除
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch backend/.env" \
  --prune-empty --tag-name-filter cat -- --all

# 強制プッシュ
git push origin --force --all
```

3. **APIキーを無効化**
   - NewsAPI, OpenWeather, その他全てのAPIキーを即座に無効化・再発行
   - データベースパスワードを変更
   - SECRET_KEY, JWT_SECRET_KEYを再生成

## 📝 推奨されるGitワークフロー

### 初回コミット

```bash
# 1. .gitignoreが正しく設定されているか確認
cat .gitignore

# 2. ステータス確認
git status

# 3. .envファイルが除外されているか確認
git check-ignore backend/.env frontend/.env

# 4. ステージング
git add .

# 5. コミット前に差分確認
git diff --cached

# 6. 機密情報がないことを確認してからコミット
git commit -m "Initial commit: Setup JoyJaunt project with security measures"

# 7. プッシュ
git push origin main
```

### 日常的なコミット

```bash
# 毎回のコミット前に確認
git status
git diff

# 機密情報が含まれていないことを確認
git diff | grep -i "api_key\|secret\|password"

# 問題なければコミット
git add .
git commit -m "Update: Feature description"
git push origin main
```

## 🔐 追加のセキュリティ推奨事項

### 本番環境での対策

1. **環境変数管理サービスを使用**
   - AWS Secrets Manager
   - Azure Key Vault
   - HashiCorp Vault

2. **HTTPS通信の強制**
   - SSL/TLS証明書の設定
   - HTTP Strict Transport Security (HSTS) の有効化

3. **レート制限の実装**
   - APIエンドポイントへの過度なアクセスを防ぐ
   - Flask-Limiterなどを使用

4. **CORS設定の厳格化**
   - 本番環境では特定のドメインのみ許可

5. **SQLインジェクション対策**
   - SQLAlchemyのORMを使用(既に実装済み)
   - ユーザー入力の検証・サニタイズ

6. **XSS対策**
   - Reactのデフォルト保護を活用
   - dangerouslySetInnerHTMLの使用を避ける

7. **ログ管理**
   - 機密情報をログに出力しない
   - ログローテーションの実装

## ✅ 最終確認

コミット前に以下を確認してください:

- [ ] `.env` ファイルが Git に追跡されていない
- [ ] `.env.example` に実際の値が含まれていない
- [ ] `docker-compose.yml` にハードコードされた機密情報がない
- [ ] フロントエンドのソースコードにAPI URLがハードコードされていない
- [ ] `db_data/` ディレクトリが除外されている
- [ ] `__pycache__/` が除外されている
- [ ] `node_modules/` が除外されている
- [ ] README.md にセットアップ手順が記載されている

全てチェックできたら、安全にコミット・プッシュできます! 🎉

---

**最終更新**: 2025年10月16日
