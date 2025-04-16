import random

with open("IDC20_Python_Project/model2.txt", "r", encoding="utf-8") as file:
    text = file.read().lower()

text = text.replace('\n', ' ').replace('--', ' ')
words = text.split()

markov_chain = {}

for i in range(len(words) - 2):
    key = (words[i], words[i+1])
    next_word = words[i+2]
    if key not in markov_chain:
        markov_chain[key] = []
    markov_chain[key].append(next_word)

def generate_response(seed=None, length=20):
    if seed:
        seed_words = seed.lower().split()
        if len(seed_words) >= 2:
            key = (seed_words[-2], seed_words[-1])
        else:
            key = random.choice(list(markov_chain.keys()))
    else:
        key = random.choice(list(markov_chain.keys()))

    result = [key[0], key[1]]

    for _ in range(length):
        next_words = markov_chain.get(key)
        if not next_words:
            break
        next_word = random.choice(next_words)
        result.append(next_word)
        key = (key[1], next_word)

    return ' '.join(result)

print("Chatbot is ready! Type 'exit' to quit.")
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    response = generate_response(user_input)
    print("Bot:", response)
