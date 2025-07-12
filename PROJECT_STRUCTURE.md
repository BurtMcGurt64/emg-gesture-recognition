# EMG Project Structure

This document provides a detailed overview of the project structure and the purpose of each component.

## Root Directory
```
EMG/
├── README.md                 # Main project documentation
├── requirements.txt          # Python dependencies
├── package.json             # Node.js dependencies for web interface
├── PROJECT_STRUCTURE.md     # This file
├── public/                  # Web interface static files
├── src/                     # React web application
├── Muscle Project/          # Python backend and ML components
├── data/                    # Processed data directory
└── venv/                    # Python virtual environment
```

## Python Backend (`Muscle Project/`)

### Core Components

#### Data Collection
- **`data_collection.py`** - Main data collection module
  - `TrainingDataCollector` class for EMG signal acquisition
  - Serial communication with Arduino
  - Real-time data filtering and CSV export
  - Audio feedback for recording sessions

- **`begin_collection.py`** - Initial setup and calibration
- **`collect_all_gestures.py`** - Automated data collection for all gestures

#### Signal Processing
- **`real_time_processor.py`** - Real-time EMG processing
  - Multi-threaded architecture for concurrent data collection and processing
  - Bandpass filtering (20-450Hz)
  - Feature extraction (RMS, mean, variance, zero-crossing rate)
  - Sliding window analysis with configurable parameters

- **`preprocess.py`** - Data preprocessing utilities
- **`feature_extractor.py`** - Feature extraction algorithms

#### Machine Learning
- **`model.py`** - Neural network implementations
  - `EMGMultiInputModel`: Hybrid CNN + MLP architecture
  - `EMGSimpleModel`: Feature-only baseline
  - Model factory functions and testing utilities

- **`process_all_features.py`** - Model training pipeline

#### Visualization and Debugging
- **`plot_emg_debug.py`** - Debug visualization of raw EMG signals
- **`plot_emg_gestures.py`** - Gesture-specific signal visualization

#### Real-time Applications
- **`test_realtime_fast.py`** - Fast real-time processing test
- **`real_time_processor.py`** - Complete real-time processing system

## Web Interface (`src/`)

### React Components

#### Core Application
- **`App.js`** - Main application component
  - State management for gesture selection and data loading
  - Error handling and loading states
  - Integration of all components

- **`App.css`** - Main application styling
  - Dark theme with glassmorphism effects
  - Responsive design for desktop and mobile
  - Custom animations and transitions

#### Components
- **`GestureSelector/`** - Gesture selection interface
  - Interactive buttons for gesture switching
  - Visual feedback and animations
  - Responsive grid layout

- **`DataStats/`** - Statistics display panel
  - Real-time calculation of data metrics
  - Sample count, duration, EMG value ranges
  - Time range information and sampling rate

- **`EMGChart/`** - Interactive data visualization
  - Line chart using Recharts library
  - Zoom, pan, and brush selection capabilities
  - Custom tooltips and performance optimization
  - Toggle between full data and sampled view

#### Styling
- **`index.css`** - Global styles and dark theme
- Component-specific CSS files for modular styling

## Data Files

### Raw EMG Data
- **`gesture0_session1.csv`** - CLENCH gesture data
- **`gesture1_session1.csv`** - DOWN gesture data
- **`gesture2_session1.csv`** - RELAX gesture data
- **`gesture3_session1.csv`** - UP gesture data

### Data Format
Each CSV file contains:
```csv
timestamp,emg_value
0.0,458
0.001,266
...
```

## Configuration Files

### Python Dependencies (`requirements.txt`)
- Core scientific computing libraries (numpy, scipy, pandas)
- Machine learning frameworks (torch, scikit-learn)
- Signal processing and visualization tools
- Hardware communication libraries

### Node.js Dependencies (`package.json`)
- React 18 for web interface
- Recharts for data visualization
- Development tools and testing libraries

## Key Features by Component

### Data Collection
- **Real-time acquisition** at 1000Hz sampling rate
- **Bandpass filtering** for noise reduction
- **Automatic CSV export** with timestamps
- **Audio feedback** for recording sessions

### Signal Processing
- **Multi-threaded architecture** prevents data loss
- **Configurable buffer sizes** for different use cases
- **Real-time filtering** using Butterworth filters
- **Feature extraction** for machine learning

### Machine Learning
- **Hybrid neural network** combining CNN and MLP
- **Multi-input architecture** for signal and feature processing
- **Real-time inference** with sub-100ms latency
- **GPU acceleration** support

### Web Interface
- **Modern dark UI** with glassmorphism effects
- **Interactive charts** with zoom and pan
- **Real-time data display** with performance optimization
- **Responsive design** for all devices

## Development Workflow

### 1. Data Collection
```bash
cd "Muscle Project"
python data_collection.py
```

### 2. Model Training
```bash
python process_all_features.py
```

### 3. Real-time Testing
```bash
python test_realtime_fast.py
```

### 4. Web Interface
```bash
npm start
```

## File Naming Conventions

- **Python files**: snake_case (e.g., `data_collection.py`)
- **React components**: PascalCase (e.g., `EMGChart.js`)
- **CSS files**: Same name as component (e.g., `EMGChart.css`)
- **Data files**: `gesture{id}_session{session}.csv`

## Dependencies and Versions

### Python Environment
- Python 3.8+
- PyTorch 1.9+
- NumPy 1.21+
- SciPy 1.7+

### Web Environment
- Node.js 14+
- React 18
- Recharts 2.8+

## Performance Considerations

### Real-time Processing
- **Buffer size**: 250 samples (250ms at 1000Hz)
- **Step size**: 125 samples for 50% overlap
- **Processing latency**: <100ms end-to-end

### Web Interface
- **Data sampling**: Automatic downsampling for large datasets
- **Memory usage**: <50MB for real-time processing
- **Chart performance**: Optimized rendering with Recharts

## Security and Best Practices

### Data Handling
- **Local processing**: All data processed locally
- **No external dependencies**: Self-contained system
- **Error handling**: Comprehensive exception handling

### Code Quality
- **Type hints**: Full type annotation in Python
- **Documentation**: Comprehensive docstrings
- **Modular design**: Separated concerns and reusable components 