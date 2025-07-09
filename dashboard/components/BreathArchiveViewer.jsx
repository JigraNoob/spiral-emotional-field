import React, { useState, useEffect } from 'react';
import { socket } from '../socket';

const BreathArchiveViewer = () => {
  const [archive, setArchive] = useState([]);

  useEffect(() => {
    // Fetch past session summaries from the server or local storage
    fetch('/api/session_archive')
      .then(response => response.json())
      .then(data => setArchive(data))
      .catch(error => console.error('Error fetching session archive:', error));

    // Listen for new session summaries
    socket.on('session_summary', (summary) => {
      setArchive(prevArchive => [summary, ...prevArchive]);
    });

    return () => socket.off('session_summary');
  }, []);

  return (
    <div className="breath-archive-viewer">
      <h2 className="text-2xl font-bold mb-4">Breath Archive</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {archive.map((summary, index) => (
          <div key={index} className="glyph-card p-4 bg-white rounded-lg shadow-md">
            <h3 className="text-lg font-semibold">{summary.final_caesura ? "Caesura Echoed" : "Release Complete"}</h3>
            <div className="flex space-x-1 mb-2 h-3 rounded overflow-hidden">
              {Object.entries(summary.phase_distribution).map(([phase, percentage]) => (
                <div
                  key={phase}
                  title={`${phase}: ${percentage}%`}
                  style={{ width: `${percentage}%`, backgroundColor: getPhaseColor(phase) }}
                />
              ))}
            </div>
            <div className="text-sm">Total Glints: <span className="font-medium">{summary.glint_counts.total}</span></div>
            <div className="text-sm">Toneform Diversity: <span className="font-medium">{summary.toneform_diversity}</span></div>
            <ul className="text-xs text-gray-700 mt-2 italic">
              {summary.soft_echo_murmurs.map((murmur, i) => (
                <li key={i}>• {murmur}</li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
};

const getPhaseColor = (phase) => ({
  inhale: '#a8e6cf',
  hold: '#ffd3b6',
  exhale: '#ffaaa5',
  silence: '#dcedc1',
  caesura: '#a3a3c2'
}[phase.toLowerCase()] || '#ffffff');

export default BreathArchiveViewer;