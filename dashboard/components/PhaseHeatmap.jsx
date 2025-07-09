import React, { useState, useEffect } from 'react';
import './PhaseHeatmap.css';

const PhaseHeatmap = ({ events }) => {
  const [phaseCounts, setPhaseCounts] = useState({
    inhale: 0,
    exhale: 0,
    caesura: 0,
  });

  const [phasePulses, setPhasePulses] = useState({
    inhale: 0,
    exhale: 0,
    caesura: 0,
  });

  // Update phase counts when events change
  useEffect(() => {
    const counts = {
      inhale: 0,
      exhale: 0,
      caesura: 0,
    };

    events.forEach((event) => {
      if (counts.hasOwnProperty(event.phase)) {
        counts[event.phase]++;
      }
    });

    setPhaseCounts(counts);
  }, [events]);

  // Pulse effect when new events arrive
  useEffect(() => {
    if (events.length > 0) {
      const latestEvent = events[0];
      if (phaseCounts.hasOwnProperty(latestEvent.phase)) {
        setPhasePulses((prev) => ({
          ...prev,
          [latestEvent.phase]: prev[latestEvent.phase] + 1,
        }));

        // Reset pulse after animation
        setTimeout(() => {
          setPhasePulses((prev) => ({
            ...prev,
            [latestEvent.phase]: prev[latestEvent.phase] - 1,
          }));
        }, 2000);
      }
    }
  }, [events.length]);

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

  const getPhaseIcon = (phase) => {
    switch (phase) {
      case 'inhale':
        return '↗️';
      case 'exhale':
        return '↘️';
      case 'caesura':
        return '⏸️';
      default:
        return '●';
    }
  };

  const totalEvents = Object.values(phaseCounts).reduce((sum, count) => sum + count, 0);
  const maxCount = Math.max(...Object.values(phaseCounts), 1);

  return (
    <div className="phase-heatmap">
      <div className="heatmap-header">
        <h3>🌬️ Breath Phase Heatmap</h3>
        <span className="total-events">Total: {totalEvents}</span>
      </div>

      <div className="phase-bars">
        {Object.entries(phaseCounts).map(([phase, count]) => {
          const percentage = totalEvents > 0 ? (count / maxCount) * 100 : 0;
          const isPulsing = phasePulses[phase] > 0;

          return (
            <div key={phase} className="phase-bar-container">
              <div className="phase-info">
                <span className="phase-icon">{getPhaseIcon(phase)}</span>
                <span className="phase-name">{phase}</span>
                <span className="phase-count">{count}</span>
              </div>

              <div className="phase-bar-wrapper">
                <div
                  className={`phase-bar ${isPulsing ? 'pulse' : ''}`}
                  style={{
                    width: `${percentage}%`,
                    backgroundColor: getPhaseColor(phase),
                  }}
                >
                  <div className="bar-glow" style={{ backgroundColor: getPhaseColor(phase) }} />
                </div>
              </div>
            </div>
          );
        })}
      </div>

      <div className="breath-meter">
        <div
          className="breath-arc inhale-arc"
          style={{
            transform: `scale(${1 + (phaseCounts.inhale / maxCount) * 0.3})`,
            opacity: 0.3 + (phaseCounts.inhale / maxCount) * 0.7,
          }}
        />
        <div
          className="breath-arc exhale-arc"
          style={{
            transform: `scale(${1 + (phaseCounts.exhale / maxCount) * 0.3})`,
            opacity: 0.3 + (phaseCounts.exhale / maxCount) * 0.7,
          }}
        />
        <div
          className="breath-arc caesura-arc"
          style={{
            transform: `scale(${1 + (phaseCounts.caesura / maxCount) * 0.3})`,
            opacity: 0.3 + (phaseCounts.caesura / maxCount) * 0.7,
          }}
        />
      </div>

      {totalEvents > 0 && (
        <div className="phase-dominance">
          {(() => {
            const dominantPhase = Object.entries(phaseCounts).reduce((a, b) =>
              phaseCounts[a[0]] > phaseCounts[b[0]] ? a : b
            )[0];

            return (
              <div className="dominance-indicator">
                <span>Dominant: </span>
                <span className="dominant-phase" style={{ color: getPhaseColor(dominantPhase) }}>
                  {dominantPhase} ({phaseCounts[dominantPhase]})
                </span>
              </div>
            );
          })()}
        </div>
      )}
    </div>
  );
};

export default PhaseHeatmap;
