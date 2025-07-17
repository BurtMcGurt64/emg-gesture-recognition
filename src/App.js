import React, { useState, useEffect } from 'react';
import './App.css';
import EMGChart from './components/EMGChart';
import DataStats from './components/DataStats';
import GestureSelector from './components/GestureSelector';
import DataCollection from './components/DataCollection';
import FileUpload from './components/FileUpload';

function App() {
  const [selectedGesture, setSelectedGesture] = useState('CLENCH');
  const [emgData, setEmgData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('visualization');
  const [uploadedFiles, setUploadedFiles] = useState({});

  const gestures = {
    'CLENCH': 'gesture0_session1.csv',
    'DOWN': 'gesture1_session1.csv',
    'RELAX': 'gesture2_session1.csv',
    'UP': 'gesture3_session1.csv',
  };

  useEffect(() => {
    // Only load from public folder if no uploaded files are available
    if (!uploadedFiles[selectedGesture]) {
      loadEMGData(selectedGesture);
    } else {
      setEmgData(uploadedFiles[selectedGesture].data);
      setLoading(false);
      setError(null);
    }
  }, [selectedGesture, uploadedFiles]);

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

  const handleFileUpload = (fileData) => {
    setUploadedFiles(prev => ({
      ...prev,
      [fileData.gesture]: fileData
    }));
    
    // If this is the currently selected gesture, update the display
    if (selectedGesture === fileData.gesture) {
      setEmgData(fileData.data);
      setLoading(false);
      setError(null);
    }
  };

  return (
    <div className="App">
      <header className="app-header">
        <div className="header-content">
          <h1 className="app-title">
            EMG Visualizer
          </h1>
          <p className="app-subtitle">Real-time muscle activity monitoring & data collection</p>
        </div>
      </header>

      <main className="app-main">
        <div className="tab-navigation">
          <button
            className={`tab-button ${activeTab === 'visualization' ? 'active' : ''}`}
            onClick={() => setActiveTab('visualization')}
          >
            Data Visualization
          </button>
          <button
            className={`tab-button ${activeTab === 'collection' ? 'active' : ''}`}
            onClick={() => setActiveTab('collection')}
          >
            Data Collection
          </button>
        </div>

        {activeTab === 'visualization' && (
          <>
            <FileUpload onFileUpload={handleFileUpload} />
            
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
                <p className="error-message">{error}</p>
                <p className="error-hint">Upload CSV files or make sure they are in the public folder</p>
              </div>
            )}

            {emgData && !loading && !error && (
              <div className="data-section">
                <DataStats data={emgData} gesture={selectedGesture} />
                <EMGChart data={emgData} gesture={selectedGesture} />
              </div>
            )}
          </>
        )}

        {activeTab === 'collection' && (
          <DataCollection />
        )}
      </main>

      <footer className="app-footer">
        <p>EMG Data Visualization & Collection Tool</p>
      </footer>
    </div>
  );
}

export default App; 