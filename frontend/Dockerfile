# ベースイメージの指定（Alpine版で軽量化）
FROM node:20-alpine

# 作業ディレクトリの設定
WORKDIR /app

# パッケージファイルのみ先にコピー（キャッシュ最適化）
COPY package.json yarn.lock* package-lock.json* ./

# 依存関係のインストール
# yarn.lockがある場合はyarn、なければnpm
RUN if [ -f yarn.lock ]; then \
      yarn install --frozen-lockfile --production=false; \
    elif [ -f package-lock.json ]; then \
      npm ci; \
    else \
      npm install; \
    fi

# Tailwind CSSのグローバルインストール
RUN npm install -g tailwindcss

# アプリケーションファイルのコピー
COPY . .

# ポートの公開
EXPOSE 3000

# 開発サーバーの起動
CMD ["yarn", "start"]
