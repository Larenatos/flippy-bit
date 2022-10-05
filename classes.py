from collections import namedtuple
import pygame

Point = namedtuple("Point", "x y")

class Missile:
  def __init__(self, vertices, screen, game_bg_colour):
    self.bg_colour = "#06001a"
    self.vertices = vertices
    self.screen = screen
    self.game_bg_colour = game_bg_colour
  
  def draw(self):
    pygame.draw.polygon(self.screen, self.bg_colour, self.vertices)
  
  def erase(self):
    pygame.draw.polygon(self.screen, self.game_bg_colour, self.vertices)

class BinaryBox:
  def __init__(self, position, size, border_width, screen):
    self.screen = screen
    self.border_width = border_width
    self.bg_colour = "#06001a"
    self.border_colour = "#666666"
    self.text_colour = "#bfbfbf"
    self.current_bit = "0"
    self.missile = None

    internal_box_size = size - 2 * border_width
    self.border_rect = pygame.Rect(position, (size,)*2)
    self.background_rect = pygame.Rect((0, 0), (internal_box_size,)*2)
    self.background_rect.center = self.border_rect.center
    self.font = pygame.font.SysFont(None, 40)
    self.draw_box()

  def draw_box(self):
    pygame.draw.rect(self.screen, self.border_colour, self.border_rect, self.border_width)
    pygame.draw.rect(self.screen, self.bg_colour, self.background_rect)
    
    binary_box_text = self.font.render(self.current_bit, True, self.text_colour)
    binary_box_text_rect = binary_box_text.get_rect()
    binary_box_text_rect.center = self.background_rect.center
    self.screen.blit(binary_box_text, binary_box_text_rect)
    if self.current_bit == "1":
      self.missile.draw()
  
  def flip_bit(self):
    if self.current_bit == "0":
      self.current_bit = "1"
      self.missile.draw()
    else:
      self.current_bit = "0"
      self.missile.erase()
    self.bg_colour, self.text_colour = self.text_colour, self.bg_colour
    self.draw_box()

  def set_missile(self, missile):
    self.missile = missile

  def get_current_bit(self):
    return self.current_bit

class HexadecimalDisplay:
  def __init__(self, size, font_size, hexadecimals, screen):
    self.screen = screen
    self.bg_colour = "#06001a"
    self.text_colour = "#bfbfbf"
    self.current_hexadecimals = hexadecimals
    self.size = size
    self.font = pygame.font.SysFont(None, font_size)

  def draw_display(self):
    pygame.draw.rect(self.screen, self.bg_colour, self.background_rect)
    display_text = self.font.render(self.current_hexadecimals, True, self.text_colour)
    display_text_rect = display_text.get_rect()
    display_text_rect.center = self.background_rect.center
    self.screen.blit(display_text, display_text_rect)
  
class Preview(HexadecimalDisplay):
  def __init__(self, position, size, font_size, hexadecimals, screen):
    HexadecimalDisplay.__init__(self, size, font_size, hexadecimals, screen)
    self.background_rect = pygame.Rect(position, (size,)*2)
    self.draw_display()

  def update_display(self, binary_boxes):
    binary = "".join(binary_box.get_current_bit() for binary_box in binary_boxes)
    self.current_hexadecimals =  f"{int(binary, 2):X}"
    self.draw_display()

class Enemy(HexadecimalDisplay):
  def __init__(self, position, size, font_size, hexadecimals, screen):
    HexadecimalDisplay.__init__(self, size, font_size, hexadecimals, screen)
    self.screen
    self.position = position
    self.border_colour = "#850020"
    self.border_width = 5
    self.is_destroyed = False
  
  def draw(self):
    self.border_rect = pygame.Rect(self.position, (self.size,)*2)
    self.background_rect = pygame.Rect((0, 0), (self.size,)*2)
    self.background_rect.center = self.border_rect.center
    self.draw_display()
    pygame.draw.rect(self.screen, self.border_colour, self.border_rect, self.border_width)
  
  def update_position(self, game_position_y, play_area_height):
    # checking if the enemy has reached the bottom
    if self.position.y in range(game_position_y, play_area_height - 50 - self.size):
      self.position = Point(self.position.x, self.position.y + 1)
      self.draw()
    else:
      self.is_destroyed = True