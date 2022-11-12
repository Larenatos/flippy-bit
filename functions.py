from random import randint
import pygame
from classes import Point, Enemy, Missile

def draw_layout(game, binary_boxes, preview, score_display):
  # calculating the position and dimensions based on information given above
  pygame.draw.rect(game.screen, game.bg_colour, game.rect) # background
  pygame.draw.rect(game.screen, game.border_colour, game.rect, game.border_width) # full border 
  # calculating the position for the line above binary bar
  start_position = (game.rect.x, game.play_area_height)
  end_position = (game.rect.right - game.border_width, game.play_area_height)
  pygame.draw.line(game.screen, game.border_colour, start_position, end_position, game.border_width)

  pygame.draw.rect(game.screen, "#004466", pygame.Rect(0, 10, 550, 50))
  highscore_text = game.font.render(f"Highscore: {game.highscore}", True, game.text_colour)
  highscore_text_rect = highscore_text.get_rect()
  highscore_text_rect.center = pygame.Rect(0, 10, 550, 50).center

  game.screen.blit(highscore_text, highscore_text_rect)
  game.screen.blit(game.score_text, game.score_text_rect)

  if not game.state_of_game:
    pygame.draw.rect(game.screen, "#06001a", (70, 380, 410, 90))
    game.screen.blit(game.start_text, game.start_text_rect)
  
  for box in binary_boxes:
    box.draw_box()
  preview.draw_display()
  score_display.draw_display()

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