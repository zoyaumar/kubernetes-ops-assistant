/**
 * Health and readiness routes.
 *
 * GET /health  — liveness: 200 if the process is running
 * GET /ready   — readiness: 200 if DB connection is healthy
 * GET /metrics — Prometheus metrics (if enabled)
 *
 * TODO(week-5): implement with real DB ping
 */

import type { FastifyInstance } from 'fastify';

export async function healthRoutes(app: FastifyInstance): Promise<void> {
  app.get('/health', async () => ({ status: 'ok' }));

  // TODO(week-5): check DB connectivity before returning 200
  app.get('/ready', async () => ({ status: 'ok' }));
}
