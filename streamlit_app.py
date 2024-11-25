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
        margin-bottom: 20px;
    }
    .puzzle-image {
        max-width: 100%;
        border-radius: 8px;
        border: 3px solid #8b4513;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

def compass_puzzle():
    st.markdown("### 🧭 The Ancient Compass")
    
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(4, 4))
    angle = st.slider("Rotate the compass", 0, 360, 0)
    
    directions = ['N', 'E', 'S', 'W']
    angles = np.deg2rad([90, 0, 270, 180])
    
    ax.set_theta_direction(-1)
    ax.set_theta_zero_location('N')
    ax.grid(True, alpha=0.3)
    ax.set_facecolor('#f5e6d3')
    
    ax.scatter(angles, [1.3]*4, color='#8b4513')
    for d, a in zip(directions, angles):
        ax.text(a, 1.7, d, ha='center', va='center', fontsize=12, fontweight='bold', color='#462f03')
    
    arrow_angle = np.deg2rad(angle)
    ax.arrow(arrow_angle, 0, 0, 0.8, alpha=0.8, width=0.1, 
             head_width=0.2, head_length=0.2, fc='#8b4513', ec='#8b4513')
    
    ax.set_rticks([])
    plt.tight_layout()
    st.pyplot(fig)
    
    return angle == 42

def constellation_puzzle():
    st.markdown("### ⭐ Navigate by the Stars")
    st.image("https://plus.unsplash.com/premium_photo-1721254059354-ae91139fdfef?q=80&w=3132&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", caption="Ancient Star Chart", use_column_width=True)
    st.write("The ancient mariners used these stars to guide their way home.")
    stars_selected = st.multiselect(
        "Select the stars of the Ancient Mariner's Path",
        options=["Polaris", "Sirius", "Vega", "Antares", "Betelgeuse", "Rigel"]
    )
    return set(stars_selected) == {"Polaris", "Sirius", "Vega"}

def sundial_puzzle():
    st.markdown("### ☀️ The Mystical Sundial")
    
    fig, ax = plt.subplots(figsize=(6, 6))
    circle = plt.Circle((0.5, 0.5), 0.4, fill=False, color='#8b4513')
    ax.add_artist(circle)
    
    for hour in range(1, 13):
        angle = np.deg2rad(hour * 30 - 90)
        x = 0.5 + 0.35 * np.cos(angle)
        y = 0.5 + 0.35 * np.sin(angle)
        ax.text(x, y, str(hour), ha='center', va='center', fontsize=12)
    
    hour = st.number_input("Set the hour", 1, 12, 1)
    minute = st.slider("Set the minute", 0, 59, 0)
    
    angle = np.deg2rad((hour + minute/60) * 30 - 90)
    ax.plot([0.5, 0.5 + 0.3 * np.cos(angle)],
            [0.5, 0.5 + 0.3 * np.sin(angle)], 
            color='#8b4513', linewidth=2)
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    plt.tight_layout()
    st.pyplot(fig)
    
    return hour == 7 and minute == 15

def morse_code_puzzle():
    st.markdown("### 📡 The Pirate's Code")
    st.image("https://plus.unsplash.com/premium_photo-1667238624718-5c5d5deb6829?q=80&w=2737&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", caption="Ancient Morse Code Chart", use_column_width=True)
    message = ".--.  ..  .-.  .-  -  ."
    st.write("A mysterious message has been intercepted:")
    st.markdown(f"**{message}**")
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
    st.write(riddle)
    st.image("https://images.unsplash.com/photo-1520299607509-dcd935f9a839?q=80&w=3131&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", caption="An Old Parchment", use_column_width=True)
    answer = st.text_input("Your answer:").lower()
    return answer == "map"

def treasure_map_puzzle():
    st.markdown("### 🗺️ The Treasure Map")
    
    fig, ax = plt.subplots(figsize=(8, 8))
    # map_img = plt.imread("https://images.unsplash.com/photo-1520299607509-dcd935f9a839")
    # ax.imshow(map_img)
    
    x = st.slider("X coordinate", 0, 100, 50)
    y = st.slider("Y coordinate", 0, 100, 50)
    
    ax.scatter(x, y, color='red', marker='x', s=100)
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
    
    return x == 73 and y == 27

def cryptogram_puzzle():
    st.markdown("### 🔒 The Captain's Cryptogram")
    encrypted = "YZNFHZM GIZMFHIZ"
    st.write("The captain left behind this encrypted message:")
    st.markdown(f"**{encrypted}**")
    answer = st.text_input("Decrypt the message:").upper()
    return answer == "TREASURE LOCATION"

def flag_sequence_puzzle():
    st.markdown("### 🏴‍☠️ The Pirate Flag Sequence")
    st.image("https://images.unsplash.com/photo-1652447275071-4bf852aebdc5?q=80&w=3270&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", caption="Famous Pirate Flags", use_column_width=True)
    st.write("Arrange these famous pirate flags in alphabetical order!")
    flags = ["Jolly Roger", "Black Bart", "Calico Jack", "Edward England"]
    sequence = st.multiselect("Select the flags in order:", flags)
    correct_sequence = ["Black Bart", "Calico Jack", "Edward England", "Jolly Roger"]
    return sequence == correct_sequence

def knot_puzzle():
    st.markdown("### ⚓ The Sailor's Knot")
    st.image("https://images.unsplash.com/photo-1618588932782-d31006819d93?q=80&w=3087&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", caption="Traditional Sailor's Knots", use_column_width=True)
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
        
        st.markdown("---")
        admin_expander = st.expander("🔑 Admin Mode")
        with admin_expander:
            password = st.text_input("Password:", type="password")
            if password == "admin":
                st.write("Select a puzzle to jump to:")
                cols = st.columns(3)
                for i, stage in enumerate(stages):
                    with cols[i % 3]:
                        if st.button(f"Puzzle {i+1}"):
                            st.session_state.current_stage = i
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