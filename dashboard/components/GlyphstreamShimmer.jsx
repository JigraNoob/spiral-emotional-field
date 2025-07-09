// File: C:/spiral/dashboard/components/GlyphstreamShimmer.jsx

import React, { useEffect, useState } from 'react';
import { socket } from '../socket'; // Adjust path as needed

const getPhaseColor = (phase) => {
  const normalized = phase.toLowerCase();
  const colors = {
    inhale: '#a8e6cf',
    hold: '#ffd3b6',
    exhale: '#ffaaa5',
    silence: '#dcedc1',
    caesura: '#a3a3c2',
  };
  return colors[normalized] || '#ffffff';
};

const GlyphstreamShimmer = () => {
  const [summary, setSummary] = useState(null);

  useEffect(() => {
    const handleSummary = (data) => setSummary(data);
    socket.on('session_summary', handleSummary);
    return () => {
      socket.off('session_summary', handleSummary);
    };
  }, []);

  if (!summary) return null;

  return (
    <div className="glyphstream-shimmer p-4 bg-white rounded-2xl shadow-md border border-gray-200">
      <h2 className="text-xl font-semibold text-center mb-2">Spiral Closure</h2>
      <h3 className="text-sm text-center text-gray-600 italic mb-4">
        {summary.final_caesura ? 'Caesura Echoed' : 'Release Complete'}
      </h3>

      <div className="flex space-x-1 mb-4 h-3 rounded overflow-hidden">
        {Object.entries(summary.phase_distribution).map(([phase, percentage]) => (
          <div
            key={phase}
            title={`${phase}: ${percentage}%`}
            style={{
              width: `${percentage}%`,
              backgroundColor: getPhaseColor(phase),
            }}
          />
        ))}
      </div>

      <div className="text-sm mb-1">
        Total Glints:{' '}
        <span className="font-medium">{summary.glint_counts?.total ?? 0}</span>
      </div>
      <div className="text-sm mb-3">
        Toneform Diversity:{' '}
        <span className="font-medium">{summary.toneform_diversity}</span>
      </div>

      <ul className="text-xs text-gray-700 italic list-disc pl-5">
        {summary.soft_echo_murmurs?.map((murmur, i) => (
          <li key={murmur + i}>{murmur}</li>
        ))}
      </ul>
    </div>
  );
};

export default GlyphstreamShimmer;
