import React, { useEffect, useState } from 'react';
import './SettlingPanel.css';

const TONEFORM_GLYPHS = {
  'settling.ambience': '🌊',
  'urgent.flow': '⚡',
  'contemplative.stillness': '🧘',
  'emergent.creation': '🌱',
  'resting.quiet': '🌑',
  default: '🌀',
};

function getToneformGlyph(toneform) {
  return TONEFORM_GLYPHS[toneform] || TONEFORM_GLYPHS['default'];
}

function getConfidenceColor(confidence) {
  if (confidence >= 0.8) return '#4CAF50'; // Green
  if (confidence >= 0.6) return '#FF9800'; // Orange
  return '#F44336'; // Red
}

const SettlingPanel = () => {
  const [journeys, setJourneys] = useState([]);
  const [loading, setLoading] = useState(true);
  const [toneform, setToneform] = useState('');
  const [phase, setPhase] = useState('');
  const [minConfidence, setMinConfidence] = useState(0);
  const [hovered, setHovered] = useState(null);

  const fetchJourneys = async () => {
    setLoading(true);
    try {
      const params = [];
      if (toneform) params.push(`toneform=${encodeURIComponent(toneform)}`);
      if (phase) params.push(`phase=${encodeURIComponent(phase)}`);
      if (minConfidence > 0) params.push(`min_confidence=${minConfidence}`);
      const url = `/api/settling_journeys${params.length ? '?' + params.join('&') : ''}`;
      const res = await fetch(url);
      if (!res.ok) {
        throw new Error(`HTTP ${res.status}: ${res.statusText}`);
      }
      const data = await res.json();
      setJourneys(data);
    } catch (error) {
      console.error('Error fetching settling journeys:', error);
      setJourneys([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchJourneys(); /* eslint-disable-next-line */
  }, [toneform, phase, minConfidence]);

  // Collect unique toneforms and phases for dropdowns
  const uniqueToneforms = Array.from(new Set(journeys.map((j) => j.toneform))).filter(Boolean);
  const uniquePhases = Array.from(
    new Set(journeys.map((j) => (j.metadata && j.metadata.phase) || ''))
  ).filter(Boolean);

  return (
    <div className="settling-panel">
      <div className="settling-panel-header">
        <h2>📜 Settling Journeys</h2>
        <div className="settling-panel-filters">
          <select value={toneform} onChange={(e) => setToneform(e.target.value)}>
            <option value="">All Toneforms</option>
            {uniqueToneforms.map((tf) => (
              <option key={tf} value={tf}>
                {getToneformGlyph(tf)} {tf}
              </option>
            ))}
          </select>
          <select value={phase} onChange={(e) => setPhase(e.target.value)}>
            <option value="">All Phases</option>
            {uniquePhases.map((ph) => (
              <option key={ph} value={ph}>
                {ph}
              </option>
            ))}
          </select>
          <div className="confidence-slider">
            <label>Min Confidence: {minConfidence}</label>
            <input
              type="range"
              min="0"
              max="1"
              step="0.01"
              value={minConfidence}
              onChange={(e) => setMinConfidence(Number(e.target.value))}
            />
          </div>
        </div>
      </div>
      {loading ? (
        <div className="settling-panel-loading">🌀 Loading...</div>
      ) : journeys.length === 0 ? (
        <div className="settling-panel-loading">
          🌱 No settling journeys found. Begin your breathwork to see them here.
        </div>
      ) : (
        <table className="settling-panel-table">
          <thead>
            <tr>
              <th>Glyph</th>
              <th>Settled Path</th>
              <th>Confidence</th>
              <th>Toneform</th>
              <th>Phase</th>
              <th>Time</th>
            </tr>
          </thead>
          <tbody>
            {journeys.map((j, idx) => (
              <tr
                key={j.glint_id + idx}
                className="settling-panel-row"
                onMouseEnter={() => setHovered(idx)}
                onMouseLeave={() => setHovered(null)}
              >
                <td className="glyph-cell" style={{ fontSize: '1.5em' }}>
                  {getToneformGlyph(j.toneform)}
                </td>
                <td>{j.settled_to}</td>
                <td>
                  <span style={{ color: getConfidenceColor(j.confidence), fontWeight: 600 }}>
                    {j.confidence.toFixed(2)}
                  </span>
                </td>
                <td>{j.toneform}</td>
                <td>{(j.metadata && j.metadata.phase) || ''}</td>
                <td>{new Date(j.settled_at).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      {/* Hover metadata reveal */}
      {hovered !== null && journeys[hovered] && (
        <div className="settling-panel-hovercard">
          <h4>Glint Metadata</h4>
          <pre>{JSON.stringify(journeys[hovered].metadata, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default SettlingPanel;
