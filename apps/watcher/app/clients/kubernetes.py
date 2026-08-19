"""Kubernetes API client wrapper.

Abstracts the official `kubernetes` Python client so that:
* Tests can inject a fake client.
* Connection/auth logic is in one place.
* In-cluster config is used inside Kubernetes; kubeconfig is used locally.

Authentication
--------------
The pod runs with a dedicated ServiceAccount (k8s-ops-watcher) that has
a namespace-scoped Role granting read-only access to:
  pods, pods/log, events, deployments.

See k8s/base/rbac.yaml for the RBAC definitions.
"""

from __future__ import annotations

# TODO(week-2): implement
# Outline:
#
# class KubernetesClient:
#     def __init__(self, in_cluster: bool = True) -> None:
#         # load_incluster_config() or load_kube_config()
#         self._core = client.CoreV1Api()
#         self._apps = client.AppsV1Api()
#
#     def core(self) -> client.CoreV1Api: ...
#     def apps(self) -> client.AppsV1Api: ...
