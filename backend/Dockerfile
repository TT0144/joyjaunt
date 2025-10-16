# ベースイメージの指定
FROM python:3.10-slim

# 作業ディレクトリの設定
WORKDIR /app

# 環境変数の設定
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# システムパッケージの更新（最小限）
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc default-libmysqlclient-dev && \
    rm -rf /var/lib/apt/lists/*

# 依存関係ファイルのコピーとインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# プロジェクトファイルのコピー
COPY . .

# ポートの公開
EXPOSE 5000

# Flaskアプリケーションを実行
CMD ["flask", "run", "--host=0.0.0.0"]
