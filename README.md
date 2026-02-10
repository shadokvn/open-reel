# 🎥 OpenReel: The Open Source AI Video Editor

OpenReel is a professional-grade, agentic video editing suite designed to turn landscape footage into viral vertical content (TikToks, Reels, Shorts) autonomously. It leverages state-of-the-art AI for transcription, content analysis, and computer vision for dynamic face tracking.

## 🚀 Key Features

- **Autonomous Viral Clipping:** Uses Gemini 2.0 Flash to analyze transcripts and identify the most engaging moments.
- **AI Transcription:** Powered by OpenAI Whisper for high-accuracy, time-synced lyrics and dialogue extraction.
- **Premium Face Tracking:** Utilizes MediaPipe Tasks (BlazeFace) to track subjects frame-by-frame.
- **Dynamic "Gimbal" Camera:** Smoothly pans and zooms the vertical crop window to follow the action, avoiding static center-crops.
- **Professional Captions:** Generates and burns in styled `.ass` (Advanced Substation Alpha) subtitles with modern, social-media-optimized typography.
- **FFmpeg Powered:** Lightning-fast video processing and high-quality re-encoding.

## 🛠 Tech Stack

- **LLM:** Google Gemini 2.0 Flash (Analysis & Hooks)
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

Run the professional pipeline:
```bash
python cli.py process path/to/video.mp4 --premium
```

## 📂 Project Structure

- `cli.py`: Main entry point and orchestration logic.
- `src/transcriber.py`: Handles audio extraction and Whisper transcription.
- `src/analyzer.py`: Communicates with Gemini to find viral segments.
- `src/tracker.py`: CV logic for face detection and motion path smoothing.
- `src/editor.py`: MoviePy/FFmpeg wrappers for cutting and dynamic cropping.
- `src/subtitler.py`: Generates styled professional subtitles.

## 📜 License

MIT License - see [LICENSE](LICENSE) for details.
