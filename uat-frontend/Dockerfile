# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Runtime stage - serve with Nginx
FROM nginx:stable-alpine
# Copy built files from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# (Optional) Replace default nginx.conf with SPA-friendly config
COPY nginx.conf /etc/nginx/nginx.conf




EXPOSE 80
# Start Nginx server

CMD ["nginx", "-g", "daemon off;"]
