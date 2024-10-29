import librosa
import soundfile as sf
import numpy as np
from pathlib import Path

def split_audio(input_file, output_dir):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    audio, _ = librosa.load(input_file, sr=16000)
    samples_per_second = 16000
    total_segments = len(audio) // samples_per_second
    for i in range(total_segments):
        start_idx = i * samples_per_second
        end_idx = (i + 1) * samples_per_second
        segment = audio[start_idx:end_idx]
        output_file = output_path / f"segment_{i:03d}.wav"
        sf.write(output_file, segment, 16000, subtype='PCM_16')
    print(f"Split audio into {total_segments} segments of 1 second each")
    remaining_samples = len(audio) % samples_per_second
    
    if remaining_samples > 0:
        last_segment = audio[-remaining_samples:]
        padded_segment = np.pad(last_segment, (0, samples_per_second - remaining_samples))
        output_file = output_path / f"segment_{total_segments:03d}.wav"
        sf.write(output_file, padded_segment, 16000, subtype='PCM_16')
        print(f"Created one additional padded segment from remaining {remaining_samples/16000:.3f} seconds")

if __name__ == "__main__":
    input_file = "hello.mp4"  # Replace with your input file path
    output_dir = "output_segments"       
    split_audio(input_file, output_dir)