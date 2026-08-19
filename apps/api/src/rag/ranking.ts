/**
 * Evidence ranking / reranking.
 *
 * After merging SQL and vector results:
 * 1. Assign a combined score:
 *    - Vector similarity score (cosine distance converted to similarity)
 *    - Recency boost (more recent events score higher for incident questions)
 *    - Severity boost (Warning events score higher than Normal)
 *
 * 2. Sort descending by combined score.
 *
 * 3. Return top-K (configurable, default 10).
 *
 * Future: add a cross-encoder reranker for higher quality.
 *
 * TODO(week-5): implement
 */

export {};
