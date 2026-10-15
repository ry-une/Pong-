"""Exercise the real event handlers with a display-free simplegui adapter."""
import runpy
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch


class Surface:
    def __getattr__(self, name):
        return lambda *args: None


class PongTests(unittest.TestCase):
    def setUp(self):
        self.keys = {"w": 87, "s": 83, "up": 38, "down": 40}
        gui = types.SimpleNamespace(KEY_MAP=self.keys, create_frame=lambda *args: Surface())
        with patch.dict(sys.modules, {"simplegui": gui}):
            loaded = runpy.run_path(str(Path(__file__).resolve().parents[1] / "PongPong"))
        self.game = loaded["draw"].__globals__
        self.canvas = Surface()

    def press(self, key):
        self.game["keydown"](self.keys[key])

    def release(self, key):
        self.game["keyup"](self.keys[key])

    def tick(self):
        self.game["draw"](self.canvas)

    def test_both_players_move_in_one_frame(self):
        start = self.game["paddle1_pos"]
        self.press("w")
        self.press("down")
        self.tick()
        self.assertEqual(self.game["paddle1_pos"], start - 5)
        self.assertEqual(self.game["paddle2_pos"], start + 5)

    def test_opposite_keys_cancel_then_resume_remaining_direction(self):
        for up, down, velocity in [("w", "s", "paddle1_vel"), ("up", "down", "paddle2_vel")]:
            for released, expected in [(up, 5), (down, -5)]:
                with self.subTest(player=velocity, released=released):
                    self.game["new_game"]()
                    self.press(up)
                    self.press(down)
                    self.assertEqual(self.game[velocity], 0)
                    self.release(released)
                    self.assertEqual(self.game[velocity], expected)

    def test_repeated_keydown_does_not_stick(self):
        self.press("w")
        self.press("w")
        self.release("w")
        self.tick()
        self.assertEqual(self.game["paddle1_pos"], self.game["HEIGHT"] / 2.5)

    def test_reset_clears_scores_and_movement(self):
        self.press("w")
        self.press("down")
        self.game.update(score1=3, score2=4)
        self.tick()
        self.game["new_game"]()
        self.assertEqual((self.game["score1"], self.game["score2"]), (0, 0))
        self.assertEqual((self.game["paddle1_vel"], self.game["paddle2_vel"]), (0, 0))
        self.assertEqual(self.game["ball_pos"], [300, 200])
        self.assertLess(self.game["ball_vel"][0], 0)
        self.tick()
        self.assertEqual((self.game["paddle1_pos"], self.game["paddle2_pos"]), (160, 160))
        self.release("w")
        self.press("up")
        self.assertEqual(self.game["paddle2_vel"], -5)

    def test_paddles_clamp_at_both_edges(self):
        for up, down, position in [("w", "s", "paddle1_pos"), ("up", "down", "paddle2_pos")]:
            for initial, key, expected in [(0, up, 0), (2, up, 0), (320, down, 320), (318, down, 320)]:
                with self.subTest(position=position, initial=initial):
                    self.game["new_game"]()
                    self.game[position] = initial
                    self.press(key)
                    self.tick()
                    self.assertEqual(self.game[position], expected)

    def test_unrelated_key_release_preserves_movement(self):
        self.press("s")
        self.game["keydown"](999)
        self.game["keyup"](999)
        self.assertEqual(self.game["paddle1_vel"], 5)

    def test_misses_award_correct_player_and_serve_direction(self):
        for x, velocity, scores, sign in [(572, 2, (1, 0), -1), (28, -2, (0, 1), 1)]:
            with self.subTest(x=x):
                self.game["new_game"]()
                self.game.update(ball_pos=[x, 50], ball_vel=[velocity, 0])
                self.tick()
                self.assertEqual((self.game["score1"], self.game["score2"]), scores)
                self.assertGreater(self.game["ball_vel"][0] * sign, 0)

    def test_paddle_hit_reverses_and_accelerates_ball(self):
        self.game.update(ball_pos=[572, 200], ball_vel=[2, 0])
        self.tick()
        self.assertAlmostEqual(self.game["ball_vel"][0], -2.4)
        self.assertEqual((self.game["score1"], self.game["score2"]), (0, 0))


if __name__ == "__main__":
    unittest.main()
