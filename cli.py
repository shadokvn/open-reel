import click
from rich.console import Console
import os
import sys
import numpy as np
import ffmpeg

# Ensure we can import from src
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.transcriber import Transcriber
from src.analyzer import VideoAnalyzer
from src.editor import VideoEditor
from src.tracker import FaceTracker
from src.subtitler import Subtitler

console = Console()

@click.group()
def cli():
    """OpenReel: The Open Source AI Video Editor."""
    pass

@cli.command()
@click.argument('video_path', type=click.Path(exists=True))
@click.option('--api-key', envvar='GEMINI_API_KEY', help='Gemini API Key')
@click.option('--premium', is_flag=True, help='Enable premium dynamic tracking and subtitles')
@click.option('--visual-ai', is_flag=True, help='Upload video to Gemini for multi-modal visual analysis')
def process(video_path, api_key, premium, visual_ai):
    """Process a video file with professional AI editing."""
    if not api_key:
        console.print("[bold red]Error: No Gemini API Key provided.[/bold red]")
        return

    console.print(f"[bold green]🚀 Starting Professional Edit:[/bold green] {video_path}")
    
    # 1. Transcribe
    transcriber = Transcriber(model_size="tiny")
    transcript = transcriber.transcribe(video_path)
    
    # 2. Analyze (Now with optional multi-modal visual analysis)
    analyzer = VideoAnalyzer(api_key=api_key)
    video_to_upload = video_path if visual_ai else None
    viral_moments = analyzer.find_viral_moments(transcript, video_path=video_to_upload)
    
    if not viral_moments:
        console.print("[bold yellow]Using fallback moment.[/bold yellow]")
        viral_moments = [{"start": 0, "end": 15, "headline": "Premium Demo", "reason": "Test"}]

    # 3. Initialize Professional Tools
    editor = VideoEditor()
    tracker = FaceTracker()
    subtitler = Subtitler()
    output_dir = os.path.join(os.path.dirname(os.path.abspath(video_path)), "clips")
    os.makedirs(output_dir, exist_ok=True)
    
    for i, moment in enumerate(viral_moments):
        # Sanitize filename
        clean_headline = "".join([c if c.isalnum() else "_" for c in moment['headline']])[:30].lower()
        base_name = f"clip_{i+1}_{clean_headline}"
        
        # A. Cut Raw Clip
        raw_output = os.path.join(output_dir, f"{base_name}_raw.mp4")
        editor.cut_segment(video_path, moment['start'], moment['end'], raw_output)
        
        if premium:
            # B. Premium Motion Tracking
            motion_path = tracker.analyze_motion_path(raw_output)
            
            # C. Dynamic Verticalization
            v_output = os.path.join(output_dir, f"{base_name}_v_temp.mp4")
            editor.premium_verticalize(raw_output, motion_path, v_output)
            
            # D. Subtitles
            clip_segs = []
            for s in transcript['segments']:
                if s['start'] >= moment['start'] and s['end'] <= moment['end']:
                    new_seg = s.copy()
                    new_seg['start'] -= moment['start']
                    new_seg['end'] -= moment['start']
                    clip_segs.append(new_seg)
            
            ass_path = os.path.join(output_dir, f"{base_name}.ass")
            subtitler.generate_ass(clip_segs, ass_path)
            
            # E. Burn-in Subtitles
            final_output = os.path.join(output_dir, f"{base_name}_PRO.mp4")
            console.print(f'[bold green]Burning professional subtitles...[/bold green]')
            
            try:
                (
                    ffmpeg
                    .input(v_output)
                    .filter('ass', ass_path)
                    .output(final_output, vcodec='libx264', acodec='copy')
                    .overwrite_output()
                    .run(quiet=True)
                )
                console.print(f"[bold cyan]✨ Professional Edit Complete:[/bold cyan] {final_output}")
                # Cleanup temp
                if os.path.exists(v_output): os.remove(v_output)
                if os.path.exists(raw_output): os.remove(raw_output)
            except Exception as e:
                console.print(f"[bold red]Subtitle burn failed:[/bold red] {e}")

if __name__ == '__main__':
    cli()