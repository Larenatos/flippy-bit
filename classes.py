from collections import namedtuple
from functools import reduce
from math import ceil
import pygame

Point = namedtuple("Point", "x y")
Triangle = namedtuple("Triangle", "left right top")

class Game:
  def __init__(self):
    self.screen = pygame.display.set_mode(size=(550, 840))
    self.rect = pygame.Rect(20, 20, 510, 800)
    self.border_width = 5
    self.play_area_height = 640
    self.border_colour = "#06001a"
    self.bg_colour = "#00334d"

    self.enemy_size = 50
    self.enemy_font_size = 40

    self.alive_enemies = []

class Missile:
  def __init__(self, vertices, game):
    self.bg_colour = "#06001a"
    self.vertices = vertices
    self.game = game
    self.target = None

  def draw(self):
    pygame.draw.polygon(self.game.screen, self.bg_colour, self.vertices)

  def erase(self):
    pygame.draw.polygon(self.game.screen, self.game.bg_colour, self.vertices)

  def step_shoot_animation(self):
    step = -ceil((0.01 * self.vertices.top.y - 8)**2)
    self.move(y=step)

  def move(self, x=0, y=0):
    self.erase()
    self.vertices = Triangle(*(Point(vertex.x + x, vertex.y + y) for vertex in self.vertices))
    self.draw()
  
  def has_collided(self):
    if pygame.Rect.collidepoint(self.target.border_rect, self.vertices.top):
        self.erase()
        self.target.destroy()
        return True
    return False

class MissileMerger:
  def __init__(self, missiles, target):
    self.final_missile = None
    self.missiles = missiles
    self.destination = target.border_rect.centerx
    self.target = target
    self.done = False
  
  def step_animation(self):
    remaining_missiles = []
    for missile in self.missiles:
      vertices = missile.vertices

      distance = self.destination - vertices.top.x

      if -2 < distance < 2:
        missile.move(x=distance)
        if not self.final_missile:
          missile.target = self.target
          self.final_missile = missile
        continue

      step = ceil((0.01 * abs(distance) + 1)**2)
      if distance < 0: step = -step
      missile.move(x=step)

      remaining_missiles.append(missile)
    
    if not remaining_missiles:
      self.missiles = [self.missiles[0]]
      self.done = True
    else:
      self.missiles = remaining_missiles
      
  def get_final_missile(self):
    missile = self.missiles[0]
    missile.target = self.target
    return missile

  def remove(self):
    for missile in self.missiles:
      missile.erase()
    if self.final_missile:
      self.final_missile.erase()

class BinaryBox:
  def __init__(self, position, size, game, missile):
    self.game = game
    self.bg_colour = "#06001a"
    self.border_colour = "#666666"
    self.text_colour = "#bfbfbf"
    self.current_bit = False
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
    
    current_bit = "1" if self.current_bit else "0"

    binary_box_text = self.font.render(current_bit, True, self.text_colour)
    binary_box_text_rect = binary_box_text.get_rect()
    binary_box_text_rect.center = self.background_rect.center
    self.game.screen.blit(binary_box_text, binary_box_text_rect)
  
  def flip_bit(self):
    if self.current_bit:
      self.current_bit = False
      self.missile.erase()
    else:
      self.current_bit = True
      self.missile.draw()
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
    binary = reduce(lambda string, box: string + str(int(box.current_bit)), binary_boxes, "")
    self.current_hexadecimals =  f"{int(binary, 2):X}"
    self.draw_display()

class Enemy(HexadecimalDisplay):
  def __init__(self, position, size, font_size, hexadecimals, game):
    HexadecimalDisplay.__init__(self, game, font_size, hexadecimals, (0, 0), size)
    self.size = size
    self.border_colour = "#850020"
    self.border_width = 5
    self.is_being_destroyed = False
    self.border_rect = pygame.Rect(position, (self.size,)*2)
  
  def draw(self):
    self.background_rect.center = self.border_rect.center
    self.draw_display()
    pygame.draw.rect(self.game.screen, self.border_colour, self.border_rect, self.border_width)
  
  def erase(self):
    pygame.draw.rect(self.game.screen, self.game.bg_colour, self.border_rect)
  
  def update_position(self):
    if self.border_rect.y in range(self.game.rect.y, self.game.play_area_height - 50 - self.size):
      self.erase()
      self.border_rect.y += 1
      self.draw()
    else:
      self.destroy()
  
  def destroy(self):
    self.erase()
    self.game.alive_enemies.remove(self)