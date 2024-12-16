import random
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from streamlit_lottie import st_lottie
import json
import requests
import urllib.request
from PIL import Image

st.set_page_config(page_title="Pirate's Treasure", layout="wide")

st.markdown("""
<style>
    .stPlotlyChart, .stPlot {
        border-radius: 10px;
        overflow: hidden;
    }
    iframe {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

if 'current_stage' not in st.session_state:
    st.session_state.current_stage = 0
if 'puzzle_states' not in st.session_state:
    st.session_state.puzzle_states = {}
if 'show_success' not in st.session_state:
    st.session_state.show_success = False
if 'guessed_letters' not in st.session_state:
    st.session_state.guessed_letters = set()
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0

def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def compass_puzzle():
    col1, col2 = st.columns([1, 1])
    
    with col1:
        raw_angle = st.slider("", -180, 180, 0, format="")
        st.write("If you're headed two ticks to the left, you're not at your best.")
        st.write("Avoid the mouth of the beast, and head south by south east.")
    
    with col2:
        fig = plt.figure(figsize=(4, 4))
        fig.patch.set_facecolor('none')
        fig.patch.set_alpha(0.0)
        ax = fig.add_subplot(111, projection='polar')
        angle = (raw_angle) % 360
        
        # Create 32 lines for compass points (every 11.25 degrees)
        angles = np.deg2rad(np.arange(0, 360, 11.25))
        lengths = [1.3 if i % 8 == 0 else  # Main directions (N,E,S,W)
                   1.1 if i % 4 == 0 else  # Intermediate directions (NE,SE,SW,NW)
                   0.9 for i in range(32)]  # Minor marks
        
        # Draw the lines
        for theta, length in zip(angles, lengths):
            ax.plot([theta, theta], [0.7, length], color='#8b4513', linewidth=2 if length > 1.1 else 1)
        
        # Main direction labels
        directions = ['N', 'E', 'S', 'W']
        main_angles = np.deg2rad([0, 90, 180, 270])
        for d, a in zip(directions, main_angles):
            ax.text(a, 2.0, d, ha='center', va='center', fontsize=12, fontweight='bold', color='#462f03')
        
        ax.set_theta_direction(-1)
        ax.set_theta_zero_location('N')
        ax.grid(False)  # Removed the grid since we have our own lines now
        ax.set_facecolor('#f5e6d3')
        ax.set_xticks([])
        
        arrow_angle = np.deg2rad(angle)
        ax.arrow(arrow_angle, 0, 0, 0.8, alpha=0.8, width=0.1, 
                 head_width=0.2, head_length=0.2, fc='#8b4513', ec='#8b4513')
        
        ax.set_rticks([])
        ax.set_rlim(0, 2.2)
        plt.tight_layout()
        st.pyplot(fig)
    
    return angle >= 157 and angle <= 158

def constellation_puzzle():
    st.write("Through mist and cloud and darkest night, which star outshines all else in sight? The brightest beacon in the dome, a faithful guide to lead you home.")
    star_selected = st.selectbox("", options=[
        "Polaris",
        "Vega", 
        "Antares",
        "Betelgeuse",
        "Rigel",
        "Aldebaran", 
        "Sirius",
        "Arcturus"
    ], index=None)
    return star_selected == "Sirius"

def sundial_puzzle():
    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_facecolor('none')
    fig.patch.set_alpha(0.0)
    circle = plt.Circle((0.5, 0.5), 0.4, fill=False, color='#8b4513')
    ax.add_artist(circle)
    
    rotation = st.slider("", 0, 360, 0)
    
    angle = np.deg2rad(-rotation + 90)
    
    ax.plot([0.5, 0.5 + 0.3 * np.cos(angle)],
            [0.5, 0.5 + 0.3 * np.sin(angle)], 
            color='#8b4513', linewidth=2)
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    plt.tight_layout()
    st.pyplot(fig)
    
    return rotation == 255

def morse_code_puzzle():
    # Using 🔘 for dot, ⎯⎯ for dash
    # Answer ".... --- .-. .. --.. --- -."
    morse_message = {
        'H': '🔘 🔘 🔘 🔘',
        'O': '⸺ ⸺ ⸺',
        'R': '🔘 ⸺ 🔘',
        'I': '🔘 🔘',
        'Z': '⸺ ⸺ 🔘 🔘',
        'O': '⸺ ⸺ ⸺',
        'N': '⸺ 🔘'
    }
    
    for letter, code in morse_message.items():
        st.write(f"{code}", end=" ")
    
    answer = st.text_input("").upper()
    return answer == "HORIZON"

def riddle_puzzle():
    riddle = """
    I have cities, but no houses.
    I have mountains, but no trees.
    I have water, but no fish.
    I have roads, but no cars.
    What am I?
    """
    st.write(riddle)
    answer = st.text_input("").lower()
    return answer == "map"

def treasure_map_puzzle():
    fig, ax = plt.subplots(figsize=(8, 8))
    fig.patch.set_facecolor('none')
    fig.patch.set_alpha(0.0)
    url = "https://images.unsplash.com/photo-1577086664693-894d8405334a?q=80&w=3134&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
    
    with urllib.request.urlopen(url) as response:
        map_img = np.array(Image.open(response))
    
    ax.imshow(map_img, extent=[0, 100, 0, 100])
    ax.set_xticks([])  # Remove x-axis ticks
    ax.set_yticks([])  # Remove y-axis ticks
    
    x = st.slider("X coordinate", 0, 100, 50)
    y = st.slider("Y coordinate", 0, 100, 50)
    
    ax.scatter(x, y, color='red', marker='x', s=100)
    st.pyplot(fig)
    
    return x == 16 and y == 18  # Straight of Gibraltar

def hangman_puzzle():
    puzzle_name = "captain's quote"
    if 'current_puzzle' not in st.session_state:
        st.session_state.current_puzzle = None
        
    if st.session_state.current_puzzle != puzzle_name:
        st.session_state.guessed_letters = set()
        st.session_state.attempts = 0
        st.session_state.current_puzzle = puzzle_name
    
    secret = "DEAD MEN TELL NO TALES"
    max_attempts = 6
    
    display = ''.join(char if char == " " or char in st.session_state.guessed_letters else "_" for char in secret)
    st.write(f"<h3>{display}</h3>", unsafe_allow_html=True)
    
    guess = st.text_input("", max_chars=1, key="guess_input").upper()
    
    if st.button("Submit", type="primary", key="guess_button"):
        if guess and guess.isalpha() and len(guess) == 1 and guess not in st.session_state.guessed_letters:
            st.session_state.guessed_letters.add(guess)
            if guess not in secret:
                st.session_state.attempts += 1
                if st.session_state.attempts >= max_attempts:
                    st.session_state.guessed_letters = set()
                    st.session_state.attempts = 0
            st.rerun()

    st.write(f"Attempts remaining: {max_attempts - st.session_state.attempts}")
    
    incorrect_guesses = sorted([letter for letter in st.session_state.guessed_letters if letter not in secret])
    if incorrect_guesses:
        st.write(", ".join(incorrect_guesses))
    
    return all(char in st.session_state.guessed_letters or char == " " for char in secret)

def chess_puzzle():
    move, img = st.columns(2)
    move.text_input("", max_chars=2).lower()
    img.image("chessboard.png")
    
    return move == "d8"

def knot_puzzle():
    st.write("Every good sailor needs to know their knots!")
    knots = ["Bowline", "Clove Hitch", "Sheet Bend", "Figure Eight"]
    selected_knot = st.pills("Select the knot that can create a fixed loop:", knots)
    return selected_knot == "Bowline"

def check_puzzle_state(puzzle_name):
    if puzzle_name not in st.session_state.puzzle_states:
        st.session_state.puzzle_states[puzzle_name] = {
            'attempts': 0,
            'solved': False
        }
    return st.session_state.puzzle_states[puzzle_name]

def introduction_page():
    st.markdown("### 📜 The Beginning of Your Journey")
    st.markdown("<br>", unsafe_allow_html=True)  # Add space after title
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style='padding: 25px; border: 2px solid #c0c0c0; border-radius: 10px; background-color: rgba(255,255,255,0.1);'>
            <p style='text-align: center;'>Beyond this page lies a series of tests to determine the worthiest of pirates and treasure hunters.</p>
            <p style='text-align: center;'>Trying to solve these alone will prove nigh impossible, but luckily, you have a mysterious friend helping you along the way.</p>
            <p style='text-align: center;'>They've delivered a message to you using their trusty friend Hedwig.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)  # Add space before button
    if st.button("Begin Your Adventure →"):
        st.session_state.current_stage += 1
        st.rerun()
    return False

def completion_page():
    st.markdown("### 🎉 Journey's End - The Final Clue")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style='padding: 25px; border: 2px solid #c0c0c0; border-radius: 10px; background-color: rgba(255,255,255,0.1);'>
            <p style='text-align: center;'>Congratulations, brave adventurer! You've proven yourself worthy of the greatest treasure.</p>
            <p style='text-align: center;'>The treasure lies where ancient walls meet Mediterranean waves...</p>
            <p style='text-align: center;'>At the crossroads of two continents, where Hercules once stood.</p>
            <p style='text-align: center;'>Seek the point where:</p>
            <p style='text-align: center; font-weight: bold;'>36.7783° N, 3.0588° E</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.balloons()
    return False

def main():
    st.title("🏴‍☠️ The Pirate Trials")
    
    stages = [
        {"name": "Introduction", "func": introduction_page},      
        {"name": "Ancient Riddle", "func": riddle_puzzle},         
        {"name": "Morse Code", "func": morse_code_puzzle},         
        {"name": "Compass Challenge", "func": compass_puzzle},     
        {"name": "Celestial Navigation", "func": constellation_puzzle},
        {"name": "Captain's Quote", "func": hangman_puzzle},
        {"name": "A Game of Kings", "func": chess_puzzle},   
        {"name": "Time's Secret", "func": sundial_puzzle},        
        {"name": "Sailor's Knot", "func": knot_puzzle},           
        {"name": "Treasure Map", "func": treasure_map_puzzle},
        {"name": "Final Revelation", "func": completion_page}      # Added completion stage
    ]
    
    with st.sidebar:
        st.markdown("### 📜 Captain's Log")
        st.write(f"Current Challenge: {stages[min(st.session_state.current_stage, len(stages)-1)]['name']}")
        st.write(f"Challenges Completed: {max(0, st.session_state.current_stage-1)}/{len(stages)-2}")  # Subtract 1 to not count intro/conclusion
        st.markdown("---")
        st.write("Select a page to jump to:")
        cols = st.columns(3)
        for i, stage in enumerate(stages):
            if st.button(f"{stage['name']}", key=f"stage_{i}"):
                st.session_state.current_stage = i
                st.rerun()
    
    st.progress(st.session_state.current_stage / len(stages))
    st.markdown("<br>", unsafe_allow_html=True)  # Add space after progress bar
    
    current_stage = stages[st.session_state.current_stage]
    
    if current_stage["func"]():
        if not st.session_state.show_success:
            st.session_state.show_success = True
            st.rerun()
        
        success_animation = load_lottie_url("https://lottie.host/68f642f5-1647-4be8-bf16-9d0667a249d1/gneIjMUkMM.json")
        if success_animation:
            st_lottie(success_animation, height=200, key="success")
        
        st.success(f"You've completed {current_stage['name']}.")
        
        if st.button("Continue to Next Challenge →"):
            st.session_state.show_success = False
            st.session_state.current_stage += 1
            st.rerun()
    else:
        st.session_state.show_success = False

if __name__ == "__main__":
    main()