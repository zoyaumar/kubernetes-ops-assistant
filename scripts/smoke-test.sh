#!/usr/bin/env bash
set -euo pipefail
API_BASE="${API_BASE:-http://localhost:3000}"
echo "Smoke testing API at ${API_BASE}..."
curl -sf "${API_BASE}/health" && echo "  ✓ /health OK"
