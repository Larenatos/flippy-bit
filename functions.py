from random import randint
from math import ceil
import pygame
from classes import Point, Triangle, Enemy

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

def update_merge_animation(merge_information):
  destination = merge_information.destination
  new_missiles = []
  for missile in merge_information.missiles:
    vertices = missile.vertices

    distance = destination - vertices.top.x

    if -2 < distance < 2:
      missile.move(x=distance)
      continue

    step = ceil((0.01 * abs(distance) + 1)**2)
    if distance < 0: step = -step
    missile.move(x=step)

    new_missiles.append(missile)
  
  if not len(new_missiles):
    merge_information.missiles = [merge_information.missiles[0]]
    merge_information.is_shot = True
  else:
    merge_information.missiles = new_missiles

  return merge_information