from collections import namedtuple
from functools import reduce
from math import ceil
import json
import pygame

Point = namedtuple("Point", "x y")
Triangle = namedtuple("Triangle", "left right top")

class Game:
  def __init__(self):
    self.screen = pygame.display.set_mode(size=(550, 880))
    self.rect = pygame.Rect(20, 60, 510, 800)
    self.border_width = 5
    self.play_area_height = 680
    self.border_colour = "#06001a"
    self.bg_colour = "#00334d"
    self.text_colour = "#bfbfbf"
    self.font = pygame.font.SysFont(None, 40)

    self.enemy_size = 50

    self.alive_enemies = []
    self.state_of_game = False # False = waiting for user to start game, True = shooting down enemies

    with open("highscore.json", "r") as file:
      highscore = json.load(file)
    self.highscore = highscore["highscore"]

    self.score_text = self.font.render("Score:", True, self.text_colour)
    self.score_text_rect = self.score_text.get_rect()
    self.score_text_rect.center = pygame.Rect(40, 770, 80, 40).center

    self.start_text = self.font.render("Press space to start!", True, self.text_colour)
    self.start_text_rect = self.start_text.get_rect()
    self.start_text_rect.center = pygame.Rect(0, 400, 550, 50).center

    self.score_display = None

  def check_highscore(self):
    score = int(self.score_display.text_content)
    if score > self.highscore:
      highscore = {"highscore": score}
      with open("highscore.json", "w") as file:
        json.dump(highscore, file)
      self.highscore = score

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
    
    if remaining_missiles:
      self.missiles = remaining_missiles
    else:
      self.done = True
      
  def get_final_missile(self):
    missile = self.missiles[0]
    missile.target = self.target
    return missile

  def remove(self):
    for missile in self.missiles:
      missile.erase()
    if self.final_missile:
      self.final_missile.erase()

class Display:
  def __init__(self, game, font_size, text, position, size):
    self.game = game
    self.background_rect = pygame.Rect(position, (size,)*2)
    self.bg_colour = "#06001a"
    self.text_colour = game.text_colour
    self.text_content = text
    self.font = pygame.font.SysFont(None, font_size)

  def draw_display(self):
    pygame.draw.rect(self.game.screen, self.bg_colour, self.background_rect)
    display_text = self.font.render(self.text_content, True, self.text_colour)
    display_text_rect = display_text.get_rect()
    display_text_rect.center = self.background_rect.center
    self.game.screen.blit(display_text, display_text_rect)

class BinaryBox(Display):
  def __init__(self, position, size, game, missile):
    Display.__init__(self, game, 40, None, position, size)
    self.game = game
    self.border_colour = "#666666"
    self.current_bit = False
    self.missile = missile

    self.border_rect = pygame.Rect(position, (size,)*2)

  def draw_box(self):
    self.text_content = "1" if self.current_bit else "0"
    self.draw_display()
    pygame.draw.rect(self.game.screen, self.border_colour, self.border_rect, self.game.border_width)
  
  def flip_bit(self):
    if self.current_bit:
      self.current_bit = False
      self.missile.erase()
    else:
      self.current_bit = True
      self.missile.draw()

    self.bg_colour, self.text_colour = self.text_colour, self.bg_colour
    self.draw_box()

class Preview(Display):
  def __init__(self, position, size, hexadecimals, game):
    Display.__init__(self, game, 50, hexadecimals, position, size,)
    self.draw_display()

  def update_display(self, binary_boxes):
    binary = reduce(lambda string, box: string + str(int(box.current_bit)), binary_boxes, "")
    self.text_content =  f"{int(binary, 2):X}"

class Enemy(Display):
  def __init__(self, position, size, hexadecimals, game):
    Display.__init__(self, game, 40, hexadecimals, (0, 0), size)
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
      self.game.state_of_game = False
      self.game.check_highscore()

  def destroy(self):
    self.erase()
    self.game.alive_enemies.remove(self)

class ScoreDisplay(Display):
  def __init__(self, value, position, size, game):
    Display.__init__(self, game, 50, value, position, size)
  
  def update(self):
    self.text_content = str(int(self.text_content) + 1)
    self.draw_display()