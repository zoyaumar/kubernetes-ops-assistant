/**
 * API service entry point.
 *
 * Registers all Fastify plugins and routes, then starts the HTTP server.
 *
 * Architecture note
 * -----------------
 * This service is the user-facing intelligence layer:
 *   1. Authentication (JWT)
 *   2. Conversation management
 *   3. RAG orchestration (retrieval + LLM + citations)
 *
 * It does NOT write to NATS — that is the watcher's responsibility.
 * It reads from PostgreSQL + pgvector for retrieval.
 *
 * Plugin registration order matters in Fastify:
 *   - cors before routes
 *   - jwt before protected routes
 *   - rate-limit before chat routes
 *   - swagger before routes (for spec generation)
 */

import Fastify from 'fastify';
import { loadConfig } from './config.js';

// TODO(week-5): register @fastify/cors
// TODO(week-5): register @fastify/jwt
// TODO(week-5): register @fastify/rate-limit
// TODO(week-5): register @fastify/swagger
// TODO(week-5): register auth routes
// TODO(week-5): register chat routes
// TODO(week-5): register conversation routes
// TODO(week-5): register cluster routes
// TODO(week-5): register health routes
// TODO(week-7): initialise OpenTelemetry tracer
// TODO(week-7): initialise Prometheus metrics

async function main(): Promise<void> {
  const config = loadConfig();

  const app = Fastify({
    logger: {
      level: config.logLevel,
      // JSON logging for Kubernetes log aggregation
      transport: process.env.NODE_ENV === 'development'
        ? { target: 'pino-pretty' }
        : undefined,
    },
  });

  // Placeholder health route — replace with proper health.ts route
  app.get('/health', async () => ({ status: 'ok' }));

  await app.listen({ port: config.port, host: '0.0.0.0' });
  app.log.info(`API server listening on port ${config.port}`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
