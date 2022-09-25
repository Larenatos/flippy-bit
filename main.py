import pygame
pygame.init()

screen = pygame.display.set_mode(size=(1000, 500))
screen.fill("grey")

class BinaryBox():
  def __init__(self, position, dimensions):
    self.bg_colour = "#06001a"
    self.border_colour = "#666666"
    self.text_colour = "#bfbfbf"
    self.position = position
    self.dimensions = dimensions
    self.current_binary = "0"

    self.border_dimensions = (self.dimensions[0] + 10, self.dimensions[1] + 10)
    self.border_rect = pygame.Rect((0, 0), self.border_dimensions)
    self.background_rect = pygame.Rect (self.position, self.dimensions)
    self.border_rect.center = self.background_rect.center
    self.font = pygame.font.SysFont(None, 40)
    pygame.draw.rect(screen, self.border_colour, self.border_rect, 5)
    self.draw_box()

  def draw_box(self):
    pygame.draw.rect(screen, self.bg_colour, self.background_rect)
    
    binary_box_text = self.font.render(self.current_binary, True, self.text_colour)
    binary_box_text_rect = binary_box_text.get_rect()
    binary_box_text_rect.center = self.background_rect.center
    screen.blit(binary_box_text, binary_box_text_rect)
  
  def flip_bit(self):
    if self.current_binary == "0":
      self.current_binary = "1"
    else:
      self.current_binary = "0"
    self.bg_colour, self.text_colour = self.bg_colour, self.text_colour
    self.draw_box()

positionx = 50
positiony = 50
dimensions = (40, 40)
distance_between = 60

binary_box_1 = BinaryBox((positionx, positiony), dimensions)
binary_box_2 = BinaryBox((positionx + distance_between, positiony), dimensions)
binary_box_3 = BinaryBox((positionx + 2*distance_between, positiony), dimensions)
binary_box_4 = BinaryBox((positionx + 3*distance_between, positiony), dimensions)
binary_box_5 = BinaryBox((positionx + 4*distance_between, positiony), dimensions)
binary_box_6 = BinaryBox((positionx + 5*distance_between, positiony), dimensions)
binary_box_7 = BinaryBox((positionx + 6*distance_between, positiony), dimensions)
binary_box_8 = BinaryBox((positionx + 7*distance_between, positiony), dimensions)

pygame.display.flip()

while True:
  for event in pygame.event.get():
    match event.type:
      case pygame.QUIT:
        pygame.quit()
      case pygame.KEYDOWN:
        match event.key:
          case pygame.K_z | pygame.K_a | pygame.K_q | pygame.K_1:
            binary_box_1.flip_bit()
          case pygame.K_x | pygame.K_s | pygame.K_w | pygame.K_2:
            binary_box_2.flip_bit()
          case pygame.K_c | pygame.K_d | pygame.K_e | pygame.K_3:
            binary_box_3.flip_bit()
          case pygame.K_v | pygame.K_f | pygame.K_r | pygame.K_4:
            binary_box_4.flip_bit()
          case pygame.K_b | pygame.K_g | pygame.K_t | pygame.K_5:
            binary_box_5.flip_bit()
          case pygame.K_n | pygame.K_h | pygame.K_y | pygame.K_6:
            binary_box_6.flip_bit()
          case pygame.K_m | pygame.K_j | pygame.K_u | pygame.K_7:
            binary_box_7.flip_bit()
          case pygame.K_COMMA | pygame.K_l | pygame.K_o | pygame.K_9:
            binary_box_8.flip_bit()

  pygame.display.update()