# syntax=docker/dockerfile:1
# ─── API service Dockerfile ─────────────────────────────────────────────────
FROM node:20-slim AS deps
WORKDIR /app
COPY package*.json .
RUN npm ci --omit=dev

FROM node:20-slim AS builder
WORKDIR /app
COPY package*.json tsconfig.json .
RUN npm ci
COPY src/ src/
RUN npm run build

FROM node:20-slim AS runtime
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY package.json .

# Run as non-root
RUN useradd -m -u 1001 api
USER api

EXPOSE 3000

CMD ["node", "dist/server.js"]
