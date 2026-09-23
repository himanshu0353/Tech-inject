import { useState } from 'react';
import { Button } from './components/Button';

function App() {
  const [count, setCount] = useState(0);

  return (
    <div style={{ padding: 40, fontFamily: 'sans-serif' }}>
      <h1>Consumer Project Integration Test</h1>
      <p>Component installed via Tech Inject CLI</p>

      <div style={{ marginTop: 20 }}>
        <Button variant="primary" onClick={() => setCount((c) => c + 1)}>
          Clicked {count} times
        </Button>
      </div>
    </div>
  );
}

export default App;
