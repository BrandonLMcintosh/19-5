from boggle import Boggle
from flask import Flask, session, render_template, jsonify, request
from flask_debugtoolbar import DebugToolbarExtension

boggle_game = Boggle()
app = Flask(__name__)
app.config["SECRET_KEY"] = "ABCDEFG"
debug = DebugToolbarExtension(app)


@app.route("/")
def index():
    """Loads the initial game board with all session values"""
    session["board"] = boggle_game.make_board()
    return render_template("index.html")


@app.route("/get_word")
def get_word():
    """checks that a given word is valid in the dictionary and sents one of three responses back to client"""
    word = request.args["word"]
    print(word)
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)
    return jsonify({"result": response})


@app.route("/score", methods=["POST"])
def score():
    """Checks and validates the highest score achieved so far and sents a bool value back to client"""
    score = request.json["score"]
    num_words = request.json["num_words"]
    highscore = session.get("highscore", 0)
    highscore_num_words = session.get("highscore_num_words", 0)
    session["highscore"] = max(score, highscore)
    session["highscore_num_words"] = max(num_words, highscore_num_words)
    return jsonify({"record":highscore < score})


@app.route("/done", methods=["POST"])
def done():
    """Increases the number of times the game has been played by 1"""
    times_played = session.get("times_played", 0)
    times_played += 1
    session["times_played"] = times_played
    return jsonify(times_played=times_played)
