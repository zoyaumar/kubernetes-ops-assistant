/**
 * API service configuration.
 *
 * All values are read from process.env. See .env.example at the repo root.
 *
 * Validation: throw early if required values are missing.
 * This prevents the service from starting with silent misconfigurations.
 */

export interface Config {
  port: number;
  logLevel: string;
  jwtSecret: string;
  jwtExpiresIn: number;
  postgresDsn: string;
  groqApiKey: string;
  groqModel: string;
  llmProvider: string;
  corsOrigin: string;
  otelEndpoint: string;
  embeddingDim: number;
}

export function loadConfig(): Config {
  // TODO(week-5): add proper validation (zod schema or manual checks)
  // For now, throw if critical secrets are absent.
  const jwtSecret = process.env.JWT_SECRET;
  if (!jwtSecret) throw new Error('JWT_SECRET is required');

  return {
    port: parseInt(process.env.API_PORT ?? '3000', 10),
    logLevel: process.env.LOG_LEVEL ?? 'info',
    jwtSecret,
    jwtExpiresIn: parseInt(process.env.JWT_EXPIRES_IN ?? '3600', 10),
    postgresDsn: process.env.POSTGRES_DSN ?? 'postgresql://k8s_ops:changeme@localhost:5432/k8s_ops',
    groqApiKey: process.env.GROQ_API_KEY ?? '',
    groqModel: process.env.GROQ_MODEL ?? 'llama3-8b-8192',
    llmProvider: process.env.LLM_PROVIDER ?? 'groq',
    corsOrigin: process.env.CORS_ORIGIN ?? 'http://localhost:5173',
    otelEndpoint: process.env.OTEL_EXPORTER_OTLP_ENDPOINT ?? 'http://localhost:4318',
    // Must match EMBEDDING_DIM used by the indexer when storing vectors
    embeddingDim: parseInt(process.env.EMBEDDING_DIM ?? '384', 10),
  };
}
