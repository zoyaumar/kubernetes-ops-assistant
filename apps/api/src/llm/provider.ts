/**
 * LLM provider abstraction.
 *
 * Defines the interface that all LLM backends must implement.
 * The rest of the application only knows about LLMProvider —
 * never about Groq, OpenAI, or Anthropic directly.
 *
 * Provider implementations:
 *   - GroqProvider (default, free tier)
 *   - MockProvider (for tests that should not call an LLM)
 *   - OpenAIProvider (future)
 *   - AnthropicProvider (future)
 *
 * Rate limiting
 * -------------
 * LLM requests must handle 429 responses with bounded exponential backoff.
 * Never retry infinitely. The orchestrator should surface a controlled error
 * to the user if all retries are exhausted.
 */

export interface LLMMessage {
  role: 'system' | 'user' | 'assistant';
  content: string;
}

export interface LLMResponse {
  content: string;
  usage: {
    promptTokens: number;
    completionTokens: number;
    totalTokens: number;
  };
}

export interface LLMProvider {
  readonly name: string;

  /**
   * Complete a chat conversation.
   *
   * @param messages - Ordered list of messages (system, user, assistant turns).
   * @param maxTokens - Maximum tokens in the completion.
   * @returns The assistant's response.
   * @throws LLMRateLimitError when rate limit is exceeded after retries.
   * @throws LLMError for other provider failures.
   */
  chat(messages: LLMMessage[], maxTokens?: number): Promise<LLMResponse>;
}

export class LLMError extends Error {
  constructor(
    message: string,
    public readonly provider: string,
    public readonly statusCode?: number,
  ) {
    super(message);
    this.name = 'LLMError';
  }
}

export class LLMRateLimitError extends LLMError {
  constructor(provider: string) {
    super('Rate limit exceeded', provider, 429);
    this.name = 'LLMRateLimitError';
  }
}
