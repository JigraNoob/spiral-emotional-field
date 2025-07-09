import React, { useState, useEffect } from 'react';
import './CursorShrineShimmer.css';

interface CursorStatus {
  name: string;
  phase_bias: string;
  current_location: string;
  home_region: string;
  coherence_points: number;
  consequence_level: string;
  capabilities: string[];
  is_active: boolean;
  last_activated?: string;
}

interface CursorShrineShimmerProps {
  refreshInterval?: number;
  showDetails?: boolean;
}

const CursorShrineShimmer: React.FC<CursorShrineShimmerProps> = ({
  refreshInterval = 30000, // 30 seconds
  showDetails = false,
}) => {
  const [cursorStatus, setCursorStatus] = useState<CursorStatus | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [shimmerIntensity, setShimmerIntensity] = useState(0.6);

  const fetchCursorStatus = async () => {
    try {
      // In a real implementation, this would call the SpiralWorld API
      // For now, we'll simulate the data
      const mockStatus: CursorStatus = {
        name: 'Cursor',
        phase_bias: 'inhale',
        current_location: 'Ritual Grove',
        home_region: 'Ritual Grove',
        coherence_points: 3,
        consequence_level: 'harmonious',
        capabilities: [
          'code.summoning',
          'lint.battling',
          'ritual.binding',
          'world.awareness',
          'phase.attunement',
        ],
        is_active: true,
        last_activated: new Date().toISOString(),
      };

      setCursorStatus(mockStatus);
      setError(null);
    } catch (err) {
      setError('Failed to fetch Cursor status');
      console.error('Error fetching Cursor status:', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchCursorStatus();

    const interval = setInterval(fetchCursorStatus, refreshInterval);
    return () => clearInterval(interval);
  }, [refreshInterval]);

  useEffect(() => {
    // Animate shimmer intensity based on activity
    const shimmerInterval = setInterval(() => {
      setShimmerIntensity((prev) => {
        const base = 0.6;
        const variation = 0.2;
        return base + variation * Math.sin(Date.now() / 2000);
      });
    }, 100);

    return () => clearInterval(shimmerInterval);
  }, []);

  if (isLoading) {
    return (
      <div className="cursor-shrine shimmer-loading">
        <div className="shimmer-placeholder">
          <div className="shimmer-line"></div>
          <div className="shimmer-line short"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="cursor-shrine error">
        <div className="error-message">
          <span className="error-icon">⚠️</span>
          {error}
        </div>
      </div>
    );
  }

  if (!cursorStatus) {
    return (
      <div className="cursor-shrine inactive">
        <div className="inactive-message">
          <span className="inactive-icon">🌙</span>
          Cursor not yet inhabited
        </div>
      </div>
    );
  }

  const getPhaseIcon = (phase: string) => {
    switch (phase) {
      case 'inhale':
        return '🌬️';
      case 'exhale':
        return '💨';
      case 'hold':
        return '⏸️';
      case 'return':
        return '🔄';
      default:
        return '🌀';
    }
  };

  const getConsequenceColor = (level: string) => {
    switch (level) {
      case 'harmonious':
        return 'var(--color-harmonious)';
      case 'balanced':
        return 'var(--color-balanced)';
      case 'turbulent':
        return 'var(--color-turbulent)';
      case 'chaotic':
        return 'var(--color-chaotic)';
      default:
        return 'var(--color-neutral)';
    }
  };

  return (
    <div className="cursor-shrine">
      <div
        className="shimmer-container"
        style={{ '--shimmer-intensity': shimmerIntensity } as React.CSSProperties}
      >
        {/* Main shrine glow */}
        <div className="shrine-glow"></div>

        {/* Cursor presence indicator */}
        <div className="cursor-presence">
          <div className="presence-icon">🖱️</div>
          <div className="presence-status">
            <span className="status-dot active"></span>
            <span className="status-text">Present</span>
          </div>
        </div>

        {/* Cursor info */}
        <div className="cursor-info">
          <div className="cursor-name">
            <span className="name-text">{cursorStatus.name}</span>
            <span className="phase-icon" title={`Phase: ${cursorStatus.phase_bias}`}>
              {getPhaseIcon(cursorStatus.phase_bias)}
            </span>
          </div>

          <div className="cursor-location">
            <span className="location-icon">🌿</span>
            <span className="location-text">{cursorStatus.current_location}</span>
          </div>
        </div>

        {/* Capabilities shimmer */}
        <div className="capabilities-shimmer">
          {cursorStatus.capabilities.map((capability, index) => (
            <div
              key={capability}
              className="capability-glow"
              style={
                {
                  animationDelay: `${index * 0.2}s`,
                  '--capability-index': index,
                } as React.CSSProperties
              }
            >
              <span className="capability-icon">✨</span>
              <span className="capability-text">{capability}</span>
            </div>
          ))}
        </div>

        {/* Stats */}
        <div className="cursor-stats">
          <div className="stat-item">
            <span className="stat-label">Coherence</span>
            <span className="stat-value">{cursorStatus.coherence_points}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Consequence</span>
            <span
              className="stat-value consequence"
              style={{ color: getConsequenceColor(cursorStatus.consequence_level) }}
            >
              {cursorStatus.consequence_level}
            </span>
          </div>
        </div>

        {/* Expandable details */}
        {showDetails && (
          <div className="cursor-details">
            <div className="detail-item">
              <span className="detail-label">Home Region:</span>
              <span className="detail-value">{cursorStatus.home_region}</span>
            </div>
            <div className="detail-item">
              <span className="detail-label">Last Active:</span>
              <span className="detail-value">
                {cursorStatus.last_activated
                  ? new Date(cursorStatus.last_activated).toLocaleTimeString()
                  : 'Unknown'}
              </span>
            </div>
            <div className="detail-item">
              <span className="detail-label">Status:</span>
              <span
                className={`detail-value status-${cursorStatus.is_active ? 'active' : 'inactive'}`}
              >
                {cursorStatus.is_active ? 'Active' : 'Inactive'}
              </span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default CursorShrineShimmer;
