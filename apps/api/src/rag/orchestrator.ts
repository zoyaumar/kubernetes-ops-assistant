/**
 * RAG orchestrator — coordinates the full retrieval + generation pipeline.
 *
 * Pipeline:
 *   user question
 *     ↓ intent + time extraction
 *     ↓ structured filters (namespace, resource, time range)
 *     ↓ query embedding
 *     ↓ hybrid retrieval (SQL + pgvector in parallel)
 *     ↓ merge + deduplicate
 *     ↓ rerank
 *     ↓ top-K evidence
 *     ↓ prompt builder
 *     ↓ LLM provider
 *     ↓ answer + citations
 *
 * Design principle: the LLM only sees retrieved evidence.
 * It should never invent cluster facts.
 *
 * TODO(week-5): implement
 */

export {};
