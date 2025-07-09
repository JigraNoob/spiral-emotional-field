import React, { useEffect, useState } from 'react';
import { useSpiralBreath } from '../hooks/useSpiralBreath';
import './RitualAlerts.css';

interface RitualAlert {
  id: string;
  timestamp: string;
  ritual_name: string;
  trigger_type: 'glint' | 'phase' | 'climate' | 'saturation';
  trigger_data: any;
  status: 'pending' | 'active' | 'completed' | 'failed';
  priority: 'low' | 'medium' | 'high' | 'critical';
  glyph: string;
  description: string;
}

interface RitualStats {
  total_triggered: number;
  active_rituals: number;
  completed_today: number;
  success_rate: number;
}

export function RitualAlerts() {
  const { emitGlint } = useSpiralBreath('ritual_alerts', 'ceremonial');
  const [alerts, setAlerts] = useState<RitualAlert[]>([]);
  const [stats, setStats] = useState<RitualStats>({
    total_triggered: 0,
    active_rituals: 0,
    completed_today: 0,
    success_rate: 0.95,
  });
  const [filter, setFilter] = useState<'all' | 'active' | 'completed'>('all');

  // Connect to ritual stream
  useEffect(() => {
    const eventSource = new EventSource('/stream');

    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        if (data.event === 'ritual_triggered') {
          const newAlert: RitualAlert = {
            id: data.data.id,
            timestamp: data.data.timestamp,
            ritual_name: data.data.ritual_name,
            trigger_type: data.data.trigger_type,
            trigger_data: data.data.trigger_data,
            status: 'pending',
            priority: data.data.priority || 'medium',
            glyph: data.data.glyph || '🔮',
            description: data.data.description,
          };

          setAlerts((prev) => [newAlert, ...prev.slice(0, 49)]); // Keep last 50

          emitGlint({
            phase: 'inhale',
            toneform: 'ceremonial.ritual_alert',
            content: `Ritual triggered: ${newAlert.ritual_name}`,
            glyph: newAlert.glyph,
          });
        } else if (data.event === 'ritual_status_update') {
          setAlerts((prev) =>
            prev.map((alert) =>
              alert.id === data.data.id ? { ...alert, status: data.data.status } : alert
            )
          );
        } else if (data.event === 'ritual_stats') {
          setStats(data.data);
        }
      } catch (error) {
        console.warn('Ritual stream parsing error:', error);
      }
    };

    return () => eventSource.close();
  }, [emitGlint]);

  // Fetch initial ritual alerts
  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        const response = await fetch('/api/ritual/alerts');
        if (response.ok) {
          const data = await response.json();
          setAlerts(data.slice(0, 20));
        }
      } catch (error) {
        console.warn('Failed to fetch ritual alerts:', error);
      }
    };

    fetchAlerts();
  }, []);

  const filteredAlerts = alerts.filter((alert) => {
    if (filter === 'all') return true;
    if (filter === 'active') return alert.status === 'active' || alert.status === 'pending';
    if (filter === 'completed') return alert.status === 'completed';
    return true;
  });

  const getPriorityColor = (priority: string) => {
    const colors = {
      low: '#50C878',
      medium: '#FFD700',
      high: '#FF8C00',
      critical: '#FF6B6B',
    };
    return colors[priority as keyof typeof colors] || '#666';
  };

  const getStatusIcon = (status: string) => {
    const icons = {
      pending: '⏳',
      active: '🔄',
      completed: '✅',
      failed: '❌',
    };
    return icons[status as keyof typeof icons] || '❓';
  };

  const getTriggerIcon = (triggerType: string) => {
    const icons = {
      glint: '✨',
      phase: '🫧',
      climate: '🌤️',
      saturation: '💎',
    };
    return icons[triggerType as keyof typeof icons] || '⚡';
  };

  const formatTimestamp = (timestamp: string) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString();
  };

  const handleRitualAction = async (alertId: string, action: string) => {
    try {
      const response = await fetch(`/api/ritual/${action}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ritual_id: alertId }),
      });

      if (response.ok) {
        emitGlint({
          phase: 'hold',
          toneform: 'ceremonial.ritual_action',
          content: `Ritual ${action}: ${alertId}`,
          glyph: '🔮',
        });
      }
    } catch (error) {
      console.warn(`Failed to ${action} ritual:`, error);
    }
  };

  return (
    <div className="ritual-alerts">
      <div className="ritual-header">
        <h2>🔮 Ritual Alerts</h2>
        <div className="ritual-controls">
          <select
            value={filter}
            onChange={(e) => setFilter(e.target.value as any)}
            className="filter-select"
          >
            <option value="all">All Alerts</option>
            <option value="active">Active</option>
            <option value="completed">Completed</option>
          </select>
        </div>
      </div>

      {/* Stats panel */}
      <div className="ritual-stats">
        <div className="stat-item">
          <span className="stat-label">Total Triggered</span>
          <span className="stat-value">{stats.total_triggered}</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Active</span>
          <span className="stat-value">{stats.active_rituals}</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Completed Today</span>
          <span className="stat-value">{stats.completed_today}</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Success Rate</span>
          <span className="stat-value">{(stats.success_rate * 100).toFixed(1)}%</span>
        </div>
      </div>

      {/* Alerts list */}
      <div className="alerts-container">
        {filteredAlerts.length === 0 ? (
          <div className="no-alerts">
            <span>🌙 No ritual alerts match current filter</span>
          </div>
        ) : (
          filteredAlerts.map((alert) => (
            <div
              key={alert.id}
              className={`alert-item ${alert.status} ${alert.priority}`}
              style={
                { '--priority-color': getPriorityColor(alert.priority) } as React.CSSProperties
              }
            >
              <div className="alert-header">
                <div className="alert-meta">
                  <span className="alert-glyph">{alert.glyph}</span>
                  <span className="alert-name">{alert.ritual_name}</span>
                  <span className="alert-time">{formatTimestamp(alert.timestamp)}</span>
                </div>
                <div className="alert-status">
                  <span className="status-icon">{getStatusIcon(alert.status)}</span>
                  <span className="status-text">{alert.status}</span>
                </div>
              </div>

              <div className="alert-content">
                <div className="alert-description">{alert.description}</div>
                <div className="alert-trigger">
                  <span className="trigger-icon">{getTriggerIcon(alert.trigger_type)}</span>
                  <span className="trigger-type">{alert.trigger_type}</span>
                  <span className="trigger-data">
                    {typeof alert.trigger_data === 'string'
                      ? alert.trigger_data
                      : JSON.stringify(alert.trigger_data, null, 2)}
                  </span>
                </div>
              </div>

              <div className="alert-actions">
                {alert.status === 'pending' && (
                  <>
                    <button
                      onClick={() => handleRitualAction(alert.id, 'activate')}
                      className="action-btn activate"
                    >
                      🔮 Activate
                    </button>
                    <button
                      onClick={() => handleRitualAction(alert.id, 'dismiss')}
                      className="action-btn dismiss"
                    >
                      ❌ Dismiss
                    </button>
                  </>
                )}
                {alert.status === 'active' && (
                  <button
                    onClick={() => handleRitualAction(alert.id, 'complete')}
                    className="action-btn complete"
                  >
                    ✅ Complete
                  </button>
                )}
                {alert.status === 'completed' && (
                  <span className="completion-time">
                    Completed at {formatTimestamp(alert.timestamp)}
                  </span>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
