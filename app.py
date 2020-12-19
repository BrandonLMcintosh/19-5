from boggle import Boggle
from Flask import flask
from flask_debugtoolbar import DebugToolbarExtension

boggle_game = Boggle()
app = Flask(__name__)
app.config['SECRET_KEY'] = "ABCDEFG"
debug = DebugToolbarExtension(app)

@app.route("/")
def index():
    session["board"] = boggle_game.make_board()
    return render_template("base.html")

