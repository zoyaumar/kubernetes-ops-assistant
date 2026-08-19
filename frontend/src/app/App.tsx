/**
 * Root application component.
 *
 * TODO(week-6): implement full routing:
 *   /login          — LoginPage
 *   /               — Dashboard (protected)
 *   /chat           — ChatPage (protected)
 *   /clusters/:id   — ClusterDetailPage (protected)
 */

const App = () => {
  return (
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%' }}>
      <h1 style={{ color: 'var(--color-accent)', fontFamily: 'var(--font-sans)' }}>
        ⎈ Kubernetes Ops Assistant
      </h1>
    </div>
  );
};

export default App;
