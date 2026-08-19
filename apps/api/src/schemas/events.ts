/**
 * Zod schemas for cluster event query parameters and responses.
 */

import { z } from 'zod';

export const EventFilterSchema = z.object({
  namespace: z.string().optional(),
  resource: z.string().optional(),
  resourceType: z.string().optional(),
  eventType: z.string().optional(),
  severity: z.enum(['Warning', 'Normal']).optional(),
  startTime: z.string().datetime().optional(),
  endTime: z.string().datetime().optional(),
});

export type EventFilter = z.infer<typeof EventFilterSchema>;
