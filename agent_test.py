"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest

import isolation
import game_agent
import timeit

from importlib import reload

class IsolationTest(unittest.TestCase):
	"""Unit tests for isolation agents"""

	def setUp(self):
		reload(game_agent)
		self.time_limit = 1500
		self.time_millis = lambda: 1000 * timeit.default_timer()
		self.move_start = self.time_millis()
		self.time_left = lambda : self.time_limit - (self.time_millis() - self.move_start)
		
		self.player1 = game_agent.MinimaxPlayer(score_fn=game_agent.minimax_score).set_name("Player 1")
		self.player2 = game_agent.MinimaxPlayer(score_fn=game_agent.minimax_score).set_name("Player 2")

		self.abPlayer1 = game_agent.AlphaBetaPlayer(score_fn=game_agent.minimax_score, timeout=10).set_name("Player 1")
		self.abPlayer2 = game_agent.AlphaBetaPlayer(score_fn=game_agent.minimax_score, timeout=10).set_name("Player 2")

		self.abPlayerOMS1 = game_agent.AlphaBetaPlayer(search_depth=10, score_fn=game_agent.open_move_score, timeout=10).set_name("Player 1")
		self.abPlayerOMS2 = game_agent.AlphaBetaPlayer(search_depth=10, score_fn=game_agent.open_move_score, timeout=10).set_name("Player 2")

		self.abPlayerRandom1 = game_agent.AlphaBetaPlayer(search_depth=10, score_fn=game_agent.custom_score, timeout=10).set_name("Player 1")
		self.abPlayerRandom2 = game_agent.AlphaBetaPlayer(search_depth=10, score_fn=game_agent.custom_score, timeout=10).set_name("Player 2")

	def test_minimaxPlayer3x3(self):
		# Scenario 1: Player 1 @ (0,0), Player 2 @ (1,1)
		# 3x3 isolation board
		self.game = isolation.Board(self.player1, self.player2, 3, 3)
		# Pre-move players
		self.game = self.game.forecast_move((0,0))
		self.assertTrue(self.game.get_player_location(self.player1) == (0,0))
		self.game = self.game.forecast_move((1,1))
		self.assertTrue(self.game.get_player_location(self.player2) == (1,1))
		# Minimax
		player1Move = self.player1.get_move(self.game, lambda : 100)
		self.assertTrue(player1Move == (1,2) or player1Move == (2,1))
		# Player 1 moves
		self.game = self.game.forecast_move(player1Move)
		self.assertTrue(self.player2 == self.game.active_player)
		print(self.game.is_winner(self.player1))
		# Player2 tries to move
		player2Move = self.player2.get_move(self.game, lambda : 100)
		self.assertTrue(player2Move == (-1,-1))

	def test_minimaxPlayer7x7(self):
		self.game = isolation.Board(self.player1, self.player2, 7, 7)
		self.game.apply_move((2, 3))
		self.game.apply_move((0, 5))
		print(self.game.to_string())
		self.assertTrue(self.player1 == self.game.active_player)
		new_game = self.game.forecast_move((1, 1))
		self.assertTrue(new_game.to_string() != self.game.to_string())
		print("\nOld state:\n{}".format(self.game.to_string()))
		print("\nNew state:\n{}".format(new_game.to_string()))
		winner, history, outcome = self.game.play()
		print("\nWinner: {}\nOutcome: {}".format(winner, outcome))
		print(self.game.to_string())
		print("Move history:\n{!s}".format(history))

	def test_alphabetaPruning(self):
		# 3x3 scenario where Player 2 always wins.
		self.game = isolation.Board(self.abPlayer1, self.abPlayer2, 3, 3)
		# Set up game at a min-level with two branches
		self.assertTrue(self.abPlayer1 == self.game.active_player, msg=self.game.active_player)
		self.game.apply_move((0, 0))
		self.assertTrue(self.abPlayer2 == self.game.active_player, msg=self.game.active_player)
		self.game.apply_move((0, 1))
		self.assertTrue(self.abPlayer1 == self.game.active_player, msg=self.game.active_player)
		self.game.apply_move((1,2))
		self.assertTrue(self.abPlayer2 == self.game.active_player, msg=self.game.active_player)
		# Execute specific move for Player 2 to force pruning of second branch
		new_game = self.game.forecast_move((2,0))
		self.assertTrue(self.abPlayer1 == new_game.active_player, msg=new_game.active_player)
		self.assertTrue(new_game.to_string() != self.game.to_string())
		print("\nOld state:\n{}".format(self.game.to_string()))
		print("\nNew state:\n{}".format(new_game.to_string()))
		winner, history, outcome = new_game.play()
		print("\nWinner: {}\nOutcome: {}".format(winner, outcome))
		print(new_game.to_string())
		print("Move history:\n{!s}".format(history))
		# Game is over before it starts :)
		self.assertFalse(history)

	def test_alphabetaPlayer3x3(self):
		# 3x3 scenario where Player 2 always wins.
		self.game = isolation.Board(self.abPlayer1, self.abPlayer2, 3, 3)
		self.game.apply_move((0, 0))
		self.game.apply_move((0, 1))
		self.assertTrue(self.abPlayer1 == self.game.active_player)
		new_game = self.game.forecast_move((2, 1))
		self.assertTrue(new_game.to_string() != self.game.to_string())
		print("\nOld state:\n{}".format(self.game.to_string()))
		print("\nNew state:\n{}".format(new_game.to_string()))
		winner, history, outcome = new_game.play()
		print("\nWinner: {}\nOutcome: {}".format(winner, outcome))
		print(new_game.to_string())
		print("Move history:\n{!s}".format(history))
		# Player 2 must win by forcing an illegal move
		self.assertTrue(winner == self.abPlayer2)
		self.assertTrue(outcome == "illegal move")

	def test_alphabetaPlayerOMS3x3(self):
		self.game = isolation.Board(self.abPlayerOMS1, self.abPlayerOMS2, 3, 3)
		self.game.apply_move((0, 0))
		self.game.apply_move((0, 1))
		self.assertTrue(self.abPlayerOMS1 == self.game.active_player)
		new_game = self.game.forecast_move((2, 1))
		self.assertTrue(new_game.to_string() != self.game.to_string())
		print("\nOld state:\n{}".format(self.game.to_string()))
		print("\nNew state:\n{}".format(new_game.to_string()))
		winner, history, outcome = new_game.play()
		print("\nWinner: {}\nOutcome: {}".format(winner, outcome))
		print(new_game.to_string())
		print("Move history:\n{!s}".format(history))
		#self.assertTrue(winner == self.abPlayerOMS2)
		self.assertTrue(outcome == "illegal move")

	def test_alphabetaPlayerOMS9x9(self):
		# One of the 9x9 Scenario as per Udacity 
		self.game = isolation.Board(self.abPlayerOMS1, self.abPlayerOMS2, 9, 9)
		self.game.apply_move((1, 2))
		self.game.apply_move((3, 2))
		self.game.apply_move((4, 2))
		self.game.apply_move((5, 2))
		self.game.apply_move((6, 2))
		self.game.apply_move((3, 3))
		self.game.apply_move((4, 3))
		self.game.apply_move((5, 3))
		self.game.apply_move((4, 4))
		self.game.apply_move((5, 4))
		self.game.apply_move((6, 4))
		self.game.apply_move((5, 5))
		self.game.apply_move((6, 5))
		self.game.apply_move((4, 6))
		self.game.apply_move((6, 7))
		self.game.apply_move((2, 5))
		self.game.apply_move((2, 4)) # Player 1
		self.assertTrue(self.abPlayerOMS2 == self.game.active_player)
		new_game = self.game.forecast_move((6, 3))
		new_game.apply_move((0,3))
		new_game.apply_move((0,5))
		new_game.apply_move((5,1))
		self.assertTrue(new_game.to_string() != self.game.to_string())
		print("\nOld state:\n{}".format(self.game.to_string()))
		print("\nNew state:\n{}".format(new_game.to_string()))
		# Player 1
		# Next move
		next_move = self.abPlayerOMS1.get_move(new_game, self.time_left)
		self.assertTrue(next_move == (1,3), msg = next_move)

	def test_alphabetaPlayerRandom3x3(self):
		self.game = isolation.Board(self.abPlayerRandom1, self.abPlayerRandom2, 3, 3)
		self.game.apply_move((0, 0))
		self.game.apply_move((0, 1))
		self.assertTrue(self.abPlayerRandom1 == self.game.active_player)
		new_game = self.game.forecast_move((2, 1))
		self.assertTrue(new_game.to_string() != self.game.to_string())
		print("\nOld state:\n{}".format(self.game.to_string()))
		print("\nNew state:\n{}".format(new_game.to_string()))
		winner, history, outcome = new_game.play()
		print("\nWinner: {}\nOutcome: {}".format(winner, outcome))
		print(new_game.to_string())
		print("Move history:\n{!s}".format(history))
		self.assertTrue(outcome == "illegal move")

if __name__ == '__main__':
	unittest.main()
