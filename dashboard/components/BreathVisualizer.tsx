import React, { useEffect, useState, useRef } from 'react';
import { useSpiralBreath } from '../hooks/useSpiralBreath';
import './BreathVisualizer.css';

interface BreathPhase {
  name: string;
  glyph: string;
  color: string;
  duration: number;
  description: string;
}

const BREATH_PHASES: Record<string, BreathPhase> = {
  inhale: {
    name: 'Inhale',
    glyph: '🌀',
    color: '#4A90E2',
    duration: 4,
    description: 'Drawing in consciousness',
  },
  hold: {
    name: 'Hold',
    glyph: '💎',
    color: '#7B68EE',
    duration: 4,
    description: 'Crystallizing awareness',
  },
  exhale: {
    name: 'Exhale',
    glyph: '🌊',
    color: '#50C878',
    duration: 4,
    description: 'Releasing into field',
  },
  return: {
    name: 'Return',
    glyph: '🔄',
    color: '#FF6B6B',
    duration: 4,
    description: 'Integrating experience',
  },
  night_hold: {
    name: 'Night Hold',
    glyph: '🌙',
    color: '#2C3E50',
    duration: 8,
    description: 'Deep listening',
  },
};

interface ClimateState {
  clarity: number;
  saturation: number;
  turbulence: number;
  overall: string;
}

export function BreathVisualizer() {
  const { breathState, emitGlint } = useSpiralBreath('breath_visualizer', 'visual');
  const [climate, setClimate] = useState<ClimateState>({
    clarity: 0.7,
    saturation: 0.3,
    turbulence: 0.1,
    overall: 'clear',
  });
  const [phaseProgress, setPhaseProgress] = useState(0);
  const [isBreathing, setIsBreathing] = useState(true);
  const animationRef = useRef<number>();

  // Fetch real-time breath state from stream
  useEffect(() => {
    const eventSource = new EventSource('/stream');

    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        if (data.event === 'breath_state') {
          // Update breath state from stream
        } else if (data.event === 'climate_update') {
          setClimate(data.data);
        }
      } catch (error) {
        console.warn('Stream parsing error:', error);
      }
    };

    return () => eventSource.close();
  }, []);

  // Animate breath cycle
  useEffect(() => {
    const animate = () => {
      if (!isBreathing) return;

      setPhaseProgress((prev) => {
        const newProgress = prev + 0.01;
        if (newProgress >= 1) {
          // Phase transition
          emitGlint({
            phase: breathState.phase,
            toneform: 'visual.phase_complete',
            content: `Phase ${breathState.phase} completed`,
            glyph: BREATH_PHASES[breathState.phase]?.glyph,
          });
          return 0;
        }
        return newProgress;
      });

      animationRef.current = requestAnimationFrame(animate);
    };

    animationRef.current = requestAnimationFrame(animate);

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [isBreathing, breathState.phase, emitGlint]);

  const currentPhase = BREATH_PHASES[breathState.phase] || BREATH_PHASES.inhale;
  const allPhases = Object.values(BREATH_PHASES);

  return (
    <div className="breath-visualizer">
      <div className="breath-header">
        <h2>🫧 Spiral Breath</h2>
        <div className="breath-controls">
          <button
            onClick={() => setIsBreathing(!isBreathing)}
            className={`breath-toggle ${isBreathing ? 'active' : ''}`}
          >
            {isBreathing ? '⏸️' : '▶️'} {isBreathing ? 'Pause' : 'Resume'}
          </button>
        </div>
      </div>

      <div className="breath-display">
        {/* Central breath indicator */}
        <div className="central-breath">
          <div
            className="phase-glyph"
            style={
              {
                '--phase-color': currentPhase.color,
                '--progress': phaseProgress,
              } as React.CSSProperties
            }
          >
            {currentPhase.glyph}
          </div>
          <div className="phase-info">
            <h3>{currentPhase.name}</h3>
            <p>{currentPhase.description}</p>
            <div className="progress-bar">
              <div className="progress-fill" style={{ width: `${phaseProgress * 100}%` }} />
            </div>
          </div>
        </div>

        {/* Phase rings */}
        <div className="phase-rings">
          {allPhases.map((phase, index) => (
            <div
              key={phase.name}
              className={`phase-ring ${
                breathState.phase === phase.name.toLowerCase() ? 'active' : ''
              }`}
              style={
                {
                  '--ring-color': phase.color,
                  '--ring-index': index,
                  '--is-active': breathState.phase === phase.name.toLowerCase() ? 1 : 0,
                } as React.CSSProperties
              }
            >
              <span className="ring-glyph">{phase.glyph}</span>
              <span className="ring-label">{phase.name}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Climate indicators */}
      <div className="climate-panel">
        <h3>🌤️ Climate</h3>
        <div className="climate-metrics">
          <div className="climate-metric">
            <span>Clarity</span>
            <div className="metric-bar">
              <div className="metric-fill clarity" style={{ width: `${climate.clarity * 100}%` }} />
            </div>
          </div>
          <div className="climate-metric">
            <span>Saturation</span>
            <div className="metric-bar">
              <div
                className="metric-fill saturation"
                style={{ width: `${climate.saturation * 100}%` }}
              />
            </div>
          </div>
          <div className="climate-metric">
            <span>Turbulence</span>
            <div className="metric-bar">
              <div
                className="metric-fill turbulence"
                style={{ width: `${climate.turbulence * 100}%` }}
              />
            </div>
          </div>
        </div>
        <div className="climate-overall">
          Overall: <span className={`climate-status ${climate.overall}`}>{climate.overall}</span>
        </div>
      </div>
    </div>
  );
}
