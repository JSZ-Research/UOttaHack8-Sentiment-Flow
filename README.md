# Sentiment Flow

**Capture sentiment, not attention.**

A real-time facial signal monitoring system that captures user feedback passively — no forms, no clicks, no friction.

---

## What is this?

Traditional surveys interrupt users and demand their time. Sentiment Flow flips that model: it observes facial signals while users consume content, turning passive viewing into actionable feedback data.

Paste any URL — a survey, a video, a product ad, a landing page — and the system tracks engagement in real time. Results sync directly to SurveyMonkey.

---
Live Demo (YouTube): Live Demo
---

## Features

- **Content-agnostic input**: Works with any URL (surveys, videos, ads, landing pages, etc.)
- **Real-time facial landmark detection**: Powered by MediaPipe
  - Fatigue indicators: eye closure, yawning, head tilt angle
  - Expression tracking: smile detection, frown detection
  - Gaze direction monitoring
- **Live dashboard**: Time-series visualization of engagement metrics
- **LLM-powered analysis**: AI-generated session summaries via OpenAI API
- **SurveyMonkey integration**: Automatic data sync to SurveyMonkey backend

---

## Architecture

```
User inputs URL → app.py opens content
                        ↓
              Webcam runs in background
                        ↓
         Facial Landmark Detection (MediaPipe)
              ├─ Fatigue signals
              ├─ Expression signals
              └─ Gaze tracking
                        ↓
         Engagement scoring + time-series data
                        ↓
              LLM analysis (OpenAI API)
                        ↓
            Sync to SurveyMonkey backend
```

The system runs as two separate processes:
- **Engine** (`sentiment_flow_engine.py`): Handles webcam input, facial analysis, and exposes an MJPEG stream
- **Dashboard** (`dashboard.py`): Streamlit frontend that reads processed data and visualizes metrics

This separation keeps the UI responsive while the vision pipeline runs continuously.

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Facial detection | MediaPipe Face Landmarker |
| Video streaming | MJPEG over HTTP |
| Dashboard | Streamlit |
| AI analysis | OpenAI API |
| Data sync | SurveyMonkey API |
| Language | Python |

---

## Getting Started

### Prerequisites

```bash
pip install -r requirements.txt
```

You'll need:
- OpenAI API key
- SurveyMonkey API credentials

### Running the system

Simply run:

```bash
python app.py
```

This will:
1. Prompt you to enter a URL
2. Open the content in your browser
3. Start the facial detection engine
4. Launch the Streamlit dashboard

Alternatively, run components separately:

**Terminal A (engine):**
```bash
python sentiment_flow_engine.py
```

**Terminal B (dashboard):**
```bash
streamlit run dashboard.py
```

Dashboard will be available at `http://127.0.0.1:8501`

---

## File Structure

```
├── app.py                    # Main entry point
├── sentiment_flow_engine.py  # Webcam + facial analysis engine
├── dashboard.py              # Streamlit visualization
├── analysis_agent.py         # LLM-powered summary generation
├── face_landmarker.task      # MediaPipe model file
├── live_data.json            # Real-time data buffer
├── find_ids.py               # Utility scripts
├── get_details.py
└── test_sync.py
```

---

## Demo

A sample stimulus video is included for testing. It uses a bait-and-switch format (tense setup → Rickroll) designed to trigger a detectable smile response, demonstrating that the facial detection pipeline works.

---

## Background

Built at **uOttaHack 8** for the SurveyMonkey Challenge.

The challenge asked participants to "make static forms obsolete" and build solutions where feedback is "invisible, gamified, or instantaneous." Sentiment Flow answers that by making the user's face the survey — no forms required.

---

## Team

- **Jiamu** 
- **Junkai**

---

## License

MIT
