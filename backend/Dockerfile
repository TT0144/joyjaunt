# ベースイメージの指定
FROM python:3.10

# 作業ディレクトリの設定
WORKDIR /app

# 依存関係ファイルのコピーとインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# プロジェクトファイルのコピー
COPY . .

# Flaskアプリケーションを実行
CMD ["flask", "run", "--host=0.0.0.0"]
