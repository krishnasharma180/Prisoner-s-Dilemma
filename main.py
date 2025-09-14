import random
import itertools
from collections import defaultdict
import math
import pandas as pd

payoff_matrix={
    ("C","C"):(3,3),
    ("C","D"):(0,5),
    ("D","C"):(5,0),
    ("D","D"):(1,1)
}

# All Strategies

def Tit_For_Tat():  #Give response just after opponent defect
    def strategy(opponent_last_move=None):
        if opponent_last_move is None:
            return "C"
        return opponent_last_move
    return strategy

def Tit_For_Two_Tats():   #Give respnse after two defects
    count=0               
    def strategy(opponent_last_move=None):
        nonlocal count
        if opponent_last_move=="D":
            count+=1
        if count>=2:
            return "D"
        return "C"
    return strategy
    
def AlwaysCooperate():   #Never defects always cooperate
    def strategy(opponent_last_move=None):
        return "C"
    return strategy

def Mostly_Cooperate():   # Cooperate Most of the Time
    def strategy(opponent_last_move=None):
        if(random.random()<0.8):
            return "C"
        return "D"
    return strategy

def AlwaysDefect():   # Always Defect
    def strategy(opponent_last_move=None):
        return "D"
    return strategy

def Mostly_Defect():   # Defect Most of the Time
    def strategy(opponent_last_move=None):
        if(random.random()<0.8):
            return "D"
        return "C"
    return strategy

def Random():   #Randdomly Chooses Cooperation and Defection
    def strategy(opponent_last_move=None):
        return random.choice(['C','D'])
    return strategy

def GrimTrigger():  # Defect Once get defected by opponent
    grim=False
    def strategy(opponent_last_move=None):
        nonlocal grim
        if opponent_last_move =="D":
            grim=True
        if grim:
            return "D"
        return "C"
    return strategy

def Mirror():   #Do What opponent does
    def strategy(opponent_last_move=None):
        if opponent_last_move is None:
            return "C"
        return opponent_last_move
    return strategy


def My_Version():
    defect_history=[]
    my_defect_debt=0
    forgiveness_threshold=3
    recent_coices=10  # Look at last 10 moves for pattern detection
    
    def strategy(opponent_last_move=None):
        nonlocal defect_history, my_defect_debt, forgiveness_threshold
        if opponent_last_move=='D':
            defect_history.append(len(defect_history)) 
        
        # If I have defect debt, pay it back
        if my_defect_debt>0:
            my_defect_debt -= 1
            return 'D'
        
        # Analyze(last 10 moves)
        recent_defections=sum(1 for d in defect_history if d >= max(0, len(defect_history) - recent_coices))
        total_defections=len(defect_history)
        
        if len(defect_history)>20:
            recent_rate=recent_defections / min(recent_coices, len(defect_history))
            if recent_rate>0.5:  
                forgiveness_threshold=2  
            else:
                forgiveness_threshold=4  
        
        # punishment if threshold exceeded
        if total_defections>forgiveness_threshold:
            if total_defections<=6:
                my_defect_debt=total_defections  
            else:
                my_defect_debt=total_defections+2
            
            defect_history = []
            return 'D'
        
        return 'C'
    
    return strategy

strategy_factories = {
    "TitForTat": Tit_For_Tat,
    "TitForTwoTats": Tit_For_Two_Tats,
    "AlwaysCooperate": AlwaysCooperate,
    "MostlyCooperate": Mostly_Cooperate,
    "AlwaysDefect": AlwaysDefect,
    "MostlyDefect": Mostly_Defect,
    "Random": Random,
    "GrimTrigger": GrimTrigger,
    "Mirror": Mirror,
    "Bearer":My_Version
}

def play_rounds(player1, player2, num_rounds=None):
    #Each round will have 280-320 matches
    if num_rounds is None:
        num_rounds = random.randint(280, 320) 
    
    score1 = 0
    score2 = 0
    prev1 = None
    prev2 = None
    history = []
    
    for _ in range(num_rounds):
        choice1 = player1(prev2)
        choice2 = player2(prev1)
        result = (choice1, choice2)
        score1 += payoff_matrix[result][0]
        score2 += payoff_matrix[result][1]
        history.append(result)
        prev1 = choice1
        prev2 = choice2

    return (score1, score2), history, num_rounds
    
    
# How much a strategy cooperate or defect
def cooperation_rate(history):
    a_coop = b_coop = mutual_coop = mutual_defect = 0
    for (a, b) in history:
        if a == 'C':
            a_coop += 1
        if b == "C":
            b_coop += 1
        if a == "C" and b == "C":
            mutual_coop += 1
        if a == "D" and b == "D":
            mutual_defect += 1
    total = len(history)
    return a_coop/total, b_coop/total, mutual_coop/total, mutual_defect/total

# Round Robin tournament each strategy play against every other and itself also

def tournament(strategy_factories, rounds=100):
    
    names = list(strategy_factories.keys())
    pairs = list(itertools.product(names, names)) # Creates all possible pairs
    scores = defaultdict(list)
    
    data_rows = []
    win_rows = []
    coop_rows = []
    pair_rows = []

    match_id = 0
    for name1, name2 in pairs:
        a_coop = b_coop = mutual_coop = mutual_defect = 0
        first_win = second_win = draw = 0
        
        for i in range(rounds):
            match_id += 1
            player1 = strategy_factories[name1]()
            player2 = strategy_factories[name2]()
            
            (scoreA, scoreB), hist, actual_rounds = play_rounds(player1, player2)
            
            data_rows.append({
                "Match": i+1,
                "Player1": name1,
                "Player2": name2,
                "Score1": scoreA,
                "Score2": scoreB,
                "Actual_Rounds": actual_rounds,
                "Match_ID": match_id
            })
            
            a, b, c, d = cooperation_rate(hist)
            a_coop += a
            b_coop += b
            mutual_coop += c
            mutual_defect += d
            
            if scoreA > scoreB:
                first_win += 1
            elif scoreB > scoreA:
                second_win += 1
            else:
                draw += 1
            scores[(name1, name2)].append((scoreA, scoreB))
            
        coop_rows.append({
            "Player1": name1,
            "Player2": name2,
            "A_Coop_Rate": a_coop/rounds,
            "B_Coop_Rate": b_coop/rounds,
            "Mutual_Coop_Rate": mutual_coop/rounds,
            "Mutual_Defect_Rate": mutual_defect/rounds
        })
        
        win_rows.append({
            "Player1": name1,
            "Player2": name2,
            "First_Win": first_win,
            "Second_Win": second_win,
            "Draws": draw
        })
    
    pair_summary = {}
    for keys, values in scores.items():
        a_vals = [v[0] for v in values]
        b_vals = [v[1] for v in values]
        pair_summary[keys] = {
            "A_avg": sum(a_vals)/len(a_vals),
            "B_avg": sum(b_vals)/len(b_vals),
            "A_std": math.sqrt(sum((x-(sum(a_vals)/len(a_vals)))**2 for x in a_vals)/len(a_vals)) if len(a_vals) > 1 else 0,
            "B_std": math.sqrt(sum((x-(sum(b_vals)/len(b_vals)))**2 for x in b_vals)/len(b_vals)) if len(b_vals) > 1 else 0
        }
        pair_rows.append({
            "Player1": keys[0],
            "Player2": keys[1],
            "A_avg": pair_summary[keys]["A_avg"],
            "B_avg": pair_summary[keys]["B_avg"],
            "A_std": pair_summary[keys]["A_std"],
            "B_std": pair_summary[keys]["B_std"]
        })
        
        
    # Creating diffrent Tables
    df_data = pd.DataFrame(data_rows)
    df_pair = pd.DataFrame(pair_rows)
    df_win = pd.DataFrame(win_rows)
    df_coop = pd.DataFrame(coop_rows)
    
    return df_data, df_pair, df_win, df_coop, pair_summary

df_data, df_pair, df_win, df_coop, pair_summary = tournament(strategy_factories)

df_data.to_csv("all_data.csv", index=False)
df_pair.to_csv("pair_data.csv", index=False)
df_win.to_csv("win_data.csv", index=False)
df_coop.to_csv("coop_data.csv", index=False)
