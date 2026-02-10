import os
from google import genai
from google.genai import types
import json
from rich.console import Console
import re

console = Console()

class VideoAnalyzer:
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)

    def find_viral_moments(self, transcription_result):
        segments = transcription_result.get('segments', [])
        transcript_text = transcription_result.get('text', '')
        
        # Use a more explicit prompt for JSON-only output
        prompt = f"""
        Analyze the following video transcript and identify the top 3 most engaging, high-impact 'viral' segments suitable for TikTok/Reels (approx 30-60s each).
        
        IMPORTANT: Your output must be ONLY a valid JSON array. Do not include any explanation, markdown formatting, or preamble.
        
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
        
        try:
            response = self.client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type='application/json',
                )
            )
            
            # The new SDK might return the parsed JSON directly if we use response_mime_type
            if hasattr(response, 'parsed') and response.parsed:
                return response.parsed
                
            text = response.text.strip()
            
            # Fallback parsing if JSON mode didn't return a direct object
            match = re.search(r'\[.*\]', text, re.DOTALL)
            if match:
                text = match.group(0)
                
            return json.loads(text)
            
        except Exception as e:
            console.print(f'[bold red]Error parsing Gemini response:[/bold red] {e}')
            if 'response' in locals():
                console.print(f'Raw response: {response.text}')
            return []
