# 构建阶段
FROM node:18-alpine AS builder

WORKDIR /app

# 复制package文件
COPY frontend/package*.json ./

# 安装依赖
RUN npm install

# 复制源代码
COPY frontend/ .

# 构建应用
RUN npm run build

# 生产阶段
FROM nginx:alpine

# 复制构建结果到nginx目录
COPY --from=builder /app/dist /usr/share/nginx/html

# 复制nginx配置
COPY docker/nginx/nginx.conf /etc/nginx/nginx.conf

# 暴露端口
EXPOSE 3000

# 启动nginx
CMD ["nginx", "-g", "daemon off;"] 