from functools import reduce
from time import time
import pygame
from classes import Game, MissileMerger, Preview, ScoreDisplay
from functions import (
  spawn_enemy, 
  active_box_missile, 
  on_keypress, 
  create_binary_bar, 
  draw_start_message, 
  draw_end_message, 
  erase_start_and_end_message, 
  reset_game_variables,
  update_highscore
)

pygame.init()

clock = pygame.time.Clock()

game = Game()

bg_colour = "#004466"
game.screen.fill(bg_colour)

game.draw_layout()
draw_start_message(game)

create_binary_bar(game)
game.binary_bar_preview = Preview((240, 770), 70, "0", game)
game.score_display = ScoreDisplay("0", (130, 770), 60, game)

while True:
  clock.tick(60)
  pygame.display.flip()

  if not game.is_running:
    for event in pygame.event.get():
      match event.type:
        case pygame.QUIT:
          pygame.quit()
          exit()
        case pygame.KEYDOWN:
          if event.key == pygame.K_SPACE:
            game.is_running = True
            reset_game_variables(game)
            erase_start_and_end_message(game)
    continue

  current_time = time()
  if current_time - game.time_since_enemy_spawn >= game.time_between_spawns:
    game.time_since_enemy_spawn = current_time
    if game.time_between_spawns > 1.5:
      game.time_between_spawns -= 0.25
    spawn_enemy(game)

  is_enemy_through = False
  for enemy in game.alive_enemies:
    if enemy.border_rect.y in range(game.rect.y, game.death_line):
      enemy.update_position()
    else:
      game.is_running = False
      update_highscore(game)
      draw_end_message(game)
      is_enemy_through = True
      break
  
    if not enemy.is_being_destroyed:
      if game.binary_bar_preview.text_content == enemy.text_content:

        active_missiles = reduce(active_box_missile, game.binary_boxes, [])
        game.binary_bar_preview.update_display()

        enemy.is_being_destroyed = True
        game.mergers[enemy] = MissileMerger(active_missiles, enemy)

  if is_enemy_through: continue

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

  for target, missile in game.shot_missiles.copy().items():
    if missile.has_collided():
      game.score_display.update()
      del game.shot_missiles[target]
    else:
      missile.step_shoot_animation()

  for box in game.binary_boxes:
    if box.current_bit:
      box.missile.draw()

  for event in pygame.event.get():
    match event.type:
      case pygame.QUIT:
        pygame.quit()
        exit()
      case pygame.KEYDOWN:
        match event.key:
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