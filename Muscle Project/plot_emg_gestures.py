import matplotlib.pyplot as plt
import csv
import os

sessions = range(1, 9)
fig, axs = plt.subplots(8, 1, figsize=(12, 16), sharex=True)

for idx, session in enumerate(sessions):
    filename = f"gesture0_session{session}.csv"
    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        continue

    timestamps = []
    emg_values = []
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                timestamps.append(float(row['timestamp']))
                emg_values.append(float(row['emg_value']))
            except Exception:
                continue

    axs[idx].plot(timestamps, emg_values)
    axs[idx].set_ylabel(f"Session {session}")
    axs[idx].grid(True)

axs[-1].set_xlabel("Time (s)")
fig.suptitle("Gesture 0 Sessions 1-8 EMG Signals")
plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.show()