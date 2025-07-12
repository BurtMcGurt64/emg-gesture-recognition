import time
from real_time_processor import RealTimeDataProcessor

class FastRealTimeTester:
    def __init__(self, port='COM3', baud_rate=115200):
        self.processor = RealTimeDataProcessor(port=port, baud_rate=baud_rate)
        self.display_interval = 2.0  # Update display every 2 seconds
        self.start_time = None
        self.last_result = None

    def run_test(self, duration=None):
        print("Starting FAST real-time EMG processor test...")
        try:
            self.processor.start()
            print("Processor started!")
            # Wait for serial port to be ready (wait for the message from processor)
            time.sleep(2.1)  # Slightly longer than processor's serial init
            self.start_time = time.time()  # Start timer after serial is ready
            last_display_update = 0
            start_time = self.start_time
            warned_no_data = False
            while True:
                current_time = time.time()
                # Check if duration exceeded
                if duration and (current_time - start_time) > duration:
                    print(f"\nTest duration ({duration}s) completed.")
                    break
                # Get latest result (non-blocking)
                result = self.processor.get_latest_result()
                if result:
                    self.last_result = result
                # Update display less frequently
                if current_time - last_display_update >= self.display_interval:
                    stats = self.processor.get_statistics()
                    elapsed = current_time - self.start_time
                    print(f"Time: {elapsed:.1f}s | Collected: {stats['samples_collected']} | Processed: {stats['samples_processed']} | Dropped: {stats['samples_dropped']}")
                    last_display_update = current_time
                    # Warn if no data after 3 seconds
                    if not warned_no_data and elapsed > 3 and stats['samples_collected'] == 0:
                        print("Warning: No data collected after 3 seconds. Check Arduino and serial connection.")
                        warned_no_data = True
                time.sleep(0.001)  # Even more minimal sleep
        except KeyboardInterrupt:
            print("\nTest stopped.")
        except Exception as e:
            print(f"\nError: {e}")
        finally:
            self.processor.stop()
            final_stats = self.processor.get_statistics()
            print("\nFINAL RESULTS:")
            print(f"Total Collected: {final_stats['samples_collected']}")
            print(f"Total Processed: {final_stats['samples_processed']}")
            print(f"Total Dropped: {final_stats['samples_dropped']}")
            if final_stats['samples_collected'] > 0:
                efficiency = (final_stats['samples_collected'] - final_stats['samples_dropped']) / final_stats['samples_collected'] * 100
                print(f"Efficiency: {efficiency:.1f}%")
                total_time = time.time() - self.start_time
                final_rate = final_stats['samples_collected'] / total_time
                print(f"Final Rate: {final_rate:.0f} samples/sec")
            print("Test completed!")

def main():
    print("FAST Real-Time EMG Processor Test (Minimal Display)")
    port = input("Enter serial port (default: COM3): ").strip() or 'COM3'
    baud_rate = input("Enter baud rate (default: 115200): ").strip() or '115200'
    duration_input = input("Enter test duration in seconds (default: infinite): ").strip()
    try:
        baud_rate = int(baud_rate)
        duration = float(duration_input) if duration_input else None
    except ValueError:
        print("Invalid input. Using defaults.")
        baud_rate = 115200
        duration = None
    tester = FastRealTimeTester(port=port, baud_rate=baud_rate)
    tester.run_test(duration=duration)

if __name__ == "__main__":
    main() 