/**
 * Zod schemas for chat request/response validation.
 *
 * TODO(week-5): implement full schemas
 */

import { z } from 'zod';

export const ChatMessageRequestSchema = z.object({
  content: z.string().min(1).max(4096),
  cluster_id: z.string().min(1),
  context: z
    .object({
      namespace: z.string().optional(),
    })
    .optional(),
});

export const CitationSchema = z.object({
  document_id: z.string().uuid(),
  source_type: z.string(),
  score: z.number().min(0).max(1),
});

export const TimelineEventSchema = z.object({
  timestamp: z.string().datetime(),
  description: z.string(),
});

export const ChatMessageResponseSchema = z.object({
  answer: z.string(),
  confidence: z.enum(['high', 'medium', 'low', 'insufficient']),
  citations: z.array(CitationSchema),
  timeline: z.array(TimelineEventSchema),
});

export type ChatMessageRequest = z.infer<typeof ChatMessageRequestSchema>;
export type ChatMessageResponse = z.infer<typeof ChatMessageResponseSchema>;
