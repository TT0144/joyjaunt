# 🚀 Docker開発クイックリファレンス

## ❓ よくある質問

### Q1: バグを修正したけど、高速起動で反映される?

**A: はい!** アプリケーションコード（`.py`, `.jsx`, `.css`など）の修正は高速起動でも即座に反映されます。

理由: `docker-compose.yml`の`volumes`設定により、ローカルファイルがコンテナにマウントされているため。

```yaml
volumes:
  - ./backend:/app  # ← ローカルの変更が即座にコンテナに反映される
```

### Q2: どんな時にクリーンビルドが必要?

**A: 依存関係を変更した時のみ**

- ✅ **クリーンビルド必要:**
  - `requirements.txt`に新しいPythonパッケージを追加
  - `package.json`に新しいnpmパッケージを追加
  - Dockerfileを変更
  
- ❌ **クリーンビルド不要（高速起動でOK）:**
  - Pythonコードのバグ修正
  - Reactコンポーネントの修正
  - CSSスタイルの変更

### Q3: .envファイルを変更したら?

**A: コンテナの再起動が必要**

```bash
docker-compose restart
# または
.\docker-start.ps1 → [1] 高速起動
```

## 🎯 状況別フローチャート

```
コードを変更した
    ↓
┌─────────────────────────────────┐
│ 何を変更しましたか?              │
└─────────────────────────────────┘
         ↓
    ┌────┴────┐
    │         │
    ↓         ↓
[コード]   [依存関係/設定]
.py, .jsx   requirements.txt
.css        package.json
            .env
            Dockerfile
    ↓         ↓
 ファイル    再起動 or
 保存のみ    クリーンビルド
    ↓         ↓
  完了!     .\docker-start.ps1
              ↓
           [1] or [2] 選択
```

## 📝 シナリオ別対応

### シナリオ1: バックエンドのAPIエンドポイントにバグ発見

```python
# backend/app/routes/danger.py
# バグ: タイポがある
longitude = request.json.get('longitde')  # ❌

# 修正
longitude = request.json.get('longitude')  # ✅
```

**対応手順:**
1. ✏️ ファイルを編集して保存
2. 🔄 Flaskが自動的にリロード（数秒）
3. ✅ 修正完了!

または、念のため再起動:
```bash
docker-compose restart backend
```

### シナリオ2: フロントエンドのReactコンポーネントにバグ

```jsx
// frontend/src/pages/Danger/Dang.js
// バグ: useState のインポート忘れ
import React from "react";  // ❌

// 修正
import React, { useState } from "react";  // ✅
```

**対応手順:**
1. ✏️ ファイルを編集して保存
2. 🔄 Reactのホットリロードが自動実行
3. ✅ ブラウザが自動更新!

### シナリオ3: 新しいPythonライブラリを追加したい

```txt
# requirements.txt
Flask==2.3.0
requests==2.31.0
pandas==2.0.0  # ← 新規追加
```

**対応手順:**
1. ✏️ requirements.txtに追加
2. 🔧 クリーンビルド必須
```bash
.\docker-start.ps1 → [2] クリーンビルド
```
3. ⏱️ 約1-2分待機
4. ✅ 完了!

### シナリオ4: API キーを変更したい

```env
# backend/.env
NEWS_API_KEY=old_api_key  # ❌
↓
NEWS_API_KEY=new_api_key  # ✅
```

**対応手順:**
1. ✏️ .envファイルを編集
2. 🔄 コンテナ再起動
```bash
docker-compose restart backend
```
3. ✅ 新しいキーで動作開始!

## 🔄 開発ワークフロー（推奨）

### 通常の開発作業

```bash
# 1. Dockerを起動（朝一回）
.\docker-start.ps1 → [1] 高速起動

# 2. コーディング
# - ファイルを編集して保存するだけ
# - 自動リロードで即座に反映

# 3. ログ確認（必要に応じて）
docker-compose logs -f backend

# 4. 作業終了
docker-compose down
```

### パッケージを追加した時

```bash
# 1. requirements.txt または package.json を編集

# 2. クリーンビルド
.\docker-start.ps1 → [2] クリーンビルド

# 3. 待機（約1-2分）

# 4. コーディング再開
```

## 🚨 トラブルシューティング

### 問題: コードを修正したのに反映されない!

**チェックリスト:**
1. ✅ ファイルを保存しましたか?
2. ✅ 正しいファイルを編集していますか?（コンテナ内のファイルではなく、ローカルのファイル）
3. ✅ Flaskの開発サーバーは動いていますか?
   ```bash
   docker-compose logs -f backend
   # "Reloading..." と表示されるはず
   ```
4. ✅ ブラウザのキャッシュをクリアしましたか?（Ctrl + Shift + R）

### 問題: 新しいパッケージをインストールしたのにImportError

**解決策:**
```bash
# クリーンビルドを実行
.\docker-start.ps1 → [2] クリーンビルド

# または手動で
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### 問題: .envを変更したのに反映されない

**解決策:**
```bash
# 再起動が必要
docker-compose restart

# または
docker-compose down
docker-compose up -d
```

## ⚡ 時間節約のコツ

| やりたいこと | 所要時間 | コマンド |
|------------|---------|----------|
| コードのバグ修正 | 0秒 | ファイル保存のみ |
| .env変更の反映 | 5-10秒 | `docker-compose restart` |
| 通常の起動 | 10-30秒 | `.\docker-start.ps1 → [1]` |
| パッケージ追加 | 1-2分 | `.\docker-start.ps1 → [2]` |

## 💡 まとめ

✅ **バグ修正 = ファイル保存のみでOK（高速起動でも問題なし）**

❌ **パッケージ追加 = クリーンビルド必須**

🔄 **.env変更 = 再起動必要**

---

困った時は: `cat DOCKER_OPTIMIZATION.md`
