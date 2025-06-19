FROM node:20
WORKDIR /app
COPY . /app
RUN yarn install
RUN npm install -g tailwindcss
CMD ["yarn", "start"]
