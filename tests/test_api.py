import unittest
from tictactoe import create_app


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app({"TESTING": True, "SECRET_KEY": "test-only"})
        self.client = self.app.test_client()
        state = self.client.get("/api/game").get_json()
        self.headers = {"X-CSRF-Token": state["csrf_token"]}

    def post(self, url, body):
        return self.client.post(url, json=body, headers=self.headers)

    def test_move_and_persistence(self):
        response = self.post("/api/move", {"index": 0})
        self.assertEqual(response.status_code, 200)
        state = response.get_json()
        self.assertEqual(state["board"].count("X"), 1)
        self.assertEqual(state["board"].count("O"), 1)
        self.assertEqual(self.client.get("/api/game").get_json()["board"], state["board"])
        self.assertGreater(state["stats"]["nodes"], 0)

    def test_play_as_o(self):
        state = self.post("/api/new", {"human": "O"}).get_json()
        self.assertEqual(state["board"][4], "X")
        self.assertEqual(state["human"], "O")

    def test_bad_payloads_and_moves(self):
        for payload in [[], {}, {"index": True}, {"index": 9}, {"index": "0"}]:
            self.assertEqual(self.post("/api/move", payload).status_code, 400)
        self.post("/api/move", {"index": 0})
        before = self.client.get("/api/game").get_json()["board"]
        self.assertEqual(self.post("/api/move", {"index": 0}).status_code, 400)
        self.assertEqual(self.client.get("/api/game").get_json()["board"], before)
        self.assertEqual(self.post("/api/new", {"human": "Z"}).status_code, 400)
        self.assertEqual(self.post("/api/new", {"reset_scores": "yes"}).status_code, 400)

    def test_csrf_and_isolated_sessions(self):
        self.assertEqual(self.client.post("/api/move", json={"index": 0}).status_code, 403)
        self.post("/api/move", {"index": 0})
        other = self.app.test_client()
        self.assertEqual(other.get("/api/game").get_json()["board"], [""] * 9)

    def test_terminal_game_scores_once(self):
        with self.client.session_transaction() as session:
            game = session["game"]
            game["board"] = ["X", "X", "", "O", "O", "", "", "", ""]
            session["game"] = game
        state = self.post("/api/move", {"index": 2}).get_json()
        self.assertEqual(state["result"], "X")
        self.assertEqual(state["scores"]["human"], 1)
        self.assertEqual(self.post("/api/move", {"index": 6}).status_code, 400)
        state = self.post("/api/new", {"human": "X"}).get_json()
        self.assertEqual(state["scores"]["human"], 1)
        state = self.post("/api/new", {"reset_scores": True}).get_json()
        self.assertEqual(sum(state["scores"].values()), 0)

    def test_request_size_and_cache(self):
        self.assertEqual(self.post("/api/move", {"padding": "x" * 5000}).status_code, 413)
        self.assertEqual(self.client.get("/api/game").headers["Cache-Control"], "no-store")
