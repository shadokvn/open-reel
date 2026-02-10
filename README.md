# 🎥 OpenReel: The Open Source AI Video Editor

OpenReel is a professional-grade, agentic video editing suite designed to turn landscape footage into viral vertical content (TikToks, Reels, Shorts) autonomously. It leverages state-of-the-art AI for transcription, multi-modal visual analysis, and computer vision for dynamic face tracking.

## 🚀 Key Features

- **Multi-modal Visual Analysis:** Uses Gemini 2.0 Flash to "watch" the video, identifying high-energy performances and dramatic lighting that transcripts miss.
- **Autonomous Viral Clipping:** Combines visual cues and transcript data to find the absolute best moments for social media.
- **AI Transcription:** Powered by OpenAI Whisper for high-accuracy, time-synced lyrics and dialogue extraction.
- **Premium Face Tracking:** Utilizes MediaPipe Tasks (BlazeFace) to track subjects frame-by-frame.
- **Dynamic "Gimbal" Camera:** Smoothly pans and zooms the vertical crop window to follow the action, avoiding static center-crops.
- **Professional Captions:** Generates and burns in styled `.ass` subtitles with modern, social-media-optimized typography.
- **FFmpeg Powered:** Lightning-fast video processing and high-quality re-encoding.

## 🛠 Tech Stack

- **LLM/Vision:** Google Gemini 2.0 Flash (Multi-modal Analysis)
- **STT:** OpenAI Whisper (Transcription)
- **CV:** MediaPipe / OpenCV (Face Tracking)
- **Engine:** FFmpeg & MoviePy (Video Manipulation)
- **CLI:** Click & Rich (User Experience)

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/shadokvn/open-reel.git
cd open-reel

# Setup virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download the Face Detection model
curl -o detector.tflite https://storage.googleapis.com/mediapipe-models/face_detector/blaze_face_short_range/float16/1/blaze_face_short_range.tflite
```

## 🎯 Usage

Set your Gemini API key:
```bash
export GEMINI_API_KEY='your_api_key_here'
```

Run the full multi-modal professional pipeline:
```bash
python cli.py process path/to/video.mp4 --premium --visual-ai
```

## 📂 Project Structure

- `cli.py`: Main entry point and orchestration logic.
- `src/transcriber.py`: Handles audio extraction and Whisper transcription.
- `src/analyzer.py`: Multi-modal analysis (Text + Vision) via Gemini.
- `src/tracker.py`: CV logic for face detection and motion path smoothing.
- `src/editor.py`: MoviePy/FFmpeg wrappers for cutting and dynamic cropping.
- `src/subtitler.py`: Generates styled professional subtitles.

## 📜 License

This project is licensed under the **PolyForm Noncommercial License 1.0.0**. 

- **Non-Commercial Use:** Free for personal and non-commercial projects.
- **Commercial Use:** Requires a separate commercial license. Please contact the maintainers for commercial inquiries.