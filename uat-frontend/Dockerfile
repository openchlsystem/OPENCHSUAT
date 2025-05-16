# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

# Install dependencies (include devDependencies for build)
COPY package*.json ./
RUN npm ci --include=dev

# Copy source files
COPY . .

# Build application
RUN npm run build

# Runtime stage
FROM node:20-alpine

WORKDIR /app

# Copy only necessary files
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package*.json ./

# Install production dependencies
RUN npm install --omit=dev -g vite

# Environment variables
ENV NODE_ENV=production
ENV PORT=5100

# Expose port
EXPOSE 5100

# Health check (corrected port)
HEALTHCHECK --interval=30s --timeout=3s \
  CMD wget -qO- http://localhost:5100/ || exit 1

# Run as non-root user
RUN chown -R node:node /app
USER node

# Startup command (explicit host/port binding)
CMD ["vite", "preview", "--host", "0.0.0.0", "--port", "5100"]