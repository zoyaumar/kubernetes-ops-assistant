/**
 * Prompt builder — constructs the grounded LLM prompt from retrieved evidence.
 *
 * Prompt structure:
 *
 *   SYSTEM
 *   You are a Kubernetes operations assistant.
 *   Only make factual claims supported by the EVIDENCE below.
 *   Label inferences as inferences. Cite evidence IDs.
 *   If evidence is insufficient, say so explicitly.
 *
 *   QUESTION
 *   {user question}
 *
 *   FILTERS (applied during retrieval)
 *   cluster: {cluster_id}
 *   namespace: {namespace}
 *   time range: {start} – {end}
 *
 *   EVIDENCE
 *   [1] id={doc_id} type={source_type} time={occurred_at}
 *       {content}
 *   [2] ...
 *
 *   INSTRUCTIONS
 *   - Explain the most likely cause.
 *   - Cite evidence IDs (e.g. [1], [2]).
 *   - Provide a concise timeline.
 *   - Distinguish observed facts from inferences.
 *   - If evidence is insufficient, say: "Insufficient evidence to determine the root cause."
 *
 * TODO(week-5): implement
 */

export {};
