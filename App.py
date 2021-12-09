import os
import tkinter as tk
import tkinter.filedialog
import traceback
import sys
import pygame
import PhysicsEngine


class App:
    def __init__(self, width: int, height: int):
        pygame.init()

        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 15, bold=False)

        self.propertiesWidth = 300
        self.propertiesSurf = PhysicsEngine.Surface(pygame.Vector2(self.width - self.propertiesWidth, 0),
                                                    pygame.Vector2(self.propertiesWidth, height))
        self.mainSurf = PhysicsEngine.Surface(pygame.Vector2(0, 0),
                                              pygame.Vector2(width - self.propertiesWidth, height))

        self.particles = []
        self.springs = []

        self.particle_grabbed = None
        self.tools = ["create_particle", "create_spring", "edit", "delete"]
        self.selected_particles = []
        self.paused = False

        self.restLengthLabel = self.font.render("Rest Length", True, (255, 255, 255))
        self.restLengthInput = PhysicsEngine.InputField(pygame.Vector2(self.propertiesWidth // 2 + 15, 10), self.font,
                                                        self.propertiesSurf)
        self.restLengthInput.text = "DEFAULT"

        self.gravityLabel = self.font.render("Gravity", True, (255, 255, 255))
        self.gravityInput = PhysicsEngine.InputField(pygame.Vector2(self.propertiesWidth // 2 + 15, 45), self.font,
                                                     self.propertiesSurf)
        self.gravityInput.text = f"{PhysicsEngine.Physics.gravity.x}, {PhysicsEngine.Physics.gravity.y}"

        self.springForceLabel = self.font.render("Spring Force", True, (255, 255, 255))
        self.springForceInput = PhysicsEngine.InputField(pygame.Vector2(self.propertiesWidth // 2 + 15, 80), self.font,
                                                         self.propertiesSurf)
        self.springForceInput.text = str(PhysicsEngine.Spring.DEFAULT_SPRING_FORCE)

        self.scriptFilePath = ""
        self.reloadScriptInput = PhysicsEngine.Button(pygame.Vector2(30, self.height - 170), "Reload Script",
                                                      lambda: self.runFileScript(True), self.font, self.propertiesSurf)
        self.reloadScriptInput.padding = pygame.Vector2(75, 12)
        self.loadScriptInput = PhysicsEngine.Button(pygame.Vector2(30, self.height - 70), "Load Script",
                                                    self.runFileScript, self.font, self.propertiesSurf)
        self.loadScriptInput.padding = pygame.Vector2(75, 12)

    def runFileScript(self, reload: bool = False):
        if (self.scriptFilePath == "") and reload:
            print("Cant reload script if script was never loaded.")
            return

        if not reload:
            root = tk.Tk()
            root.withdraw()
            self.scriptFilePath = tk.filedialog.askopenfilename()

            if not self.scriptFilePath.endswith(".ph"):
                print("Invalid file format.")
                return

        with open(self.scriptFilePath, "r") as f:
            raw = f.read()
        try:
            exec(raw)
        except Exception as err:
            detail = err.args[0]
            cl, exc, tb = sys.exc_info()
            bs = "\\"
            print(
                f"[{self.scriptFilePath.replace(os.getcwd().replace(bs, '/'), '')}, Line {traceback.extract_tb(tb)[-1][1]}]: {detail}")

    def draw(self):
        self.mainSurf.fill((243, 236, 176))
        self.propertiesSurf.fill((50, 50, 50))

        # Draw particles and springs
        for particle in self.selected_particles:
            particle.drawColor = pygame.Color(83, 151, 145)
        for spring in self.springs:
            spring.draw(self.mainSurf)
        for particle in self.particles:
            particle.draw(self.mainSurf)

        # Draw lines for the properties window
        pygame.draw.line(self.propertiesSurf, (100, 100, 100),
                         (self.propertiesWidth // 2, 0), (self.propertiesWidth // 2, self.height - 200), 5)
        pygame.draw.line(self.propertiesSurf, (100, 100, 100),
                         (0, self.height - 200), (self.propertiesWidth, self.height - 200), 5)
        pygame.draw.line(self.propertiesSurf, (100, 100, 100),
                         (0, self.height - 100), (self.propertiesWidth, self.height - 100), 5)

        # Draw all buttons and Input fields
        for inst in PhysicsEngine.InputField.instances: inst.draw(self.propertiesSurf)
        for inst in PhysicsEngine.Button.instances: inst.draw(self.propertiesSurf)

        # Draw labels
        self.propertiesSurf.blit(self.restLengthLabel, (10, 13))
        self.propertiesSurf.blit(self.gravityLabel, (10, 47))
        self.propertiesSurf.blit(self.springForceLabel, (10, 81))

    def update(self):
        mousePos = pygame.Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        pygame.display.set_caption(f"Current tool: {self.tools[0]}, Paused: {self.paused}")

        # Set gravity to the gravity input from properties window
        if len(self.gravityInput.text.split(", ")) == 2:
            try:
                PhysicsEngine.Physics.gravity = pygame.Vector2(
                    float(self.gravityInput.text.split(", ")[0]),
                    float(self.gravityInput.text.split(", ")[1]))
            except ValueError:
                pass

        # Set the spring force to the spring force input from properties window
        if len(self.springForceInput.text) != 0:
            try:
                PhysicsEngine.Spring.DEFAULT_SPRING_FORCE = float(self.springForceInput.text)
                for spring in self.springs:
                    spring.k = PhysicsEngine.Spring.DEFAULT_SPRING_FORCE
            except ValueError:
                pass

        # Set the particle_grabbed position to mousePos and velocity to none if the particle is not static.
        if self.particle_grabbed is not None:
            self.particle_grabbed.position = mousePos
            self.particle_grabbed.velocity = pygame.Vector2(0, 0)
            self.particle_grabbed.acceleration = pygame.Vector2(0, 0)

        # Reset selected particles when not creating a spring.
        if self.tools[0] != "create_spring":
            self.selected_particles = []

        # If two particles are selected, create a spring and reset the selected particles.
        if len(self.selected_particles) == 2:
            try:
                if self.restLengthInput.text == "DEFAULT":
                    restLength = PhysicsEngine.Utils.getLineLength(self.selected_particles[0].position,
                                                                   self.selected_particles[1].position)
                    self.springs.append(PhysicsEngine.Spring(
                        self.selected_particles[0], self.selected_particles[1], restLength))
                else:
                    self.springs.append(PhysicsEngine.Spring(
                        self.selected_particles[0], self.selected_particles[1],
                        int(self.restLengthInput.text)))
            except ValueError:
                restLength = PhysicsEngine.Utils.getLineLength(self.selected_particles[0].position,
                                                               self.selected_particles[1].position)
                self.springs.append(PhysicsEngine.Spring(
                    self.selected_particles[0], self.selected_particles[1], restLength))

            for p in self.selected_particles:
                p.resetColor()
            self.selected_particles = []

        # Update particles and springs
        if not self.paused:
            for particle in self.particles:
                particle.update()
                particle.applyForce(PhysicsEngine.Physics.gravity)
            for spring in self.springs:
                spring.update()

    def events(self, event: pygame.event):
        mousePos = pygame.Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

        for inst in PhysicsEngine.InputField.instances: inst.events(event)
        for inst in PhysicsEngine.Button.instances: inst.events(event)
        if any(x.active for x in PhysicsEngine.InputField.instances):
            return

        if event.type == pygame.KEYDOWN:
            # Switching tools.
            if event.key == pygame.K_TAB:
                self.tools.append(self.tools.pop(0))
            # Pausing / Resuming the app
            elif event.key == pygame.K_ESCAPE:
                self.paused = not self.paused
            # Resetting all particles and springs when backspace is pressed
            elif event.key == pygame.K_BACKSPACE:
                self.springs = []
                self.particles = []

        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed(3)[0]:
                # Set the particle_grabbed to the particle the mouse is pointing to.
                if self.tools[0] == "edit":
                    for particle in self.particles:
                        if PhysicsEngine.Utils.pointOnCircle(particle.position, mousePos, 40):
                            self.particle_grabbed = particle

                elif self.tools[0] == "create_particle":
                    self.particles.append(PhysicsEngine.Particle(mousePos))

                # Append selected particles with the particle the mouse is pointing to.
                elif self.tools[0] == "create_spring":
                    for particle in self.particles:
                        if PhysicsEngine.Utils.pointOnCircle(particle.position, mousePos, particle.drawRadius):
                            if particle not in self.selected_particles:
                                self.selected_particles.append(particle)

            if pygame.mouse.get_pressed(3)[2]:
                # Create static particle if right click is pressed and current tool is create_particle.
                if self.tools[0] == "create_particle":
                    p = PhysicsEngine.Particle(mousePos)
                    p.setStatic(True)
                    self.particles.append(p)

        if event.type == pygame.MOUSEBUTTONUP:
            # Set the particle_grabbed to none if the mouse button is released.
            if self.particle_grabbed is not None:
                self.particle_grabbed = None

        if pygame.mouse.get_pressed(3)[0]:
            # Remove selected particle and its adjacent springs
            if self.tools[0] == "delete":
                for particle in self.particles:
                    if PhysicsEngine.Utils.pointOnCircle(particle.position, mousePos, particle.drawRadius):
                        for spring in self.springs:
                            if (spring.a == particle) or (spring.b == particle):
                                self.springs.remove(spring)
                        self.particles.remove(particle)

        if pygame.mouse.get_pressed(3)[2]:
            # Remove the selected spring when mouse button 2 is pressed.
            if self.tools[0] == "delete":
                for spring in self.springs:
                    if PhysicsEngine.Utils.pointOnLine(spring.a.position, spring.b.position, mousePos, 0.1):
                        self.springs.remove(spring)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    os._exit(0)
                self.events(event)

            self.draw()
            self.update()

            self.mainSurf.draw(self.screen)
            self.propertiesSurf.draw(self.screen)

            # Update pygame.
            pygame.display.update()
            self.clock.tick(60)


if __name__ == '__main__':
    app = App(1200, 800)
    app.run()
