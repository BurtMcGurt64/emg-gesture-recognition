import React from 'react';
import './DataStats.css';

const DataStats = ({ data, gesture }) => {
  if (!data || data.length === 0) return null;

  const stats = {
    samples: data.length,
    duration: data[data.length - 1].timestamp - data[0].timestamp,
    minEMG: Math.min(...data.map(d => d.emg_value)),
    maxEMG: Math.max(...data.map(d => d.emg_value)),
    avgEMG: Math.round(data.reduce((sum, d) => sum + d.emg_value, 0) / data.length),
    startTime: data[0].timestamp,
    endTime: data[data.length - 1].timestamp,
  };

  const getStatusColor = (gesture) => {
    switch (gesture) {
      case 'CLENCH': return '#ff6b6b';
      case 'DOWN': return '#4ecdc4';
      case 'RELAX': return '#45b7d1';
      case 'UP': return '#96ceb4';
      default: return '#00d4ff';
    }
  };

  return (
    <div className="data-stats">
      <h3 className="stats-title">
        <span className="stats-icon">📊</span>
        {gesture} Statistics
      </h3>
      
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-value">{stats.samples.toLocaleString()}</div>
          <div className="stat-label">Samples</div>
        </div>
        
        <div className="stat-card">
          <div className="stat-value">{stats.duration.toFixed(2)}s</div>
          <div className="stat-label">Duration</div>
        </div>
        
        <div className="stat-card">
          <div className="stat-value">{stats.minEMG}</div>
          <div className="stat-label">Min EMG</div>
        </div>
        
        <div className="stat-card">
          <div className="stat-value">{stats.maxEMG}</div>
          <div className="stat-label">Max EMG</div>
        </div>
        
        <div className="stat-card">
          <div className="stat-value">{stats.avgEMG}</div>
          <div className="stat-label">Avg EMG</div>
        </div>
        
        <div className="stat-card">
          <div className="stat-value">{(stats.samples / stats.duration).toFixed(0)}</div>
          <div className="stat-label">Samples/s</div>
        </div>
      </div>
      
      <div className="time-range">
        <div className="time-item">
          <span className="time-label">Start:</span>
          <span className="time-value">{stats.startTime.toFixed(3)}s</span>
        </div>
        <div className="time-item">
          <span className="time-label">End:</span>
          <span className="time-value">{stats.endTime.toFixed(3)}s</span>
        </div>
      </div>
      
      <div 
        className="gesture-indicator"
        style={{ backgroundColor: getStatusColor(gesture) }}
      >
        <span className="indicator-text">{gesture}</span>
      </div>
    </div>
  );
};

export default DataStats; 