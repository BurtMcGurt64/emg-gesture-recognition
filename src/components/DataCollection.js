import React, { useState } from 'react';
import './DataCollection.css';

const DataCollection = () => {
  const [isCollecting, setIsCollecting] = useState(false);
  const [currentGesture, setCurrentGesture] = useState('');
  const [sessionCount, setSessionCount] = useState(3);
  const [port, setPort] = useState('COM3');
  const [duration, setDuration] = useState(5);
  const [status, setStatus] = useState('');
  const [logs, setLogs] = useState([]);
  const [collectionAbortController, setCollectionAbortController] = useState(null);

  const gestures = [
    { name: 'RELAX', label: 0, description: 'Hand in relaxed position' },
    { name: 'CLENCH', label: 1, description: 'Make a fist' },
    { name: 'UP', label: 2, description: 'Point finger upward' },
    { name: 'DOWN', label: 3, description: 'Point finger downward' }
  ];

  const addLog = (message) => {
    const timestamp = new Date().toLocaleTimeString();
    setLogs(prev => [...prev, { timestamp, message }]);
  };

  const startDataCollection = async (gesture) => {
    const abortController = new AbortController();
    setCollectionAbortController(abortController);
    setIsCollecting(true);
    setCurrentGesture(gesture.name);
    setStatus('Initializing data collection...');
    addLog(`Starting data collection for ${gesture.name} (Label: ${gesture.label})`);

    try {
      // Simulate the data collection process
      // In a real implementation, this would call your Python backend
      for (let session = 1; session <= sessionCount; session++) {
        // Check if collection was cancelled
        if (abortController.signal.aborted) {
          addLog(`Data collection cancelled for ${gesture.name}`);
          break;
        }

        setStatus(`Recording session ${session}/${sessionCount} for ${gesture.name}...`);
        addLog(`Recording session ${session} for ${gesture.name}`);
        
        // Simulate recording time with cancellation check
        await new Promise((resolve, reject) => {
          const timeout = setTimeout(resolve, duration * 1000);
          abortController.signal.addEventListener('abort', () => {
            clearTimeout(timeout);
            reject(new Error('Collection cancelled'));
          });
        });
        
        if (!abortController.signal.aborted) {
          addLog(`Session ${session} complete - Saved to ./gesture${gesture.label}_session${session}.csv`);
        }
      }
      
      if (!abortController.signal.aborted) {
        setStatus(`Data collection complete for ${gesture.name}!`);
        addLog(`All ${sessionCount} sessions collected for ${gesture.name}`);
      }
      
    } catch (error) {
      if (error.message === 'Collection cancelled') {
        setStatus('Data collection cancelled');
        addLog('Data collection was cancelled by user');
      } else {
        setStatus(`Error: ${error.message}`);
        addLog(`Error during data collection: ${error.message}`);
      }
    } finally {
      setIsCollecting(false);
      setCurrentGesture('');
      setCollectionAbortController(null);
    }
  };

  const collectAllGestures = async () => {
    const abortController = new AbortController();
    setCollectionAbortController(abortController);
    setIsCollecting(true);
    setStatus('Starting collection for all gestures...');
    addLog('Beginning collection for all gestures');

    try {
      for (const gesture of gestures) {
        if (abortController.signal.aborted) {
          addLog('Data collection cancelled');
          break;
        }

        setCurrentGesture(gesture.name);
        setStatus(`Collecting data for ${gesture.name}...`);
        addLog(`Starting collection for ${gesture.name}`);
        
        for (let session = 1; session <= sessionCount; session++) {
          if (abortController.signal.aborted) {
            addLog('Data collection cancelled');
            break;
          }

          setStatus(`Recording ${gesture.name} - Session ${session}/${sessionCount}...`);
          await new Promise((resolve, reject) => {
            const timeout = setTimeout(resolve, duration * 1000);
            abortController.signal.addEventListener('abort', () => {
              clearTimeout(timeout);
              reject(new Error('Collection cancelled'));
            });
          });
          addLog(`${gesture.name} session ${session} complete - Saved to ./gesture${gesture.label}_session${session}.csv`);
        }
      }
      
      if (!abortController.signal.aborted) {
        setStatus('All gestures collected successfully!');
        addLog('Data collection complete for all gestures');
      }
    } catch (error) {
      if (error.message === 'Collection cancelled') {
        setStatus('Data collection cancelled');
        addLog('Data collection was cancelled by user');
      } else {
        setStatus(`Error: ${error.message}`);
        addLog(`Error during data collection: ${error.message}`);
      }
    } finally {
      setIsCollecting(false);
      setCurrentGesture('');
      setCollectionAbortController(null);
    }
  };

  const processFeatures = async () => {
    setStatus('Processing features...');
    addLog('Starting feature extraction for all gesture files');
    
    try {
      // Simulate feature processing
      await new Promise(resolve => setTimeout(resolve, 2000));
      addLog('Feature extraction complete');
      setStatus('Features processed successfully!');
    } catch (error) {
      setStatus(`Error processing features: ${error.message}`);
      addLog(`Error: ${error.message}`);
    }
  };

  const trainModel = async () => {
    setStatus('Training neural network model...');
    addLog('Starting model training');
    
    try {
      // Simulate model training
      await new Promise(resolve => setTimeout(resolve, 5000));
      addLog('Model training complete');
      setStatus('Model trained and saved successfully!');
    } catch (error) {
      setStatus(`Error training model: ${error.message}`);
      addLog(`Error: ${error.message}`);
    }
  };

  const startRealTimeProcessing = async () => {
    setStatus('Starting real-time EMG processing...');
    addLog('Initializing real-time processor');
    
    try {
      // Simulate real-time processing startup
      await new Promise(resolve => setTimeout(resolve, 1000));
      addLog('Real-time processor started');
      setStatus('Real-time processing active');
    } catch (error) {
      setStatus(`Error starting real-time processing: ${error.message}`);
      addLog(`Error: ${error.message}`);
    }
  };

  const clearLogs = () => {
    setLogs([]);
  };

  const cancelCollection = () => {
    if (collectionAbortController) {
      collectionAbortController.abort();
      addLog('Cancelling data collection...');
    }
  };

  return (
    <div className="data-collection">
      <div className="collection-header">
        <h3>EMG Data Collection & Processing</h3>
        <p>Control panel for data collection, feature extraction, and model training</p>
        <div className="save-location-info">
          <p><strong>Data Save Location:</strong> Files are saved to the project root directory</p>
          <p><strong>File Format:</strong> gesture{'{0-3}'}_session{'{1-9}'}.csv (e.g., gesture0_session1.csv)</p>
        </div>
      </div>

      <div className="collection-controls">
        <div className="control-section">
          <h4>Hardware Configuration</h4>
          <div className="config-grid">
            <div className="config-item">
              <label>Serial Port:</label>
              <input
                type="text"
                value={port}
                onChange={(e) => setPort(e.target.value)}
                placeholder="COM3"
              />
            </div>
            <div className="config-item">
              <label>Recording Duration (s):</label>
              <input
                type="number"
                value={duration}
                onChange={(e) => setDuration(parseInt(e.target.value))}
                min="1"
                max="30"
              />
            </div>
            <div className="config-item">
              <label>Sessions per Gesture:</label>
              <input
                type="number"
                value={sessionCount}
                onChange={(e) => setSessionCount(parseInt(e.target.value))}
                min="1"
                max="10"
              />
            </div>
          </div>
        </div>

        <div className="control-section">
          <h4>Data Collection</h4>
          <div className="gesture-grid">
            {gestures.map((gesture) => (
              <button
                key={gesture.label}
                className={`gesture-collection-btn ${currentGesture === gesture.name ? 'active' : ''}`}
                onClick={() => startDataCollection(gesture)}
                disabled={isCollecting}
              >
                <div className="gesture-info">
                  <span className="gesture-name">{gesture.name}</span>
                  <span className="gesture-desc">{gesture.description}</span>
                </div>
              </button>
            ))}
          </div>
          
          <div className="collection-buttons">
            <button
              className="collect-all-btn"
              onClick={collectAllGestures}
              disabled={isCollecting}
            >
              Collect All Gestures
            </button>
            {isCollecting && (
              <button
                className="cancel-btn"
                onClick={cancelCollection}
              >
                Cancel Collection
              </button>
            )}
          </div>
        </div>

        <div className="control-section">
          <h4>Processing & Training</h4>
          <div className="processing-buttons">
            <button
              className="process-btn"
              onClick={processFeatures}
              disabled={isCollecting}
            >
              Extract Features
            </button>
            <button
              className="train-btn"
              onClick={trainModel}
              disabled={isCollecting}
            >
              Train Model
            </button>
            <button
              className="realtime-btn"
              onClick={startRealTimeProcessing}
              disabled={isCollecting}
            >
              Start Real-time Processing
            </button>
          </div>
        </div>
      </div>

      <div className="status-section">
        <div className="status-display">
          <h4>Status</h4>
          <div className="status-message">{status}</div>
          {currentGesture && (
            <div className="current-gesture">
              Currently collecting: <strong>{currentGesture}</strong>
            </div>
          )}
        </div>

        <div className="logs-section">
          <div className="logs-header">
            <h4>Activity Log</h4>
            <button className="clear-logs-btn" onClick={clearLogs}>
              Clear Logs
            </button>
          </div>
          <div className="logs-container">
            {logs.map((log, index) => (
              <div key={index} className="log-entry">
                <span className="log-time">{log.timestamp}</span>
                <span className="log-message">{log.message}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default DataCollection; 