import streamlit as st
import numpy as np
from PIL import Image
import math
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(page_title="Pirate's Treasury", layout="wide")

# Session state initialization
if 'current_stage' not in st.session_state:
    st.session_state.current_stage = 0

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #f5e6d3;
    }
    .treasure-text {
        font-family: serif;
        color: #462f03;
    }
    </style>
    """, unsafe_allow_html=True)

def create_rotating_compass(angle):
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    directions = ['N', 'E', 'S', 'W']
    angles = np.deg2rad([90, 0, 270, 180])
    
    # Setup compass
    ax.set_theta_direction(-1)
    ax.set_theta_zero_location('N')
    
    # Draw compass points
    ax.scatter(angles, [1]*4, color='black')
    for d, a in zip(directions, angles):
        ax.text(a, 1.1, d, ha='center', va='center')
    
    # Add rotating arrow
    arrow_angle = np.deg2rad(angle)
    ax.arrow(arrow_angle, 0, 0, 0.8, alpha=0.5, width=0.1, 
             head_width=0.2, head_length=0.2, fc='red', ec='red')
    
    ax.set_rticks([])
    return fig

def compass_puzzle():
    st.markdown("### 🧭 The Ancient Compass")
    col1, col2 = st.columns([2,1])
    
    with col1:
        angle = st.slider("Rotate the compass", 0, 360, 0)
        fig = create_rotating_compass(angle)
        st.pyplot(fig)
        
    with col2:
        st.write("Align the compass with the secret bearing...")
        if angle == 42:  # Example correct angle
            return True
    return False

def constellation_puzzle():
    st.markdown("### ⭐ Navigate by the Stars")
    stars_selected = st.multiselect("Select the stars of the Ancient Mariner's Path",
                                  options=["Polaris", "Sirius", "Vega", "Antares"])
    return set(stars_selected) == {"Polaris", "Sirius", "Vega"}

def sundial_puzzle():
    st.markdown("### ☀️ The Mystical Sundial")
    hour = st.number_input("Set the hour", 1, 12, 1)
    minute = st.slider("Set the minute", 0, 59, 0)
    return hour == 7 and minute == 15  # Example correct time

def main():
    st.title("🏴‍☠️ The Pirate's Lost Treasure")
    
    stages = [
        {"name": "The Compass Challenge", "func": compass_puzzle},
        {"name": "Celestial Navigation", "func": constellation_puzzle},
        {"name": "Time's Secret", "func": sundial_puzzle}
    ]
    
    # Ensure current_stage doesn't exceed available stages
    if st.session_state.current_stage >= len(stages):
        st.success("Congratulations! You've completed all challenges!")
        return
    
    # Display current stage
    current_stage = stages[st.session_state.current_stage]
    
    # Show progress
    st.progress((st.session_state.current_stage) / len(stages))
    
    # Display stage content
    if current_stage["func"]():
        st.balloons()
        if st.button("Continue to next challenge"):
            st.session_state.current_stage += 1
            st.rerun()  # Changed from experimental_rerun to rerun
    
    # Easter eggs and atmosphere
    with st.sidebar:
        st.markdown("### Captain's Log")
        st.write(f"Current Challenge: {current_stage['name']}")
        st.write(f"Challenges Completed: {st.session_state.current_stage}/{len(stages)}")

if __name__ == "__main__":
    main()