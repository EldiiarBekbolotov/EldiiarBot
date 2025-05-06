# (c) 2025 Eldiiar Bekbolotov. Licensed under the MIT License.

# Necessary imports
import os  # Provides access to operating system functionalities, like environment variables.

import re  # Regular expression library for text pattern matching and formatting.

import html  # Utility for escaping HTML to prevent XSS attacks.

import psycopg2  # Python library for interacting with PostgreSQL databases.

from dotenv import (
    load_dotenv,
)  # Loads environment variables from a .env file for secure configuration.

from flask import (
    Flask,
    request,
    jsonify,
    render_template,
)  # Flask framework for building web applications.

from groq import Groq  # Client library for interacting with the Groq AI API.

from backend import (
    increment_view,
    increment_upvote,
    get_stats,
)  # Custom backend functions for database operations.

# Load environment variables from .env
# The .env file stores sensitive data (e.g., API keys) to keep them out of the codebase.
load_dotenv()

# Setup Flask app
# Initialize the Flask application
app = Flask(__name__)  # Creates a Flask app instance.
# Initialize Groq client with the API key from environment variables.
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def format_response(text):
    """
    Converts raw markdown text into HTML for safe rendering in a web browser.
    Supports formatting for code blocks, headers, lists, links, and more, while escaping HTML to prevent cross site scripting (XSS).
    Args:
        text (str): The raw text to format.
    Returns:
        str: The formatted HTML string.
    """
    # Escape HTML to prevent script injection (e.g., <script> tags).
    text = html.escape(text)

    # 1. Fenced code blocks (e.g., ```python ... ```)
    def repl_code_block(m):
        lang = m.group(1) or ""  # Extract language (e.g., "python") or empty string.
        code = m.group(2)  # Extract code content.
        class_attr = (
            f' class="{lang}"' if lang else ""
        )  # Add language class for syntax highlighting.
        return f"<pre><code{class_attr}>{html.escape(code)}</code></pre>"

    text = re.sub(r"```(\w+)?\n([\s\S]*?)```", repl_code_block, text)

    # 2. Inline code (e.g., `code`)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)

    # 3. Headers (H1 to H6, e.g., # Header, ## Header)
    for i in range(6, 0, -1):
        text = re.sub(
            r"^" + r"\#" * i + r"\s*(.+)$",
            lambda m, level=i: f"<h{level}>{html.escape(m.group(1))}</h{level}>",
            text,
            flags=re.MULTILINE,
        )

    # 4. Blockquotes (e.g., > Quote)
    def repl_blockquote(m):
        content = re.sub(
            r"^>\s?", "", m.group(0), flags=re.MULTILINE
        )  # Remove "> " prefix.
        return f"<blockquote>{html.escape(content)}</blockquote>"

    text = re.sub(r"(^>\s?.+(?:\n>.*)*)", repl_blockquote, text, flags=re.MULTILINE)

    # 5. Tables (e.g., | Header | Header |)
    def repl_table(m):
        block = m.group(0).strip().split("\n")  # Split table into lines.
        headers = [
            h.strip() for h in block[0].strip("|").split("|")
        ]  # Extract headers.
        rows = []
        for row in block[2:]:  # Skip header and separator line.
            if row.strip():
                rows.append(
                    [c.strip() for c in row.strip("|").split("|")]
                )  # Extract row cells.
        html_table = "<table><thead><tr>"
        html_table += "".join(
            f"<th>{html.escape(h)}</th>" for h in headers
        )  # Build header row.
        html_table += "</tr></thead>"
        if rows:
            html_table += "<tbody>"
            for r in rows:
                html_table += (
                    "<tr>" + "".join(f"<td>{html.escape(c)}</td>" for c in r) + "</tr>"
                )  # Build data rows.
            html_table += "</tbody>"
        html_table += "</table>"
        return html_table

    text = re.sub(r"(\|.*\|\n\|[-\s|]+\|\n(?:\|.*\|\n?)*)", repl_table, text)

    # 6. Definition lists (e.g., Term\n: Definition)
    def repl_def(m):
        term = m.group(1).strip()  # Extract term.
        definition = m.group(2).strip()  # Extract definition.
        return (
            f"<dl><dt>{html.escape(term)}</dt><dd>{html.escape(definition)}</dd></dl>"
        )

    text = re.sub(r"^([^\n:][^\n]+)\n:\s*(.+)$", repl_def, text, flags=re.MULTILINE)

    # 7. Task lists (e.g., - [x] Task)
    text = re.sub(
        r"^\s*[-+*]\s+\[( |x)\]\s+(.*)$",
        lambda m: '<ul><li><input type="checkbox"{} disabled> {}</li></ul>'.format(
            " checked" if m.group(1) == "x" else "", html.escape(m.group(2))
        ),
        text,
        flags=re.MULTILINE,
    )

    # 8. Unordered lists (e.g., - Item)
    def repl_ul(match):
        items = [
            item.strip()
            for item in match.group(0).split("\n")
            if re.match(r"^\s*[-+*]\s+", item)
        ]
        lis = "".join(
            "<li>" + re.sub(r"^\s*[-+*]\s+", "", item) + "</li>" for item in items
        )
        return "<ul>" + lis + "</ul>"

    text = re.sub(r"((?:^\s*[-+*]\s+.*\n?)+)", repl_ul, text, flags=re.MULTILINE)

    # 9. Ordered lists (e.g., 1. Item)
    def repl_ol(match):
        items = [
            item.strip()
            for item in match.group(0).split("\n")
            if re.match(r"^\s*\d+\.\s+", item)
        ]
        lis = "".join(
            "<li>" + re.sub(r"^\s*\d+\.\s+", "", item) + "</li>" for item in items
        )
        return "<ol>" + lis + "</ol>"

    text = re.sub(r"((?:^\s*\d+\.\s+.*\n?)+)", repl_ol, text, flags=re.MULTILINE)

    # 10. Links and images
    # Inline images (e.g., ![Alt](url))
    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img src="\2" alt="\1">', text)
    # Inline links (e.g., [Text](url))
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)

    # 11. Emphasis and strikethrough
    text = re.sub(
        r"~~(.+?)~~", r"<del>\1</del>", text
    )  # Strikethrough (e.g., ~~Text~~)
    text = re.sub(
        r"\*\*\*(.+?)\*\*\*", r"<strong><em>\1</em></strong>", text
    )  # Bold+Italic
    text = re.sub(
        r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text
    )  # Bold (e.g., **Text**)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)  # Italic (e.g., *Text*)

    # 12. Preserve line breaks by converting newlines to <br> tags
    text = text.replace("\n", "<br>")

    return text


# Route for the homepage
@app.route("/")
def index():
    """
    Renders the homepage (index.html) and increments the view counter.
    Returns:
        Response: Rendered HTML template with view and upvote stats.
    """
    increment_view()  # Increment view count in the database.

    stats = get_stats()  # Fetch current views and upvotes.

    return render_template("index.html", stats=stats)  # Render template with stats.


# Route for the about page
@app.route("/about")
def about():
    """
    Renders the about page (about.html) and increments the view counter.
    Returns:
        Response: Rendered HTML template with view and upvote stats.
    """
    increment_view()  # Increment view count in the database.

    stats = get_stats()  # Fetch current views and upvotes.

    return render_template("about.html", stats=stats)  # Render template with stats.


# Route for upvoting
@app.route("/upvote")
def upvote():
    """
    Increments the upvote counter and renders the about page (about.html).
    Returns:
        Response: Rendered HTML template with updated view and upvote stats.
    """
    increment_upvote()  # Increment upvote count in the database.

    stats = get_stats()  # Fetch current views and upvotes.

    return render_template("about.html", stats=stats)  # Render template with stats.


# Route for handling chat requests
@app.route("/chat", methods=["POST"])
def chat():
    """
    Handles POST requests for chat interactions with the Groq AI model.
    Accepts a user message and persona, processes it, and returns a formatted HTML response.
    Args:
        request.json: JSON payload with 'message' (user input) and optional 'persona' (e.g., 'scientist').
    Returns:
        Response: JSON object with the formatted AI response or an error message.
    Raises:
        Exception: If the request fails (e.g., invalid JSON, API error).
    """
    try:
        # Extract user input and persona from the JSON request.
        user_input = request.json.get("message")

        persona = request.json.get(
            "persona", "default"
        )  # Default to 'default' persona if not provided.

        # Define system prompts for different personas to customize AI behavior.
        system_prompt = {
            # default system prompt
            "default": """You are created by a sophomore in high school named Eldiiar Bekbolotov. You were created in April 2025. Your name is EldiiarBot, and you are an LLM built with Python and Flask. You will speak as if you are a state-of-the-art personal AI assistant that is knowledgeable, professional, and a mentor. Your knowledge cutoff is August 2024.""",
            # scientist system prompt
            "scientist": """You are EldiiarBot, a scientific assistant created by Eldiiar Bekbolotov in April 2025. You are built using Python and Flask and specialize in scientific reasoning, data interpretation, and factual precision. Use clear, formal language and prioritize accuracy. Explain your reasoning using the scientific method when appropriate. Your knowledge cutoff is August 2024.""",
            # tutor system prompt
            "socratic_tutor": """You are EldiiarBot, a Socratic tutor created by Eldiiar Bekbolotov in April 2025. You are built using Python and Flask. Guide the user through thoughtful questioning, prompting them to explore ideas rather than giving direct answers. Encourage critical thinking and clarity. Speak with patience and curiosity. Your knowledge cutoff is August 2024.""",
            # gym coach system prompt
            "gym_coach": """You are EldiiarBot, a fitness coach created by Eldiiar Bekbolotov in April 2025 using Python and Flask. You provide personalized workout plans, nutrition advice, and motivation. Use encouraging language and adapt to the user's fitness level. Your knowledge cutoff is August 2024.""",
            # philosopher system prompt
            "philosopher": """You are EldiiarBot, a philosophical AI created by Eldiiar Bekbolotov in April 2025 using Python and Flask. You offer deep, reflective insight into questions about existence, meaning, ethics, and knowledge. Use thoughtful, elegant language and draw on philosophical traditions where helpful. You are not afraid of ambiguity or nuance. Your knowledge cutoff is August 2024.""",
            # humorist system prompt
            "humorist": """You are EldiiarBot, a witty and entertaining AI humorist created by Eldiiar Bekbolotov in April 2025 using Python and Flask. Your mission is to amuse and inform, using clever jokes, wordplay, and light sarcasm when appropriate. You are smart but never mean, and you balance humor with helpfulness. Your knowledge cutoff is August 2024.""",
        }[persona]

        # Call the Groq API to generate a response based on the system prompt and user input.
        chat_completion = client.chat.completions.create(
            model="meta-llama/llama-4-maverick-17b-128e-instruct",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input},
            ],
        )

        # Extract the raw response from the API.
        raw_response = chat_completion.choices[0].message.content

        # Format the raw response into HTML using the format_response function.
        formatted_response = format_response(raw_response)

        # Return the formatted response as JSON.
        return jsonify({"response": formatted_response})
    except Exception as e:
        # Handle any errors (e.g., invalid JSON, API failure) and return a 500 error.
        return jsonify(
            {"error": "An error occurred while processing your request."}
        ), 500


# Run Flask app
if __name__ == "__main__":
    """
    Runs the Flask application in debug mode when the script is executed directly.
    Debug mode enables auto-reloading and detailed error messages for development.
    """
    app.run(debug=True)
