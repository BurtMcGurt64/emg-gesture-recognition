import pandas as pd
import numpy as np
from scipy.signal import butter, filtfilt

class FeatureExtractor:
    def __init__(self, sampling_rate=1000):
        self.sampling_rate = sampling_rate
        self.nyquist = sampling_rate / 2
        
        # Precompute filter coefficients
        low = 20 / self.nyquist
        high = 450 / self.nyquist
        self.b, self.a = butter(4, [low, high], btype='band')

    def load_csv_data(self, filename):
        """Load EMG data from CSV file."""
        df = pd.read_csv(filename)
        return df['emg_value'].values

    def preprocess_signal(self, data):
        """Apply bandpass filter to the signal (no normalization)."""
        # Apply bandpass filter
        filtered_data = filtfilt(self.b, self.a, data)
        return filtered_data

    def extract_features(self, window):
        """Extract 4 features from a single window."""
        # Mean Absolute Value (MAV)
        mav = np.mean(np.abs(window))
        
        # Standard Deviation
        std = np.std(window)
        
        # Slope Sign Changes (SSC)
        diff1 = np.diff(window)
        ssc = np.sum((diff1[:-1] * diff1[1:]) < 0)
        
        # Zero Crossings (ZC)
        zc = np.sum(np.diff(np.sign(window)) != 0)
        
        return np.array([mav, std, ssc, zc])

    def window_and_extract_features(self, data, window_size=250, step_size=125):
        """
        Window the data and extract features for each window.
        
        Args:
            data: 1D array of EMG signal
            window_size: Number of samples per window
            step_size: Number of samples to step between windows
            
        Returns:
            windows: 2D array of shape (num_windows, window_size)
            features: 2D array of shape (num_windows, 4) containing [MAV, STD, SSC, ZC]
        """
        windows = []
        features = []
        
        num_samples = len(data)
        
        for start in range(0, num_samples - window_size + 1, step_size):
            window = data[start:start + window_size]
            windows.append(window)
            
            # Extract features for this window
            window_features = self.extract_features(window)
            features.append(window_features)
        
        return np.array(windows), np.array(features)

    def process_csv_file(self, filename, window_size=250, step_size=125):
        """
        Complete pipeline: load CSV, preprocess, window, and extract features.
        
        Args:
            filename: Path to CSV file
            window_size: Number of samples per window
            step_size: Number of samples to step between windows
            
        Returns:
            windows: 2D array of shape (num_windows, window_size)
            features: 2D array of shape (num_windows, 4)
        """
        # Load data
        raw_data = self.load_csv_data(filename)
        
        # Preprocess
        processed_data = self.preprocess_signal(raw_data)
        
        # Window and extract features
        windows, features = self.window_and_extract_features(
            processed_data, window_size, step_size
        )
        
        return windows, features

    def save_features_to_csv(self, features, output_filename):
        """Save extracted features to CSV file."""
        feature_names = ['MAV', 'STD', 'SSC', 'ZC']
        df = pd.DataFrame(features, columns=feature_names)
        df.to_csv(output_filename, index=False)
        print(f"Features saved to {output_filename}")
        print(f"Shape: {features.shape}")

# Example usage function
def process_gesture_data(gesture_label, session_number, window_size=250, step_size=125):
    """
    Process a single gesture session and save features.
    
    Args:
        gesture_label: Label for the gesture (e.g., 1, 2, 3)
        session_number: Session number
        window_size: Window size in samples
        step_size: Step size in samples
    """
    extractor = FeatureExtractor()
    
    # Input and output filenames
    input_filename = f'gesture{gesture_label}_session{session_number}.csv'
    output_filename = f'gesture{gesture_label}_session{session_number}_features.csv'
    
    try:
        # Process the data
        windows, features = extractor.process_csv_file(
            input_filename, window_size, step_size
        )
        
        # Save features
        extractor.save_features_to_csv(features, output_filename)
        
        print(f"Processed {input_filename}")
        print(f"Number of windows: {len(windows)}")
        print(f"Feature array shape: {features.shape}")
        
        return windows, features
        
    except FileNotFoundError:
        print(f"Error: Could not find {input_filename}")
        return None, None 