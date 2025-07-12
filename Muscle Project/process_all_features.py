import os
from feature_extractor import process_gesture_data

# Get all gesture session CSV files (excluding feature files)
csv_files = [f for f in os.listdir('.') if f.startswith('gesture') and f.endswith('.csv') and '_features' not in f]

for filename in csv_files:
    print(f"Processing features for {filename}...")
    try:
        process_gesture_data(filename)
    except Exception as e:
        print(f"Error processing {filename}: {e}")

print("\nAll feature extraction complete!") 