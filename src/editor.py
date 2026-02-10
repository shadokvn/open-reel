from moviepy import VideoFileClip, vfx
import numpy as np
from rich.console import Console
import os

console = Console()

class VideoEditor:
    def cut_segment(self, input_path, start, end, output_path):
        console.print(f'[bold cyan]Cutting segment:[/bold cyan] {start}s to {end}s')
        with VideoFileClip(input_path) as video:
            new = video.subclipped(start, end)
            new.write_videofile(output_path, codec="libx264", audio_codec="aac", logger=None)
        return output_path

    def premium_verticalize(self, input_path, motion_path, output_path):
        """
        Applies a dynamic camera following the motion_path (x, y, scale).
        """
        console.print(f'[bold magenta]Applying Premium Dynamic Tracking...[/bold magenta]')
        
        with VideoFileClip(input_path) as clip:
            w, h = clip.size
            target_h = h
            target_w = int(h * 9/16)
            
            fps = clip.fps
            
            def get_crop_params(t):
                frame_idx = int(t * fps)
                if frame_idx >= len(motion_path):
                    frame_idx = len(motion_path) - 1
                
                center_x, center_y, scale = motion_path[frame_idx]
                
                # Convert normalized to pixels
                px_x = center_x * w
                
                # Calculate X offset for crop
                x1 = px_x - (target_w / 2)
                
                # Clamp to frame boundaries
                x1 = max(0, min(x1, w - target_w))
                
                return x1

            # MoviePy 2.x dynamic cropping
            # We iterate through frames or use a transformation
            # For a "Premium" feel, we'll use a cropping transformation
            
            def crop_fn(get_frame, t):
                frame = get_frame(t)
                x1 = int(get_crop_params(t))
                return frame[:, x1:x1+target_w]

            # Apply the dynamic crop
            final_clip = clip.transform(crop_fn)
            
            # Write with high-quality settings
            final_clip.write_videofile(
                output_path, 
                codec="libx264", 
                audio_codec="aac", 
                bitrate="5000k", 
                preset="medium",
                logger=None
            )
            
        return output_path
