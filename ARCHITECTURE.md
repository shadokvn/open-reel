# OpenReel Architecture

OpenReel follows a modular pipeline architecture designed for high-performance video processing on consumer hardware, now enhanced with cloud-based multi-modal perception.

## Pipeline Workflow

1. **Ingestion Stage**: 
    - The video is processed locally for audio.
    - (Optional) The video is uploaded to Gemini Cloud for visual context analysis.

2. **Perception Stage**: 
    - **Transcription**: Whisper processes audio into time-synced segments.
    - **Visual Analysis**: Gemini 2.0 "watches" the raw video to detect visual energy, scene changes, and production quality.
    - **Face Tracking**: MediaPipe analyzes frames locally to generate a normalized motion path (X, Y, Scale).

3. **Cognition Stage**: The `VideoAnalyzer` performs a hybrid analysis. It merges linguistic impact from the transcript with visual impact from the multi-modal analysis to select the top 5 'viral' candidates.

4. **Production Stage**:
    - **Cutting**: Segments are extracted using FFmpeg.
    - **Dynamic Transform**: A moving-crop filter is applied based on the motion path data.
    - **Subtitle Synthesis**: .ass files are generated with professional social media styling.
    - **Compositing**: Subtitles are burned into the final vertical output.