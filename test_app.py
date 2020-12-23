from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle 


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!
    def setUp(self):
        """setting up each test""" 
        self.client = app.test_client()
        app.config["TESTING"] = True
        
    def test_index(self):
        with self.client:
            response = self.client.get("/")
            self.assertIsNone(session.get("highscore"))
            self.assertIsNone(session.get("times_played"))
            html = self.client.get_data(as_text=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn("<th>Score</th>", html)

    def test_get_word(self):
        with self.client:
            with self.client.session_transaction() as setSession:
                setSession["board"] = [["B", "A", "L", "D", "M"],["B", "A", "L", "D", "M"],["B", "A", "L", "D", "M"],["B", "A", "L", "D", "M"],["B", "A", "L", "D", "M"]]
            response = self.client.get("/check-word?word=bald")
            self.assertEqual(response.json["result"], 'ok')
            response = self.client.get("/check-word?word=bat")
            self.assertEqual(response.json["result"], 'not-on-board')
            response = self.client.get("/check-word?word=fugly")
            self.assertEqual(response.json["result"], 'not-word')

    def test_score(self):
        with self.client:
            session["highscore"] = 10
            response = self.client.post("/score", data={"score": 43, "num_words": 10})
            self.assertEqual(response.data, True)

    def test_done(self):
        with self.client:
            session["times_played"] = 0
            response = self.client.post("/done")
            self.assertEqual(response.data.times_played, 1)