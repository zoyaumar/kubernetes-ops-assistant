/**
 * Authentication routes.
 *
 * POST /api/v1/auth/register  — create account (email + password)
 * POST /api/v1/auth/login     — issue JWT access token
 * POST /api/v1/auth/refresh   — refresh access token
 * POST /api/v1/auth/logout    — invalidate token (if blocklist used)
 *
 * Security notes
 * --------------
 * - Passwords hashed with bcrypt (cost factor ≥ 12).
 * - Access tokens are short-lived (JWT_EXPIRES_IN seconds).
 * - No OAuth/SSO in v1 — keep it simple.
 * - Rate limiting applied at the route level.
 *
 * TODO(week-5): implement
 */

import type { FastifyInstance } from 'fastify';

export async function authRoutes(app: FastifyInstance): Promise<void> {
  // TODO(week-5): POST /register
  // TODO(week-5): POST /login
  // TODO(week-5): POST /refresh
  // TODO(week-5): POST /logout
}
