import os

from flask import Flask, render_template, request, send_file
import ollama

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

app = Flask(__name__)

generated_story = ""

def generate_story(name, genre, theme):

    prompt = f"""
    Write a {genre} story.

    Character Name: {name}

    Theme:
    {theme}

    Make the story creative and engaging.
    """

    response = ollama.chat(
        model="llama3.2:latest",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    story = response["message"]["content"]


    return story



@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():

    global generated_story

    name = request.form["name"]
    theme = request.form["theme"]
    genre = request.form["genre"]

    story = generate_story(
        name,
        genre,
        theme
    )

    generated_story = story
   
      
    return render_template(
        "index.html",
        story=story,
    )


@app.route("/download")
def download_story():

    pdf_file = "StoryForge.pdf"

    doc = SimpleDocTemplate(pdf_file)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph("AI StoryForge Story", styles["Title"])
    )

    elements.append(Spacer(1, 12))

    elements.append(
        Paragraph(generated_story, styles["BodyText"])
    )

    doc.build(elements)

    return send_file(
        pdf_file,
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True)
