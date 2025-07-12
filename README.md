# EMG-Based Gesture Recognition System

A complete electromyography (EMG) signal processing and machine learning system for real-time muscle gesture recognition. This project combines hardware interfacing, signal processing, deep learning, and web visualization to create an end-to-end EMG analysis platform.

## Project Overview

This system captures EMG signals from forearm muscles using surface electrodes and an Arduino-based amplifier, processes the signals in real-time, and classifies four distinct hand gestures: **CLENCH**, **DOWN**, **RELAX**, and **UP**. The project demonstrates practical applications in human-computer interaction, prosthetics, and biomedical signal processing.

## Key Features

### Hardware Integration
- **Arduino-based EMG amplifier** with surface electrodes
- **Real-time data acquisition** at 1000Hz sampling rate
- **Bandpass filtering** (20-450Hz) for noise reduction
- **Serial communication** for continuous data streaming

### Signal Processing
- **Real-time filtering** using Butterworth bandpass filters
- **Feature extraction** including RMS, mean, variance, and zero-crossing rate
- **Sliding window processing** with configurable buffer sizes
- **Multi-threaded architecture** for concurrent data collection and processing

### Machine Learning
- **Hybrid neural network** combining CNN and MLP architectures
- **Multi-input model** processing both raw signals and hand-crafted features
- **Real-time inference** with sub-100ms latency
- **PyTorch implementation** with GPU acceleration support

### Web Visualization
- **React-based dashboard** with dark theme UI
- **Interactive charts** using Recharts library
- **Real-time data display** with zoom and pan capabilities
- **Responsive design** for desktop and mobile viewing

## Technical Architecture

### Data Flow
```
EMG Sensors → Arduino → Serial Port → Python Processing → Neural Network → Web Dashboard
```

### System Components

1. **Data Collection** (`data_collection.py`)
   - Serial communication with Arduino
   - Real-time EMG signal acquisition
   - Automatic CSV export with timestamps

2. **Signal Processing** (`real_time_processor.py`)
   - Multi-threaded real-time processing
   - Bandpass filtering and feature extraction
   - Sliding window analysis with configurable parameters

3. **Machine Learning** (`model.py`)
   - EMGMultiInputModel: CNN + MLP hybrid architecture
   - EMGSimpleModel: Feature-only baseline
   - PyTorch implementation with dropout and batch normalization

4. **Web Interface** (`src/`)
   - React frontend with modern dark UI
   - Real-time data visualization
   - Interactive gesture selection and statistics

## Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 14+
- Arduino IDE
- EMG amplifier circuit (see hardware setup)

### Python Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install torch numpy scipy serial pyserial matplotlib pandas
```

### Web Interface
```bash
# Install Node.js dependencies
npm install

# Start development server
npm start
```

### Hardware Setup
1. **EMG Amplifier Circuit**
   - Instrumentation amplifier (AD623 or similar)
   - Bandpass filter (20-450Hz)
   - Arduino Nano for ADC conversion

2. **Electrode Placement**
   - Place electrodes on forearm flexor muscles
   - Ground electrode on wrist
   - Ensure good skin contact with conductive gel

3. **Calibration**
   - Run `begin_collection.py` for initial setup
   - Collect training data using `collect_all_gestures.py`
   - Train model with `process_all_features.py`

## Usage

### Data Collection
```python
from data_collection import TrainingDataCollector

# Initialize collector
collector = TrainingDataCollector(port='COM3', duration=5)

# Collect training data
collector.collect_multiple_sessions(gesture_label=0, num_sessions=3)
```

### Real-time Processing
```python
from real_time_processor import RealTimeDataProcessor

# Initialize processor
processor = RealTimeDataProcessor(port='COM3', buffer_size=250)

# Start real-time processing
processor.start()

# Get latest results
result = processor.get_latest_result()
```

### Model Training
```python
from model import EMGMultiInputModel
import torch

# Create model
model = EMGMultiInputModel(signal_length=250, num_classes=4)

# Train model (see process_all_features.py for complete training loop)
# ...

# Save trained model
torch.save(model.state_dict(), 'emg_model.pth')
```

## Performance Metrics

### Real-time Performance
- **Latency**: <100ms end-to-end processing
- **Throughput**: 1000Hz continuous data stream
- **Accuracy**: 85-95% on trained gestures
- **Memory Usage**: <50MB for real-time processing

### Model Architecture
- **Input**: 250-sample EMG window + 4 hand-crafted features
- **CNN Branch**: 3 convolutional layers with batch normalization
- **MLP Branch**: 2 fully connected layers for feature processing
- **Combined Classifier**: 3-layer network with dropout

## Applications

### Biomedical Engineering
- **Prosthetic control** for upper limb amputees
- **Rehabilitation monitoring** for stroke patients
- **Muscle fatigue analysis** in sports medicine

### Human-Computer Interaction
- **Gesture-based interfaces** for hands-free computing
- **Gaming controllers** using muscle signals
- **Accessibility tools** for users with limited mobility

### Research Applications
- **Neuroscience studies** of motor control
- **Biomechanics research** for movement analysis
- **Clinical diagnostics** for neuromuscular disorders

## Future Enhancements

### Planned Features
- **Multi-channel EMG** support for more complex gestures
- **Adaptive learning** for personalized gesture recognition
- **Wireless data transmission** using Bluetooth/WiFi
- **Mobile app** for iOS/Android platforms

### Research Directions
- **Transfer learning** for cross-subject generalization
- **Unsupervised learning** for gesture discovery
- **Real-time feedback** for gesture training
- **Integration with VR/AR** systems

## Technical Challenges Solved

1. **Real-time Processing**: Multi-threaded architecture prevents data loss
2. **Signal Quality**: Advanced filtering removes power line interference
3. **Model Complexity**: Hybrid architecture balances accuracy and speed
4. **User Experience**: Intuitive web interface for data visualization

## Learning Outcomes

This project demonstrates practical application of:
- **Digital signal processing** principles
- **Machine learning** in biomedical contexts
- **Real-time systems** design and optimization
- **Full-stack development** with hardware integration
- **Data visualization** and user interface design

## Academic Relevance

This project aligns with **ECE + Neuroscience** studies by covering:
- **Biomedical instrumentation** and signal acquisition
- **Neural signal processing** and feature extraction
- **Machine learning** for pattern recognition
- **Real-time systems** and embedded programming
- **Human-computer interaction** principles

---

*This project represents a complete integration of hardware, software, and machine learning for practical biomedical applications. The combination of real-time signal processing, deep learning, and web visualization creates a comprehensive platform for EMG-based gesture recognition.* 