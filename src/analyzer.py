import os
import time
from google import genai
from google.genai import types
import json
from rich.console import Console
import re
import mimetypes

console = Console()

class VideoAnalyzer:
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)

    def analyze_visuals_with_gemini(self, video_path):
        """
        Uploads the video to Gemini and analyzes visual cues using the latest SDK syntax.
        """
        console.print(f'[bold magenta]Uploading video to Gemini for visual analysis...[/bold magenta]')
        
        mime_type, _ = mimetypes.guess_type(video_path)
        if not mime_type:
            mime_type = "video/mp4" # Default fallback
            
        # New SDK uses 'file' instead of 'path' in some versions or direct upload
        with open(video_path, "rb") as f:
            file_ref = self.client.files.upload(file=f, config=types.UploadFileConfig(mime_type=mime_type))
        
        while file_ref.state.name == "PROCESSING":
            console.print("   ⏳ Processing video in Gemini's cloud...", end="\r")
            time.sleep(5)
            file_ref = self.client.files.get(name=file_ref.name)
            
        if file_ref.state.name == "FAILED":
            raise ValueError(f"Video processing failed in Gemini: {file_ref.state}")

        console.print('\n[bold green]Video processed! Analyzing visual high-energy moments...[/bold green]')
        
        prompt = """
        Analyze this video visually. Identify the top 3 most visually engaging segments (good lighting, high energy, dramatic movement, or significant scene changes).
        
        Return the result EXCLUSIVELY as a JSON list:
        [
          {
            "start": float,
            "end": float,
            "reason": "visual reason (e.g., dynamic performance, dramatic lighting shift)",
            "headline": "catchy visual hook"
          }
        ]
        """
        
        response = self.client.models.generate_content(
            model='gemini-2.0-flash',
            contents=[types.Content(role="user", parts=[types.Part.from_uri(file_uri=file_ref.uri, mime_type=file_ref.mime_type)]), prompt],
            config=types.GenerateContentConfig(
                response_mime_type='application/json',
            )
        )
        
        # Cleanup file from Gemini
        self.client.files.delete(name=file_ref.name)
        
        moments = []
        try:
            if hasattr(response, 'parsed') and response.parsed:
                moments = response.parsed
            else:
                moments = json.loads(response.text.strip())
        except Exception as e:
            console.print(f"[yellow]Failed to parse visual moments: {e}[/yellow]")
            
        return moments if isinstance(moments, list) else []

    def find_viral_moments(self, transcription_result, video_path=None):
        """
        Combines Transcript Analysis with Visual Analysis if video_path is provided.
        """
        segments = transcription_result.get('segments', [])
        transcript_text = transcription_result.get('text', '')
        
        # 1. Visual Analysis (Multi-modal)
        visual_moments = []
        if video_path:
            try:
                visual_moments = self.analyze_visuals_with_gemini(video_path)
            except Exception as e:
                console.print(f"[yellow]Visual analysis skipped: {e}[/yellow]")

        # 2. Textual Analysis
        prompt = f"""
        Analyze the following video transcript. Identify high-impact moments based on lyrics/dialogue.
        
        Transcript:
        {transcript_text}
        
        Required JSON Structure:
        [
          {{
            "start": float,
            "end": float,
            "reason": "why this is viral",
            "headline": "catchy hook headline"
          }}
        ]
        
        Segment Timestamps:
        {json.dumps([{'start': s['start'], 'end': s['end'], 'text': s['text']} for s in segments[:100]])}
        """
        
        console.print('[bold magenta]Analyzing transcript with Gemini 2.0...[/bold magenta]')
        
        text_moments = []
        try:
            response = self.client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type='application/json',
                )
            )
            text_moments = response.parsed if hasattr(response, 'parsed') else json.loads(response.text.strip())
        except Exception as e:
            console.print(f"[yellow]Textual analysis failed: {e}[/yellow]")

        # Combine and deduplicate
        if not isinstance(text_moments, list): text_moments = []
        if not isinstance(visual_moments, list): visual_moments = []
        
        all_moments = visual_moments + text_moments
        return all_moments[:5]