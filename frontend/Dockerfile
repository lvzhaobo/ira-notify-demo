# 构建 React 静态资源，由 Nginx 提供；/api 反代到 compose 中的 api 服务
FROM node:20-alpine AS build
WORKDIR /app
COPY package.json ./
RUN npm install
COPY public ./public
COPY src ./src
RUN npm run build

FROM nginx:1.25-alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
