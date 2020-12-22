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
            self.assertIn()

    def test_get_word(self):
        with self.client:
            with self.client.session_transaction() as setSession:
                setSession["board"] = 
                [["B", "A", "L", "D", "M"],
                ["B", "A", "L", "D", "M"],
                ["B", "A", "L", "D", "M"],
                ["B", "A", "L", "D", "M"],
                ["B", "A", "L", "D", "M"]]
            response = self.client.get("/check-word?word=bald")
            self.assertEqual(response.json["result"], 'ok')
            response = self.client.get("/check-word?word=bat")
            self.assertEqual(response.json["result"], 'not-on-board')
            response = self.client.get("/check-word?word=fugly")
            self.assertEqual(response.json["result"], 'not-word')
    def test_score(self):
        response = self.client.post("/score")
    def test_done(self):
        with self.client:
            self.client.
    
