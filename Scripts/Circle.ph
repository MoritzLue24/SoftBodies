r = 30
center = pygame.Vector2(300, 300)

self.particles = []
self.springs = []
for i in range(1, 361 ,10):
	self.particles.append(PhysicsEngine.Particle(PhysicsEngine.Utils.getCirclePoint(center, r, i)))

PhysicsEngine.Spring.connectAll(self.particles, self.springs, "DEFAULT")

self.particles.append(PhysicsEngine.Particle(pygame.Vector2(300, 50)))
self.particles[-1].setStatic(True)
self.springs.append(PhysicsEngine.Spring(self.particles[-1], self.particles[0], "DEFAULT"))
