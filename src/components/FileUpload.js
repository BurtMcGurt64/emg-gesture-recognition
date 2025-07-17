import React, { useState } from 'react';
import './FileUpload.css';

const FileUpload = ({ onFileUpload }) => {
  const [dragActive, setDragActive] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState([]);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFiles(e.dataTransfer.files);
    }
  };

  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      handleFiles(e.target.files);
    }
  };

  const handleFiles = (files) => {
    const newFiles = Array.from(files).filter(file => 
      file.name.endsWith('.csv') || file.name.endsWith('.CSV')
    );

    if (newFiles.length === 0) {
      alert('Please select CSV files only.');
      return;
    }

    const processedFiles = newFiles.map(file => ({
      id: Date.now() + Math.random(),
      name: file.name,
      file: file,
      uploadedAt: new Date().toLocaleTimeString()
    }));

    setUploadedFiles(prev => [...prev, ...processedFiles]);
    
    // Process each file
    newFiles.forEach(file => {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const csvText = e.target.result;
          const lines = csvText.split('\n').filter(line => line.trim());
          
          if (lines.length < 2) {
            console.error('Invalid CSV file:', file.name);
            return;
          }

          const data = lines.slice(1).map(line => {
            const values = line.split(',');
            return {
              timestamp: parseFloat(values[0]),
              emg_value: parseInt(values[1])
            };
          });

          // Extract gesture name from filename
          const gestureName = extractGestureName(file.name);
          
          onFileUpload({
            gesture: gestureName,
            data: data,
            filename: file.name
          });
        } catch (error) {
          console.error('Error processing file:', file.name, error);
        }
      };
      reader.readAsText(file);
    });
  };

  const extractGestureName = (filename) => {
    // Extract gesture name from filename patterns like:
    // gesture0_session1.csv -> CLENCH
    // gesture1_session1.csv -> DOWN
    // etc.
    const match = filename.match(/gesture(\d+)/);
    if (match) {
      const gestureNum = parseInt(match[1]);
      const gestureMap = {
        0: 'RELAX',
        1: 'CLENCH', 
        2: 'UP',
        3: 'DOWN'
      };
      return gestureMap[gestureNum] || 'UNKNOWN';
    }
    
    // If no pattern match, use filename without extension
    return filename.replace('.csv', '').replace('.CSV', '');
  };

  const removeFile = (fileId) => {
    setUploadedFiles(prev => prev.filter(file => file.id !== fileId));
  };

  const clearAllFiles = () => {
    setUploadedFiles([]);
  };

  return (
    <div className="file-upload">
      <div className="upload-header">
        <h4>Upload EMG Data Files</h4>
        <p>Drag and drop CSV files or click to browse</p>
      </div>

      <div 
        className={`upload-area ${dragActive ? 'drag-active' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <input
          type="file"
          multiple
          accept=".csv,.CSV"
          onChange={handleChange}
          className="file-input"
          id="file-input"
        />
        <label htmlFor="file-input" className="upload-label">
          <div className="upload-icon">📁</div>
          <div className="upload-text">
            <span className="upload-title">Drop CSV files here</span>
            <span className="upload-subtitle">or click to browse</span>
          </div>
        </label>
      </div>

      {uploadedFiles.length > 0 && (
        <div className="uploaded-files">
          <div className="files-header">
            <h5>Uploaded Files ({uploadedFiles.length})</h5>
            <button className="clear-files-btn" onClick={clearAllFiles}>
              Clear All
            </button>
          </div>
          <div className="files-list">
            {uploadedFiles.map((file) => (
              <div key={file.id} className="file-item">
                <div className="file-info">
                  <span className="file-name">{file.name}</span>
                  <span className="file-time">{file.uploadedAt}</span>
                </div>
                <button 
                  className="remove-file-btn"
                  onClick={() => removeFile(file.id)}
                >
                  ×
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="upload-info">
        <h5>Supported File Format</h5>
        <ul>
          <li>CSV files with timestamp and EMG value columns</li>
          <li>Files should be named: gesture{'{0-3}'}_session{'{1-9}'}.csv</li>
          <li>Example: gesture0_session1.csv, gesture1_session2.csv</li>
        </ul>
      </div>
    </div>
  );
};

export default FileUpload; 