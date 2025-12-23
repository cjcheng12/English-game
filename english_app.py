import random
import json
import os
import time

# --- CONFIGURATION ---
ROUNDS_PER_GAME = 20
MASTERY_THRESHOLD = 5  # If he gets a word right 5 times total, it stops appearing.
DATA_FILE = "baseball_vocab_progress.json"

# --- THE 100+ VOCABULARY LIST ---
# This list contains words likely found in "Baseball Superstars" and general sports biographies
# suitable for a Grade 6 ESL student.
initial_word_data = [
    # --- Baseball Specific ---
    {"word": "Pitcher", "def": "投手"},
    {"word": "Catcher", "def": "捕手"},
    {"word": "Umpire", "def": "裁判"},
    {"word": "Inning", "def": "局 (棒球比賽的)"},
    {"word": "Dugout", "def": "球員休息區"},
    {"word": "Bullpen", "def": "牛棚 (投手練投區)"},
    {"word": "Roster", "def": "球員名單"},
    {"word": "Statistic", "def": "統計數據"},
    {"word": "League", "def": "聯盟"},
    {"word": "Tournament", "def": "錦標賽"},
    {"word": "Championship", "def": "冠軍賽"},
    {"word": "Trophy", "def": "獎盃"},
    {"word": "MVP (Most Valuable Player)", "def": "最有價值球員"},
    {"word": "Rookie", "def": "新秀 / 菜鳥"},
    {"word": "Veteran", "def": "老將 / 資深球員"},
    {"word": "Manager", "def": "總教練 / 經理"},
    {"word": "Stadium", "def": "體育場"},
    {"word": "Grand Slam", "def": "滿貫全壘打"},
    {"word": "Strikeout", "def": "三振出局"},
    {"word": "Walk", "def": "保送"},
    {"word": "Infielder", "def": "內野手"},
    {"word": "Outfielder", "def": "外野手"},
    {"word": "Mound", "def": "投手丘"},
    {"word": "Batter", "def": "打擊者"},
    {"word": "Helmet", "def": "頭盔"},
    {"word": "Jersey", "def": "球衣"},
    {"word": "Mascot", "def": "吉祥物"},
    {"word": "Scoreboard", "def": "計分板"},
    {"word": "Spectator", "def": "觀眾"},
    {"word": "Base", "def": "壘包"},

    # --- Descriptive Adjectives (The "Hard" Words) ---
    {"word": "Phenomenal", "def": "非凡的 / 驚人的"},
    {"word": "Legendary", "def": "傳奇的"},
    {"word": "Dominant", "def": "佔優勢的 / 主導的"},
    {"word": "Versatile", "def": "多才多藝的 / 全能的"},
    {"word": "Aggressive", "def": "積極的 / 侵略性的"},
    {"word": "Defensive", "def": "防守的"},
    {"word": "Offensive", "def": "進攻的"},
    {"word": "Spectacular", "def": "壯觀的 / 精彩的"},
    {"word": "Consistent", "def": "始終如一的 / 穩定的"},
    {"word": "Athletic", "def": "運動的 / 體格健壯的"},
    {"word": "Talented", "def": "有天賦的"},
    {"word": "Famous", "def": "著名的"},
    {"word": "Professional", "def": "專業的 / 職業的"},
    {"word": "Competitive", "def": "競爭激烈的 / 好勝的"},
    {"word": "Accurate", "def": "準確的"},
    {"word": "Powerful", "def": "強大的 / 有力的"},
    {"word": "Incredible", "def": "難以置信的"},
    {"word": "Historic", "def": "歷史性的"},
    {"word": "Memorable", "def": "難忘的"},
    {"word": "Intense", "def": "強烈的 / 激烈的"},
    {"word": "Reliable", "def": "可靠的"},
    {"word": "Remarkable", "def": "卓越的 / 值得注意的"},
    {"word": "Outstanding", "def": "傑出的"},
    {"word": "Determined", "def": "堅決的"},
    {"word": "Confident", "def": "有自信的"},
    {"word": "Ambitious", "def": "有野心的"},
    {"word": "Energetic", "def": "精力充沛的"},
    {"word": "Focus", "def": "專注"},
    {"word": "Precise", "def": "精確的"},
    {"word": "Rapid", "def": "迅速的"},

    # --- Verbs (Action & Career) ---
    {"word": "Sprint", "def": "衝刺"},
    {"word": "Launch", "def": "發射 / 大力擊出"},
    {"word": "Celebrate", "def": "慶祝"},
    {"word": "Achieve", "def": "達成 / 實現"},
    {"word": "Defeat", "def": "擊敗"},
    {"word": "Conquer", "def": "征服 / 克服"},
    {"word": "Participate", "def": "參加"},
    {"word": "Improve", "def": "改善 / 進步"},
    {"word": "Demonstrate", "def": "示範 / 展示"},
    {"word": "Perform", "def": "表演 / 表現"},
    {"word": "Injure", "def": "受傷"},
    {"word": "Recover", "def": "恢復 / 康復"},
    {"word": "Retire", "def": "退休"},
    {"word": "Draft", "def": "徵召 / 選秀"},
    {"word": "Trade", "def": "交易"},
    {"word": "Encourage", "def": "鼓勵"},
    {"word": "Inspire", "def": "啟發 / 激勵"},
    {"word": "Represent", "def": "代表"},
    {"word": "Compete", "def": "競爭"},
    {"word": "Train", "def": "訓練"},

    # --- General Academic / Context Words ---
    {"word": "Opportunity", "def": "機會"},
    {"word": "Strategy", "def": "策略"},
    {"word": "Technique", "def": "技巧 / 技術"},
    {"word": "Victory", "def": "勝利"},
    {"word": "Dedication", "def": "奉獻 / 專注"},
    {"word": "Obstacle", "def": "障礙"},
    {"word": "Challenge", "def": "挑戰"},
    {"word": "Record", "def": "紀錄"},
    {"word": "Highlight", "def": "精彩片段 / 亮點"},
    {"word": "Career", "def": "職業生涯"},
    {"word": "Biography", "def": "傳記"},
    {"word": "Interview", "def": "採訪 / 面試"},
    {"word": "Season", "def": "賽季 / 季節"},
    {"word": "Series", "def": "系列賽"},
    {"word": "Generation", "def": "世代"},
    {"word": "Nation", "def": "國家"},
    {"word": "Pressure", "def": "壓力"},
    {"word": "Success", "def": "成功"},
    {"word": "Failure", "def": "失敗"},
    {"word": "Effort", "def": "努力"}
]

# --- FUNCTIONS ---

def load_data():
    """Loads progress from a file, or creates new data if file doesn't exist."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            print("Error loading save file. Starting fresh.")
            return initialize_data()
    else:
        return initialize_data()

def initialize_data():
    """Adds the 'score' field to our initial list."""
    data = []
    for item in initial_word_data:
        # Each word starts with a mastery score of 0
        data.append({"word": item["word"], "def": item["def"], "score": 0})
    return data

def save_data(data):
    """Saves the current progress to a file."""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_candidates(data):
    """Returns a list of words that have NOT yet been mastered (score < 5)."""
    return [item for item in data if item['score'] < MASTERY_THRESHOLD]

def run_game():
    data = load_data()
    
    # Filter words that still need practice
    candidates = get_candidates(data)
    
    if len(candidates) == 0:
        print("\n🎉 CONGRATULATIONS! 🎉")
        print("You have mastered ALL 100 words in the book!")
        print("You are a Baseball Vocabulary Superstar!")
        return

    # Determine how many rounds to play (max 20, or fewer if not enough words left)
    num_rounds = min(ROUNDS_PER_GAME, len(candidates))
    
    # Select random words for THIS session (no repeats in this game)
    session_words = random.sample(candidates, num_rounds)
    
    session_score = 0
    print(f"\n⚾ PLAY BALL! ⚾")
    print(f"Goal: Play {num_rounds} rounds.")
    print(f"Mastery Rule: Get a word right {MASTERY_THRESHOLD} times to retire it forever!\n")
    print("-" * 50)

    for i, target in enumerate(session_words):
        print(f"\nQuestion {i + 1}/{num_rounds}")
        print(f"Word:  👉  ** {target['word']} **")
        
        # Prepare options: 1 correct + 3 random wrong answers
        correct_def = target['def']
        
        # Pick 3 wrong definitions from the FULL list (to ensure variety)
        # We exclude the current correct answer
        all_defs = [item['def'] for item in data if item['def'] != correct_def]
        wrong_defs = random.sample(all_defs, 3)
        
        options = wrong_defs + [correct_def]
        random.shuffle(options)
        
        # Display Options
        for idx, option in enumerate(options):
            print(f"   {idx + 1}. {option}")
            
        # Get User Input
        while True:
            try:
                choice = int(input("\nSelect the correct Chinese definition (1-4): "))
                if 1 <= choice <= 4:
                    break
                else:
                    print("Please enter a number between 1 and 4.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        # Check Answer
        selected_def = options[choice - 1]
        
        if selected_def == correct_def:
            print("✅ CORRECT! Home Run!")
            session_score += 1
            
            # Find the word in the MAIN data list and update its mastery score
            for item in data:
                if item['word'] == target['word']:
                    item['score'] += 1
                    new_score = item['score']
                    if new_score >= MASTERY_THRESHOLD:
                        print(f"🌟 You have MASTERED the word '{target['word']}'! It won't appear again.")
                    else:
                        print(f"   (Mastery Level: {new_score}/{MASTERY_THRESHOLD})")
                    break
        else:
            print(f"❌ STRIKE OUT. The correct answer was: {correct_def}")
            # Optional: You could decrease score here, but for encouragement, we usually don't.
        
        time.sleep(1) # Pause briefly so he can read the result
        print("-" * 30)

    # End of Game Summary
    print("\n" + "=" * 50)
    print(f"GAME OVER! Final Score: {session_score} / {num_rounds}")
    
    percentage = (session_score / num_rounds) * 100
    if percentage == 100:
        print("🏆 PERFECT GAME! Amazing job!")
    elif percentage >= 80:
        print("🥈 Great job! You are an All-Star!")
    else:
        print("🧢 Good practice! Keep training!")

    # Save progress
    save_data(data)
    print("\nProgress saved. See you next game!")
    print("=" * 50)

# --- EXECUTE ---
if __name__ == "__main__":
    run_game()
      
