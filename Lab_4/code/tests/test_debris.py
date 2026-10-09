import os
import unittest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame

from game.game_engine import GameEngine


class DebrisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()

    def make_game(self):
        return GameEngine(800, 600)

    def test_partial_trim_spawns_debris_for_both_cut_sides(self):
        game = self.make_game()
        top = game.stack[-1]
        game.active_block.x = top.x - 12
        game.active_block.width = top.width + 24
        game.active_block.y = 150
        top.y = 182

        game.drop_block()

        self.assertEqual([piece.width for piece in game.debris], [12, 12])
        self.assertEqual(game.stack[-1].width, top.width)
        self.assertEqual(game.score, 1)
        self.assertEqual([piece.y for piece in game.debris], [182, 182])

    def test_debris_falls_rotates_and_expires(self):
        game = self.make_game()
        top = game.stack[-1]
        game.active_block.x = top.x + 12
        game.drop_block()
        piece = game.debris[0]
        initial_y = piece.y

        game.update()

        self.assertGreater(piece.y, initial_y)
        self.assertNotEqual(piece.rotation, 0)
        piece.render(pygame.Surface((800, 600)))
        for _ in range(piece.lifetime_frames):
            game.update()
        self.assertEqual(game.debris, [])

    def test_reset_clears_active_debris_and_restores_base(self):
        game = self.make_game()
        top = game.stack[-1]
        game.active_block.x = top.x + 12
        game.drop_block()
        self.assertTrue(game.debris)

        game.reset()

        self.assertEqual(game.debris, [])
        self.assertEqual(len(game.stack), 1)
        self.assertEqual(game.stack[0].width, game.base_width)

    def test_perfect_drop_and_complete_miss_do_not_spawn_debris(self):
        game = self.make_game()
        top = game.stack[-1]
        game.active_block.x = top.x
        game.drop_block()

        self.assertEqual(game.debris, [])
        self.assertEqual(game.stack[-1].width, top.width)
        self.assertEqual(game.score, 1 + game.perfect_bonus)
        self.assertEqual(game.consecutive_perfects, 1)

        top = game.stack[-1]
        game.active_block.x = top.x + top.width + 1
        game.drop_block()

        self.assertTrue(game.game_over)
        self.assertEqual(game.debris, [])

    def test_task_two_streak_restoration_and_imperfect_reset_remain_intact(self):
        game = self.make_game()
        top = game.stack[-1]
        game.active_block.x = top.x + 10
        game.drop_block()
        self.assertEqual(game.stack[-1].width, top.width - 10)

        for _ in range(3):
            game.active_block.x = game.stack[-1].x
            game.drop_block()

        self.assertEqual(game.stack[-1].width, top.width - 2)
        self.assertEqual(game.score, 1 + 3 * (1 + game.perfect_bonus))
        self.assertEqual(game.consecutive_perfects, 3)

        top = game.stack[-1]
        game.active_block.x = top.x + 10
        game.drop_block()

        self.assertEqual(game.consecutive_perfects, 0)
        self.assertEqual(game.stack[-1].width, top.width - 10)

    def test_task_four_background_tracks_height_and_resets(self):
        game = self.make_game()
        screen = pygame.Surface((800, 600))
        game.render(screen)
        initial_pixel = screen.get_at((5, 300))[:3]

        for _ in range(12):
            game.active_block.x = game.stack[-1].x
            game.drop_block()

        game.render(screen)
        taller_tower_pixel = screen.get_at((5, 300))[:3]
        self.assertNotEqual(taller_tower_pixel, initial_pixel)

        game.reset()
        game.render(screen)
        self.assertEqual(screen.get_at((5, 300))[:3], initial_pixel)


if __name__ == "__main__":
    unittest.main()