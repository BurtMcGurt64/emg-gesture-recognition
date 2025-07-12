import numpy as np
from collections import deque
import threading
import time
import serial
import queue
from scipy import signal
import torch
from typing import Tuple, List, Dict, Optional, Callable
import winsound

class RealTimeDataProcessor:
    def __init__(
        self,
        port: str = 'COM3',
        baud_rate: int = 115200,
        buffer_size: int = 250,
        step_size: int = 125,
        sampling_freq: int = 1000,
        low_freq: float = 20.0,
        high_freq: float = 450.0,
        filter_order: int = 4
    ):
        """
        Initialize the real-time EMG data processor with threading.
        
        Args:
            port: Serial port for Arduino
            baud_rate: Baud rate for serial communication
            buffer_size: Size of the rolling buffer in samples
            step_size: Number of samples to step forward after processing
            sampling_freq: Sampling frequency in Hz
            low_freq: Lower cutoff frequency for bandpass filter
            high_freq: Upper cutoff frequency for bandpass filter
            filter_order: Order of the Butterworth filter
        """
        self.port = port
        self.baud_rate = baud_rate
        self.buffer_size = buffer_size
        self.step_size = step_size
        self.sampling_freq = sampling_freq
        
        # Initialize the rolling buffer
        self.buffer = deque(maxlen=buffer_size)
        
        # Precompute filter coefficients (more efficient than filtfilt for real-time)
        nyquist = sampling_freq / 2
        low = low_freq / nyquist
        high = high_freq / nyquist
        self.b, self.a = signal.butter(filter_order, [low, high], btype='band')
        
        # Initialize filter state for real-time filtering
        self.filter_state = None
        
        # Initialize model (to be loaded later)
        self.model = None
        
        # Threading components
        self.data_queue = queue.Queue(maxsize=1000)  # Buffer for incoming data
        self.result_queue = queue.Queue(maxsize=100)  # Buffer for processed results
        self.running = False
        self.collection_thread = None
        self.processing_thread = None
        
        # Statistics
        self.samples_collected = 0
        self.samples_processed = 0
        self.samples_dropped = 0
        
    def start(self):
        """Start the real-time processing."""
        if self.running:
            print("Processor is already running!")
            return
            
        self.running = True
        
        # Start data collection thread
        self.collection_thread = threading.Thread(target=self._data_collection_loop)
        self.collection_thread.daemon = True
        self.collection_thread.start()
        
        # Start processing thread
        self.processing_thread = threading.Thread(target=self._processing_loop)
        self.processing_thread.daemon = True
        self.processing_thread.start()
        
        print("Real-time processor started!")
        
    def stop(self):
        """Stop the real-time processing."""
        self.running = False
        if self.collection_thread:
            self.collection_thread.join(timeout=1)
        if self.processing_thread:
            self.processing_thread.join(timeout=1)
        print("Real-time processor stopped!")
        
    def _data_collection_loop(self):
        """Thread for collecting data from serial port."""
        try:
            ser = serial.Serial(self.port, self.baud_rate, timeout=1)
            time.sleep(2)  # Give time to initialize
            print("Serial port initialized, ready to collect data!")
            
            while self.running:
                if ser.in_waiting > 0:
                    try:
                        value = int(ser.readline().decode().strip())
                        self.samples_collected += 1
                        
                        # Try to add to queue, drop if full (prevents blocking)
                        try:
                            self.data_queue.put_nowait(value)
                        except queue.Full:
                            self.samples_dropped += 1
                            
                    except ValueError:
                        continue
                else:
                    time.sleep(0.001)  # Small sleep to prevent busy waiting
                    
        except Exception as e:
            print(f"Error in data collection: {e}")
        finally:
            if 'ser' in locals():
                ser.close()
                
    def _processing_loop(self):
        """Thread for processing data."""
        while self.running:
            try:
                # Get data from queue with timeout
                value = self.data_queue.get(timeout=0.1)
                
                # Add to buffer
                self.buffer.append(value)
                
                # Process if buffer is full
                if len(self.buffer) == self.buffer_size:
                    result = self._process_window()
                    if result:
                        # Try to add result to queue, drop if full
                        try:
                            self.result_queue.put_nowait(result)
                        except queue.Full:
                            pass  # Drop old results if queue is full
                            
            except queue.Empty:
                continue
            except Exception as e:
                # More detailed error reporting
                import traceback
                print(f"Error in processing: {e}")
                print(f"Error type: {type(e).__name__}")
                print(f"Buffer size: {len(self.buffer)}")
                print(f"Data queue size: {self.data_queue.qsize()}")
                # Only print full traceback occasionally to avoid spam
                if hasattr(self, '_last_error_time'):
                    if time.time() - self._last_error_time > 5:  # Print full traceback every 5 seconds
                        print("Full traceback:")
                        traceback.print_exc()
                        self._last_error_time = time.time()
                else:
                    self._last_error_time = time.time()
                    print("Full traceback:")
                    traceback.print_exc()
                
    def _process_window(self) -> Optional[Dict]:
        """
        Process a full window of data.
        
        Returns:
            Dictionary containing raw signal, filtered signal, features, and prediction
        """
        try:
            # Convert buffer to numpy array
            window = np.array(list(self.buffer))
            
            # Check for valid data
            if len(window) != self.buffer_size:
                print(f"Warning: Window size mismatch. Expected {self.buffer_size}, got {len(window)}")
                return None
            
            # Check for NaN or inf values
            if np.any(np.isnan(window)) or np.any(np.isinf(window)):
                print("Warning: Invalid values (NaN or inf) in window data")
                return None
            
            # Apply real-time filter (more efficient than filtfilt)
            # Initialize filter state if not already done
            if self.filter_state is None:
                self.filter_state = signal.lfilter_zi(self.b, self.a)
            
            filtered_signal, self.filter_state = signal.lfilter(
                self.b, self.a, window, zi=self.filter_state
            )
            
            # Check filtered signal for issues
            if np.any(np.isnan(filtered_signal)) or np.any(np.isinf(filtered_signal)):
                print("Warning: Invalid values in filtered signal")
                return None
            
            # Extract features
            features = self._extract_features(filtered_signal)
            
            # Get prediction if model is loaded
            prediction = None
            if self.model is not None:
                try:
                    prediction = self._get_prediction(filtered_signal, features)
                except Exception as e:
                    print(f"Warning: Model prediction failed: {e}")
                    prediction = None
            
            # Remove processed samples
            for _ in range(self.step_size):
                if self.buffer:
                    self.buffer.popleft()
                    
            self.samples_processed += 1
                
            return {
                'raw_signal': window.tolist(),
                'filtered_signal': filtered_signal.tolist(),
                'features': features,
                'prediction': prediction,
                'timestamp': time.time()
            }
            
        except Exception as e:
            print(f"Error in _process_window: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _extract_features(self, signal: np.ndarray) -> Dict[str, float]:
        """
        Extract features from the filtered signal.
        
        Args:
            signal: Filtered EMG signal
            
        Returns:
            Dictionary of extracted features
        """
        # Mean Absolute Value (MAV)
        mav = np.mean(np.abs(signal))
        
        # Standard Deviation (STD)
        std = np.std(signal)
        
        # Slope Sign Changes (SSC)
        diff = np.diff(signal)
        ssc = np.sum((diff[:-1] * diff[1:]) < 0)
        
        # Zero Crossings (ZC)
        zc = np.sum(np.diff(np.signbit(signal)))
        
        return {
            'mav': float(mav),
            'std': float(std),
            'ssc': float(ssc),
            'zc': float(zc)
        }
    
    def _get_prediction(self, filtered_signal: np.ndarray, features: Dict[str, float]) -> Optional[int]:
        """
        Get prediction from the loaded model using both signal and features as separate inputs.
        
        Args:
            filtered_signal: Filtered EMG signal (already filtered with butter bandpass)
            features: Dictionary of extracted features
            
        Returns:
            Predicted class index
        """
        if self.model is None:
            return None
            
        try:
            # Prepare signal input (already filtered with butter bandpass)
            signal_tensor = torch.tensor(filtered_signal, dtype=torch.float32).unsqueeze(0)  # Add batch dimension
            
            # Prepare features input
            feature_tensor = torch.tensor([
                features['mav'],
                features['std'],
                features['ssc'],
                features['zc']
            ], dtype=torch.float32).unsqueeze(0)  # Add batch dimension
            
            # Get prediction with multi-input model
            with torch.no_grad():
                # Model expects: model(signal, features) or model([signal, features])
                # You can modify this based on your model's forward method
                try:
                    # Option 1: If model expects separate arguments
                    output = self.model(signal_tensor, feature_tensor)
                except TypeError:
                    try:
                        # Option 2: If model expects a list/tuple of inputs
                        output = self.model([signal_tensor, feature_tensor])
                    except TypeError:
                        try:
                            # Option 3: If model expects a single concatenated input (fallback)
                            combined_input = torch.cat([signal_tensor.flatten(), feature_tensor.flatten()]).unsqueeze(0)
                            output = self.model(combined_input)
                        except Exception as e:
                            print(f"Warning: All model input formats failed: {e}")
                            return None
                
                prediction = torch.argmax(output, dim=1).item()
                return prediction
                
        except Exception as e:
            print(f"Error in model prediction: {e}")
            return None
    
    def get_latest_result(self) -> Optional[Dict]:
        """
        Get the latest processed result.
        
        Returns:
            Latest result dictionary or None if no results available
        """
        try:
            return self.result_queue.get_nowait()
        except queue.Empty:
            return None
    
    def get_statistics(self) -> Dict:
        """Get processing statistics."""
        return {
            'samples_collected': self.samples_collected,
            'samples_processed': self.samples_processed,
            'samples_dropped': self.samples_dropped,
            'buffer_size': len(self.buffer),
            'data_queue_size': self.data_queue.qsize(),
            'result_queue_size': self.result_queue.qsize()
        }
    
    def load_model(self, model_path: str):
        """
        Load a pre-trained PyTorch model.
        
        Args:
            model_path: Path to the model file
        """
        try:
            self.model = torch.load(model_path, map_location='cpu')
            self.model.eval()
            print(f"Model loaded from {model_path}")
        except Exception as e:
            print(f"Error loading model: {e}")

# Example usage function
def run_real_time_demo():
    """Run a demo of the real-time processor."""
    processor = RealTimeDataProcessor()
    
    try:
        processor.start()
        
        print("Real-time processing started. Press Ctrl+C to stop.")
        print("Collecting data and processing in real-time...")
        
        while True:
            result = processor.get_latest_result()
            if result:
                print(f"Prediction: {result['prediction']}, "
                      f"MAV: {result['features']['mav']:.3f}, "
                      f"STD: {result['features']['std']:.3f}")
            
            # Print statistics every 5 seconds
            if processor.samples_processed % 50 == 0 and processor.samples_processed > 0:
                stats = processor.get_statistics()
                print(f"\nStats: Collected={stats['samples_collected']}, "
                      f"Processed={stats['samples_processed']}, "
                      f"Dropped={stats['samples_dropped']}")
            
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\nStopping real-time processor...")
    finally:
        processor.stop()
        stats = processor.get_statistics()
        print(f"\nFinal Stats: Collected={stats['samples_collected']}, "
              f"Processed={stats['samples_processed']}, "
              f"Dropped={stats['samples_dropped']}")

if __name__ == "__main__":
    run_real_time_demo() 