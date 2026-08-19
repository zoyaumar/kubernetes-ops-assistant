#!/usr/bin/env bash
# Creates the local kind cluster.
#
# Usage: bash scripts/kind-up.sh
# Or:    make kind-up
#
# The cluster is named k8s-ops-assistant by default (matches CLUSTER_NAME in Makefile).
# A single-node cluster is used initially to minimize resource requirements.
# See docs/decisions/ADR-001-kind.md for the decision rationale.

set -euo pipefail

CLUSTER_NAME="${CLUSTER_NAME:-k8s-ops-assistant}"

if kind get clusters 2>/dev/null | grep -q "^${CLUSTER_NAME}$"; then
  echo "Cluster '${CLUSTER_NAME}' already exists. Skipping creation."
  exit 0
fi

echo "Creating kind cluster: ${CLUSTER_NAME}"
kind create cluster \
  --name "${CLUSTER_NAME}" \
  --config - <<EOF
apiVersion: kind.x-k8s.io/v1alpha4
kind: Cluster
nodes:
  - role: control-plane
    # TODO(multi-node): add worker nodes here when demonstrating scheduling features
EOF

echo "Cluster '${CLUSTER_NAME}' created."
echo "Kubeconfig context: kind-${CLUSTER_NAME}"
kubectl cluster-info --context "kind-${CLUSTER_NAME}"
