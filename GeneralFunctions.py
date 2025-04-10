import pygame
import threading
from pygame import mixer

pygame.init()
mixer.init()


def sound_effect(file, volume):
    sound = mixer.Sound(file)
    sound.set_volume(volume)
    sound.play()


class Button:
    def __init__(self, cor, color, text, text_color, font):
        self.x, self.y = cor
        self.font = font
        self.text_surface = self.font.render(text, True, text_color)
        self.x_size = self.text_surface.get_width() + 20
        self.y_size = self.text_surface.get_height() + 20
        self.surface = pygame.surface.Surface((self.x_size, self.y_size))
        self.surface.fill(color)
        self.text_x = (self.x_size - self.text_surface.get_width()) // 2
        self.text_y = (self.y_size - self.text_surface.get_height()) // 2
        self.rect = pygame.Rect(self.x - (self.x_size / 2), self.y - (self.y_size / 2), self.x_size, self.y_size)

        self.shadow_offset = 5
        self.shadow_surface = pygame.surface.Surface((self.x_size, self.y_size))
        self.shadow_surface.fill((0, 0, 0))
        self.shadow_surface.set_alpha(100)
        self.shadow_text_surface = self.font.render(text, True, (0, 0, 0))
        self.shadow_text_x = ((self.x_size - self.shadow_text_surface.get_width()) // 2) + self.shadow_offset
        self.shadow_text_y = ((self.y_size - self.shadow_text_surface.get_height()) // 2) + self.shadow_offset
        self.shown = False

    def draw(self, display):
        display.blit(self.shadow_surface,
                     (self.x - (self.x_size / 2) + self.shadow_offset, self.y - (self.y_size / 2) + self.shadow_offset))
        display.blit(self.surface, (self.x - (self.x_size / 2), self.y - (self.y_size / 2)))
        display.blit(self.shadow_text_surface,
                     (self.x - (self.x_size / 2) + self.shadow_text_x, self.y - (self.y_size / 2) + self.shadow_text_y))
        display.blit(self.text_surface,
                     (self.x - (self.x_size / 2) + self.text_x, self.y - (self.y_size / 2) + self.text_y))
        self.shown = True

    def hide(self):
        self.shown = False

    def press_check(self, event, volume):
        if self.shown:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    sound_effect('Images_Sounds/ButtonSound1.mp3', volume)
                    return True
            return False


class ImageButton(pygame.sprite.Sprite):
    def __init__(self, image, cor, x_size, group):
        super().__init__()
        self.image = pygame.image.load(image)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.image = pygame.transform.scale(self.image, (x_size, int(self.height / (self.width / x_size))))
        self.x, self.y = cor
        self.x_size = x_size
        self.y_size = int(self.height / (self.width / x_size))
        self.rect = pygame.Rect(self.x - (self.x_size / 2), self.y - (self.y_size / 2), self.x_size, self.y_size)
        self.image_name = image

        group.add(self)

    def draw(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y))

    def press_check(self, event, volume):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                sound_effect('Images_Sounds/ButtonSound1.mp3', volume)
                self.image.set_alpha(200)
                timer = threading.Timer(0.5, self.reset_alpha)
                timer.daemon = True
                timer.start()
                return True
        return False

    def reset_alpha(self):
        self.image.set_alpha(255)


pygame.quit()
