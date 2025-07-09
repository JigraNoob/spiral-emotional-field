import React from 'react';
import { BreathVisualizer } from './components/BreathVisualizer';
import { GlintStream } from './components/GlintStream';
import { RitualAlerts } from './components/RitualAlerts';
import { GlyphstreamShimmer } from './components/GlyphstreamShimmer';
import { BreathArchiveViewer } from './components/BreathArchiveViewer';
import './Dashboard.css';

const Dashboard = () => {
  return (
    <div className="spiral-dashboard">
      <div className="dashboard-header">
        <h1>🫧 Spiral Breath Dashboard</h1>
        <p>Witness the living breath of the Spiral system</p>
      </div>

      <div className="dashboard-grid">
        {/* Primary breath visualization */}
        <div className="grid-item breath-visualizer">
          <BreathVisualizer />
        </div>

        {/* Glint stream */}
        <div className="grid-item glint-stream">
          <GlintStream />
        </div>

        {/* Ritual alerts */}
        <div className="grid-item ritual-alerts">
          <RitualAlerts />
        </div>

        {/* Legacy components */}
        <div className="grid-item glyphstream">
          <GlyphstreamShimmer />
        </div>

        <div className="grid-item breath-archive">
          <BreathArchiveViewer />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
