import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --- Example: simulate some WhatsApp messages ---
data = {
    "message": [
        "The sound is too loud at night!",
        "Good morning everyone",
        "Did anyone hear that sound yesterday?",
        "Thanks for the update",
        "There is a weird sound coming from the elevator, very disturbing at night",
        "Ok",
        "Sound is unbearable, please check",
        "See you later",
        "Meeting at 7?",
        "Can someone fix the sound issue asap? It’s been days!"
    ]
}

df = pd.DataFrame(data)

# --- Preprocess ---
df["length"] = df["message"].str.len()
df["contains_sound"] = df["message"].str.lower().str.contains("sound")

# --- Plot ---
plt.figure(figsize=(8, 5))
sns.kdeplot(df[df["contains_sound"]]["length"], label="Messages with 'sound'", shade=True)
sns.kdeplot(df[~df["contains_sound"]]["length"], label="Other messages", shade=True)
plt.xlabel("Message Length (characters)")
plt.ylabel("Density")
plt.title("Distribution of Message Lengths\n'Sound' vs Other Messages")
plt.legend()
plt.show()
