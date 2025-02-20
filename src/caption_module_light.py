import os
import subprocess
from datetime import timedelta
import torch
from faster_whisper import WhisperModel
from pydub import AudioSegment

# Load Silero VAD model
vad_model, utils = torch.hub.load(repo_or_dir="snakers4/silero-vad", model="silero_vad", force_reload=True)
(get_speech_timestamps, _, _, _, _) = utils


def extract_audio(video_path, audio_path):
    """Extracts audio from a video file using FFmpeg."""
    command = ['ffmpeg', '-y', '-i', video_path, '-vn', '-acodec', 'mp3', audio_path]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def convert_to_wav(audio_path):
    """Converts audio to 16kHz mono WAV format."""
    wav_path = os.path.splitext(audio_path)[0] + "_converted.wav"
    audio = AudioSegment.from_file(audio_path)
    audio = audio.set_channels(1).set_frame_rate(16000)
    audio.export(wav_path, format="wav")
    return wav_path


def format_timestamp(seconds):
    """Converts seconds to SRT timestamp format."""
    return str(timedelta(seconds=int(seconds))) + f",{int(seconds % 1 * 1000):03d}"


def transcribe_audio(wav_path):
    """Transcribes audio with word-level timestamps using Faster-Whisper."""
    model = WhisperModel("small", compute_type="int8")
    segments, _ = model.transcribe(wav_path, word_timestamps=True)

    whisper_segments = []
    for segment in segments:
        seg_start, seg_end = segment.start, segment.end
        words = [(word.start, word.end, word.word) for word in segment.words]
        whisper_segments.append((seg_start, seg_end, words))

    return whisper_segments


def detect_voice_segments(audio_path):
    """Detects speech segments using Silero VAD."""
    wav_path = convert_to_wav(audio_path)

    # Load and normalize audio
    audio = AudioSegment.from_wav(wav_path)
    samples = torch.tensor(audio.get_array_of_samples(), dtype=torch.float32) / 32768.0

    # Detect speech segments
    vad_timestamps = get_speech_timestamps(samples, vad_model, sampling_rate=16000)
    vad_segments = [(ts["start"] / 16000, ts["end"] / 16000) for ts in vad_timestamps]

    return vad_segments, wav_path


def refine_sync(whisper_segments, vad_segments):
    """Refines Whisper's timestamps using Silero VAD detections and prevents overlaps."""
    refined_segments = []
    last_end_time = 0  # Track end time of last caption

    for seg_start, seg_end, words in whisper_segments:
        # Find the closest VAD boundary for segment adjustment
        vad_start = next((s for s, e in vad_segments if s <= seg_start <= e), seg_start)
        vad_end = next((e for s, e in vad_segments if s <= seg_end <= e), seg_end)

        # Ensure no overlapping captions
        adjusted_start = max(vad_start, last_end_time)
        adjusted_end = max(vad_end, adjusted_start + 0.5)  # Ensure min duration of 0.5s

        # Ensure words are properly spaced
        text = " ".join(w[2].strip() for w in words if w[2].strip())

        # Store the refined segment
        refined_segments.append((adjusted_start, adjusted_end, text))

        # Update last end time
        last_end_time = adjusted_end

    return refined_segments


def generate_srt(segments, output_path):
    """Generates SRT file from refined segments."""
    with open(output_path, 'w', encoding='utf-8') as f:
        for i, (start, end, text) in enumerate(segments):
            f.write(f"{i + 1}\n{format_timestamp(start)} --> {format_timestamp(end)}\n{text}\n\n")


def generate_subtitles(video_path):
    """Main processing pipeline."""
    base_name = os.path.splitext(video_path)[0]
    audio_path = base_name + ".mp3"
    srt_path = base_name + ".srt"

    print("Extracting audio...")
    extract_audio(video_path, audio_path)

    print("Transcribing audio with Whisper...")
    whisper_segments = transcribe_audio(audio_path)

    print("Detecting speech segments with Silero VAD...")
    vad_segments, wav_path = detect_voice_segments(audio_path)

    print("Refining timestamps...")
    refined_segments = refine_sync(whisper_segments, vad_segments)

    print("Generating SRT...")
    generate_srt(refined_segments, srt_path)

    os.remove(audio_path)
    os.remove(wav_path)
    print(f"Subtitles saved to: {srt_path}")


if __name__ == "__main__":
    video_path = input("Enter video file path: ")
    generate_subtitles(video_path)
