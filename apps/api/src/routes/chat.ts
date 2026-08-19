/**
 * Chat routes — the primary user-facing API.
 *
 * POST /api/v1/conversations/:conversationId/messages
 *   Body: { content: string, cluster_id: string, context?: { namespace?: string } }
 *   Response: { answer, confidence, citations, timeline }
 *
 * Pipeline per request:
 *   1. Validate input (Zod schema).
 *   2. Extract intent + time range from the user question.
 *   3. Run hybrid retrieval (SQL filters + pgvector).
 *   4. Build grounded prompt from retrieved evidence.
 *   5. Call LLM provider (Groq by default).
 *   6. Parse response and extract citations.
 *   7. Persist message + citations to DB.
 *   8. Return structured response.
 *
 * Rate limiting: applied to prevent LLM cost explosion.
 *
 * TODO(week-5): implement
 */

import type { FastifyInstance } from 'fastify';

export async function chatRoutes(app: FastifyInstance): Promise<void> {
  // TODO(week-5): POST /conversations/:conversationId/messages
}
