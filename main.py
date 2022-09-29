from collections import namedtuple
import pygame
pygame.init()

screen = pygame.display.set_mode(size=(600, 300))
screen_bg_colour = "#00334d"
screen.fill(screen_bg_colour)

class Missile():
  def __init__(self, vertices):
    self.bg_colour = "#06001a"
    self.vertices = vertices
  
  def draw(self):
    pygame.draw.polygon(screen, self.bg_colour, self.vertices)
  
  def erase(self):
    pygame.draw.polygon(screen, screen_bg_colour, self.vertices)

class BinaryBox():
  def __init__(self, position, size, border_width):
    self.bg_colour = "#06001a"
    self.border_colour = "#666666"
    self.text_colour = "#bfbfbf"
    self.current_bit = "0"

    internal_box_size = size - 2 * border_width
    border_rect = pygame.Rect(position, (size,)*2)
    self.background_rect = pygame.Rect((0, 0), (internal_box_size,)*2)
    self.background_rect.center = border_rect.center
    self.font = pygame.font.SysFont(None, 40)
    pygame.draw.rect(screen, self.border_colour, border_rect, border_width)
    self.draw_box()

  def draw_box(self):
    pygame.draw.rect(screen, self.bg_colour, self.background_rect)
    
    binary_box_text = self.font.render(self.current_bit, True, self.text_colour)
    binary_box_text_rect = binary_box_text.get_rect()
    binary_box_text_rect.center = self.background_rect.center
    screen.blit(binary_box_text, binary_box_text_rect)
  
  def flip_bit(self, bit_index, bit_missiles):
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
  def __init__(self, position, size, font_size):
    self.bg_colour = "#06001a"
    self.text_colour = "#bfbfbf"
    self.current_hexadecimals = ""

    self.font = pygame.font.SysFont(None, font_size)
    self.background_rect = pygame.Rect(position, (size,)*2)
    self.draw_display()

  def draw_display(self):
    pygame.draw.rect(screen, self.bg_colour, self.background_rect)
    display_text = self.font.render(self.current_hexadecimals, True, self.text_colour)
    display_text_rect = display_text.get_rect()
    display_text_rect.center = self.background_rect.center
    screen.blit(display_text, display_text_rect)
  
  def update_display(self, binary_boxes):
    binary = "".join(binary_box.get_current_bit() for binary_box in binary_boxes)
    self.current_hexadecimals =  f"{int(binary, 2):X}"
    self.draw_display()

bar_position_x = 50
bar_position_y = 100
box_size = 50
internal_box_size = 40
box_border_width = 5
box_padding = 10
whole_box_width = box_size + box_padding

binary_boxes = [BinaryBox((bar_position_x + i*(whole_box_width), bar_position_y), box_size, box_border_width) for i in range(8)]

bit_missiles = []
Point = namedtuple("Point", "x y")

for i in range(8):
  # calculating the position and dimensions for each missile based on the loaction of binary bar
  vertex_1 = Point(bar_position_x + box_border_width + i * whole_box_width, bar_position_y - 20)
  vertex_2 = Point(vertex_1.x + internal_box_size, vertex_1.y)
  vertex_3 = Point(vertex_1.x + internal_box_size / 2, vertex_1.y - internal_box_size)
  bit_missiles.append(Missile((vertex_1, vertex_2, vertex_3)))

display_size = 70
# center the display relative to the binary bar
display_position_x = bar_position_x + 4 * whole_box_width - box_padding / 2 - display_size / 2
display_position_y = bar_position_y + box_size + 30
hexadecimal_display = HexadecimalDisplay((display_position_x, display_position_y), display_size, 50)

def on_keypress(bit_index):
  binary_boxes[bit_index].flip_bit(bit_index, bit_missiles)
  hexadecimal_display.update_display(binary_boxes)

while True:
  pygame.display.flip()
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