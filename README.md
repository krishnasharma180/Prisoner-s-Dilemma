# 🎲 Game Theory: Prisoner’s Dilemma Tournament  

This project explores **Game Theory** through the classic **Iterated Prisoner’s Dilemma (IPD)**.  
Different strategies — from simple cooperators and defectors to retaliators and hybrids — compete in a Python-based tournament.  

Alongside well-known strategies like *Tit-for-Tat* and *Grim Trigger*, I also introduced my custom strategy, **Bearer**, to test how it performs in repeated interactions.  

---

## 📌 Features  

- Implementation of multiple strategies:  
  - Tit-for-Tat, Tit-for-Two-Tats, Grim Trigger, Mirror  
  - Always Cooperate, Always Defect  
  - Mostly Cooperate, Mostly Defect, Random  
  - **Bearer (custom strategy)**  

- Tournament system:  
  - Round-robin matches between all strategies   
  - Tracks scores, wins/losses/draws, and cooperation rates  

- Visualizations:  
  - Average score per strategy  
  - Head-to-head performance heatmaps  
  - Win/draw distributions  
  - Score stability (variance)  
  - Cooperation vs payoff tradeoff plot 

---

## 🧠 Key Insights  

- **Balanced reciprocity wins**: Strategies that reward cooperation but punish defection (e.g., GrimTrigger, Tit-for-Two-Tats) perform best overall.  
- **Pure cooperation is fragile**: AlwaysCooperate is highly volatile — excellent against nice players, disastrous against defectors.  
- **Pure defection is limited**: AlwaysDefect is consistent but stagnates in all-defector environments.  
- **Bearer strategy**: Performs in the mid-to-upper tier, achieving better stability and cooperation than naïve or random strategies, though not outperforming the strongest reciprocators.  

---

## 🚀 How to Run  

1. Clone the repository:  
   ```bash
   git clone https://github.com/krishnasharma180/Prisoner's_Dilemma.git
   cd Prisoner's_Dilemma

2. Run the tornament:
   ```bash
   python main.py

  ---
  
  ## 📺 Learn More

- For a quick explanation of Game Theory and the Prisoner’s Dilemma, check out this video:
- 👉 https://www.youtube.com/watch?v=mScpHTIi-kM&t=13s
