import pygame
from sys import exit
from classes import Game, Preview, ScoreDisplay
from functions import (
  create_binary_bar, 
  draw_start_message, 
  erase_messages, 
  spawn_enemy,
  update_enemies,
  update_missile_mergers,
  update_shot_missiles,
  on_keydown,
  resource_path
)

pygame.init()
clock = pygame.time.Clock()
game = Game()

game.screen.fill(game.screen_bg_colour)
pygame.display.set_caption("Flippy Bit practice")
icon = pygame.image.load(resource_path("icon.png"))
pygame.display.set_icon(icon)
game.draw_layout()

create_binary_bar(game)
game.binary_bar_preview = Preview(game, (240, 770), 70, "0")
game.score_display = ScoreDisplay(game, (130, 770), 60, "0")
draw_start_message(game)

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
            erase_messages(game)
            game.setup()
    continue

  update_enemies(game)
  update_missile_mergers(game)
  update_shot_missiles(game)

  for box in game.binary_boxes:
    if box.is_active:
      box.missile.draw()

  for event in pygame.event.get():
    match event.type:
      case pygame.QUIT:
        pygame.quit()
        exit()
      case pygame.KEYDOWN:
        on_keydown(game, event.key)