# cd /Users/jiamulin/Desktop/Sentiment-Flow/UOttaHack8-Sentiment-Flow
# streamlit run dashboard.py
import streamlit as st
import json
import time
import pandas as pd
from pathlib import Path
import os
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Sentiment-Flow | Dashboard", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0E1117; color: #F0F0F0; }
    .stMetric { background-color: rgba(45, 20, 10, 0.6); border: 1px solid #303030; padding: 15px; border-radius: 10px; }
    [data-testid="stMetricValue"] { color: #B4FF96; }
    </style>
    """, unsafe_allow_html=True)

st_autorefresh(interval=200, key="datarefresh")

def get_live_data():
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    p = Path(os.path.join(script_dir, "live_data.json"))
    
    if p.exists():
        try:
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            return None
    return None

if "history" not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=["ts", "eye", "yawn", "smile", "confused"])


left_col, right_col = st.columns([2, 1], gap="large")

with left_col:
    st.markdown("<h2 style='color: #B4FF96;'>RESEARCH STIMULUS</h2>", unsafe_allow_html=True)
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") 
    st.caption("💡 Invisible Feedback is active. AI is analyzing your reaction to this content.")
    
    st.divider()
    if st.button("🏁 GENERATE INSIGHT REPORT"):
        st.write("🔄 Connecting to OpenAI to synthesize your emotional journey...")
        
with right_col:
    st.markdown("<h2 style='color: #F0F0F0;'>LIVE ANALYTICS</h2>", unsafe_allow_html=True)
    
    live = get_live_data()
    
    if live:
        eye_v = float(live.get("eye_score") or 0.0)
        yawn_v = float(live.get("yawn_score") or 0.0)
        smile_v = float(live.get("smile_score") or 0.0)
        confused_v = float(live.get("confused_score") or 0.0)
        status = str(live.get("status") or "SCANNING")

        
        new_row = {
            "ts": time.time(),
            "eye": eye_v,
            "yawn": yawn_v,
            "smile": smile_v,
            "confused": confused_v
        }
        st.session_state.history = pd.concat([st.session_state.history, pd.DataFrame([new_row])], ignore_index=True).tail(100)
        st.info(f"Current State: {status}")

        
        c1, c2 = st.columns(2)
        with c1:
            st.metric("EYE", f"{eye_v:.2f}")
            st.metric("SMILE", f"{smile_v:.2f}")
        with c2:
            st.metric("YAWN", f"{yawn_v:.2f}")
            st.metric("CONFUSION", f"{confused_v:.2f}")

        
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=st.session_state.history["eye"], name="Eye", line=dict(color='#B4FF96')))
        fig.add_trace(go.Scatter(y=st.session_state.history["smile"], name="Smile", line=dict(color='#FFB450')))
        fig.add_trace(go.Scatter(y=st.session_state.history["confused"], name="Confusion", line=dict(color='#FF6464')))
        fig.update_layout(height=350, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("📡 Waiting for engine data...")
