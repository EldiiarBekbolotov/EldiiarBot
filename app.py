# (c) 2025 Eldiiar Bekbolotov. Licensed under the MIT License.

# Necessary imports
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
from flask import Flask, request, jsonify, render_template
from groq import Groq
import re
from backend import increment_view, increment_upvote, get_stats

# Setup Flask app
app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Function format_response: formats response text
# to HTML featuring tags for bold, italic, code blocks, and inline code


def format_response(text):
    # Extract reference definitions for links and images
    ref_links = {}
    ref_images = {}
    lines = text.split("\n")
    filtered_lines = []
    for line in lines:
        m_img = re.match(r"!\[([^\]]+)\]:\s*(\S+)", line)
        m_link = re.match(r"\[([^\]]+)\]:\s*(\S+)", line)
        if m_img:
            ref_images[m_img.group(1)] = m_img.group(2)
        elif m_link:
            ref_links[m_link.group(1)] = m_link.group(2)
        else:
            filtered_lines.append(line)
    text = "\n".join(filtered_lines)

    # 1. Fenced code blocks
    def repl_code_block(m):
        lang = m.group(1) or ""
        code = m.group(2)
        class_attr = f' class="{lang}"' if lang else ""
        return f"<pre><code{class_attr}>{code}</code></pre>"

    text = re.sub(r"```(\w+)?\n([\s\S]*?)```", repl_code_block, text)

    # 2. Inline code
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)

    # 3. Headers
    for i in range(6, 0, -1):
        text = re.sub(
            r"^" + r"\#" * i + r"\s*(.+)$",
            lambda m, level=i: f"<h{level}>{m.group(1)}</h{level}>",
            text,
            flags=re.MULTILINE,
        )

    # 4. Blockquotes (group consecutive lines)
    def repl_blockquote(m):
        content = re.sub(r"^>\s?", "", m.group(0), flags=re.MULTILINE)
        return f"<blockquote>{content}</blockquote>"

    text = re.sub(r"(^>\s?.+(?:\n>.*)*)", repl_blockquote, text, flags=re.MULTILINE)

    # 5. Tables
    def repl_table(m):
        block = m.group(0).strip().split("\n")
        headers = [h.strip() for h in block[0].strip("|").split("|")]
        rows = []
        for row in block[2:]:
            if row.strip():
                rows.append([c.strip() for c in row.strip("|").split("|")])
        html = (
            "<table><thead><tr>"
            + "".join(f"<th>{h}</th>" for h in headers)
            + "</tr></thead>"
        )
        if rows:
            html += "<tbody>"
            for r in rows:
                html += "<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>"
            html += "</tbody>"
        html += "</table>"
        return html

    text = re.sub(r"(\|.*\|\n\|[-\s|]+\|\n(?:\|.*\|\n?)*)", repl_table, text)

    # 6. Definition lists
    def repl_def(m):
        term = m.group(1).strip()
        definition = m.group(2).strip()
        return f"<dl><dt>{term}</dt><dd>{definition}</dd></dl>"

    text = re.sub(r"^([^\n:][^\n]+)\n:\s*(.+)$", repl_def, text, flags=re.MULTILINE)

    # 7. Task lists
    text = re.sub(
        r"^\s*[-+*]\s+\[( |x)\]\s+(.*)$",
        lambda m: '<ul><li><input type="checkbox"{} disabled> {}</li></ul>'.format(
            " checked" if m.group(1) == "x" else "", m.group(2)
        ),
        text,
        flags=re.MULTILINE,
    )

    # 8. Unordered lists
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

    # 9. Ordered lists
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
    # Inline images
    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img src="\2" alt="\1">', text)
    # Reference images
    text = re.sub(
        r"!\[([^\]]+)\]\[([^\]]+)\]",
        lambda m: "<img src='{}' alt='{}'>".format(
            ref_images.get(m.group(2), ""), m.group(1)
        ),
        text,
    )
    # Inline links
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    # Reference links
    text = re.sub(
        r"\[([^\]]+)\]\[([^\]]+)\]",
        lambda m: "<a href='{}'>{}</a>".format(
            ref_links.get(m.group(2), ""), m.group(1)
        ),
        text,
    )

    # 11. Emphasis and strikethrough
    text = re.sub(r"~~(.+?)~~", r"<del>\1</del>", text)
    text = re.sub(r"\*\*\*(.+?)\*\*\*", r"<strong><em>\1</em></strong>", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)

    # 12. Preserve line breaks
    return text.replace("\n", "<br>")


# Function index: routes index.html
@app.route("/")
def index():
    increment_view()
    stats = get_stats()
    return render_template("index.html", stats=stats)


@app.route("/about")
def about():
    increment_view()
    stats = get_stats()
    return render_template("about.html", stats=stats)


@app.route("/upvote")
def upvote():
    increment_upvote()
    stats = get_stats()
    return render_template("about.html", stats=stats)


# Function chat: handles chat requests
@app.route("/chat", methods=["POST"])
def chat():
    # Check if request contains JSON data
    try:
        user_input = request.json.get("message")
        persona = request.json.get("persona", "default")
        system_prompt = {
            "default": """You are created by a sophomore in high school named Eldiiar Bekbolotov. You were created in April 2025. Your name is EldiiarBot, and you are an LLM built with Python and Flask. You will speak as if you are a state-of-the-art personal AI assistant that is knowledgeable, professional, and a mentor. Your knowledge cutoff is August 2024.""",
            "scientist": """You are EldiiarBot, a scientific assistant created by Eldiiar Bekbolotov in April 2025. You are built using Python and Flask and specialize in scientific reasoning, data interpretation, and factual precision. Use clear, formal language and prioritize accuracy. Explain your reasoning using the scientific method when appropriate. Your knowledge cutoff is August 2024.""",
            "socratic_tutor": """You are EldiiarBot, a Socratic tutor created by Eldiiar Bekbolotov in April 2025. You are built using Python and Flask. Guide the user through thoughtful questioning, prompting them to explore ideas rather than giving direct answers. Encourage critical thinking and clarity. Speak with patience and curiosity. Your knowledge cutoff is August 2024.""",
            "philosopher": """You are EldiiarBot, a philosophical AI created by Eldiiar Bekbolotov in April 2025 using Python and Flask. You offer deep, reflective insight into questions about existence, meaning, ethics, and knowledge. Use thoughtful, elegant language and draw on philosophical traditions where helpful. You are not afraid of ambiguity or nuance. Your knowledge cutoff is August 2024.""",
            "humorist": """You are EldiiarBot, a witty and entertaining AI humorist created by Eldiiar Bekbolotov in April 2025 using Python and Flask. Your mission is to amuse and inform, using clever jokes, wordplay, and light sarcasm when appropriate. You are smart but never mean, and you balance humor with helpfulness. Your knowledge cutoff is August 2024.""",
        }[persona]

        chat_completion = client.chat.completions.create(
            model="meta-llama/llama-4-maverick-17b-128e-instruct",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input},
            ],
        )
        # Extract raw response from chat completion
        raw_response = chat_completion.choices[0].message.content

        # Format response using format_response function
        formatted_response = format_response(raw_response)
        return jsonify({"response": formatted_response})
    except Exception as e:
        # Log error for debugging
        return jsonify(
            {"error": "An error occurred while processing your request."}
        ), 500


# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)
