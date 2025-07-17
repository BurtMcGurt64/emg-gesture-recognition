## About This Project

This is a personal project I developed over the summer to explore EMG-based control systems. I'm interested in how machine learning and real-time signal processing can be used for human/brain-computer interfaces, especially in biomedical and neuroengineering applications. I designed the system end-to-end, from sensor setup, signal processing, creating the neural network, and a visualization dashboard.

## Project Overview

This system captures EMG signals from forearm muscles using surface electrodes and an Arduino-based amplifier, processes the signals in real-time, and classifies (using a PyTorch neural network) four different hand gestures: relax, clench, up, and down.

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
- **PyTorch implementation** with GPU acceleration support

### Web Visualization
- **React-based dashboard**
- **Interactive charts** using Recharts library
- **Real-time data display** with zoom and pan capabilities

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
   - React frontend
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

## Web Interface Usage

### Starting the Web App
```bash
# Navigate to project directory
cd EMG

# Install dependencies (first time only)
npm install

# Start the development server
npm start
```

The app will open automatically at `http://localhost:3000`

## Thoughts

This project started as a way for me to explore how electrical signals from the body - specifically EMG signals - can be used to create real time interfaces. I was curious about the overlap between neuroscience, electrical engineering, and machine learning, and I wanted to see how far I could get building a full-stack system on my own.

While this system has limitations, working on it gave me a better understanding of several real-world areas where these ideas apply, like:
- Assistive technologies for motor impairments
- EMG-controlled prosthetics
- Gesture-based human-computer interaction
- Signal decoding in neuroengineering research

Along the way, I learned a lot - both in software and modeling, and also in working with real hardware. I had to figure out how to solder connections, choose the right jumper wires, and understand how to safely wire up components using VIN, GND, and ENV ports on a microcontroller. I also spent time tuning parameters like baud rate and sampling frequency to ensure stable data transfer.

On the signal side, the project deepened my understanding of concepts like Nyquist frequency, aliasing, sampling rate tradeoffs, and filter design (by using a Butterworth bandpass to isolate muscle activity). Debugging these systems in real time really forced me to think about how noise, latency, and theoretical choices affect the final product's performance.