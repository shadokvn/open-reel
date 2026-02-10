# OpenReel Architecture

OpenReel follows a modular pipeline architecture designed for high-performance video processing on consumer hardware.

## Pipeline Workflow

1. **Extraction Stage**: Audio is stripped from the source video using FFmpeg.
2. **Perception Stage**: 
    - **Transcription**: Whisper processes audio into time-synced segments.
    - **Face Tracking**: MediaPipe analyzes frames to generate a normalized motion path (X, Y, Scale).
3. **Cognition Stage**: The transcript is fed to Gemini 2.0 Flash with a specialized prompt to extract 'viral moments' based on linguistic impact and timing.
4. **Production Stage**:
    - **Cutting**: Segments are extracted.
    - **Dynamic Transform**: A moving-crop filter is applied based on the perception data.
    - **Subtitle Synthesis**: .ass files are generated with primary/secondary color styling.
    - **Compositing**: Subtitles are burned into the final vertical output.
