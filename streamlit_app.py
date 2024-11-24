import streamlit as st
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="Pirate's Treasury", layout="wide")
if 'current_stage' not in st.session_state:
    st.session_state.current_stage = 0

st.markdown("""
    <style>
    .stApp {background-color: #f5e6d3;}
    .treasure-text {font-family: 'Pirata One', serif; color: #462f03;}
    .stProgress > div > div {background-color: #c17f59 !important;}
    .log-container {
        background-color: #deb887;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #8b4513;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

def create_rotating_compass(angle):
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(6, 6))
    directions = ['N', 'E', 'S', 'W']
    angles = np.deg2rad([90, 0, 270, 180])
    
    ax.set_theta_direction(-1)
    ax.set_theta_zero_location('N')
    
    ax.scatter(angles, [1.3]*4, color='black')
    for d, a in zip(directions, angles):
        ax.text(a, 1.7, d, ha='center', va='center', fontsize=12, fontweight='bold')
    
    arrow_angle = np.deg2rad(angle)
    ax.arrow(arrow_angle, 0, 0, 0.8, alpha=0.5, width=0.1, 
             head_width=0.2, head_length=0.2, fc='red', ec='red')
    
    ax.set_rticks([])
    plt.tight_layout()
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
        return angle == 42

def constellation_puzzle():
    st.markdown("### ⭐ Navigate by the Stars")
    st.write("The ancient mariners used these stars to guide their way home.")
    stars_selected = st.multiselect(
        "Select the stars of the Ancient Mariner's Path",
        options=["Polaris", "Sirius", "Vega", "Antares", "Betelgeuse", "Rigel"]
    )
    return set(stars_selected) == {"Polaris", "Sirius", "Vega"}

def sundial_puzzle():
    st.markdown("### ☀️ The Mystical Sundial")
    st.write("The ancient sundial holds a secret time...")
    hour = st.number_input("Set the hour", 1, 12, 1)
    minute = st.slider("Set the minute", 0, 59, 0)
    return hour == 7 and minute == 15

def morse_code_puzzle():
    st.markdown("### 📡 The Pirate's Code")
    message = ".--.  ..  .-.  .-  -  ."
    st.write("A mysterious message has been intercepted:")
    st.markdown(f"**{message}**")
    st.write("Hint: Each letter is separated by a space")
    answer = st.text_input("Your answer:").upper()
    return answer == "PIRATE"

def riddle_puzzle():
    st.markdown("### 🤔 The Ancient Riddle")
    riddle = """
    I have cities, but no houses.
    I have mountains, but no trees.
    I have water, but no fish.
    I have roads, but no cars.
    What am I?
    """
    st.markdown(f"**{riddle}**")
    answer = st.text_input("Your answer:").lower()
    return answer == "map"

def treasure_map_puzzle():
    st.markdown("### 🗺️ The Treasure Map")
    st.write("Find the X that marks the spot!")
    col1, col2 = st.columns([1,1])
    with col1:
        x = st.slider("X coordinate", 0, 100, 50)
    with col2:
        y = st.slider("Y coordinate", 0, 100, 50)
    return x == 73 and y == 27

def cryptogram_puzzle():
    st.markdown("### 🔒 The Captain's Cryptogram")
    encrypted = "YZNFHZM GIZMFHIZ"
    st.write("The captain left behind this encrypted message:")
    st.markdown(f"**{encrypted}**")
    st.write("Hint: The letters have been shifted...")
    answer = st.text_input("Decrypt the message:").upper()
    return answer == "TREASURE LOCATION"

def flag_sequence_puzzle():
    st.markdown("### 🏴‍☠️ The Pirate Flag Sequence")
    st.write("Arrange these famous pirate flags in alphabetical order!")
    flags = ["Jolly Roger", "Black Bart", "Calico Jack", "Edward England"]
    sequence = st.multiselect("Select the flags in order:", flags)
    correct_sequence = ["Black Bart", "Calico Jack", "Edward England", "Jolly Roger"]
    return sequence == correct_sequence

def knot_puzzle():
    st.markdown("### ⚓ The Sailor's Knot")
    st.write("Every good sailor needs to know their knots!")
    knots = ["Bowline", "Clove Hitch", "Sheet Bend", "Figure Eight"]
    selected_knot = st.selectbox("Select the knot that can create a fixed loop:", knots)
    return selected_knot == "Bowline"

def main():
    st.title("🏴‍☠️ The Pirate's Lost Treasure")
    
    stages = [
        {"name": "The Compass Challenge", "func": compass_puzzle},
        {"name": "Celestial Navigation", "func": constellation_puzzle},
        {"name": "Time's Secret", "func": sundial_puzzle},
        {"name": "The Morse Code", "func": morse_code_puzzle},
        {"name": "The Ancient Riddle", "func": riddle_puzzle},
        {"name": "The Treasure Map", "func": treasure_map_puzzle},
        {"name": "The Captain's Cryptogram", "func": cryptogram_puzzle},
        {"name": "The Flag Sequence", "func": flag_sequence_puzzle},
        {"name": "The Sailor's Knot", "func": knot_puzzle}
    ]
    
    with st.sidebar:
        st.markdown('<div class="log-container">', unsafe_allow_html=True)
        st.markdown("### 📜 Captain's Log")
        st.write(f"Current Challenge: {stages[min(st.session_state.current_stage, len(stages)-1)]['name']}")
        st.write(f"Challenges Completed: {st.session_state.current_stage}/{len(stages)}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Admin Mode
        st.markdown("---")
        if st.checkbox("🔑 Admin Mode"):
            selected_stage = st.selectbox(
                "Jump to puzzle:",
                options=range(len(stages)),
                format_func=lambda x: stages[x]["name"]
            )
            if st.button("Jump"):
                st.session_state.current_stage = selected_stage
                st.rerun()
    
    if st.session_state.current_stage >= len(stages):
        st.success("🎉 Congratulations! You've found the treasure!")
        st.balloons()
        return
    
    st.progress(st.session_state.current_stage / len(stages))
    current_stage = stages[st.session_state.current_stage]
    
    if current_stage["func"]():
        st.success("Well done, matey!")
        if st.button("Sail to next challenge"):
            st.session_state.current_stage += 1
            st.rerun()

if __name__ == "__main__":
    main()