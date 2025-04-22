train_data = 'model2.txt'

first_possible_words = {}
second_possible_words = {}
transitions = {}

def expandDict(dictionary, key, value):
    if key not in dictionary:
        dictionary[key] = []
    dictionary[key].append(value)
    
def get_next_probability(given_list):  # returns dictionary
    probability_dict = {}
    given_list_length = len(given_list)
    for item in given_list:
        probability_dict[item] = probability_dict.get(item, 0) + 1
    for key, value in probability_dict.items():
        probability_dict[key] = value / given_list_length
    return probability_dict

def trainMarkovModel():
    for line in open(train_data):
        tokens = line.rstrip().lower().split()
        tokens_length = len(tokens)
        for i in range(tokens_length):
            token = tokens[i]
            if i == 0:
                first_possible_words[token] = first_possible_words.get(token, 0) + 1
            else:
                prev_token = tokens[i - 1]
                if i == tokens_length - 1:
                    expandDict(transitions, (prev_token, token), 'END')
                if i == 1:
                    expandDict(second_possible_words, prev_token, token)
                else:
                    prev_prev_token = tokens[i - 2]
                    expandDict(transitions, (prev_prev_token, prev_token), token)
    
    first_possible_words_total = sum(first_possible_words.values())
    for key, value in first_possible_words.items():
        first_possible_words[key] = value / first_possible_words_total
        
    for prev_word, next_word_list in second_possible_words.items():
        second_possible_words[prev_word] = get_next_probability(next_word_list)
        
    for word_pair, next_word_list in transitions.items():
        transitions[word_pair] = get_next_probability(next_word_list)
    

def next_word(tpl):
    if isinstance(tpl, str):  # First word of sentence; return second possible words
        d = second_possible_words.get(tpl)
        if d is not None:
            return list(d.keys())
    if isinstance(tpl, tuple):  # Incoming words are a combination of two words; find next word based on transitions
        d = transitions.get(tpl)
        if d is None:
            return []
        return list(d.keys())
    return None  # Wrong input, return nothing

trainMarkovModel()  # Generate first, second words list and transitions

########## demo code below ################
print("Usage: start typing... program will suggest words. Press tab to choose the first suggestion or keep typing.\n")

def suggest_next_word(sentence):
    tokens = sentence.split()
    if len(tokens) < 2:  # Only first word typed
        return next_word(tokens[0].lower())
    else:  # Send a tuple of the last two words
        return next_word((tokens[-2].lower(), tokens[-1].lower()))

# Instead of msvcrt, we just use input() for the demonstration
while True:
    sentence = input("You: ")
    if sentence.strip() == '':  # End when user presses enter with no input
        break
    
    # Show next word suggestions
    suggestions = suggest_next_word(sentence)
    print("Suggestions:", suggestions)
    
    # Simulate auto-completion if suggestions are available
    if suggestions:
        # Auto-complete with the first suggestion
        sentence += ' ' + suggestions[0]
        print(f"Auto-completed: {sentence}")
