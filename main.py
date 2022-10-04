from collections import namedtuple
import random
import time
import pygame
pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode(size=(550, 840))
bg_colour = "#004466"
screen.fill(bg_colour)

game_position_x = 20
game_position_y = 20
game_width = 510
game_height = 800
border_width = 5
play_area_height = game_height - 160
game_border_colour = "#06001a"
game_bg_colour = "#00334d"

def draw_layout():
  game_rect = pygame.Rect(game_position_x, game_position_y, game_width, game_height)

  # calculating the position and dimensions based on information given above
  background = pygame.draw.rect(screen, game_bg_colour, game_rect)
  game_border = pygame.draw.rect(screen, game_border_colour, game_rect, border_width)
  # calculating the position for the line above binary bar
  area_separator = pygame.draw.line(screen, game_border_colour, (game_position_x, play_area_height), (game_position_x + game_width - border_width, play_area_height), border_width)
  dead_line = pygame.draw.line(screen, "#550000", (game_position_x + border_width, play_area_height - 50), (game_position_x + game_width - border_width, play_area_height - 50), border_width)

class Missile():
  def __init__(self, vertices):
    self.bg_colour = "#06001a"
    self.vertices = vertices
  
  def draw(self):
    pygame.draw.polygon(screen, self.bg_colour, self.vertices)
  
  def erase(self):
    pygame.draw.polygon(screen, game_bg_colour, self.vertices)

class BinaryBox():
  def __init__(self, position, size, border_width, index):
    self.bg_colour = "#06001a"
    self.border_colour = "#666666"
    self.text_colour = "#bfbfbf"
    self.current_bit = "0"
    self.index = index
    self.bit_missiles = []

    internal_box_size = size - 2 * border_width
    self.border_rect = pygame.Rect(position, (size,)*2)
    self.background_rect = pygame.Rect((0, 0), (internal_box_size,)*2)
    self.background_rect.center = self.border_rect.center
    self.font = pygame.font.SysFont(None, 40)
    self.draw_box()

  def draw_box(self):
    pygame.draw.rect(screen, self.border_colour, self.border_rect, border_width)
    pygame.draw.rect(screen, self.bg_colour, self.background_rect)
    
    binary_box_text = self.font.render(self.current_bit, True, self.text_colour)
    binary_box_text_rect = binary_box_text.get_rect()
    binary_box_text_rect.center = self.background_rect.center
    screen.blit(binary_box_text, binary_box_text_rect)
    if self.current_bit == "1":
      self.bit_missiles[self.index].draw()
  
  def flip_bit(self, bit_index, bit_missiles):
    self.bit_missiles = bit_missiles
    if self.current_bit == "0":
      self.current_bit = "1"
      bit_missiles[bit_index].draw()
    else:
      self.current_bit = "0"
      bit_missiles[bit_index].erase()
    self.bg_colour, self.text_colour = self.text_colour, self.bg_colour
    self.draw_box()

  def get_current_bit(self):
    return self.current_bit

class HexadecimalDisplay():
  def __init__(self, size, font_size, hexadecimals):
    self.bg_colour = "#06001a"
    self.text_colour = "#bfbfbf"
    self.current_hexadecimals = hexadecimals
    self.size = size
    self.font = pygame.font.SysFont(None, font_size)

  def draw_display(self):
    pygame.draw.rect(screen, self.bg_colour, self.background_rect)
    display_text = self.font.render(self.current_hexadecimals, True, self.text_colour)
    display_text_rect = display_text.get_rect()
    display_text_rect.center = self.background_rect.center
    screen.blit(display_text, display_text_rect)
  
class Preview(HexadecimalDisplay):
  def __init__(self, position, size, font_size, hexadecimals):
    HexadecimalDisplay.__init__(self, size, font_size, hexadecimals)
    self.background_rect = pygame.Rect(position, (size,)*2)
    self.draw_display()

  def update_display(self, binary_boxes):
    binary = "".join(binary_box.get_current_bit() for binary_box in binary_boxes)
    self.current_hexadecimals =  f"{int(binary, 2):X}"
    self.draw_display()

class Enemy(HexadecimalDisplay):
  def __init__(self, position, size, font_size, hexadecimals):
    HexadecimalDisplay.__init__(self, size, font_size, hexadecimals)
    self.position = position
    self.border_colour = "#850020"
    self.border_width = 5
    self.status = "alive"
  
  def draw(self):
    self.border_rect = pygame.Rect(self.position, (self.size,)*2)
    self.background_rect = pygame.Rect((0, 0), (self.size,)*2)
    self.background_rect.center = self.border_rect.center
    self.draw_display()
    pygame.draw.rect(screen, self.border_colour, self.border_rect, self.border_width)
  
  def update_position(self):
    # checking if the enemy has reached the bottom
    if self.position.y in range(game_position_y, play_area_height - 50 - self.size):
      self.position = Point(self.position.x, self.position.y + 1)
      self.draw()
    else:
      self.status = "dead"

bar_position_x = 40
bar_position_y = game_height - 140
box_size = 50
internal_box_size = 40
box_border_width = 5
box_padding = 10
whole_box_width = box_size + box_padding

binary_boxes = [BinaryBox((bar_position_x + i*(whole_box_width), bar_position_y), box_size, box_border_width, i) for i in range(8)]

bit_missiles = []
Point = namedtuple("Point", "x y")

for i in range(8):
  # calculating the position and dimensions for each missile based on the location of binary bar
  vertex_1 = Point(bar_position_x + box_border_width + i * whole_box_width, bar_position_y - 30)
  vertex_2 = Point(vertex_1.x + internal_box_size, vertex_1.y)
  vertex_3 = Point(vertex_1.x + internal_box_size / 2, vertex_1.y - internal_box_size)
  bit_missiles.append(Missile((vertex_1, vertex_2, vertex_3)))

display_size = 70
# center the display relative to the binary bar
display_position_x = bar_position_x + 4 * whole_box_width - box_padding / 2 - display_size / 2
display_position_y = bar_position_y + box_size + 20
hexadecimal_display = Preview((display_position_x, display_position_y), display_size, 50, "0")

hexadecimals = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
enemy_size = 50

alive_enemies = []

def create_enemy():
  first_hexadecimal = random.choice(hexadecimals)
  second_hexadecimal = random.choice(hexadecimals)

  if first_hexadecimal == "0": 
    first_hexadecimal = ""

  # moving the enemy to correct area
  enemy = Enemy(Point(random.randint(game_position_x + 10, game_width - enemy_size + 10), game_position_y + 10), enemy_size, 40, f"{first_hexadecimal}{second_hexadecimal}")
  enemy.draw()
  alive_enemies.append(enemy)


def redraw_screen():
  screen.fill(bg_colour)
  draw_layout()
  hexadecimal_display.draw_display()
  for box in binary_boxes:
    box.draw_box()
  for enemy in alive_enemies:
    enemy.draw()

def on_keypress(bit_index):
  binary_boxes[bit_index].flip_bit(bit_index, bit_missiles)
  hexadecimal_display.update_display(binary_boxes)

time_since_enemy_spawn = time.time()

while True:
  clock.tick(60)
  pygame.display.flip()

  current_time = time.time()
  if current_time - time_since_enemy_spawn >= 5:
    print("enemy spawned")
    time_since_enemy_spawn = current_time
    create_enemy()

  for enemy in alive_enemies:
    if enemy.status == "dead":
      alive_enemies.remove(enemy)
    enemy.update_position()
  
  redraw_screen()

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