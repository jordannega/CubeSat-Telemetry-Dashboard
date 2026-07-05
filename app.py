import streamlit as st
import random
import time
import pandas as pd

# 1. Set up the web page title and layout
st.set_page_config(page_title="CubeSat Ground Control", layout="wide")
st.title("🛰️ CubeSat Live Telemetry Dashboard")
st.write("Real-time data stream from virtual high-altitude simulation.")

# 2. Initialize simulation values in Streamlit's memory
if "altitude" not in st.session_state:
    st.session_state.altitude = 1000  # Starting altitude in meters
    st.session_state.battery = 100.0   # Starting battery percentage
    st.session_state.data_history = [] # List to store data for the chart

# 3. Create placeholders in the web UI that we can update live
metric_placeholder = st.empty()
chart_placeholder = st.empty()

# 4. The Live Simulation Loop
while True:
    # Simulate realistic changes per second
    altitude_gain = random.randint(5, 15)
    st.session_state.altitude += altitude_gain
    
    # Temperature drops by roughly 0.0065°C per meter gained
    temperature = 15.0 - (st.session_state.altitude * 0.0065)
    
    # Battery drains slowly over time
    st.session_state.battery = max(0.0, st.session_state.battery - 0.05)
    
    # Save the current stats to our history for the chart
    st.session_state.data_history.append({
        "Seconds": len(st.session_state.data_history),
        "Altitude (m)": st.session_state.altitude,
        "Temp (°C)": temperature
    })
    
    # Keep the chart history from getting too cluttered (show last 30 data points)
    df = pd.DataFrame(st.session_state.data_history[-30:])
    
    # ... (Keep your existing simulation logic above this) ...

    # 5. Update the UI placeholders with the new numbers
    with metric_placeholder.container():
        # --- NEW: CRITICAL ALERT SYSTEM ---
        if temperature < 0:
            st.error(f"⚠️ CRITICAL ALERT: Freezing temperatures detected! Systems risking freeze-lock.")
        elif st.session_state.battery < 20:
            st.warning("⚠️ LOW BATTERY: Entering power-saving mode.")
        else:
            st.success("✅ Systems Nominal: Stable orbit trajectory.")
        # ----------------------------------

        col1, col2, col3 = st.columns(3)
        col1.metric(label="🛰️ Altitude", value=f"{st.session_state.altitude} m", delta=f"+{altitude_gain} m/s")
        col2.metric(label="🌡️ Outside Temp", value=f"{temperature:.2f} °C")
        col3.metric(label="🔋 Battery Life", value=f"{st.session_state.battery:.2f} %")
        
    with chart_placeholder.container():
        st.subheader("Altitude Trajectory Over Time")
        st.line_chart(data=df, x="Seconds", y="Altitude (m)")

    # Wait exactly 1 second before generating the next data point
    time.sleep(1)
