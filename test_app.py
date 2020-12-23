from unittest import TestCase
from app import app
from flask import session, jsonify
from boggle import Boggle 


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!
    def setUp(self):
        """setting up each test""" 
        self.client = app.test_client()
        app.config["TESTING"] = True
        app.secret_key = "secretKey"

    def test_index(self):
        with self.client:
            response = self.client.get("/")
            self.assertIsNone(session.get("highscore"))
            self.assertIsNone(session.get("times_played"))
            html = response.get_data(as_text=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn("<th>Score</th>", html)

    def test_get_word(self):
        with self.client:
            with self.client.session_transaction() as setSession:
                setSession["board"] = [["B", "A", "L", "D", "M"],["B", "A", "L", "D", "M"],["B", "A", "L", "D", "M"],["B", "A", "L", "D", "M"],["B", "A", "L", "D", "M"]]
        response = self.client.get("/get_word?word=bald")
        self.assertEqual(response.json["result"], 'ok')
        response = self.client.get("/get_word?word=bat")
        self.assertEqual(response.json["result"], 'not-on-board')
        response = self.client.get("/get_word?word=fugly")
        self.assertEqual(response.json["result"], 'not-word')

    def test_score(self):
        with self.client:
            with self.client.session_transaction() as sesh:
                sesh["highscore"] = 10
        response = self.client.post("/score", json={"score":43, "num_words":10})
        response = response.get_json()
        self.assertEqual(response["record"], True)

    def test_done(self):
        with self.client:
            with self.client.session_transaction() as sesh:
                sesh["times_played"] = 0
        response = self.client.post("/done")
        response = response.get_json()
        self.assertEqual(response["times_played"], 1)