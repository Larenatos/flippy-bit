from random import randint
import time
import pygame
from classes import BinaryBox, Missile, Preview, Enemy, Point

pygame.init()

game = type("Game", (), {})()

clock = pygame.time.Clock()

game.screen = pygame.display.set_mode(size=(550, 840))
bg_colour = "#004466"
game.screen.fill(bg_colour)

game_position_x = 20
game_position_y = 20
game_width = 510
game_height = 800
game.border_width = 5
play_area_height = game_height - 160
game_border_colour = "#06001a"
game.game_bg_colour = "#00334d"
game_rect = pygame.Rect(game_position_x, game_position_y, game_width, game_height)

def draw_layout():
  # calculating the position and dimensions based on information given above
  pygame.draw.rect(game.screen, game.game_bg_colour, game_rect) # background
  pygame.draw.rect(game.screen, game_border_colour, game_rect, game.border_width) # full border 
  # calculating the position for the line above binary bar
  pygame.draw.line(game.screen, game_border_colour, (game_position_x, play_area_height), (game_position_x + game_width - game.border_width, play_area_height), game.border_width)
  # The line where enemies have to reach
  # pygame.draw.line(screen, "#550000", (game_position_x + border_width, play_area_height - 50), (game_position_x + game_width - border_width, play_area_height - 50), border_width)

bar_position_x = 40
bar_position_y = game_height - 140
game.binary_box_size = 50
internal_box_size = 40
box_padding = 10
whole_box_width = game.binary_box_size + box_padding

binary_boxes = [BinaryBox((bar_position_x + i*(whole_box_width), bar_position_y), game) for i in range(8)]

bit_missiles = []

for i in range(8):
  # calculating the position and dimensions for each missile based on the location of binary bar
  vertex_1 = Point(bar_position_x + game.border_width + i * whole_box_width, bar_position_y - 30)
  vertex_2 = Point(vertex_1.x + internal_box_size, vertex_1.y)
  vertex_3 = Point(vertex_1.x + internal_box_size / 2, vertex_1.y - internal_box_size)
  bit_missiles.append(Missile((vertex_1, vertex_2, vertex_3), game))

for i, box in enumerate(binary_boxes):
  box.set_missile(bit_missiles[i])

game.preview_size = 70
game.preview_font_size = 50
# center the display relative to the binary bar
display_position_x = bar_position_x + 4 * whole_box_width - box_padding / 2 - game.preview_size / 2
display_position_y = bar_position_y + game.binary_box_size + 20
binary_bar_preview = Preview((display_position_x, display_position_y), game, "0")

game.enemy_size = 50
game.enemy_font_size = 40

alive_enemies = []

def create_enemy():
  integer = randint(0, 255)
  hexadecimal =  f"{integer:X}"

  position = Point(randint(game_position_x + 10, game_width - game.enemy_size + 10), game_position_y + 10)

  # moving the enemy to correct area
  enemy = Enemy(position, game, hexadecimal)
  enemy.draw()
  alive_enemies.append(enemy)

def draw_screen():
  game.screen.fill(bg_colour)
  draw_layout()
  binary_bar_preview.draw_display()
  for box in binary_boxes:
    box.draw_box()

def update_enemy_position():
  for enemy in alive_enemies:
    pygame.draw.rect(game.screen, game.game_bg_colour, (enemy.position, (game.enemy_size,)*2))
    enemy.update_position(game_position_y, play_area_height)
    enemy.draw()

def remove_enemy(enemy):
  pygame.draw.rect(game.screen, game.game_bg_colour, (enemy.position, (game.enemy_size,)*2))

def on_keypress(bit_index):
  binary_boxes[bit_index].flip_bit()
  binary_bar_preview.update_display(binary_boxes)

time_since_enemy_spawn = time.time()
time_between_spawns = 5

draw_screen()

while True:
  clock.tick(60)
  pygame.display.flip()

  current_time = time.time()
  if current_time - time_since_enemy_spawn >= time_between_spawns:
    time_since_enemy_spawn = current_time
    if time_between_spawns > 1.5:
      time_between_spawns -= 0.25
    create_enemy()

  for enemy in alive_enemies:
    if enemy.is_destroyed:
      remove_enemy(enemy)
      alive_enemies.remove(enemy)
  update_enemy_position()

  for event in pygame.event.get():
    match event.type:
      case pygame.QUIT:
        pygame.quit()
        exit()
      case pygame.KEYDOWN:
        match event.key:
          case pygame.K_z | pygame.K_a | pygame.K_q | pygame.K_1:
            on_keypress(0)
          case pygame.K_x | pygame.K_s | pygame.K_w | pygame.K_2:
            on_keypress(1)
          case pygame.K_c | pygame.K_d | pygame.K_e | pygame.K_3:
            on_keypress(2)
          case pygame.K_v | pygame.K_f | pygame.K_r | pygame.K_4:
            on_keypress(3)
          case pygame.K_b | pygame.K_g | pygame.K_t | pygame.K_5:
            on_keypress(4)
          case pygame.K_n | pygame.K_h | pygame.K_y | pygame.K_6:
            on_keypress(5)
          case pygame.K_m | pygame.K_j | pygame.K_u | pygame.K_7:
            on_keypress(6)
          case pygame.K_COMMA | pygame.K_k | pygame.K_i | pygame.K_8:
            on_keypress(7)