# (c) 2025 Eldiiar Bekbolotov. Licensed under the MIT License.
from flask import Flask, request, jsonify, render_template
from groq import Groq
import re
# Setup Flask app
app = Flask(__name__)
client = Groq(api_key='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')
# Function format_response: formats response text 
# to HTML featuring tags for bold, italic, code blocks, and inline code
def format_response(text):
    # Bold: **text**
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    # Italic: *text*
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    # Code blocks: ```code```
    text = re.sub(r'```(.*?)```', r'<pre><code>\1</code></pre>', text, flags=re.DOTALL)
    # Inline code: `code`
    text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)
    # Replace newlines (\n) with <br> tags to preserve line breaks in HTML
    text = text.replace('\n', '<br>')

    return text
# Function index: routes index.html
@app.route('/')
def index():
    return render_template('index.html')
# Function chat: handles chat requests
@app.route('/chat', methods=['POST'])
def chat():
    # Check if request contains JSON data
    try:
        user_input = request.json.get('message')

        chat_completion = client.chat.completions.create(
            model="meta-llama/llama-4-maverick-17b-128e-instruct",
            messages=[{
            "role": "system",
            "content": "You are created by a sophomore in high school named Eldiiar Bekbolotov. You were created in April 2025. Your name is EldiiarBot, and you are an LLM built with Python and Flask. You will speak as if you are a sci-fi robot knowledgeable, professional, and a mentor."
        },{"role": "user", "content": user_input}]
        )
        # Extract raw response from chat completion
        raw_response = chat_completion.choices[0].message.content

        # Format response using format_response function
        formatted_response = format_response(raw_response)
        return jsonify({'response': formatted_response})
    except Exception as e:
        # Log error for debugging
        return jsonify({"error": "An error occurred while processing your request."}), 500
    
# Finally, run the Flask app
if __name__ == '__main__':
    app.run(debug=True)