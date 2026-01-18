# UOttaHack8-Sentiment-Flow
 Project by Jiamu and Junkai in UOttaHack8
# Sentiment Flow (UOttaHack 8)

This is a small UOttaHack 8 project that turns a webcam stream into a live “signal flow” dashboard. The engine keeps running in its own process, and the dashboard just reads the latest outputs, so the UI stays smooth instead of freezing when the vision loop gets heavy.

You’ll see a live camera panel, a few time-series curves, and (optionally) an AI-generated summary based on the recent data.

## Running it

You need two terminals.

Terminal A (engine):

```bash
source venv/bin/activate
python3 sentiment_flow_engine.py
```

If you want to sanity check the video stream:

```bash
curl -I http://127.0.0.1:8000/video_feed
```

Terminal B (dashboard):

```bash
source venv/bin/activate
streamlit run dashboard.py
```

Then open:
`http://127.0.0.1:8501`

## What’s in here

`sentiment_flow_engine.py` handles the webcam + face processing and writes out the “latest state” files used by the UI. It also serves the MJPEG feed at `http://127.0.0.1:8000/video_feed`.

`dashboard.py` is the Streamlit front end. It reads `live_data.json`, plots the live curves, and embeds the MJPEG stream.

`analysis_agent.py` is the optional AI helper. The dashboard imports it to generate a short report/summary. If you don’t care about that part, you can ignore it.

## Notes

If the dashboard loads but the camera panel is blank, the first thing to check is whether the engine is actually running and the stream endpoint responds. Opening `http://127.0.0.1:8000/video_feed` directly in a browser is the fastest test.

Also, `127.0.0.1` only works when the engine and dashboard are on the same machine. If you ever split them across two laptops, the dashboard needs to point to the engine machine’s LAN IP instead.

## Why it’s split into two processes

I tried doing “read frame → display in Streamlit” at first, and it was flickery and choppy. Keeping the engine separate and using MJPEG for the camera feed ended up being a lot more stable for a demo.
