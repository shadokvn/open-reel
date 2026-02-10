import whisper
import torch
from rich.console import Console

console = Console()

class Transcriber:
    def __init__(self, model_size='tiny'):
        console.print(f'[bold blue]Loading Whisper model ({model_size})...[/bold blue]')
        self.model = whisper.load_model(model_size)

    def transcribe(self, video_path):
        console.print(f'[bold blue]Transcribing {video_path}...[/bold blue]')
        result = self.model.transcribe(video_path)
        return result
