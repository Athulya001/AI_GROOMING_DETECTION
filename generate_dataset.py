import csv
import random

safe_messages = [
    "Hello how are you",
    "Good morning",
    "Nice to meet you",
    "How was your day",
    "What are you doing today",
    "Let's study together",
    "Hope you are doing well",
    "See you tomorrow",
    "Take care",
    "Have a great day"
]

harassment_messages = [
    "You are stupid",
    "Nobody likes you",
    "Shut up idiot",
    "You are useless",
    "I hate you",
    "You are pathetic",
    "Stop talking nonsense",
    "You are so annoying",
    "You are worthless",
    "Go away"
]

threat_messages = [
    "I will hurt you",
    "I will destroy your life",
    "I will kill you",
    "Watch what happens to you",
    "You better be careful",
    "I will find you",
    "You are going to regret this",
    "I will expose you",
    "Something bad will happen to you",
    "You cannot escape"
]

grooming_messages = [
    "Don't tell anyone about this",
    "You are mature for your age",
    "Send me your picture",
    "Are you alone right now",
    "You can trust me",
    "Let's keep this secret",
    "I like you more than your friends",
    "You don't need to tell your parents",
    "Send me a private photo",
    "It's just between us"
]

def generate_variation(text):
    variations = [
        text,
        text + " please",
        "Hey, " + text,
        text + " now",
        text + " quickly",
        "Can you " + text.lower(),
        "Why don't you " + text.lower()
    ]
    return random.choice(variations)

data = []

for _ in range(250):
    data.append([generate_variation(random.choice(safe_messages)), "safe"])
    data.append([generate_variation(random.choice(harassment_messages)), "harassment"])
    data.append([generate_variation(random.choice(threat_messages)), "threat"])
    data.append([generate_variation(random.choice(grooming_messages)), "grooming"])

random.shuffle(data)

with open("dataset.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["text", "label"])
    writer.writerows(data)

print("✅ 1000-sample dataset generated successfully!")