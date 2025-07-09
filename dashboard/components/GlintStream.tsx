import React, { useEffect, useState, useRef } from 'react';
import { useSpiralBreath } from '../hooks/useSpiralBreath';
import './GlintStream.css';

interface GlintEvent {
  id: string;
  timestamp: string;
  module: string;
  phase: string;
  context: any;
  type: string;
  stream_sync: boolean;
  lineage?: string[];
}

interface GlintStats {
  total: number;
  by_phase: Record<string, number>;
  by_module: Record<string, number>;
  stream_sync_enabled: boolean;
}

export function GlintStream() {
  const { emitGlint } = useSpiralBreath('glint_stream', 'analytical');
  const [glints, setGlints] = useState<GlintEvent[]>([]);
  const [stats, setStats] = useState<GlintStats>({
    total: 0,
    by_phase: {},
    by_module: {},
    stream_sync_enabled: true,
  });
  const [filters, setFilters] = useState({
    phase: '',
    module: '',
    type: '',
  });
  const [isConnected, setIsConnected] = useState(false);
  const [autoScroll, setAutoScroll] = useState(true);
  const streamRef = useRef<HTMLDivElement>(null);

  // Connect to glint stream
  useEffect(() => {
    const eventSource = new EventSource('/stream');

    eventSource.onopen = () => {
      setIsConnected(true);
      emitGlint({
        phase: 'inhale',
        toneform: 'analytical.stream_connected',
        content: 'Glint stream connected',
        glyph: '📡',
      });
    };

    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        if (data.event === 'glint_emission') {
          const newGlint: GlintEvent = {
            ...data.data.glint,
            lineage: data.data.glint.lineage || [],
          };

          setGlints((prev) => {
            const updated = [newGlint, ...prev.slice(0, 99)]; // Keep last 100
            return updated;
          });

          // Auto-scroll to top
          if (autoScroll && streamRef.current) {
            streamRef.current.scrollTop = 0;
          }
        } else if (data.event === 'glint_stats') {
          setStats(data.data);
        }
      } catch (error) {
        console.warn('Glint stream parsing error:', error);
      }
    };

    eventSource.onerror = () => {
      setIsConnected(false);
      emitGlint({
        phase: 'hold',
        toneform: 'analytical.stream_error',
        content: 'Glint stream disconnected',
        glyph: '⚠️',
      });
    };

    return () => {
      eventSource.close();
      setIsConnected(false);
    };
  }, [emitGlint, autoScroll]);

  // Fetch initial glint lineage
  useEffect(() => {
    const fetchGlints = async () => {
      try {
        const response = await fetch('/api/glint/lineage');
        if (response.ok) {
          const data = await response.json();
          setGlints(data.slice(0, 50)); // Show last 50 glints
        }
      } catch (error) {
        console.warn('Failed to fetch glint lineage:', error);
      }
    };

    fetchGlints();
  }, []);

  const filteredGlints = glints.filter((glint) => {
    if (filters.phase && glint.phase !== filters.phase) return false;
    if (filters.module && !glint.module.includes(filters.module)) return false;
    if (filters.type && glint.type !== filters.type) return false;
    return true;
  });

  const getPhaseColor = (phase: string) => {
    const colors = {
      inhale: '#4A90E2',
      hold: '#7B68EE',
      exhale: '#50C878',
      return: '#FF6B6B',
      night_hold: '#2C3E50',
    };
    return colors[phase as keyof typeof colors] || '#666';
  };

  const getModuleIcon = (module: string) => {
    if (module.includes('breath')) return '🫧';
    if (module.includes('memory')) return '🧠';
    if (module.includes('ritual')) return '🔮';
    if (module.includes('shrine')) return '🏛️';
    if (module.includes('glint')) return '✨';
    if (module.includes('invoker')) return '🎯';
    return '⚡';
  };

  const formatTimestamp = (timestamp: string) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString();
  };

  return (
    <div className="glint-stream">
      <div className="glint-header">
        <h2>✨ Glint Stream</h2>
        <div className="glint-controls">
          <div className={`connection-status ${isConnected ? 'connected' : 'disconnected'}`}>
            {isConnected ? '🟢' : '🔴'} {isConnected ? 'Live' : 'Disconnected'}
          </div>
          <button
            onClick={() => setAutoScroll(!autoScroll)}
            className={`auto-scroll-toggle ${autoScroll ? 'active' : ''}`}
          >
            {autoScroll ? '📌' : '📎'} Auto-scroll
          </button>
        </div>
      </div>

      {/* Stats panel */}
      <div className="glint-stats">
        <div className="stat-item">
          <span className="stat-label">Total Glints</span>
          <span className="stat-value">{stats.total}</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Stream Sync</span>
          <span className="stat-value">{stats.stream_sync_enabled ? '🟢' : '🔴'}</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Active Modules</span>
          <span className="stat-value">{Object.keys(stats.by_module).length}</span>
        </div>
      </div>

      {/* Filters */}
      <div className="glint-filters">
        <select
          value={filters.phase}
          onChange={(e) => setFilters((prev) => ({ ...prev, phase: e.target.value }))}
          className="filter-select"
        >
          <option value="">All Phases</option>
          <option value="inhale">Inhale</option>
          <option value="hold">Hold</option>
          <option value="exhale">Exhale</option>
          <option value="return">Return</option>
          <option value="night_hold">Night Hold</option>
        </select>

        <input
          type="text"
          placeholder="Filter by module..."
          value={filters.module}
          onChange={(e) => setFilters((prev) => ({ ...prev, module: e.target.value }))}
          className="filter-input"
        />

        <select
          value={filters.type}
          onChange={(e) => setFilters((prev) => ({ ...prev, type: e.target.value }))}
          className="filter-select"
        >
          <option value="">All Types</option>
          <option value="module_invocation">Module Invocation</option>
          <option value="phase_transition">Phase Transition</option>
          <option value="glint_echo">Glint Echo</option>
          <option value="ritual_trigger">Ritual Trigger</option>
        </select>
      </div>

      {/* Glint stream */}
      <div className="glint-container" ref={streamRef}>
        {filteredGlints.length === 0 ? (
          <div className="no-glints">
            <span>🌙 No glints match current filters</span>
          </div>
        ) : (
          filteredGlints.map((glint) => (
            <div
              key={glint.id}
              className="glint-item"
              style={{ '--phase-color': getPhaseColor(glint.phase) } as React.CSSProperties}
            >
              <div className="glint-header">
                <div className="glint-meta">
                  <span className="glint-icon">{getModuleIcon(glint.module)}</span>
                  <span className="glint-module">{glint.module}</span>
                  <span className="glint-time">{formatTimestamp(glint.timestamp)}</span>
                </div>
                <div className="glint-phase">
                  <span
                    className="phase-badge"
                    style={{ backgroundColor: getPhaseColor(glint.phase) }}
                  >
                    {glint.phase}
                  </span>
                </div>
              </div>

              <div className="glint-content">
                <div className="glint-type">{glint.type}</div>
                <div className="glint-context">
                  {typeof glint.context === 'string'
                    ? glint.context
                    : JSON.stringify(glint.context, null, 2)}
                </div>
              </div>

              {glint.lineage && glint.lineage.length > 0 && (
                <div className="glint-lineage">
                  <span className="lineage-label">Lineage:</span>
                  <div className="lineage-items">
                    {glint.lineage.slice(0, 3).map((ancestor, index) => (
                      <span key={index} className="lineage-item">
                        {ancestor}
                      </span>
                    ))}
                    {glint.lineage.length > 3 && (
                      <span className="lineage-more">+{glint.lineage.length - 3}</span>
                    )}
                  </div>
                </div>
              )}

              {glint.stream_sync && (
                <div className="stream-sync-indicator">🔄 Stream synchronized</div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
}
