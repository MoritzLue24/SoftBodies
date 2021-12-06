import numpy as np

self.particles = []
self.springs = []

rectW = 8
rectH = 5

xOffset = 100
yOffset = 200
dist = 30

for i in range(rectH):
    for j in range(rectW):
        self.particles.append(PhysicsEngine.Particle(pygame.Vector2(xOffset + j*dist, yOffset + i*dist)))

particles = np.array(self.particles)
particles2d = np.reshape(particles,(-1,8))

k = 0.01

for i in range(len(particles2d)):
    for j in range(len(particles2d[0])):
        pMid = particles2d[i][j]

        if (j == rectW-1) and (i > 0) and (i < rectH-1):
            self.springs.append(PhysicsEngine.Spring(pMid, particles2d[i-1][j], "DEFAULT", k))
            self.springs.append(PhysicsEngine.Spring(pMid, particles2d[i+1][j], "DEFAULT", k))

        if (j == 0) and (i > 0) and (i < rectH-1):
            self.springs.append(PhysicsEngine.Spring(pMid, particles2d[i-1][j], "DEFAULT", k))
            self.springs.append(PhysicsEngine.Spring(pMid, particles2d[i+1][j], "DEFAULT", k))

        if (i == 0) and (j < rectW-1):
            self.springs.append(PhysicsEngine.Spring(pMid, particles2d[i][j+1], "DEFAULT", k))

        if (i == rectH-1) and (j < rectW-1):
            self.springs.append(PhysicsEngine.Spring(pMid, particles2d[i][j+1], "DEFAULT", k))

        if (i != 0) and (i != rectH-1) and (j < rectW-1):
            self.springs.append(PhysicsEngine.Spring(pMid, particles2d[i][j+1], "DEFAULT", k))

            self.springs.append(PhysicsEngine.Spring(pMid, particles2d[i-1][j], "DEFAULT", k))
            self.springs.append(PhysicsEngine.Spring(pMid, particles2d[i+1][j], "DEFAULT", k))

            if (j > 0):
                self.springs.append(PhysicsEngine.Spring(pMid, particles2d[i-1][j-1], "DEFAULT", k))
                self.springs.append(PhysicsEngine.Spring(pMid, particles2d[i-1][j+1], "DEFAULT", k))
                self.springs.append(PhysicsEngine.Spring(pMid, particles2d[i+1][j-1], "DEFAULT", k))
                self.springs.append(PhysicsEngine.Spring(pMid, particles2d[i+1][j+1], "DEFAULT", k))

        if (i != 0) and (i != rectH-1) and (j == 0) and (j < rectW-1):
            self.springs.append(PhysicsEngine.Spring(pMid, particles2d[i-1][j+1], "DEFAULT", k))
            self.springs.append(PhysicsEngine.Spring(pMid, particles2d[i+1][j+1], "DEFAULT", k))

        if (i != 0) and (i != rectH-1) and (j == rectW-1):
            self.springs.append(PhysicsEngine.Spring(pMid, particles2d[i-1][j-1], "DEFAULT", k))
            self.springs.append(PhysicsEngine.Spring(pMid, particles2d[i+1][j-1], "DEFAULT", k))
