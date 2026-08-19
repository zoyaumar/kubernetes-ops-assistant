/**
 * Conversation management routes.
 *
 * POST /api/v1/conversations         — create new conversation
 * GET  /api/v1/conversations         — list user's conversations
 * GET  /api/v1/conversations/:id     — get conversation + messages
 *
 * TODO(week-5): implement
 */

import type { FastifyInstance } from 'fastify';

export async function conversationRoutes(app: FastifyInstance): Promise<void> {
  // TODO(week-5): implement CRUD
}
