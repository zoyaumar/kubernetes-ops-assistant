/**
 * Cluster data query routes.
 *
 * GET /api/v1/clusters
 * GET /api/v1/clusters/:clusterId
 * GET /api/v1/clusters/:clusterId/events
 * GET /api/v1/clusters/:clusterId/resources
 *
 * Supports filters: namespace, resourceType, eventType, severity, startTime, endTime.
 *
 * These routes provide structured (SQL) access to cluster data.
 * The chat endpoint uses RAG — these routes are for direct inspection.
 *
 * TODO(week-5): implement
 */

import type { FastifyInstance } from 'fastify';

export async function clusterRoutes(app: FastifyInstance): Promise<void> {
  // TODO(week-5): implement
}
