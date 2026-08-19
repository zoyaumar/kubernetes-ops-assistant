/**
 * Request ID middleware.
 *
 * Assigns a unique ID to every request for traceability.
 * Propagated to:
 *   - Response header: X-Request-ID
 *   - Log fields: requestId
 *   - OTel span attributes
 *
 * TODO(week-5): implement as Fastify onRequest hook
 */

export {};
