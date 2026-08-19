#!/usr/bin/env bash
set -euo pipefail
NAMESPACE="k8s-ops"
echo "Starting port-forwards..."
kubectl port-forward -n "${NAMESPACE}" svc/api 3000:3000 &
kubectl port-forward -n "${NAMESPACE}" svc/nats 4222:4222 &
kubectl port-forward -n "${NAMESPACE}" svc/grafana 3001:3000 &
wait
