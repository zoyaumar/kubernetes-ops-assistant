/**
 * Hybrid retrieval: combines SQL structured filters with pgvector similarity search.
 *
 * Retrieval strategy
 * ------------------
 * 1. SQL filters (fast, exact):
 *    - cluster_id, namespace, resource_name, event_type
 *    - time range (occurred_at BETWEEN start AND end)
 *    - severity (Warning > Normal)
 *
 * 2. Vector search (semantic):
 *    - Embed the user question.
 *    - Use pgvector cosine similarity to find top-K documents.
 *    - Apply the same time + cluster filters to avoid cross-cluster contamination.
 *
 * 3. Merge: combine results, remove duplicates (by document_id).
 *
 * Design note
 * -----------
 * Always filter by cluster_id and time range BEFORE the vector search.
 * This prevents semantically similar events from unrelated clusters
 * or time periods from dominating the answer.
 *
 * TODO(week-5): implement
 */

export {};
