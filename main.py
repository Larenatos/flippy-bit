from functools import reduce
from time import time
import pygame
from classes import Game, MissileMerger
from functions import draw_layout, create_enemy, active_box_missile, on_keypress

pygame.init()

clock = pygame.time.Clock()

game = Game()

bg_colour = "#004466"
game.screen.fill(bg_colour)

while True:
  clock.tick(60)
  pygame.display.flip()

  if not game.game_running:
    draw_layout(game)
    for event in pygame.event.get():
      match event.type:
        case pygame.QUIT:
          pygame.quit()
          exit()
        case pygame.KEYDOWN:
          if event.key == pygame.K_SPACE:
            game.state_of_game = True
            draw_layout(game)
    continue

  current_time = time()
  if current_time - time_since_enemy_spawn >= game.time_between_spawns:
    time_since_enemy_spawn = current_time
    if game.time_between_spawns > 1.5:
      game.time_between_spawns -= 0.25
    game.alive_enemies.append(create_enemy(game))

  for enemy in game.alive_enemies:
    if not enemy.is_being_destroyed:
      if game.binary_bar_preview.text_content == enemy.text_content:

        active_missiles = reduce(active_box_missile, game.binary_boxes, [])
        game.binary_bar_preview.update_display()

        enemy.is_being_destroyed = True
        game.mergers[enemy] = MissileMerger(active_missiles, enemy)

    enemy.update_position()

  for target, merger in game.mergers.copy().items():
    if not target in game.alive_enemies:
      merger.remove()
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