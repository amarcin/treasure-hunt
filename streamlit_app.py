import datetime
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
    
    return angle >= 150 and angle <= 165

def constellation_puzzle():
    st.write("One star to rule them all, one way to find it, one path to bring you all and in the darkness arrive home; in the Land of Pirates where the thieves lie. Seek the cardinal star.")
    star_selected = st.selectbox("", options=[
        "Aldebaran",
        "Antares",
        "Arcturus",
        "Betelgeuse",
        "Polaris",
        "Rigel",
        "Sirius",
        "Vega"
    ], index=None)
    return star_selected == "Polaris"

def clock_puzzle():
    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_facecolor('none')
    fig.patch.set_alpha(0.0)
    circle = plt.Circle((0.5, 0.5), 0.4, fill=False, color='#8b4513')
    ax.add_artist(circle)
    
    col1, col2 = st.columns(2)
    
    hours = col1.slider("", 1, 12, 12)
    minutes = col1.slider("", 0, 59, 0)
    
    minute_angle = np.deg2rad(-minutes * 6 + 90)
    hour_angle = np.deg2rad(-(hours * 30 + minutes * 0.5) + 90)
    
    ax.plot([0.5, 0.5 + 0.3 * np.cos(minute_angle)],
            [0.5, 0.5 + 0.3 * np.sin(minute_angle)], 
            color='#8b4513', linewidth=2)
            
    ax.plot([0.5, 0.5 + 0.25 * np.cos(hour_angle)],
            [0.5, 0.5 + 0.25 * np.sin(hour_angle)], 
            color='#8b4513', linewidth=2)
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    plt.tight_layout()
    
    col2.pyplot(fig)
    
    current_time = datetime.datetime.now()
    current_hour = current_time.hour % 12 or 12  # Convert 24h to 12h format
    current_minute = current_time.minute
    current_hour_in_pst = current_hour + 4

    st.write(f"Current time registered: {current_hour}:{current_minute}")
    st.write(f"Current calculated time in PST: {current_hour_in_pst}:{current_minute}")
    st.write(datetime.datetime.now())
    return minutes == current_minute and hours == current_hour_in_pst

def morse_code_puzzle():
    morse_message = [
        ('H', '🔘 🔘 🔘 🔘'),
        ('O', '⸺ ⸺ ⸺'),
        ('R', '🔘 ⸺ 🔘'),
        ('I', '🔘 🔘'),
        ('Z', '⸺ ⸺ 🔘 🔘'),
        ('O', '⸺ ⸺ ⸺'),
        ('N', '⸺ 🔘')
    ]
    
    for letter, code in morse_message:
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
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.write("")
    with col2:
        st.write("Twelve labors did he undertake, with strength innate")
        st.write("As penance for crimes committed by fate")
        st.write("Why cross the range of Atlas, when you can split the mountain gate?")
        st.write("Seek the pillars, and sail Strait.")
    with col3:
        st.write("")

    fig, ax = plt.subplots(figsize=(8, 8))
    fig.patch.set_facecolor('none')
    fig.patch.set_alpha(0.0)
    url = "https://images.unsplash.com/photo-1577086664693-894d8405334a?q=80&w=3134&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
    
    with urllib.request.urlopen(url) as response:
        map_img = np.array(Image.open(response))
    
    ax.imshow(map_img, extent=[0, 100, 0, 100])
    
    # Remove tick marks and numbers from x and y axes
    ax.set_xticks([])  # Remove x-axis ticks
    ax.set_yticks([])  # Remove y-axis ticks
    
    x = st.slider("", 0, 100, 50, format="", key="x_coord")
    y = st.slider("", 0, 100, 50, format="", key="y_coord")
    
    ax.scatter(x, y, color='red', marker='x', s=100)
    
    st.pyplot(fig)
    
    return (15 <= x <= 17) and (17 <= y <= 19) 

def hangman_puzzle():
    puzzle_name = "captain's quote"
    if 'current_puzzle' not in st.session_state:
        st.session_state.current_puzzle = None
        
    if st.session_state.current_puzzle != puzzle_name:
        st.session_state.guessed_letters = set()
        st.session_state.attempts = 0
        st.session_state.current_puzzle = puzzle_name
    
    secret = "DEAD MEN TELL NO TALES"
    max_attempts = 5
    
    display = ''.join(char if char == " " or char in st.session_state.guessed_letters else "_" for char in secret)
    st.write(f"<h1>{display}</h1>", unsafe_allow_html=True)
    
    guess = st.text_input("", max_chars=1, key="guess_input", help="The Enter key doesn't work here, click the Submit button (sometimes multiple times) for your attempts").upper()
    
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
    user_move = move.text_input("", max_chars=2).lower()
    img.image("imgs/chessboard.png")
    
    return user_move == "d8"

def knot_puzzle():
    col1, col2, col3, col4 = st.columns(4)
    cols = [col1, col2, col3, col4]
    
    knots = ["Bowline", "Clove Hitch", "Sheet Bend", "Figure Eight"]
    
    matches = {}
    for i, col in enumerate(cols):
        col.image(f"imgs/{knots[i].lower().replace(' ', '')}.png")
        matches[i] = col.selectbox(f"", ["", "Bowline", "Clove Hitch", "Sheet Bend", "Figure Eight"], key=f"knot_{i}")
    
    correct_matches = all(matches[i] == knots[i] for i in range(4))
    
    col1, col2 = st.columns([3,1])
    with col1:
        st.markdown("<br>", unsafe_allow_html=True)
        st.write("Aboard the ship, swabbing the deck")
        st.write("Creak in the ship, crick in your neck")
        st.write("Too busy working, you've missed the view")
        st.write("Which knot will let you fix the loop?")
        selected_knot = st.pills("", ["Sheet Bend", "Figure Eight", "Clove Hitch", "Bowline"])

    col2.image("imgs/ship.png")

    return correct_matches and selected_knot == "Bowline"

def check_puzzle_state(puzzle_name):
    if puzzle_name not in st.session_state.puzzle_states:
        st.session_state.puzzle_states[puzzle_name] = {
            'attempts': 0,
            'solved': False
        }
    return st.session_state.puzzle_states[puzzle_name]

def introduction_page():
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style='padding: 25px; border: 2px solid #c0c0c0; border-radius: 10px; background-color: rgba(255,255,255,0.1);'>
            <p style='text-align: center;'>Beyond this page lies a series of tests to determine the worthiest of pirates and treasure hunters.</p>
            <p style='text-align: center;'>Stay sharp, and keep your wits about you.</p>
            <p style='text-align: center;'>Enjoy the journey.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Begin Your Adventure →"):
        st.session_state.current_stage += 1
        st.rerun()
    return False

def completion_page():
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style='padding: 25px; border: 2px solid #c0c0c0; border-radius: 10px; background-color: rgba(255,255,255,0.1);'>
            <p style='text-align: center;'>Congratulations</p>
            <p style='text-align: center;'>Final Clue goes here.</p>
            <p style='text-align: center;'> TBD.</p>
            <p style='text-align: center;'></p>
            <p style='text-align: center; font-weight: bold;'></p>
        </div>
        """, unsafe_allow_html=True)
    
    st.balloons()
    return False

def main():
    st.title("🏴‍☠️ The Pirate Trials")
    
    stages = [
        {"name": "Introduction", "func": introduction_page},      
        {"name": "Ancient Riddle", "func": riddle_puzzle},         
        {"name": "Three Dots and a Dash", "func": morse_code_puzzle},         
        {"name": "Compass Challenge", "func": compass_puzzle},     
        {"name": "Celestial Navigation", "func": constellation_puzzle},
        {"name": "Captain's Quote", "func": hangman_puzzle},
        {"name": "A Game of Kings", "func": chess_puzzle},   
        {"name": "Time's Secret", "func": clock_puzzle},        
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
    
    st.progress(min(1.0, st.session_state.current_stage / (len(stages) - 1)))
    st.markdown("<br>", unsafe_allow_html=True)
    
    current_stage = stages[st.session_state.current_stage]
    
    if current_stage["func"]():
        if not st.session_state.show_success:
            st.session_state.show_success = True
            st.rerun()
        
        success_animation = load_lottie_url("https://lottie.host/68f642f5-1647-4be8-bf16-9d0667a249d1/gneIjMUkMM.json")
        if success_animation:
            st_lottie(success_animation, height=200, key="success")
        
        st.success(f"You've completed {current_stage['name']}.")
        
        if st.button("Continue →"):
            st.session_state.show_success = False
            st.session_state.current_stage += 1
            st.rerun()
    else:
        st.session_state.show_success = False

if __name__ == "__main__":
    main()