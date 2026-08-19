#!/usr/bin/env bash
set -euo pipefail
NAMESPACE="payments"
echo "Creating namespace: ${NAMESPACE}"
kubectl create namespace "${NAMESPACE}" --dry-run=client -o yaml | kubectl apply -f -
echo "Seed complete."
