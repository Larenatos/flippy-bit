from random import randint
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

    if missile.vertices.top.x < merge_information.destination:
      missile.erase()
      if destination - vertices.top.x < 3:
        new_vertices = (Point(vertex.x + 1, vertex.y) for vertex in vertices)
        missile.vertices = Triangle(*new_vertices)
      elif destination - vertices.top.x < 6:
        new_vertices = (Point(vertex.x + 2, vertex.y) for vertex in vertices)
        missile.vertices = Triangle(*new_vertices)
      elif destination - vertices.top.x > 50:
        new_vertices = (Point(vertex.x + 6, vertex.y) for vertex in vertices)
        missile.vertices = Triangle(*new_vertices)
      else:
        new_vertices = (Point(vertex.x + 3, vertex.y) for vertex in vertices)
        missile.vertices = Triangle(*new_vertices)
      missile.draw()

    elif vertices.top.x > destination:
      missile.erase()
      if vertices.top.x - destination < 3:
        new_vertices = (Point(vertex.x +- 1, vertex.y) for vertex in vertices)
        missile.vertices = Triangle(*new_vertices)
      elif vertices.top.x - destination < 6:
        new_vertices = (Point(vertex.x - 2, vertex.y) for vertex in vertices)
        missile.vertices = Triangle(*new_vertices)
      elif vertices.top.x - destination > 50:
        new_vertices = (Point(vertex.x - 6, vertex.y) for vertex in vertices)
        missile.vertices = Triangle(*new_vertices)
      else:
        new_vertices = (Point(vertex.x - 3, vertex.y) for vertex in vertices)
        missile.vertices = Triangle(*new_vertices)
      missile.draw()
      
    if not vertices.top.x == destination:
      new_missiles.append(missile)
  
  merge_information.missiles = new_missiles
  return merge_information