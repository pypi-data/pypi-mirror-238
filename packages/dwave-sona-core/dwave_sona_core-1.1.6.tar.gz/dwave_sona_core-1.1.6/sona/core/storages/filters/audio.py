from pathlib import Path

from sona.core.messages import File


class AudioNormalizer:
    def decode(self, file: File):
        filepath = Path(file.path)
        if filepath.suffix in [
            ".wav",
            ".mp3",
            ".flac",
            ".aac",
            ".opus",
            ".wma",
            ".amr",
            ".m4a",
        ]:
            return file.to_wav()
        return file

    def encode(self, file: File):
        filepath = Path(file.path)
        if filepath.suffix in [".wav"]:
            return file.to_flac()
        return file
