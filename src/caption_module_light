import os
import subprocess
import hashlib
from tqdm import tqdm
from faster_whisper import WhisperModel
import torch

class VideoCaptioner:
    def __init__(self, video_path, model_size="small", compute_type="int8"):
        self.video_path = video_path
        self.model_size = model_size
        self.compute_type = compute_type
        self.audio_path = "temp_audio.wav"
        self.output_srt = f"captions_{hashlib.md5(video_path.encode()).hexdigest()}.srt"
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # Load Whisper model
        self.whisper_model = WhisperModel(self.model_size, device=self.device, compute_type=self.compute_type)

    def extract_audio(self):
        """Extract audio from video"""
        try:
            subprocess.run([
                "ffmpeg", "-i", self.video_path, "-vn",
                "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
                self.audio_path, "-y"
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            raise RuntimeError("Audio extraction failed.")

    def transcribe_audio(self):
        """Transcribe audio using Whisper with automatic segmentation"""
        try:
            segments, _ = self.whisper_model.transcribe(
                self.audio_path, beam_size=5, vad_filter=True
            )

            # Write subtitles in SRT format
            with open(self.output_srt, "w", encoding="utf-8") as f:
                for idx, seg in tqdm(enumerate(segments, start=1), desc="Generating Captions"):
                    f.write(f"{idx}\n{self._format_ts(seg.start)} --> {self._format_ts(seg.end)}\n{seg.text}\n\n")

        except Exception as e:
            raise RuntimeError(f"Transcription failed: {e}")

    def _format_ts(self, seconds):
        """Convert seconds to SRT timestamp format"""
        ms = int((seconds % 1) * 1000)
        h, m, s = int(seconds // 3600), int((seconds % 3600) // 60), int(seconds % 60)
        return f"{h:02}:{m:02}:{s:02},{ms:03}"

    def process(self):
        """Run the entire pipeline"""
        try:
            self.extract_audio()
            self.transcribe_audio()
            print(f"Success! Captions saved to {self.output_srt}")
        except Exception as e:
            print(f"Processing failed: {str(e)}")
        finally:
            if os.path.exists(self.audio_path):
                os.remove(self.audio_path)

if __name__ == "__main__":
    VideoCaptioner("sample2.mp4").process()
