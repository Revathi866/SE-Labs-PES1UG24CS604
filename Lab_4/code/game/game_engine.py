import random
import pygame
from game.block import Block
from game.debris import Debris


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.block_height = 28
        self.base_width = 180
        self.perfect_tolerance = 8.0
        self.perfect_bonus = 2
        self.perfect_streak_for_restore = 3
        self.width_restore_amount = 8.0

        self.font_title = pygame.font.SysFont(None, 38)
        self.font_hud = pygame.font.SysFont(None, 28)
        self.font_big = pygame.font.SysFont(None, 46)

        self.reset()

    def get_color(self, index):
        palette = [
            (230, 75, 75),   # Crimson
            (240, 140, 45),  # Orange
            (245, 210, 50),  # Gold
            (60, 195, 110),  # Green
            (50, 150, 240),  # Blue
            (165, 80, 225),  # Purple
        ]
        return palette[index % len(palette)]

    def get_background_gradient(self):
        atmosphere = [
            ((24, 27, 36), (45, 63, 77)),
            ((25, 91, 104), (96, 142, 138)),
            ((150, 86, 75), (237, 172, 112)),
        ]
        progress = min((len(self.stack) - 1) / 18, 1.0)
        stage = progress * (len(atmosphere) - 1)
        lower_index = min(int(stage), len(atmosphere) - 2)
        amount = stage - lower_index

        return tuple(
            tuple(
                round(start + (end - start) * amount)
                for start, end in zip(atmosphere[lower_index][color_index], atmosphere[lower_index + 1][color_index])
            )
            for color_index in range(2)
        )

    def render_background(self, screen):
        top_color, bottom_color = self.get_background_gradient()
        for y in range(self.height):
            amount = y / max(1, self.height - 1)
            color = tuple(
                round(top + (bottom - top) * amount)
                for top, bottom in zip(top_color, bottom_color)
            )
            pygame.draw.line(screen, color, (0, y), (self.width, y))

    def reset(self):
        self.score = 0
        self.game_over = False
        self.consecutive_perfects = 0
        self.perfect_message_until = 0
        self.debris = []

        base_x = (self.width - self.base_width) // 2
        base_y = self.height - 60
        base_block = Block(base_x, base_y, self.base_width, self.block_height, self.get_color(0), speed=0)
        self.stack = [base_block]

        self.spawn_active_block()

    def spawn_active_block(self):
        top_block = self.stack[-1]
        next_y = top_block.y - self.block_height - 4
        speed = min(10.0, 4.5 + (len(self.stack) * 0.35))
        color = self.get_color(len(self.stack))

        start_x = 25 if random.choice([True, False]) else self.width - 25 - top_block.width
        self.active_block = Block(start_x, next_y, top_block.width, self.block_height, color, speed=speed)

    def drop_block(self):
        if self.game_over:
            return

        top_block = self.stack[-1]
        act = self.active_block

        left = max(act.x, top_block.x)
        right = min(act.x + act.width, top_block.x + top_block.width)
        overlap = right - left
        
        is_successful_drop = overlap > 0

        if is_successful_drop:
            is_perfect = (
                abs(act.x - top_block.x) <= self.perfect_tolerance
                and abs((act.x + act.width) - (top_block.x + top_block.width)) <= self.perfect_tolerance
            )

            if is_perfect:
                self.consecutive_perfects += 1
                if (
                    self.consecutive_perfects % self.perfect_streak_for_restore == 0
                    and top_block.width < self.base_width
                ):
                    restored_width = min(
                        self.width_restore_amount,
                        self.base_width - top_block.width,
                    )
                    top_block.x -= restored_width / 2
                    top_block.width += restored_width

                new_block = Block(
                    top_block.x,
                    act.y,
                    top_block.width,
                    self.block_height,
                    act.color,
                    speed=0,
                )
                self.score += 1 + self.perfect_bonus
                self.perfect_message_until = pygame.time.get_ticks() + 1000
            else:
                self.consecutive_perfects = 0
                self.perfect_message_until = 0
                trimmed_width = max(10.0, overlap)
                new_block = Block(left, act.y, trimmed_width, self.block_height, act.color, speed=0)
                self.score += 1

                left_cut = top_block.x - act.x
                if left_cut > 0:
                    self.debris.append(
                        Debris(act.x, act.y, left_cut, self.block_height, act.color, -1.8, -6.0)
                    )

                right_cut = act.x + act.width - (top_block.x + top_block.width)
                if right_cut > 0:
                    self.debris.append(
                        Debris(
                            top_block.x + top_block.width,
                            act.y,
                            right_cut,
                            self.block_height,
                            act.color,
                            1.8,
                            6.0,
                        )
                    )

            self.stack.append(new_block)

            if new_block.y < 180:
                shift_amount = self.block_height + 4
                for b in self.stack:
                    b.y += shift_amount
                for piece in self.debris:
                    piece.y += shift_amount

            self.spawn_active_block()
        else:
            self.consecutive_perfects = 0
            self.perfect_message_until = 0
            self.game_over = True

    def handle_event(self, event):
        if self.game_over:
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_r) or \
               (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                self.reset()
            return

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.drop_block()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.drop_block()

    def update(self):
        if not self.game_over:
            self.active_block.update(self.width)
        self.debris = [piece for piece in self.debris if piece.update()]

    def render(self, screen):
        self.render_background(screen)

        title_surf = self.font_title.render("Skyscraper Stack", True, (245, 245, 245))
        screen.blit(title_surf, (self.width // 2 - title_surf.get_width() // 2, 16))

        score_surf = self.font_hud.render(f"Height: {self.score}", True, (255, 220, 80))
        screen.blit(score_surf, (self.width // 2 - score_surf.get_width() // 2, 54))

        if pygame.time.get_ticks() < self.perfect_message_until:
            perfect_surf = self.font_hud.render("PERFECT!", True, (80, 235, 170))
            screen.blit(perfect_surf, (self.width // 2 - perfect_surf.get_width() // 2, 84))

        for b in self.stack:
            b.render(screen)

        for piece in self.debris:
            piece.render(screen)

        if not self.game_over:
            self.active_block.render(screen)

        if self.game_over:
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 195))
            screen.blit(overlay, (0, 0))

            over_surf = self.font_big.render("TOWER COLLAPSED!", True, (240, 75, 75))
            screen.blit(over_surf, (self.width // 2 - over_surf.get_width() // 2, self.height // 2 - 40))

            final_surf = self.font_hud.render(f"Final Height: {self.score}", True, (255, 255, 255))
            screen.blit(final_surf, (self.width // 2 - final_surf.get_width() // 2, self.height // 2 + 10))

            restart_surf = self.font_hud.render("Press [Space] or [R] to Play Again", True, (200, 200, 200))
            screen.blit(restart_surf, (self.width // 2 - restart_surf.get_width() // 2, self.height // 2 + 50))
