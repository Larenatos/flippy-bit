from time import time
from functools import reduce
import pygame
from classes import Game, BinaryBox, Missile, Preview, MissileMerger, Point, Triangle
from functions import draw_layout, create_enemy, active_box_missile

pygame.init()

clock = pygame.time.Clock()

game = Game()

bg_colour = "#004466"
game.screen.fill(bg_colour)

bar_position_x = 40
bar_position_y = game.rect.height - 140
binary_box_size = 50
internal_box_size = 40
box_padding = 10
whole_box_width = binary_box_size + box_padding

binary_boxes = []

for i in range(8):
  # calculating the position and dimensions for each missile based on the location of binary bar
  vertex_1 = Point(bar_position_x + game.border_width + i * whole_box_width, bar_position_y - 30)
  vertex_2 = Point(vertex_1.x + internal_box_size, vertex_1.y)
  vertex_3 = Point(vertex_1.x + internal_box_size / 2, vertex_1.y - internal_box_size)

  binary_boxes.append(BinaryBox(
    (bar_position_x + i*(whole_box_width), bar_position_y), 
    binary_box_size,
    game, 
    Missile(Triangle(vertex_1, vertex_2, vertex_3), game)
  ))

preview_size = 70
preview_font_size = 50
# center the display relative to the binary bar
display_position_x = bar_position_x + 4 * whole_box_width - box_padding / 2 - preview_size / 2
display_position_y = bar_position_y + binary_box_size + 20
binary_bar_preview = Preview((display_position_x, display_position_y), preview_size, preview_font_size, "0", game)

draw_layout(game)
binary_bar_preview.draw_display()
for box in binary_boxes:
  box.draw_box()

def on_keypress(bit_index):
  binary_boxes[bit_index].flip_bit()
  binary_bar_preview.update_display(binary_boxes)

time_since_enemy_spawn = time()
time_between_spawns = 5

mergers = {}
shot_missiles = {}

while True:
  clock.tick(60)
  pygame.display.flip()

  current_time = time()
  if current_time - time_since_enemy_spawn >= time_between_spawns:
    time_since_enemy_spawn = current_time
    if time_between_spawns > 1.5:
      time_between_spawns -= 0.25
    game.alive_enemies.append(create_enemy(game))

  for enemy in game.alive_enemies:
    if not enemy.is_being_destroyed:
      if binary_bar_preview.current_hexadecimals == enemy.current_hexadecimals:

        active_missiles = reduce(active_box_missile, binary_boxes, [])
        binary_bar_preview.update_display(binary_boxes)

        enemy.is_being_destroyed = True
        mergers[enemy] = MissileMerger(active_missiles, enemy)

    enemy.update_position()

  for target, merger in mergers.copy().items():
    if not target in game.alive_enemies:
      merger.remove()
      del mergers[target]
      continue

    if merger.done:
      shot_missiles[target] = merger.final_missile
      del mergers[target]
    else:
      merger.step_animation()

  for target, missile in shot_missiles.copy().items():
    if missile.has_collided():
      del shot_missiles[target]
    else:
      missile.step_shoot_animation()

  for box in binary_boxes:
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