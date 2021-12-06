import pygame


class Particle:
    PARTICLE_COL = pygame.Color(51, 78, 91)
    STATIC_PARTICLE_COL = pygame.Color(224, 74, 74)
    def __init__(self, position: pygame.Vector2):
        self.acceleration = pygame.Vector2(0, 0)
        self.velocity = pygame.Vector2(0, 0)
        self.position = position
        self.mass = 1
        self._static = False
        self.drawRadius = 8
        self.drawColor = self.PARTICLE_COL

    def setStatic(self, static: bool):
        self._static = static
        self.drawColor = self.STATIC_PARTICLE_COL if static else self.PARTICLE_COL

    def resetColor(self):
        self.drawColor = self.STATIC_PARTICLE_COL if self._static else self.PARTICLE_COL

    def applyForce(self, force: pygame.Vector2):
        if not self._static:
            f = force
            f /= self.mass
            self.acceleration += f

    def update(self):
        if not self._static:
            self.velocity *= 0.99

            self.velocity += self.acceleration
            self.position += self.velocity
            self.acceleration *= 0

    def draw(self, surface: pygame.Surface):
        pygame.draw.circle(surface, self.drawColor, self.position, self.drawRadius)
