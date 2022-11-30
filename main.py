import pygame
from classes import Game, Preview, ScoreDisplay
from functions import (
  create_binary_bar, 
  draw_start_message, 
  erase_start_and_end_message, 
  enemy_creation_check,
  update_enemies,
  merger_updater,
  shot_missile_updater,
  event_key_check,
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

game.setup_game_variables()

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
            game.setup_game_variables(game)
            erase_start_and_end_message(game)
    continue

  enemy_creation_check(game)

  is_enemy_through = update_enemies(game)
  if is_enemy_through: continue

  merger_updater(game)

  shot_missile_updater(game)

  for box in game.binary_boxes:
    if box.current_bit:
      box.missile.draw()

  for event in pygame.event.get():
    match event.type:
      case pygame.QUIT:
        pygame.quit()
        exit()
      case pygame.KEYDOWN:
        event_key_check(game, event.key)