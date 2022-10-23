import cohere
import os
from flask import Flask, request, render_template

co = cohere.Client(os.environ["COHERE_API_KEY"])
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == "POST":
        input1 = request.form.get("input")
        input2 = "a " + request.form.get("type") if request.form.get("type")[0] != "e" else "an " + request.form.get("type")
        result = co.generate(
            prompt="Person 1: This is my " + request.form.get("type")[0] + " : \n" + input1 + "\n\nPerson 2 (stranger): Here is some formal, literary, concise, grammatically correct, and academic feedback: \n",
            max_tokens=300,
            temperature=0,
            frequency_penalty=1,
            presence_penalty=1,
        )
        output = result.generations[0].text.split("\n")
        for i in output:
            if i.isspace() or i == "":
                output.remove(i)
        return render_template('feedback.html', loading="", output="\n".join(output[0:2]))
    return render_template('feedback.html', loading="", output="")