# CubeSat-Telemetry-Dashboard
Description:
This project is a real-time software simulation of a high-altitude CubeSat (miniature satellite) ascent, built entirely in Python using the Streamlit framework. Because physical space hardware is highly restricted by cost and availability, this system acts as a virtual testing environment for data ingestion.The application utilizes atmospheric physics equations to simulate live sensor data streams—dynamically dropping the calculated outside temperature by exactly $0.0065 degree celcius for every meter of altitude gained to perfectly mirror the real-world physics of the Earth's troposphere. Additionally, the ground station features an automated safety logic engine. The backend continuously evaluates incoming data metrics and immediately triggers visual emergency alerts across the user dashboard if the virtual satellite encounters sub-zero freezing conditions or critical low-battery thresholds.
# AETHER Mission Control Software (MCS) Dashboard

A real-time, dynamic telemetry and command dashboard for the hypothetical aerospace vehicle **AETHER**. Built using Streamlit, PyDeck, and NumPy, this interface simulates an aerospace systems lab environment, tracking spatial coordinates, structural rotational streams, and critical subsystem metrics.

---

## 🚀 Objective
The objective of this project is to simulate a high-fidelity **Mission Control Software (MCS)** environment inside a web browser. It provides real-time monitoring of a high-altitude or orbital asset's health, structural dynamics, and geographical position, while allowing engineers to issue active uplink commands to alter the flight path and resource management profile.

---

## ✨ Key Features

- **Real-Time Simulation Engine:** Telemetry parameters (Altitude, Temperature, Battery, Heading, and Signal) dynamically evolve every 0.8 seconds using underlying physics formulas and random variance modeling.
- **Interactive Uplink Control Panel:** A collapsible matrix interface allows real-time state mutation:
  - **Vector Burns:** Manually adjust the heading matrix (Port / Starboard burns).
  - **Resource Allocation:** Deploy Solar Sails to mitigate battery consumption or adjust Thrust Velocity.
  - **Emergency Override:** Execute a hard system De-Orbit sequence, pulling the vehicle down to surface level while logging a critical error.
- **Spatial Position Tracking:** Integrated 3D geospatial mapping using `pydeck` mapping the vehicle’s live coordinate changes and rendering a historical flight path breadcrumb trail over a dark matter layout.
- **Structural Rotational Streams:** Live charting of dynamic body orientation components (Roll, Pitch, Yaw) powered by high-speed mathematical sine and cosine sweeps.
- **Seamless State Architecture:** Employs explicit callback routines (`on_change`/`on_click`) coupled with persistent `st.session_state` values to allow complete configuration changes without breaking the synchronous simulation framework.

---

## 🛠️ Architecture Design & Anti-Ghosting Optimization

Standard Python infinite iterations (`while True:`) block Streamlit's structural reruns, resulting in a common UI pipeline bug where stale layout matrices stack up—creating a faded "duplicated page" ghosting anomaly. 

This project solves that structural limitation by introducing a **Single-Frame Rendering Loop**:
1. The dashboard processes and captures user configuration inputs via instant state mutation callbacks.
2. The core simulation engine updates the vehicle's vector data precisely for **one single time frame**.
3. The page draws the entire updated interface flawlessly without visual clutter, pauses for 0.8 seconds, and safely triggers a clean frame restart via `st.rerun()`.

---

## 📦 Installation & Setup

Ensure you have Python installed, then follow these steps to run the application locally:

1. Clone the repository:
   bash
   git clone [https://github.com/YOUR_USERNAME/aether-mcs.git](https://github.com/YOUR_USERNAME/aether-mcs.git)
   cd aether-mcs

2. Install required dependencies: pip install streamlit pandas pydeck numpy
3. Launch the Mission Control Software: streamlit run app.py
