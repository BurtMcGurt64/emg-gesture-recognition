import React, { useState, useEffect } from 'react';
import './App.css';
import EMGChart from './components/EMGChart';
import DataStats from './components/DataStats';
import GestureSelector from './components/GestureSelector';

function App() {
  const [selectedGesture, setSelectedGesture] = useState('CLENCH');
  const [emgData, setEmgData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const gestures = {
    'CLENCH': 'gesture0_session1.csv',
    'DOWN': 'gesture1_session1.csv',
    'RELAX': 'gesture2_session1.csv',
    'UP': 'gesture3_session1.csv',
  };

  useEffect(() => {
    loadEMGData(selectedGesture);
  }, [selectedGesture]);

  const loadEMGData = async (gesture) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(gestures[gesture]);
      if (!response.ok) {
        throw new Error(`Failed to load ${gesture} data`);
      }
      
      const csvText = await response.text();
      const lines = csvText.split('\n').filter(line => line.trim());
      const headers = lines[0].split(',');
      
      const data = lines.slice(1).map(line => {
        const values = line.split(',');
        return {
          timestamp: parseFloat(values[0]),
          emg_value: parseInt(values[1])
        };
      });

      setEmgData(data);
    } catch (err) {
      setError(err.message);
      console.error('Error loading EMG data:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="app-header">
        <div className="header-content">
          <h1 className="app-title">
            <span className="title-icon">⚡</span>
            EMG Visualizer
          </h1>
          <p className="app-subtitle">Real-time muscle activity monitoring</p>
        </div>
      </header>

      <main className="app-main">
        <div className="controls-section">
          <GestureSelector
            gestures={Object.keys(gestures)}
            selectedGesture={selectedGesture}
            onGestureChange={setSelectedGesture}
          />
        </div>

        {loading && (
          <div className="loading-container">
            <div className="loading-spinner"></div>
            <p>Loading EMG data...</p>
          </div>
        )}

        {error && (
          <div className="error-container">
            <p className="error-message">⚠️ {error}</p>
            <p className="error-hint">Make sure the CSV files are in the public folder</p>
          </div>
        )}

        {emgData && !loading && !error && (
          <div className="data-section">
            <DataStats data={emgData} gesture={selectedGesture} />
            <EMGChart data={emgData} gesture={selectedGesture} />
          </div>
        )}
      </main>

      <footer className="app-footer">
        <p>EMG Data Visualization Tool</p>
      </footer>
    </div>
  );
}

export default App; 