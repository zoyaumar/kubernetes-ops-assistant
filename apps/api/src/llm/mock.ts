/**
 * Mock LLM provider for tests.
 *
 * Returns deterministic responses without calling any external API.
 * Allows retrieval evaluation to run without LLM API keys.
 */

import type { LLMMessage, LLMProvider, LLMResponse } from './provider.js';

export class MockLLMProvider implements LLMProvider {
  readonly name = 'mock';

  private readonly _response: string;

  constructor(response = 'Mock LLM response') {
    this._response = response;
  }

  async chat(_messages: LLMMessage[], _maxTokens?: number): Promise<LLMResponse> {
    return {
      content: this._response,
      usage: { promptTokens: 0, completionTokens: 0, totalTokens: 0 },
    };
  }
}
