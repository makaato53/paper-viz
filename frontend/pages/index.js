import { useState } from 'react';

export default function Home() {
  const [latex, setLatex] = useState('');
  const [result, setResult] = useState(null);

  const handleSubmit = async () => {
    const res = await fetch('/api/proxy', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ latex })
    });
    const data = await res.json();
    setResult(data);
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Paper Visualization</h1>
      <textarea
        rows={4}
        cols={50}
        placeholder="Paste LaTeX here"
        onChange={e => setLatex(e.target.value)}
      />
      <br/><br/>
      <button onClick={handleSubmit}>Visualize</button>

      {result && (
        <div style={{ marginTop: '2rem' }}>
          <h2>Summary</h2>
          <p>{result.summary}</p>
          <h2>Animation</h2>
          <video src={result.video_url} controls width="480" />
        </div>
      )}
    </div>
  );
}
