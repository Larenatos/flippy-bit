from random import randint
from time import time
import pygame
from classes import Point, Triangle, Enemy, Missile, BinaryBox

def create_binary_bar(game):
  bar_position_x = 40
  bar_position_y = game.rect.height - 100
  binary_box_size = 50
  internal_box_size = 40
  box_padding = 10
  whole_box_width = binary_box_size + box_padding

  game.binary_boxes = []

  for i in range(8):
    # calculating the position and dimensions for each missile based on the location of binary bar
    vertex_1 = Point(bar_position_x + game.border_width + i * whole_box_width, bar_position_y - 30)
    vertex_2 = Point(vertex_1.x + internal_box_size, vertex_1.y)
    vertex_3 = Point(vertex_1.x + internal_box_size / 2, vertex_1.y - internal_box_size)

    game.binary_boxes.append(BinaryBox(
      (bar_position_x + i*(whole_box_width), bar_position_y), 
      binary_box_size,
      game, 
      Missile(Triangle(vertex_1, vertex_2, vertex_3), game)
    ))

def on_keypress(bit_index, game):
  game.binary_boxes[bit_index].flip_bit()
  game.binary_bar_preview.update_display()

def create_enemy(game):
  integer = randint(0, 255)
  hexadecimal =  f"{integer:X}"

  position = Point(randint(game.rect.x + 10, game.rect.width - game.enemy_size + 10), game.rect.y + 10)

  # moving the enemy to correct area
  enemy = Enemy(position, game.enemy_size, hexadecimal, game)
  enemy.draw()
  return enemy

def active_box_missile(acc, box):
  if box.current_bit:
    box.flip_bit()
    acc.append(Missile(box.missile.vertices, box.game))
  return acc

def draw_start_message(game):
  game.shadow_surface.set_alpha(100)
  game.shadow_surface.fill("#002233")
  game.screen.blit(game.shadow_surface, (25, 65))

  pygame.draw.rect(game.screen, "#06001a", game.start_message_rect)
  game.screen.blit(game.start_text, game.start_text_rect)

def erase_start_and_end_message(game):
  game.shadow_surface.set_alpha(255)
  game.shadow_surface.fill(game.bg_colour)
  game.screen.blit(game.shadow_surface, (25, 65))
  pygame.draw.rect(game.screen, game.bg_colour, game.start_message_rect)

def draw_end_message(game, draw_start_message):
  draw_start_message(game)
  pygame.draw.rect(game.screen, "#06001a", game.end_message_rect)
  game.screen.blit(game.end_text, game.end_text_rect)

def reset_game_variables(game):
  game.time_since_enemy_spawn = time()
  game.time_between_spawns = 5
  game.mergers = {}
  game.shot_missiles = {}
  game.alive_enemies = []
  game.score = 0
  game.score_display.text_content = "0"
  game.score_display.draw_display()
  for box in game.binary_boxes:
    if box.current_bit: 
      box.flip_bit()

def update_highscore(game):
  if game.score > game.highscore:
    with open("highscore", "w") as file:
      file.write(str(game.score))
    game.highscore = game.score

    pygame.draw.rect(game.screen, "#004466", (180, 20, 100, 30))
    game.highscore_text = game.font.render(f"Highscore: {game.highscore}", True, game.text_colour)
    game.screen.blit(game.highscore_text, game.highscore_text_rect)