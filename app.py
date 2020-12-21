from boggle import Boggle
from flask import Flask, session, render_template
from flask_debugtoolbar import DebugToolbarExtension

boggle_game = Boggle()
app = Flask(__name__)
app.config['SECRET_KEY'] = "ABCDEFG"
debug = DebugToolbarExtension(app)

@app.route("/")
def index():
    session["board"] = boggle_game.make_board()
    return render_template("index.html")