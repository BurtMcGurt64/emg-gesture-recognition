import React from 'react';
import './GestureSelector.css';

const GestureSelector = ({ gestures, selectedGesture, onGestureChange }) => {
  return (
    <div className="gesture-selector">
      <h3 className="selector-title">Select Gesture</h3>
      <div className="gesture-buttons">
        {gestures.map((gesture) => (
          <button
            key={gesture}
            className={`gesture-button ${selectedGesture === gesture ? 'active' : ''}`}
            onClick={() => onGestureChange(gesture)}
          >
            <span className="gesture-icon">
              {gesture === 'CLENCH' && '✊'}
              {gesture === 'DOWN' && '👇'}
              {gesture === 'RELAX' && '🖐️'}
              {gesture === 'UP' && '👆'}
            </span>
            <span className="gesture-name">{gesture}</span>
          </button>
        ))}
      </div>
    </div>
  );
};

export default GestureSelector; 