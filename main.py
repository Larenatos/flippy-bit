import pygame
pygame.init()

screen = pygame.display.set_mode(size=(600, 300))
screen.fill("#00334d")

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
  
  
  def flip_bit(self):
    if self.current_bit == "0":
      self.current_bit = "1"
    else:
      self.current_bit = "0"
    self.bg_colour, self.text_colour = self.text_colour, self.bg_colour
    self.draw_box()
    
  def get_current_bit(self):
    return self.current_bit

class HexadecimalDisplay():
  def __init__(self, position, dimensions, font_size):
    self.bg_colour = "#06001a"
    self.text_colour = "#bfbfbf"
    self.current_hexadecimal = "EE"
    self.position = position
    self.dimensions = dimensions

    self.font = pygame.font.SysFont(None, font_size)
    self.draw_display()

  def draw_display(self):
    background = pygame.draw.rect(screen, self.bg_colour, (self.position, self.dimensions))
    display_text = self.font.render(self.current_hexadecimal, True, self.text_colour)
    display_text_rect = display_text.get_rect()
    display_text_rect.center = background.center
    screen.blit(display_text, display_text_rect)

bar_position_x = 50
bar_position_y = 50
box_width = 50
box_padding = 10

binary_boxes = [BinaryBox((bar_position_x + i*(box_width + box_padding), bar_position_y)) for i in range(8)]

display_dimensions = (70, 70)
display_position_x = bar_position_x + 4 * (box_width + box_padding) - 5 - display_dimensions[0] / 2
hexadecimal_display = HexadecimalDisplay((display_position_x, 130), display_dimensions, 50)

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
            binary_boxes[0].flip_bit()
          case pygame.K_x | pygame.K_s | pygame.K_w | pygame.K_2:
            binary_boxes[1].flip_bit()
          case pygame.K_c | pygame.K_d | pygame.K_e | pygame.K_3:
            binary_boxes[2].flip_bit()
          case pygame.K_v | pygame.K_f | pygame.K_r | pygame.K_4:
            binary_boxes[3].flip_bit()
          case pygame.K_b | pygame.K_g | pygame.K_t | pygame.K_5:
            binary_boxes[4].flip_bit()
          case pygame.K_n | pygame.K_h | pygame.K_y | pygame.K_6:
            binary_boxes[5].flip_bit()
          case pygame.K_m | pygame.K_j | pygame.K_u | pygame.K_7:
            binary_boxes[6].flip_bit()
          case pygame.K_COMMA | pygame.K_l | pygame.K_o | pygame.K_9:
            binary_boxes[7].flip_bit()