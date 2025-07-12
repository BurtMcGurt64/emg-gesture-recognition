import time
from data_collection import TrainingDataCollector

gestures = [
    ("RELAX", 0),
    ("CLENCH", 1),
    ("UP", 2),
    ("DOWN", 3),
]

collector = TrainingDataCollector()

try:
    for gesture_name, gesture_label in gestures:
        input(f"\nGet ready for gesture: {gesture_name}. Press Enter when ready...")
        collector.collect_session(gesture_label=gesture_label, session_number=1)
        print(f"Finished collecting for {gesture_name}.")
    print("\nAll gestures collected!")
finally:
    collector.close() 