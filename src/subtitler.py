import os

class Subtitler:
    def format_timestamp(self, seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        centiseconds = int((seconds % 1) * 100)
        return f"{hours}:{minutes:02d}:{secs:02d}.{centiseconds:02d}"

    def generate_ass(self, segments, output_path):
        """Generates a styled .ass subtitle file."""
        header = """[Script Info]
ScriptType: v4.00+
PlayResX: 384
PlayResY: 640

[v4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,24,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,2,1,2,10,10,100,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
        with open(output_path, 'w') as f:
            f.write(header)
            for seg in segments:
                start = self.format_timestamp(seg['start'])
                end = self.format_timestamp(seg['end'])
                text = seg['text'].strip().upper()
                # Split long lines
                if len(text) > 20:
                    words = text.split()
                    # Use double backslash for .ass newline
                    text = "\\N".join([" ".join(words[i:i+3]) for i in range(0, len(words), 3)])
                
                f.write(f"Dialogue: 0,{start},{end},Default,,0,0,0,,{text}\n")
        return output_path