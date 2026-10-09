import pygame


class Debris:
    lifetime_frames = 90
    gravity = 0.35

    def __init__(self, x, y, width, height, color, velocity_x, angular_velocity):
        self.x = float(x)
        self.y = float(y)
        self.width = float(width)
        self.height = float(height)
        self.color = color
        self.velocity_x = velocity_x
        self.velocity_y = 0.0
        self.rotation = 0.0
        self.angular_velocity = angular_velocity
        self.age = 0

    def update(self):
        self.x += self.velocity_x
        self.velocity_y += self.gravity
        self.y += self.velocity_y
        self.rotation = (self.rotation + self.angular_velocity) % 360
        self.age += 1
        return self.age < self.lifetime_frames

    def render(self, surface):
        width = max(1, round(self.width))
        height = max(1, round(self.height))
        piece = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(piece, self.color, piece.get_rect(), border_radius=4)
        pygame.draw.rect(piece, (245, 245, 250), piece.get_rect(), width=2, border_radius=4)
        rotated = pygame.transform.rotate(piece, self.rotation)
        rect = rotated.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
        surface.blit(rotated, rect)