from boggle import Boggle
from flask import Flask, session, render_template, jsonify, request
from flask_debugtoolbar import DebugToolbarExtension

boggle_game = Boggle()
app = Flask(__name__)
app.config['SECRET_KEY'] = "ABCDEFG"
debug = DebugToolbarExtension(app)

@app.route("/")
def index():
    session["board"] = boggle_game.make_board()
    return render_template("index.html")

@app.route("/get_word")
def get_word():
    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)
    return jsonify({"result": response})