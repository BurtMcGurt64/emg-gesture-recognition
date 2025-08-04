import serial
import time
import csv
import numpy as np
import winsound
from scipy.signal import butter, filtfilt
from typing import List, Tuple, Optional


class TrainingDataCollector:
    """
    A class for collecting EMG training data from an Arduino-based amplifier.
    
    This collector handles real-time EMG signal acquisition, applies bandpass
    filtering to remove noise, and saves data in CSV format for machine learning.
    """
    
    def __init__(self, port: str = 'COM3', baud_rate: int = 115200, 
                 sampling_rate: int = 1000, duration: int = 5, pause: int = 3):
        """
        Initialize the EMG data collector.
        
        Args:
            port: Serial port for Arduino connection
            baud_rate: Baud rate for serial communication
            sampling_rate: Expected sampling frequency in Hz
            duration: Recording duration in seconds
            pause: Pause between recordings in seconds
        """
        self.port = port
        self.baud_rate = baud_rate
        self.sampling_rate = sampling_rate
        self.duration = duration
        self.pause = pause
        
        # Initialize serial connection
        try:
            self.ser = serial.Serial(self.port, self.baud_rate, timeout=1)
            time.sleep(2)  # Allow time for Arduino initialization
            print(f"Successfully connected to {port}")
        except serial.SerialException as e:
            raise ConnectionError(f"Failed to connect to {port}: {e}")

        # Precompute bandpass filter coefficients (20-450Hz)
        nyquist = sampling_rate / 2
        low_freq = 20 / nyquist
        high_freq = 450 / nyquist
        self.b, self.a = butter(4, [low_freq, high_freq], btype='band')

    def beep(self, freq: int = 1000, duration: int = 500) -> None:
        """
        Generate an audio beep for user feedback.
        
        Args:
            freq: Frequency in Hz
            duration: Duration in milliseconds
        """
        try:
            winsound.Beep(freq, duration)
        except RuntimeError:
            # Fallback for systems without audio support
            print("Beep!")

    def collect_session(self, gesture_label: int, session_number: int) -> str:
        """
        Collect EMG data for a single session and save as CSV.
        
        Args:
            gesture_label: Integer label for the gesture (0-3)
            session_number: Session number for this recording
            
        Returns:
            Filename of the saved CSV file
            
        Raises:
            ValueError: If no valid data is collected
        """
        num_samples = int(self.sampling_rate * self.duration)
        raw_data = []
        sample_count = 0

        print(f"\n{'='*50}")
        print(f"Recording Gesture {gesture_label}, Session {session_number}")
        print(f"Duration: {self.duration}s | Expected samples: {num_samples}")
        print("="*50)
        
        # Countdown and preparation
        print("Preparing to record...")
        for i in range(3, 0, -1):
            print(f"Starting in {i}...")
            time.sleep(1)
        
        self.beep(1000, 500)
        print("🎙️  RECORDING STARTED")
        start_time = time.time()

        # Data collection loop
        while time.time() - start_time < self.duration:
            if self.ser.in_waiting > 0:
                try:
                    value = int(self.ser.readline().decode().strip())
                    sample_count += 1
                    if sample_count % 2 == 0:  # Decimate to reduce noise
                        raw_data.append(value)
                except (ValueError, UnicodeDecodeError):
                    continue

        end_time = time.time()
        actual_duration = end_time - start_time
        self.beep(800, 500)

        # Validate collected data
        if len(raw_data) < num_samples * 0.5:  # At least 50% of expected samples
            raise ValueError(f"Insufficient data collected: {len(raw_data)} samples")

        # Save data to CSV
        filename = f'gesture{gesture_label}_session{session_number}.csv'
        self._save_to_csv(filename, raw_data)
        
        # Print summary
        print(f"✅ Recording complete!")
        print(f"📁 Saved to: {filename}")
        print(f"📊 Samples collected: {len(raw_data)}")
        print(f"⏱️  Actual duration: {actual_duration:.2f}s")
        print(f"📈 Sampling rate: {len(raw_data)/actual_duration:.0f} Hz")
        print(f"😴 Resting for {self.pause}s...\n")
        
        time.sleep(self.pause)
        return filename

    def _save_to_csv(self, filename: str, data: List[int]) -> None:
        """
        Save EMG data to CSV file with timestamps.
        
        Args:
            filename: Output CSV filename
            data: List of EMG values
        """
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp", "emg_value"])
            
            for i, value in enumerate(data):
                timestamp = i / self.sampling_rate
                writer.writerow([timestamp, value])

    def collect_multiple_sessions(self, gesture_label: int, num_sessions: int) -> List[str]:
        """
        Collect multiple sessions for a gesture.
        
        Args:
            gesture_label: Integer label for the gesture
            num_sessions: Number of sessions to record
            
        Returns:
            List of saved CSV filenames
        """
        filenames = []
        
        for session in range(1, num_sessions + 1):
            try:
                filename = self.collect_session(gesture_label, session)
                filenames.append(filename)
            except Exception as e:
                print(f"❌ Error in session {session}: {e}")
                continue
                
        return filenames

    def close(self) -> None:
        """Close the serial connection."""
        if hasattr(self, 'ser'):
            self.ser.close()
            print("Serial connection closed.")


def main():
    """Example usage of the TrainingDataCollector."""
    try:
        # Initialize collector
        collector = TrainingDataCollector(
            port='COM3',
            duration=5,
            pause=3
        )
        
        # Collect data for all gestures
        gestures = {
            0: "CLENCH",
            1: "DOWN", 
            2: "RELAX",
            3: "UP"
        }
        
        for gesture_id, gesture_name in gestures.items():
            print(f"\n🎯 Collecting data for {gesture_name} gesture...")
            collector.collect_multiple_sessions(gesture_id, num_sessions=3)
            
    except KeyboardInterrupt:
        print("\n⚠️  Data collection interrupted by user")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        collector.close()


if __name__ == "__main__":
    main() 
