import React, { useState, useMemo } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Brush } from 'recharts';
import './EMGChart.css';

const EMGChart = ({ data, gesture }) => {
  const [showFullData, setShowFullData] = useState(false);
  
  // Sample data for better performance (show every nth point)
  const chartData = useMemo(() => {
    if (!data) return [];
    
    const step = showFullData ? 1 : Math.max(1, Math.floor(data.length / 1000));
    return data.filter((_, index) => index % step === 0);
  }, [data, showFullData]);

  const getGestureColor = (gesture) => {
    switch (gesture) {
      case 'CLENCH': return '#d32f2f';  // Dark red
      case 'DOWN': return '#1976d2';     // Blue
      case 'RELAX': return '#388e3c';    // Green
      case 'UP': return '#f57c00';       // Orange
      default: return '#757575';         // Gray
    }
  };

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="custom-tooltip">
          <p className="tooltip-time">Time: {label.toFixed(3)}s</p>
          <p className="tooltip-value">EMG: {payload[0].value}</p>
        </div>
      );
    }
    return null;
  };

  if (!data || data.length === 0) {
    return (
      <div className="chart-container">
        <div className="no-data">No EMG data available</div>
      </div>
    );
  }

  return (
    <div className="chart-container">
      <div className="chart-header">
        <h3 className="chart-title">
          <span className="chart-icon">📈</span>
          {gesture} EMG Signal
        </h3>
        <div className="chart-controls">
          <button
            className={`control-button ${showFullData ? 'active' : ''}`}
            onClick={() => setShowFullData(!showFullData)}
          >
            {showFullData ? 'Show Sampled' : 'Show Full Data'}
          </button>
        </div>
      </div>
      
      <div className="chart-wrapper">
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255, 255, 255, 0.1)" />
            <XAxis 
              dataKey="timestamp" 
              stroke="#888"
              tick={{ fill: '#888', fontSize: 12 }}
              tickFormatter={(value) => `${value.toFixed(1)}s`}
            />
            <YAxis 
              stroke="#888"
              tick={{ fill: '#888', fontSize: 12 }}
              domain={['dataMin - 50', 'dataMax + 50']}
            />
            <Tooltip content={<CustomTooltip />} />
            <Brush 
              dataKey="timestamp" 
              height={30} 
              stroke={getGestureColor(gesture)}
              fill="rgba(255, 255, 255, 0.05)"
            />
            <Line
              type="monotone"
              dataKey="emg_value"
              stroke={getGestureColor(gesture)}
              strokeWidth={1.5}
              dot={false}
              activeDot={{ r: 4, fill: getGestureColor(gesture) }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
      
      <div className="chart-info">
        <div className="info-item">
          <span className="info-label">Data Points:</span>
          <span className="info-value">{chartData.length.toLocaleString()}</span>
        </div>
        <div className="info-item">
          <span className="info-label">Time Range:</span>
          <span className="info-value">
            {chartData[0]?.timestamp.toFixed(2)}s - {chartData[chartData.length - 1]?.timestamp.toFixed(2)}s
          </span>
        </div>
        <div className="info-item">
          <span className="info-label">Display Mode:</span>
          <span className="info-value">{showFullData ? 'Full Data' : 'Sampled'}</span>
        </div>
      </div>
    </div>
  );
};

export default EMGChart; 