import pygame


class Surface(pygame.Surface):
    def __init__(self, position: pygame.Vector2, size: pygame.Vector2):
        self.position = position
        self.size = size
        super().__init__(size)

    def draw(self, screen: pygame.Surface):
        screen.blit(self, self.position)


class InputField:
    instances = []
    def __init__(self, position: pygame.Vector2, font: pygame.font.Font, surface: Surface, size: pygame.Vector2=pygame.Vector2(120, 22)):
        self.position = position
        self.size = size
        self.font = font
        self.surface = surface

        self.text = ""
        self.color_active = pygame.Color(128, 128, 128)
        self.color_passive = pygame.Color(89, 89, 89)
        self.font_color = pygame.Color(255, 255, 255)
        self.active = False
        self.padding = pygame.Vector2(4, 4)

        self.instances.append(self)

    def draw(self, surface: pygame.Surface):
        rect = pygame.Rect(self.position.x, self.position.y, self.size.x, self.size.y)
        pygame.draw.rect(surface, self.color_active if self.active else self.color_passive, rect, border_radius=3)
        text_surf = self.font.render(self.text, True, self.font_color)
        surface.blit(text_surf, (rect.x + self.padding.x, rect.y + self.padding.y))

    def events(self, event: pygame.event):
        rect = pygame.Rect(self.position.x + self.surface.position.x, self.position.y + self.surface.position.y, self.size.x, self.size.y)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if rect.collidepoint(pygame.mouse.get_pos()):
                self.active = not self.active
            else:
                self.active = False

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode


class Button:
    instances = []
    def __init__(self, position: pygame.Vector2, text: str, function, font: pygame.font.Font, surface: Surface, size: pygame.Vector2=pygame.Vector2(240, 40)):
        self.position = position
        self.font = font
        self.surface = surface
        self.size = size
        self.text = text
        self.function = function

        self.color_active = pygame.Color(128, 128, 128)
        self.color_passive = pygame.Color(89, 89, 89)
        self.font_color = pygame.Color(255, 255, 255)
        self.active = False
        self.padding = pygame.Vector2(4, 4)

        self.instances.append(self)

    def draw(self, surface: pygame.Surface):
        rect = pygame.Rect(self.position.x, self.position.y, self.size.x, self.size.y)
        pygame.draw.rect(surface, self.color_active if self.active else self.color_passive, rect, border_radius=3)
        text_surf = self.font.render(self.text, True, self.font_color)
        surface.blit(text_surf, (rect.x + self.padding.x, rect.y + self.padding.y))

    def events(self, event: pygame.event):
        rect = pygame.Rect(self.position.x + self.surface.position.x, self.position.y + self.surface.position.y, self.size.x, self.size.y)
        if rect.collidepoint(pygame.mouse.get_pos()):
            self.active = True
            if (event.type == pygame.MOUSEBUTTONDOWN) and (pygame.mouse.get_pressed(3)[0]):
                self.function()
        else:
            self.active = False
