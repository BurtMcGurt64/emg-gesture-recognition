import pandas as pd
import matplotlib.pyplot as plt

# Filenames for each gesture
files = {
    'CLENCH': 'gesture0_session1.csv',
    'DOWN': 'gesture1_session1.csv',
    'RELAX': 'gesture2_session1.csv',
    'UP': 'gesture3_session1.csv',
}

plt.figure(figsize=(15, 10))

for i, (gesture, filename) in enumerate(files.items(), 1):
    df = pd.read_csv(filename)
    
    # Print statistics
    print(f"\n{gesture}:")
    print(f"  Number of samples: {len(df)}")
    print(f"  Time range: {df['timestamp'].min():.3f}s to {df['timestamp'].max():.3f}s")
    print(f"  Duration: {df['timestamp'].max() - df['timestamp'].min():.3f}s")
    print(f"  EMG range: {df['emg_value'].min()} to {df['emg_value'].max()}")
    
    # Plot
    plt.subplot(2, 2, i)
    plt.plot(df['timestamp'], df['emg_value'], label=gesture, linewidth=0.5)
    plt.title(f'{gesture} (Session 1)\nSamples: {len(df)}, Duration: {df["timestamp"].max():.1f}s')
    plt.xlabel('Time (s)')
    plt.ylabel('EMG Value')
    plt.grid(True, alpha=0.3)
    plt.legend()

plt.suptitle('Raw EMG Signals - Debug View', fontsize=16, y=0.98)
plt.tight_layout()
plt.show()

print("\nExpected: ~5000 samples, 5.0 seconds duration")
print("If you see fewer samples or shorter duration, there may be a data collection issue.") 