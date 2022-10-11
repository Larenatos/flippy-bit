from random import randint
import pygame
from classes import Point, Enemy, Missile

def draw_layout(game):
  # calculating the position and dimensions based on information given above
  pygame.draw.rect(game.screen, game.bg_colour, game.rect) # background
  pygame.draw.rect(game.screen, game.border_colour, game.rect, game.border_width) # full border 
  # calculating the position for the line above binary bar
  start_position = (game.rect.x, game.play_area_height)
  end_position = (game.rect.right - game.border_width, game.play_area_height)
  pygame.draw.line(game.screen, game.border_colour, start_position, end_position, game.border_width)

def create_enemy(game):
  integer = randint(0, 255)
  hexadecimal =  f"{integer:X}"

  position = Point(randint(game.rect.x + 10, game.rect.width - game.enemy_size + 10), game.rect.y + 10)

  # moving the enemy to correct area
  enemy = Enemy(position, game.enemy_size, game.enemy_font_size, hexadecimal, game)
  enemy.draw()
  return enemy

def merge_missiles(destination, missile_locations, game):
  print(missile_locations)
  missiles = [Missile(location, game) for location in missile_locations]
  for missile in missiles:
    if missile.vertices[3] < destination:
      missile.erase()
      for vertex in missile.vertices:
        vertex.x += 1
      missile.draw()
    elif missile.vertices > destination:
      missile.erase()
      for vertex in missile.vertices:
        vertex.x -= 1
      missile.draw()
  