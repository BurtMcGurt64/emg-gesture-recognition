from data_collection import TrainingDataCollector
from feature_extractor import process_gesture_data
import os

if __name__ == "__main__":
    gesture_label = input("Enter gesture label (e.g., 0, 1, 2, 3): ").strip()
    num_sessions = int(input("Enter number of sessions to collect: ").strip())
    collector = TrainingDataCollector()
    try:
        for session in range(1, num_sessions + 1):
            collector.collect_session(gesture_label, session)
            filename = f"gesture{gesture_label}_session{session}.csv"
            if os.path.exists(filename):
                print(f"First 5 lines of {filename}:")
                with open(filename, 'r') as f:
                    for i in range(5):
                        line = f.readline()
                        if not line:
                            break
                        print(line.strip())
                print("---\n")
    finally:
        collector.close()

    # Process features for each session
    for session in range(1, num_sessions + 1):
        print(f"Processing features for gesture {gesture_label}, session {session}...")
        try:
            process_gesture_data(gesture_label, session)
        except Exception as e:
            print(f"Error processing gesture {gesture_label}, session {session}: {e}")
    print("\nAll done!") 