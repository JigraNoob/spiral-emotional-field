import React, { useState, useEffect } from 'react';
import './SettlingJourneyPanel.css';

const SettlingJourneyPanel = () => {
  const [journeys, setJourneys] = useState([]);
  const [stats, setStats] = useState(null);
  const [recursionAnalysis, setRecursionAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');
  const [filterValue, setFilterValue] = useState('');

  useEffect(() => {
    loadSettlingJourneyData();
  }, []);

  const loadSettlingJourneyData = async () => {
    try {
      setLoading(true);

      // In a real implementation, this would fetch from your API
      // For now, we'll simulate the data structure
      const mockJourneys = [
        {
          glint_id: 'ΔPATH.042',
          invoked_from: './ritual/start',
          settled_to: './archive/soil',
          confidence: 0.88,
          toneform: 'settling.ambience',
          settled_at: '2025-07-08T03:22:13.487058Z',
          metadata: {
            breath_phase: 'exhale',
            soil_density: 'breathable',
            alternatives: ['./data', './shrine'],
            reasoning: 'Chose breathable soil for contemplative work',
            ancestor_glint: 'ΔRITUAL.001',
            context: 'Meditation session initiation',
          },
        },
        {
          glint_id: 'ΔCONTEMPLATIVE.001',
          invoked_from: './ritual/meditation',
          settled_to: './contemplative_space',
          confidence: 0.75,
          toneform: 'settling.ambience',
          settled_at: '2025-07-08T03:23:11.250500Z',
          metadata: {
            breath_phase: 'exhale',
            soil_density: 'breathable',
            alternatives: ['./archive', './shrine'],
            reasoning: 'Chose breathable soil for contemplative work',
          },
        },
        {
          glint_id: 'ΔURGENT.001',
          invoked_from: './tasks/urgent',
          settled_to: './data',
          confidence: 0.92,
          toneform: 'urgent.flow',
          settled_at: '2025-07-08T03:24:15.123456Z',
          metadata: {
            breath_phase: 'inhale',
            soil_density: 'thin',
            alternatives: ['./archive', './logs'],
            reasoning: 'Quick access needed for urgent task',
          },
        },
      ];

      setJourneys(mockJourneys);

      // Calculate stats
      const totalJourneys = mockJourneys.length;
      const avgConfidence = mockJourneys.reduce((sum, j) => sum + j.confidence, 0) / totalJourneys;

      const toneformCounts = {};
      const breathPhaseCounts = {};
      const soilDensityCounts = {};

      mockJourneys.forEach((journey) => {
        toneformCounts[journey.toneform] = (toneformCounts[journey.toneform] || 0) + 1;
        breathPhaseCounts[journey.metadata.breath_phase] =
          (breathPhaseCounts[journey.metadata.breath_phase] || 0) + 1;
        soilDensityCounts[journey.metadata.soil_density] =
          (soilDensityCounts[journey.metadata.soil_density] || 0) + 1;
      });

      setStats({
        total_journeys: totalJourneys,
        average_confidence: avgConfidence,
        toneform_distribution: toneformCounts,
        breath_phase_distribution: breathPhaseCounts,
        soil_density_distribution: soilDensityCounts,
      });

      // Calculate recursion analysis
      const settlementCounts = {};
      mockJourneys.forEach((journey) => {
        settlementCounts[journey.settled_to] = (settlementCounts[journey.settled_to] || 0) + 1;
      });

      const repeatSettlements = Object.fromEntries(
        Object.entries(settlementCounts).filter(([_, count]) => count > 1)
      );

      setRecursionAnalysis({
        total_repeat_settlements: Object.keys(repeatSettlements).length,
        repeat_settlements: repeatSettlements,
        low_confidence_clusters: [],
      });
    } catch (error) {
      console.error('Error loading settling journey data:', error);
    } finally {
      setLoading(false);
    }
  };

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.8) return '#4CAF50'; // Green
    if (confidence >= 0.6) return '#FF9800'; // Orange
    return '#F44336'; // Red
  };

  const getToneformIcon = (toneform) => {
    switch (toneform) {
      case 'settling.ambience':
        return '🌊';
      case 'urgent.flow':
        return '⚡';
      case 'contemplative.stillness':
        return '🧘';
      default:
        return '🌀';
    }
  };

  const getBreathPhaseIcon = (phase) => {
    switch (phase) {
      case 'inhale':
        return '🌬️';
      case 'hold':
        return '⏸️';
      case 'exhale':
        return '💨';
      case 'caesura':
        return '⏸️';
      default:
        return '🌬️';
    }
  };

  const getSoilDensityIcon = (density) => {
    switch (density) {
      case 'breathable':
        return '🌱';
      case 'thin':
        return '🌿';
      case 'void':
        return '🌫️';
      default:
        return '🌱';
    }
  };

  const filteredJourneys = journeys.filter((journey) => {
    if (filter === 'all') return true;
    if (filter === 'toneform' && filterValue) return journey.toneform === filterValue;
    if (filter === 'breath_phase' && filterValue)
      return journey.metadata.breath_phase === filterValue;
    if (filter === 'soil_density' && filterValue)
      return journey.metadata.soil_density === filterValue;
    if (filter === 'confidence' && filterValue)
      return journey.confidence >= parseFloat(filterValue);
    return true;
  });

  if (loading) {
    return (
      <div className="settling-journey-panel">
        <div className="loading">🌀 Loading settling journeys...</div>
      </div>
    );
  }

  return (
    <div className="settling-journey-panel">
      <div className="panel-header">
        <h2>📜 Settling Journeys</h2>
        <div className="filter-controls">
          <select
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className="filter-select"
          >
            <option value="all">All Journeys</option>
            <option value="toneform">By Toneform</option>
            <option value="breath_phase">By Breath Phase</option>
            <option value="soil_density">By Soil Density</option>
            <option value="confidence">By Confidence</option>
          </select>
          {filter !== 'all' && (
            <input
              type="text"
              placeholder="Filter value..."
              value={filterValue}
              onChange={(e) => setFilterValue(e.target.value)}
              className="filter-input"
            />
          )}
        </div>
      </div>

      {/* Statistics Overview */}
      {stats && (
        <div className="stats-overview">
          <div className="stat-card">
            <div className="stat-number">{stats.total_journeys}</div>
            <div className="stat-label">Total Journeys</div>
          </div>
          <div className="stat-card">
            <div className="stat-number">{stats.average_confidence.toFixed(3)}</div>
            <div className="stat-label">Avg Confidence</div>
          </div>
          <div className="stat-card">
            <div className="stat-number">{Object.keys(stats.toneform_distribution).length}</div>
            <div className="stat-label">Toneforms</div>
          </div>
        </div>
      )}

      {/* Recursion Analysis */}
      {recursionAnalysis && recursionAnalysis.total_repeat_settlements > 0 && (
        <div className="recursion-alert">
          <div className="alert-icon">🔄</div>
          <div className="alert-content">
            <strong>Recursion Detected:</strong> {recursionAnalysis.total_repeat_settlements} paths
            settled multiple times
          </div>
        </div>
      )}

      {/* Journeys List */}
      <div className="journeys-list">
        {filteredJourneys.map((journey, index) => (
          <div key={`${journey.glint_id}-${index}`} className="journey-card">
            <div className="journey-header">
              <div className="journey-id">{journey.glint_id}</div>
              <div
                className="confidence-badge"
                style={{ backgroundColor: getConfidenceColor(journey.confidence) }}
              >
                {journey.confidence.toFixed(2)}
              </div>
            </div>

            <div className="journey-path">
              <span className="path-arrow">→</span>
              <span className="settled-path">{journey.settled_to}</span>
            </div>

            <div className="journey-metadata">
              <div className="metadata-item">
                <span className="metadata-icon">{getToneformIcon(journey.toneform)}</span>
                <span className="metadata-label">{journey.toneform}</span>
              </div>
              <div className="metadata-item">
                <span className="metadata-icon">
                  {getBreathPhaseIcon(journey.metadata.breath_phase)}
                </span>
                <span className="metadata-label">{journey.metadata.breath_phase}</span>
              </div>
              <div className="metadata-item">
                <span className="metadata-icon">
                  {getSoilDensityIcon(journey.metadata.soil_density)}
                </span>
                <span className="metadata-label">{journey.metadata.soil_density}</span>
              </div>
            </div>

            {journey.metadata.reasoning && (
              <div className="journey-reasoning">
                <span className="reasoning-icon">💭</span>
                <span className="reasoning-text">{journey.metadata.reasoning}</span>
              </div>
            )}

            <div className="journey-timestamp">{new Date(journey.settled_at).toLocaleString()}</div>
          </div>
        ))}
      </div>

      {filteredJourneys.length === 0 && (
        <div className="no-journeys">📭 No journeys found matching the current filter.</div>
      )}
    </div>
  );
};

export default SettlingJourneyPanel;
