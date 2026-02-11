import unittest
from unittest.mock import patch
import main

class TestGame(unittest.TestCase):
    @patch('time.sleep', lambda *a, **k: None)
    def test_choose_handles_invalid_then_valid(self):
        inputs = iter(['x','1'])
        with patch('builtins.input', lambda *a: next(inputs)):
            result = main.choose("Pilih:", ["A","B"])
            self.assertEqual(result, "A")

    @patch('time.sleep', lambda *a, **k: None)
    @patch('random.randint')
    @patch('random.random')
    def test_combat_player_wins(self, mock_random, mock_randint):
        mock_random.return_value = 0.6
        mock_randint.side_effect = [30, 1, 30, 1]
        player = main.Player(name="Test", hp=100, atk=12)
        inputs = iter(['1','1','1','1'])
        with patch('builtins.input', lambda *a: next(inputs)):
            alive = main.combat(player, "Weak", 40, 5)
            self.assertTrue(alive)
            self.assertGreater(player.hp, 0)

if __name__ == '__main__':
    unittest.main()
