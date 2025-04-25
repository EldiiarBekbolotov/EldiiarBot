import time
from transformers import pipeline

# Load the text-generation pipeline with the specified model
text_generator = pipeline(task="text-generation", model="Qwen/Qwen2.5-1.5B")

# Function to simulate a typing effect
def typewriter_effect(text, delay=0.03):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()  # New line after finishing

# Function to simulate a conversation
def chat_with_bot():
    print("Bot is ready! Type 'exit' to end the conversation.")
    
    while True:
        # Get user input
        user_input = input("You: ")
        # Exit condition
        if user_input.lower() == "exit":
            print("Bot: Goodbye!")
            break
        
        # Show "thinking" animation
        print("Bot is thinking", end="", flush=True)
        for _ in range(3):  # Show 3 dots for the typing effect
            time.sleep(0.5)  # Simulate time delay
            print(".", end="", flush=True)
        print()  # New line after thinking
        
        # Generate a response using the model
        response = text_generator(user_input, truncation=True, max_new_tokens=100)  # Generate initial response
        
        # Print the bot's reply with a typewriter effect
        bot_reply = response[0]['generated_text']
        typewriter_effect(bot_reply)
        
        # Offer to continue if the sentence feels incomplete
        while True:
            user_decision = input("Bot: Would you like me to continue? (yes/no): ")
            if user_decision.lower() in ["yes", "y"]:
                # Generate additional completion
                print("Bot is continuing", end="", flush=True)
                for _ in range(3):
                    time.sleep(0.5)
                    print(".", end="", flush=True)
                print()
                
                # Generate more tokens starting from the last response
                additional_response = text_generator(bot_reply, truncation=True, max_new_tokens=100)
                bot_reply = additional_response[0]['generated_text']
                typewriter_effect(bot_reply)
            elif user_decision.lower() in ["no", "n"]:
                break
            else:
                print("Bot: Please reply with 'yes' or 'no'.")
                continue

# Start the chat
if __name__ == "__main__":
    chat_with_bot()