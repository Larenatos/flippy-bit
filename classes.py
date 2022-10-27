from collections import namedtuple
import pygame

Point = namedtuple("Point", "x y")

class Game:
  def __init__(self):
    self.screen = pygame.display.set_mode(size=(550, 840))
    self.rect = pygame.Rect(20, 20, 510, 800)
    self.border_width = 5
    self.play_area_height = 640
    self.border_colour = "#06001a"
    self.bg_colour = "#00334d"
    self.text_colour = "#bfbfbf"
    self.font = pygame.font.SysFont(None, 40)

    self.enemy_size = 50
    self.enemy_font_size = 40

class Missile:
  def __init__(self, vertices, game):
    self.bg_colour = "#06001a"
    self.vertices = vertices
    self.game = game
  
  def draw(self):
    pygame.draw.polygon(self.game.screen, self.bg_colour, self.vertices)
  
  def erase(self):
    pygame.draw.polygon(self.game.screen, self.game.bg_colour, self.vertices)

class BinaryBox:
  def __init__(self, position, size, game, missile):
    self.game = game
    self.bg_colour = "#06001a"
    self.border_colour = "#666666"
    self.text_colour = "#bfbfbf"
    self.current_bit = "0"
    self.missile = missile

    internal_box_size = size - 2 * game.border_width
    self.border_rect = pygame.Rect(position, (size,)*2)
    self.background_rect = pygame.Rect((0, 0), (internal_box_size,)*2)
    self.background_rect.center = self.border_rect.center
    self.font = pygame.font.SysFont(None, 40)
    self.draw_box()

  def draw_box(self):
    pygame.draw.rect(self.game.screen, self.border_colour, self.border_rect, self.game.border_width)
    pygame.draw.rect(self.game.screen, self.bg_colour, self.background_rect)
    
    binary_box_text = self.font.render(self.current_bit, True, self.text_colour)
    binary_box_text_rect = binary_box_text.get_rect()
    binary_box_text_rect.center = self.background_rect.center
    self.game.screen.blit(binary_box_text, binary_box_text_rect)
  
  def flip_bit(self):
    if self.current_bit == "0":
      self.current_bit = "1"
      self.missile.draw()
    else:
      self.current_bit = "0"
      self.missile.erase()
    self.bg_colour, self.text_colour = self.text_colour, self.bg_colour
    self.draw_box()

class HexadecimalDisplay:
  def __init__(self, game, font_size, hexadecimals, position, size):
    self.game = game
    self.background_rect = pygame.Rect(position, (size,)*2)
    self.bg_colour = "#06001a"
    self.text_colour = "#bfbfbf"
    self.current_hexadecimals = hexadecimals
    self.font = pygame.font.SysFont(None, font_size)

  def draw_display(self):
    pygame.draw.rect(self.game.screen, self.bg_colour, self.background_rect)
    display_text = self.font.render(self.current_hexadecimals, True, self.text_colour)
    display_text_rect = display_text.get_rect()
    display_text_rect.center = self.background_rect.center
    self.game.screen.blit(display_text, display_text_rect)
  
class Preview(HexadecimalDisplay):
  def __init__(self, position, size, font_size, hexadecimals, game):
    HexadecimalDisplay.__init__(self, game, font_size, hexadecimals, position, size,)
    self.draw_display()

  def update_display(self, binary_boxes):
    binary = "".join(binary_box.current_bit for binary_box in binary_boxes)
    self.current_hexadecimals =  f"{int(binary, 2):X}"
    self.draw_display()

class Enemy(HexadecimalDisplay):
  def __init__(self, position, size, font_size, hexadecimals, game):
    HexadecimalDisplay.__init__(self, game, font_size, hexadecimals, (0, 0), size)
    self.size = size
    self.border_colour = "#850020"
    self.border_width = 5
    self.is_destroyed = False
    self.border_rect = pygame.Rect(position, (self.size,)*2)
  
  def draw(self):
    self.background_rect.center = self.border_rect.center
    self.draw_display()
    pygame.draw.rect(self.game.screen, self.border_colour, self.border_rect, self.border_width)
  
  def update_position(self):
    # checking if the enemy has reached the bottom
    pygame.draw.rect(self.game.screen, self.game.bg_colour, self.border_rect)
    if self.border_rect.y in range(self.game.rect.y, self.game.play_area_height - 50 - self.size):
      self.border_rect.y += 1
      self.draw()
    else:
      self.is_destroyed = True

class Display():
  def __init__(self, text, position, size, game):
    self.text = text
    self.game = game
    self.border_colour = "#666666"
    self.bg_colour = "#06001a"
    self.text_colour = "#bfbfbf"
    self.border_width = 5
    self.border_rect = pygame.Rect(position, (size,)*2)
    self.font = pygame.font.SysFont(None, 20)
  
  def draw(self):
    pygame.draw.rect(self.game.screen, self.bg_colour, self.border_rect)
    pygame.draw.rect(self.game.screen, self.border_colour, self.border_rect, self.border_width)
    if type(self.text) == int:
      display_text = self.font.render(str(self.text), True, self.text_colour)
    else:
      display_text = self.font.render(self.text, True, self.text_colour)
    display_text_rect = display_text.get_rect()
    display_text_rect.center = self.border_rect.center
    self.game.screen.blit(display_text, display_text_rect)
  
  def update(self):
    if type(self.text) == int:
      self.text += 1
    self.draw()