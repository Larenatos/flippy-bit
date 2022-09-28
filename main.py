import pygame
pygame.init()

screen = pygame.display.set_mode(size=(600, 300))
screen_bg_colour = "#00334d"
screen.fill(screen_bg_colour)

class Missile():
  def __init__(self, positions):
    self.bg_colour = "#06001a"
    self.positions = positions
  
  def draw_missile(self):
    pygame.draw.polygon(screen, self.bg_colour, self.positions)
  
  def erase_missile(self):
    pygame.draw.polygon(screen, screen_bg_colour, self.positions)

class BinaryBox():
  def __init__(self, position):
    self.bg_colour = "#06001a"
    self.border_colour = "#666666"
    self.text_colour = "#bfbfbf"
    self.position = position
    self.dimensions = (50, 50)
    self.current_bit = "0"

    self.border_rect = pygame.Rect(self.position, self.dimensions)
    self.background_rect = pygame.Rect((0, 0), (self.dimensions[0]- 10, self.dimensions[1] - 10))
    self.background_rect.center = self.border_rect.center
    self.font = pygame.font.SysFont(None, 40)
    pygame.draw.rect(screen, self.border_colour, self.border_rect, 5)
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
      bit_missiles[bit_index].draw_missile()
    else:
      self.current_bit = "0"
      bit_missiles[bit_index].erase_missile()
    self.bg_colour, self.text_colour = self.text_colour, self.bg_colour
    self.draw_box()

  def get_current_bit(self):
    return self.current_bit

class HexadecimalDisplay():
  def __init__(self, position, dimensions, font_size):
    self.bg_colour = "#06001a"
    self.text_colour = "#bfbfbf"
    self.current_hexadecimals = ""

    self.font = pygame.font.SysFont(None, font_size)
    self.background_rect = pygame.Rect(position, dimensions)
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
box_height = box_width = 50
box_padding = 10

binary_boxes = [BinaryBox((bar_position_x + i*(box_width + box_padding), bar_position_y)) for i in range(8)]

bit_missiles = []
for i in range(8):
# calculating the position and dimensions for each missile based on the loaction of binary bar
  position_1 = (bar_position_x + 5 + i * (box_width + box_padding), bar_position_y-20)
  position_2 = (bar_position_x + box_width - 5 + i * (box_width + box_padding), bar_position_y-20)
  position_3 = (bar_position_x + 5 + (box_width - 10) / 2 + i * (box_width + box_padding), bar_position_y - 20 - box_width + 10)
  bit_missiles.append(Missile((position_1, position_2, position_3)))

display_dimensions = (70, 70)
# center the display relative to the binary bar
display_position_x = bar_position_x + 4 * (box_width + box_padding) - box_padding / 2 - display_dimensions[0] / 2
display_position_y = bar_position_y + box_height + 30
hexadecimal_display = HexadecimalDisplay((display_position_x, display_position_y), display_dimensions, 50)

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