/**
 * Groq LLM provider.
 *
 * Uses the official groq-sdk.
 * Implements bounded retry with exponential backoff on 429 responses.
 *
 * Rate limits (as of plan date — subject to change):
 *   See https://console.groq.com/docs/rate-limits for current limits.
 *   Design for graceful degradation, not for a specific limit value.
 *
 * TODO(week-5): implement
 */

import type { LLMMessage, LLMProvider, LLMResponse } from './provider.js';

export class GroqProvider implements LLMProvider {
  readonly name = 'groq';

  constructor(
    private readonly apiKey: string,
    private readonly model: string,
  ) {}

  async chat(_messages: LLMMessage[], _maxTokens = 1024): Promise<LLMResponse> {
    // TODO(week-5): implement using groq-sdk
    // 1. Call groq.chat.completions.create()
    // 2. Handle 429 with exponential backoff (max 3 retries)
    // 3. Map to LLMResponse
    throw new Error('GroqProvider.chat not implemented');
  }
}
