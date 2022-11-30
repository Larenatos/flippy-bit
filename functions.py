from random import randint
from time import time
from functools import reduce
import pygame
from classes import Point, Triangle, Enemy, Missile, BinaryBox, MissileMerger

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
      game,
      (bar_position_x + i*(whole_box_width), bar_position_y), 
      binary_box_size,
      Missile(game, Triangle(vertex_1, vertex_2, vertex_3))
    ))

def on_keypress(bit_index, game):
  game.binary_boxes[bit_index].flip_bit()
  game.binary_bar_preview.update_display()

def spawn_enemy(game):
  integer = randint(0, 255)
  hexadecimal =  f"{integer:X}"

  # moving the enemy to correct area
  position = Point(randint(game.rect.x + 10, game.rect.width - 50 + 10), game.rect.y + 10)

  enemy = Enemy(game, position, 50, hexadecimal)
  enemy.draw()
  game.alive_enemies.append(enemy)

def active_box_missile(acc, box):
  if box.current_bit:
    box.flip_bit()
    acc.append(Missile(box.game, box.missile.vertices))
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

def draw_end_message(game):
  draw_start_message(game)
  pygame.draw.rect(game.screen, "#06001a", game.end_message_rect)
  game.screen.blit(game.end_text, game.end_text_rect)

def update_highscore(game):
  if game.score > game.highscore:
    with open("highscore", "w") as file:
      file.write(str(game.score))
    game.highscore = game.score

    pygame.draw.rect(game.screen, game.screen_bg_colour, (180, 20, 100, 30))
    game.highscore_text = game.font.render(f"Highscore: {game.highscore}", True, game.text_colour)
    game.screen.blit(game.highscore_text, game.highscore_text_rect)

def enemy_creation_check(game):
  current_time = time()
  if current_time - game.time_since_enemy_spawn >= game.time_between_spawns:
    game.time_since_enemy_spawn = current_time
    if game.time_between_spawns > 1.5:
      game.time_between_spawns -= 0.25
    spawn_enemy(game)

def update_enemies(game):
  for enemy in game.alive_enemies:
    if enemy.border_rect.y in range(game.rect.y, game.death_line):
      enemy.update_position()
    else:
      game.is_running = False
      update_highscore(game)
      draw_end_message(game)
      return True
  
    if not enemy.is_being_destroyed:
      if game.binary_bar_preview.text_content == enemy.text_content:

        active_missiles = reduce(active_box_missile, game.binary_boxes, [])
        game.binary_bar_preview.update_display()

        enemy.is_being_destroyed = True
        game.mergers[enemy] = MissileMerger(active_missiles, enemy)
  return False

def merger_updater(game):
  for target, merger in game.mergers.copy().items():
    if not target in game.alive_enemies:
      merger.erase()
      del game.mergers[target]
      continue

    if merger.done:
      game.shot_missiles[target] = merger.final_missile
      del game.mergers[target]
    else:
      merger.step_animation()

def shot_missile_updater(game):
  for target, missile in game.shot_missiles.copy().items():
    if missile.has_collided():
      game.score_display.update()
      del game.shot_missiles[target]
    else:
      missile.step_shoot_animation()

def event_key_check(game, key):
  match key:
    case pygame.K_z | pygame.K_a | pygame.K_q | pygame.K_1:
      on_keypress(0, game)
    case pygame.K_x | pygame.K_s | pygame.K_w | pygame.K_2:
      on_keypress(1, game)
    case pygame.K_c | pygame.K_d | pygame.K_e | pygame.K_3:
      on_keypress(2, game)
    case pygame.K_v | pygame.K_f | pygame.K_r | pygame.K_4:
      on_keypress(3, game)
    case pygame.K_b | pygame.K_g | pygame.K_t | pygame.K_5:
      on_keypress(4, game)
    case pygame.K_n | pygame.K_h | pygame.K_y | pygame.K_6:
      on_keypress(5, game)
    case pygame.K_m | pygame.K_j | pygame.K_u | pygame.K_7:
      on_keypress(6, game)
    case pygame.K_COMMA | pygame.K_k | pygame.K_i | pygame.K_8:
      on_keypress(7, game)