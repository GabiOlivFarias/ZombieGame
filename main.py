from flask import Flask, render_template_string

app = Flask(__name__)

@app.route("/")
def game():
     return "<h1>Olá Jogador</h1>"

if __name__ == "__main__":
    app.run(debug=True)
