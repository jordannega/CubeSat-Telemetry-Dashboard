import streamlit as st
import random
import time
import pandas as pd
import pydeck as pdk
import numpy as np
from datetime import datetime

# ---------- 1. PAGE CONFIG ----------
st.set_page_config(
    page_title="AETHER MCS",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- 2. INITIALIZE STATE ----------
if "theme" not in st.session_state:
    st.session_state.theme = "dark"
if "show_controls" not in st.session_state:
    st.session_state.show_controls = False

# Persistent Mission Vars
if "altitude" not in st.session_state:
    st.session_state.altitude = 12000
if "battery" not in st.session_state:
    st.session_state.battery = 100.0
if "lat" not in st.session_state:
    st.session_state.lat = 9.03
if "lon" not in st.session_state:
    st.session_state.lon = 38.74
if "path_history" not in st.session_state:
    st.session_state.path_history = [{"lat": 9.03, "lon": 38.74}]
if "heading" not in st.session_state:
    st.session_state.heading = 0.75
if "step_counter" not in st.session_state:
    st.session_state.step_counter = 0
if "mission_start" not in st.session_state:
    st.session_state.mission_start = datetime.now()
if "command_log" not in st.session_state:
    st.session_state.command_log = ["System Initialization Successful"]

# Protected Control States (Prevents resetting when panel is hidden)
if "speed_val" not in st.session_state:
    st.session_state.speed_val = 3
if "sails_val" not in st.session_state:
    st.session_state.sails_val = False

if "data_history" not in st.session_state:
    st.session_state.data_history = []
    for i in range(5):
        st.session_state.data_history.append({
            "Cycle": i,
            "Roll": np.sin(i * 0.2) * 15,
            "Pitch": np.cos(i * 0.15) * 10,
            "Yaw": np.sin(i * 0.05) * 35
        })

# ---------- 3. STATE CALLBACKS ----------
def toggle_controls_cb():
    st.session_state.show_controls = not st.session_state.show_controls

def toggle_theme_cb():
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"

def sync_controls():
    st.session_state.speed_val = st.session_state.speed_widget
    st.session_state.sails_val = st.session_state.sails_widget

def port_burn_cb():
    st.session_state.heading -= 0.35
    st.session_state.command_log.append(f"Port burn @ {datetime.now().strftime('%H:%M:%S')}")

def starboard_burn_cb():
    st.session_state.heading += 0.35
    st.session_state.command_log.append(f"Starboard burn @ {datetime.now().strftime('%H:%M:%S')}")

def deorbit_cb():
    st.session_state.altitude = 0
    st.session_state.lat = 9.03
    st.session_state.lon = 38.74
    st.session_state.heading = 0.75
    st.session_state.path_history = [{"lat": 9.03, "lon": 38.74}]
    st.session_state.command_log.append(f"⚠️ DE-ORBIT @ {datetime.now().strftime('%H:%M:%S')}")

# ---------- 4. THEME CSS (ANTI-GHOSTING) ----------
def get_css(theme):
    base_bg = "#f5f7fa" if theme == "light" else "#0b0f1a"
    base_txt = "#1a1a2e" if theme == "light" else "#ffffff"
    container_bg = "rgba(255, 255, 255, 0.95)" if theme == "light" else "rgba(255, 255, 255, 0.05)"
    container_border = "rgba(0, 0, 0, 0.08)" if theme == "light" else "rgba(255, 255, 255, 0.08)"
    metric_bg = "rgba(255, 255, 255, 0.8)" if theme == "light" else "rgba(255, 255, 255, 0.04)"
    metric_border = "rgba(0, 0, 0, 0.06)" if theme == "light" else "rgba(255, 255, 255, 0.1)"
    log_border = "rgba(0, 0, 0, 0.04)" if theme == "light" else "rgba(255, 255, 255, 0.04)"
    
    return f"""
    <style>
    /* PREVENTS STREAMLIT FROM FADING THE PAGE DURING RERUNS */
    [data-stale="true"] {{ opacity: 1 !important; transition: none !important; }}
    
    .stApp {{ background: {base_bg}; color: {base_txt}; }}
    .main > div {{ padding: 1.5rem 2rem !important; max-width: 1400px !important; margin: 0 auto !important; }}
    #MainMenu, footer, header {{visibility: hidden;}}
    
    .controls-container {{ background: {container_bg}; border: 1px solid {container_border}; border-radius: 12px; padding: 20px; margin-bottom: 20px; }}
    div[data-testid="stMetric"] {{ background: {metric_bg}; border: 1px solid {metric_border}; border-radius: 12px; padding: 14px 16px 12px 16px; }}
    div[data-testid="stMetricValue"] {{ color: {base_txt} !important; font-weight: 600 !important; font-size: 22px !important; }}
    div[data-testid="stMetricLabel"] {{ color: {base_txt} !important; opacity: 0.95 !important; font-weight: 600 !important; font-size: 11px !important; text-transform: uppercase; letter-spacing: 1px; }}
    
    h1, h2, h3, h4 {{ color: {base_txt} !important; }}
    h3 {{ font-weight: 600 !important; font-size: 13px !important; letter-spacing: 1px !important; text-transform: uppercase; margin-bottom: 10px !important; opacity: 1.0 !important; }}
    
    .brand-title {{ color: {base_txt} !important; font-size: 26px !important; font-weight: 300 !important; letter-spacing: 3px !important; }}
    .stButton > button {{ background: rgba(255, 255, 255, 0.08) !important; border: 1px solid rgba(255, 255, 255, 0.2) !important; color: {base_txt} !important; border-radius: 8px !important; padding: 6px 14px !important; font-size: 12px !important; font-weight: 600 !important; width: 100% !important; }}
    
    .stToggle label, div[data-testid="stSlider"] label {{ color: {base_txt} !important; opacity: 1.0 !important; font-weight: 600 !important; }}
    
    .log-entry {{ color: {base_txt} !important; opacity: 0.85 !important; font-size: 11px !important; font-family: 'Courier New', monospace !important; padding: 4px 0 !important; border-bottom: 1px solid {log_border} !important; }}
    .log-entry.danger {{ color: #ff6b6b !important; opacity: 1.0 !important; font-weight: bold; }}
    .log-entry.warning {{ color: #f2b05e !important; opacity: 1.0 !important; font-weight: bold; }}
    
    hr, .section-divider {{ border: none; border-top: 1px solid {container_border}; margin: 12px 0 16px 0; }}
    </style>
    """

st.markdown(get_css(st.session_state.theme), unsafe_allow_html=True)

# ---------- 5. CONTROLS INTERFACE ----------
st.button("☰ Toggle Control Panel Matrix", on_click=toggle_controls_cb)

if st.session_state.show_controls:
    with st.container():
        st.markdown('<div class="controls-container">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown("**Theme**")
            st.button("🌓 Switch Mode", on_click=toggle_theme_cb, use_container_width=True)
        
        with col2:
            st.markdown("**Propulsion Configuration**")
            st.toggle("Solar Sails Deploy", value=st.session_state.sails_val, key="sails_widget", on_change=sync_controls)
            st.slider("Thrust Velocity", min_value=1, max_value=15, value=st.session_state.speed_val, key="speed_widget", on_change=sync_controls)
        
        col3, col4, col5 = st.columns(3)
        with col3:
            st.markdown("**Attitude Adjustments**")
            st.button("◀ Port Vector Burn", on_click=port_burn_cb, use_container_width=True)
        with col4:
            st.markdown("**&nbsp;**")
            st.button("▶ Starboard Vector Burn", on_click=starboard_burn_cb, use_container_width=True)
        with col5:
            st.markdown("**Emergency Override**")
            st.button("🚨 System De-Orbit", on_click=deorbit_cb, use_container_width=True)
        
        st.markdown("**Uplink Execution Log**")
        if st.session_state.command_log:
            for entry in st.session_state.command_log[-4:]:
                if "DE-ORBIT" in entry:
                    st.markdown(f'<div class="log-entry danger">▸ {entry}</div>', unsafe_allow_html=True)
                elif "⚠️" in entry:
                    st.markdown(f'<div class="log-entry warning">▸ {entry}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="log-entry">▸ {entry}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# ---------- 6. MISSION LOGIC PROCESSING (ONE FRAME) ----------
st.session_state.step_counter += 1

elapsed = datetime.now() - st.session_state.mission_start
h, rem = divmod(elapsed.seconds, 3600)
m, s = divmod(rem, 60)

current_speed = st.session_state.speed_val
current_sails = st.session_state.sails_val

if st.session_state.altitude > 0:
    alt_gain = random.randint(25, 60) * current_speed
    st.session_state.altitude += alt_gain
    temp = -45.2 + (np.sin(st.session_state.step_counter * 0.1) * 5.5)

    if current_sails:
        st.session_state.battery = min(100.0, st.session_state.battery + 0.4)
    else:
        st.session_state.battery = max(0.0, st.session_state.battery - (0.05 * current_speed))

    step = 0.0025 * current_speed
    st.session_state.lat += step * np.cos(st.session_state.heading)
    st.session_state.lon += step * np.sin(st.session_state.heading)
else:
    alt_gain = 0
    temp = 21.5
    st.session_state.battery = 100.0

st.session_state.path_history.append({"lat": st.session_state.lat, "lon": st.session_state.lon})
if len(st.session_state.path_history) > 500:
    st.session_state.path_history = st.session_state.path_history[-500:]

t = st.session_state.step_counter
data = {
    "Cycle": t,
    "Roll": np.sin(t * 0.2) * 15,
    "Pitch": np.cos(t * 0.15) * 10,
    "Yaw": np.sin(t * 0.05) * 35
}
st.session_state.data_history.append(data)
if len(st.session_state.data_history) > 100:
    st.session_state.data_history = st.session_state.data_history[-100:]

df_history = pd.DataFrame(st.session_state.data_history[-25:])
df_path = pd.DataFrame(st.session_state.path_history)
df_current = pd.DataFrame([{"lat": st.session_state.lat, "lon": st.session_state.lon}])

# ---------- 7. RENDER MAIN UI ----------
col_head1, col_head2, col_head3 = st.columns([2.5, 1, 1])
with col_head1:
    st.markdown('<div class="brand-title">AETHER MCS</div>', unsafe_allow_html=True)
    st.caption("SIT Aerospace Systems Lab")
with col_head2:
    st.metric("Status", "Nominal")
with col_head3:
    st.metric("Bandwidth", "4.8 Gbps")

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

col_left, col_right = st.columns([1.2, 1.8])

with col_left:
    st.markdown("### Status Tracking")
    if st.session_state.altitude == 0:
        st.error("🔴 System Compromised // Surface Link Offline")
    elif current_sails:
        st.success("🟢 Energy Profile: Sail Arrays Optimized")
    elif st.session_state.battery < 20:
        st.warning("🟡 Power State: Critical Depletion Risk")
    else:
        st.success("🟢 Subsystems Nominal")

    st.markdown("### Telemetry Matrix")
    a, b, c = st.columns(3)
    a.metric("Altitude", f"{st.session_state.altitude:,}m", delta=f"+{alt_gain}m" if st.session_state.altitude > 0 else "0m")
    b.metric("Temperature", f"{temp:.1f}°C")
    c.metric("Battery Status", f"{st.session_state.battery:.1f}%")

    d, e, f = st.columns(3)
    d.metric("Heading Vector", f"{int(np.degrees(st.session_state.heading) % 360)}°")
    e.metric("Mission Track", f"{h:02d}:{m:02d}:{s:02d}")
    signal = min(100, 85 + random.randint(-5, 10))
    f.metric("Signal Link", f"{signal}%")

    st.markdown("### Structural Rotational Streams")
    if not df_history.empty and len(df_history) > 1:
        st.line_chart(
            data=df_history,
            x="Cycle",
            y=["Roll", "Pitch", "Yaw"],
            height=180,
            use_container_width=True
        )

with col_right:
    st.markdown("### Spatial Position Tracking")
    view = pdk.ViewState(
        latitude=st.session_state.lat,
        longitude=st.session_state.lon,
        zoom=10,
        pitch=45,
        bearing=25
    )

    path_layer = pdk.Layer(
        "ScatterplotLayer",
        data=df_path,
        get_position="[lon, lat]",
        get_fill_color="[100, 180, 255, 100]",
        get_radius=60,
        opacity=0.5,
    )

    pos_layer = pdk.Layer(
        "ScatterplotLayer",
        data=df_current,
        get_position="[lon, lat]",
        get_fill_color="[100, 180, 255, 200]",
        get_radius=150,
        opacity=0.8,
    )

    st.pydeck_chart(pdk.Deck(
        map_style="https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json",
        initial_view_state=view,
        layers=[path_layer, pos_layer],
        height=450
    ))

# ---------- 8. TRIGGER REFRESH RATE ----------
time.sleep(0.8)
st.rerun()