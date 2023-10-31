import wave
from pathlib import Path
from typing import Dict

from ffmpeg import FFmpeg

from .base import MessageBase


class File(MessageBase):
    label: str
    path: str
    metadata: Dict = {}

    def to_wav(self, *args, **kwargs):
        file_path = Path(self.path)
        if file_path.suffix == ".wav":
            return self
        wav_path = str(file_path.parent / f"{file_path.stem}.wav")
        (
            FFmpeg()
            .option("y")
            .input(self.path)
            .output(wav_path, *args, **kwargs)
            .execute()
        )
        metadata = {}
        with wave.open(wav_path, "rb") as w:
            metadata["OrigFilename"] = Path(self.path).name
            metadata["Channel"] = "stereo" if w.getnchannels() == 2 else "mono"
            metadata["Duration"] = float(w.getnframes()) / float(w.getframerate())
            metadata["Samplerate"] = w.getframerate()
        Path(self.path).unlink(missing_ok=True)
        return self.mutate(path=wav_path, metadata={"audio": metadata, **self.metadata})

    def to_flac(self, *args, **kwargs):
        file_path = Path(self.path)
        if file_path.suffix == ".flac":
            return self
        wav_path = str(file_path.parent / f"{file_path.stem}.flac")
        (
            FFmpeg()
            .option("y")
            .input(self.path)
            .output(wav_path, *args, **kwargs)
            .execute()
        )
        Path(self.path).unlink(missing_ok=True)
        return self.mutate(path=wav_path)

    def delete(self):
        Path(self.path).unlink(missing_ok=True)
