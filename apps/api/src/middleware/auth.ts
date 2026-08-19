/**
 * JWT authentication middleware.
 *
 * Applied to all protected routes.
 * Public routes: /health, /ready, /metrics, /api/v1/auth/*
 *
 * Token format: Bearer <jwt>
 * Claims: { sub: userId, email: string, iat: number, exp: number }
 *
 * TODO(week-5): implement Fastify preHandler hook using @fastify/jwt
 */

export {}; // placeholder — replace with real implementation
