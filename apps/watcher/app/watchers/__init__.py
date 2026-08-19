"""
Watcher coroutines — one per Kubernetes resource type.

Each watcher runs an infinite async loop using the Kubernetes watch API.
On reconnect it uses the last resourceVersion to resume without missing events.
"""
