from .Utils import *
from .Particle import Particle


class Spring:
    SPRING_COL = pygame.Color(243, 181, 129)
    DEFAULT_SPRING_FORCE = 0.00075
    def __init__(self, a: Particle, b: Particle, length: float, k: float=DEFAULT_SPRING_FORCE):
        self.a = a
        self.b = b
        if length == "DEFAULT":
            self.length = Utils.getLineLength(a.position, b.position)
        else:
            self.length = length
        self.k = k

    def update(self):
        f = self.a.position - self.b.position
        x = f.magnitude() - self.length
        f.normalize()

        f *= self.k * x
        self.b.applyForce(f)
        f *= -1
        self.a.applyForce(f)

    def draw(self, surface: pygame.Surface):
        pygame.draw.line(surface, self.SPRING_COL, self.a.position, self.b.position, 4)

    @staticmethod
    def connectAll(particles: list, springs: list, length, k: float=0.00075):
        """
        for i in range(len(particles)):
            if i < len(particles)-1:
                if length == "DEFAULT":
                    restLength = Utils.getLineLength(particles[i].position, particles[i + 1].position)
                    springs.append(Spring(particles[i], particles[i + 1], restLength, k))
                else:
                    springs.append(Spring(particles[i], particles[i+1], length, k))
        """

        for i in range(len(particles)):
            for j in range(len(particles)):
                if i != j:
                    if length == "DEFAULT":
                        restLength = Utils.getLineLength(particles[i].position, particles[j].position)
                        springs.append(Spring(particles[i], particles[j], restLength, k))
                    else:
                        springs.append(Spring(particles[i], particles[j], length, k))
