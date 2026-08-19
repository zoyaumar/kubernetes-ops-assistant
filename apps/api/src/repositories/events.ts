/**
 * Events repository (API side).
 *
 * Read-only access to cluster_events and documents for retrieval.
 * The indexer owns writes — the API only reads.
 *
 * Key queries:
 *   - Filter by cluster_id, namespace, resource_name, severity, time range.
 *   - Join with resources for enriched metadata.
 *   - Used by hybrid retrieval alongside pgvector search.
 *
 * TODO(week-5): implement using `postgres` npm package
 */

export {};
