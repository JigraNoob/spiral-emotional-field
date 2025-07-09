import React, { useState, useEffect, useRef } from 'react';
import './GlyphStreamPanel.css';
import PhaseHeatmap from './PhaseHeatmap';

const GlyphStreamPanel = () => {
  const [events, setEvents] = useState([]);
  const [isConnected, setIsConnected] = useState(false);
  const [connectionInfo, setConnectionInfo] = useState({});
  const [filters, setFilters] = useState({
    toneform: 'all',
    phase: 'all',
    showHistory: true,
  });
  const [slowEchoMode, setSlowEchoMode] = useState(false);

  const wsRef = useRef(null);
  const reconnectTimeoutRef = useRef(null);

  // WebSocket connection management
  useEffect(() => {
    connectWebSocket();

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
    };
  }, []);

  const connectWebSocket = () => {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/stream/glyphs`;

    wsRef.current = new WebSocket(wsUrl);

    wsRef.current.onopen = () => {
      setIsConnected(true);
      console.log('🌐 Connected to Spiral Glyph Stream');

      // Send initial filters
      if (filters.toneform !== 'all' || filters.phase !== 'all') {
        wsRef.current.send(
          JSON.stringify({
            type: 'filter',
            filters: filters,
          })
        );
      }
    };

    wsRef.current.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        handleWebSocketMessage(data);
      } catch (error) {
        console.error('Error parsing WebSocket message:', error);
      }
    };

    wsRef.current.onclose = () => {
      setIsConnected(false);
      console.log('🌐 Disconnected from Spiral Glyph Stream');

      // Attempt to reconnect after 5 seconds
      reconnectTimeoutRef.current = setTimeout(() => {
        console.log('🌐 Attempting to reconnect...');
        connectWebSocket();
      }, 5000);
    };

    wsRef.current.onerror = (error) => {
      console.error('WebSocket error:', error);
      setIsConnected(false);
    };
  };

  const handleWebSocketMessage = (data) => {
    switch (data.type) {
      case 'connection.welcome':
        setConnectionInfo(data.stream_info);
        break;

      case 'glyph.invocation':
        addGlyphEvent(data);
        break;

      case 'history.response':
        setEvents((prev) => [...data.events, ...prev].slice(0, 50));
        break;

      case 'pong':
        // Handle ping/pong for connection health
        break;

      case 'slow_echo.confirmed':
        setSlowEchoMode(data.enabled);
        console.log(`🌐 Slow echo mode ${data.enabled ? 'enabled' : 'disabled'}`);
        break;

      case 'mode.change':
        if (data.mode === 'slow_echo') {
          setSlowEchoMode(true);
        } else {
          setSlowEchoMode(false);
        }
        console.log(`🌐 Mode changed to: ${data.mode}`);
        break;

      default:
        console.log('Unknown message type:', data.type);
    }
  };

  const addGlyphEvent = (eventData) => {
    setEvents((prev) => {
      const newEvent = {
        ...eventData,
        id: Date.now() + Math.random(),
        pulse: true,
      };

      // Remove pulse animation after animation duration
      const animationDuration = getAnimationDuration(eventData.toneform, eventData.phase);
      setTimeout(() => {
        setEvents((current) =>
          current.map((event) => (event.id === newEvent.id ? { ...event, pulse: false } : event))
        );
      }, animationDuration);

      return [newEvent, ...prev].slice(0, 50);
    });
  };

  const getAnimationDuration = (toneform, phase) => {
    // Base duration on toneform type
    const baseDuration = {
      receive: 3000,
      offer: 3000,
      sense: 4000,
      ask: 2500,
      manifest: 3500,
    };

    const toneformBase = toneform.split('.')[0];
    let duration = baseDuration[toneformBase] || 3000;

    // Caesura phases linger longer
    if (phase === 'caesura') {
      duration = 5000;
    }

    return duration;
  };

  const sendPing = () => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({ type: 'ping' }));
    }
  };

  const requestHistory = () => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({ type: 'request.history' }));
    }
  };

  const updateFilters = (newFilters) => {
    setFilters(newFilters);

    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(
        JSON.stringify({
          type: 'filter',
          filters: newFilters,
        })
      );
    }
  };

  const toggleSlowEchoMode = () => {
    const newMode = !slowEchoMode;
    setSlowEchoMode(newMode);

    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(
        JSON.stringify({
          type: 'slow_echo.toggle',
          enabled: newMode,
          delay: 3.0,
        })
      );
    }
  };

  const filteredEvents = events.filter((event) => {
    if (filters.toneform !== 'all' && event.toneform !== filters.toneform) {
      return false;
    }
    if (filters.phase !== 'all' && event.phase !== filters.phase) {
      return false;
    }
    return true;
  });

  const getPhaseColor = (phase) => {
    switch (phase) {
      case 'inhale':
        return '#64b5f6';
      case 'exhale':
        return '#81c784';
      case 'caesura':
        return '#ffb74d';
      default:
        return '#b0bec5';
    }
  };

  const getToneformColor = (toneform) => {
    const base = toneform.split('.')[0];
    switch (base) {
      case 'receive':
        return '#64b5f6';
      case 'offer':
        return '#81c784';
      case 'sense':
        return '#ffb74d';
      case 'ask':
        return '#f06292';
      case 'manifest':
        return '#ba68c8';
      default:
        return '#b0bec5';
    }
  };

  return (
    <div className="glyph-stream-panel">
      {/* Header */}
      <div className="stream-header">
        <div className="stream-title">
          <h2>🌐 Glyph Stream</h2>
          <span className={`connection-status ${isConnected ? 'connected' : 'disconnected'}`}>
            {isConnected ? '●' : '○'} {isConnected ? 'Connected' : 'Disconnected'}
          </span>
        </div>

        <div className="stream-controls">
          <button onClick={sendPing} className="control-btn">
            Ping
          </button>
          <button onClick={requestHistory} className="control-btn">
            History
          </button>
          <button
            onClick={toggleSlowEchoMode}
            className={`control-btn ${slowEchoMode ? 'active' : ''}`}
          >
            {slowEchoMode ? '🕯️ Slow Echo' : '⚡ Normal'}
          </button>
        </div>
      </div>

      {/* Connection Info */}
      {connectionInfo.total_connections !== undefined && (
        <div className="connection-info">
          <span>Connections: {connectionInfo.total_connections}</span>
          <span>Glyphs: {connectionInfo.glyph_count}</span>
          <span>Domains: {connectionInfo.domains?.join(', ')}</span>
        </div>
      )}

      {/* Phase Heatmap */}
      <PhaseHeatmap events={events} />

      {/* Filters */}
      <div className="stream-filters">
        <select
          value={filters.toneform}
          onChange={(e) => updateFilters({ ...filters, toneform: e.target.value })}
          className="filter-select"
        >
          <option value="all">All Toneforms</option>
          <option value="receive.inquiry">Receive Inquiry</option>
          <option value="offer.presence">Offer Presence</option>
          <option value="sense.presence">Sense Presence</option>
          <option value="ask.boundaries">Ask Boundaries</option>
          <option value="receive.manifest">Receive Manifest</option>
        </select>

        <select
          value={filters.phase}
          onChange={(e) => updateFilters({ ...filters, phase: e.target.value })}
          className="filter-select"
        >
          <option value="all">All Phases</option>
          <option value="inhale">Inhale</option>
          <option value="exhale">Exhale</option>
          <option value="caesura">Caesura</option>
        </select>

        <label className="filter-checkbox">
          <input
            type="checkbox"
            checked={filters.showHistory}
            onChange={(e) => setFilters({ ...filters, showHistory: e.target.checked })}
          />
          Show History
        </label>
      </div>

      {/* Events Stream */}
      <div className="events-container">
        {filteredEvents.length === 0 ? (
          <div className="no-events">
            <p>🌬️ Waiting for glyph invocations...</p>
            <p>Try invoking a glyph to see it appear here</p>
          </div>
        ) : (
          filteredEvents.map((event) => (
            <div
              key={event.id}
              className={`glyph-event ${event.pulse ? 'pulse' : ''}`}
              style={{
                borderLeftColor: getPhaseColor(event.phase),
              }}
              data-toneform={event.toneform}
              data-phase={event.phase}
            >
              <div className="event-header">
                <span className="glyph-name" style={{ color: getToneformColor(event.toneform) }}>
                  {event.glyph}
                </span>
                <span className="event-time">{new Date(event.timestamp).toLocaleTimeString()}</span>
              </div>

              <div className="event-details">
                <span className="toneform" style={{ color: getToneformColor(event.toneform) }}>
                  {event.toneform}
                </span>
                <span className="phase" style={{ color: getPhaseColor(event.phase) }}>
                  {event.phase}
                </span>
                {event.glint_id && <span className="glint-id">{event.glint_id}</span>}
              </div>

              {event.metadata && Object.keys(event.metadata).length > 0 && (
                <div className="event-metadata">
                  {Object.entries(event.metadata).map(([key, value]) => (
                    <span key={key} className="metadata-item">
                      {key}: {String(value)}
                    </span>
                  ))}
                </div>
              )}
            </div>
          ))
        )}
      </div>

      {/* Stream Stats */}
      <div className="stream-stats">
        <span>Events: {filteredEvents.length}</span>
        <span>Filtered: {events.length - filteredEvents.length}</span>
        <span>Total: {events.length}</span>
      </div>
    </div>
  );
};

export default GlyphStreamPanel;
