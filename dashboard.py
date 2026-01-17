# cd /Users/jiamulin/Desktop/Sentiment-Flow/UOttaHack8-Sentiment-Flow
# streamlit run dashboard.py

import streamlit as st
import json
import time
import pandas as pd
from pathlib import Path
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh
import os

st.set_page_config(page_title="Sentiment-Flow | Dashboard", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0E1117; color: #F0F0F0; }
    .stMetric { background-color: rgba(45, 20, 10, 0.6); border: 1px solid #303030; padding: 15px; border-radius: 10px; }
    [data-testid="stMetricValue"] { color: #B4FF96; }
    </style>
    """, unsafe_allow_html=True)

st_autorefresh(interval=300, key="datarefresh")

def get_live_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    p = Path(os.path.join(script_dir, "live_data.json"))
    if p.exists():
        try:
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
        except: return None
    return None

if "history" not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=["ts", "eye_open", "smile", "tilt", "confused"])

left_col, right_col = st.columns([2, 1], gap="large")

with left_col:
    st.markdown("<h2 style='color: #B4FF96;'>RESEARCH STIMULUS</h2>", unsafe_allow_html=True)
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") 
    st.caption("💡 Natural responses are being quantified through JSZ Sentiment Engine.")
    
    st.divider()
    if st.button("🏁 GENERATE AI INSIGHT REPORT"):
        st.info("🔄 Processing historical data points for OpenAI synthesis...")

with right_col:
    st.markdown("<h2 style='color: #F0F0F0;'>LIVE ANALYTICS</h2>", unsafe_allow_html=True)
    
    live = get_live_data()
    if live:
        raw_eye = float(live.get("eye_score") or 0.0)
        eye_openness = 1.0 - raw_eye 
        
        smile_v = float(live.get("smile_score") or 0.0)
        tilt_v = float(live.get("tilt_val") or 0.0)
        confused_v = float(live.get("confused_score") or 0.0)
        status = str(live.get("status") or "SCANNING")

        new_row = {
            "ts": time.time(),
            "eye_open": eye_openness,
            "smile": smile_v,
            "tilt": tilt_v,
            "confused": confused_v
        }
        st.session_state.history = pd.concat([st.session_state.history, pd.DataFrame([new_row])], ignore_index=True).tail(80)

        st.info(f"Analysis State: {status}")

        c1, c2 = st.columns(2)
        with c1:
            st.metric("EYE OPEN", f"{eye_openness:.2f}")
            st.metric("SMILE", f"{smile_v:.2f}")
        with c2:
            st.metric("STABILITY", f"{100-tilt_v:.1f}%")
            st.metric("CONFUSION", f"{confused_v:.2f}")

        from plotly.subplots import make_subplots
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(go.Scatter(y=st.session_state.history["eye_open"], 
                                 name="Eye Openness", 
                                 line=dict(color='#B4FF96', width=3, shape='spline')), secondary_y=False)
        
        fig.add_trace(go.Scatter(y=st.session_state.history["smile"], 
                                 name="Smile Index", 
                                 line=dict(color='#FFB450', width=3, shape='spline')), secondary_y=False)

        fig.add_trace(go.Scatter(y=st.session_state.history["tilt"], 
                                 name="Head Tilt (Deg)", 
                                 line=dict(color='#64B4FF', width=2, dash='dot', shape='spline')), secondary_y=True)

        fig.update_layout(
            height=400,
            margin=dict(l=0, r=0, t=20, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation="h", yanchor="bottom", y=1.1, xanchor="center", x=0.5),
            yaxis=dict(range=[0, 1.1], showgrid=True, gridcolor='#303030', title="Score (0-1)"),
            yaxis2=dict(range=[0, 60], showgrid=False, title="Degrees")
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("📡 Waiting for engine data sync...")
