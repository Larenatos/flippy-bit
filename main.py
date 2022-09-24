import pygame
pygame.init()

screen = pygame.display.set_mode(size=(1000, 500))
screen.fill("grey")

binary_box_bg_colour = "#06001a"
binary_box_border_colour = "#666666"
binary_box_text_colour = "#bfbfbf"

class binary_box():
  def __init__(self, position, dimensions):
    self.bg_colour = binary_box_bg_colour
    self.border_colour = binary_box_border_colour
    self.text_colour = binary_box_text_colour
    self.position = position
    self.dimensions = dimensions
    self.current_binary = "0"
    self.create_box()

  def create_box(self):
    self.background = pygame.draw.rect(screen, self.bg_colour, pygame.Rect(self.position, self.dimensions))
    border_dimensions = (self.dimensions[0] + 5, self.dimensions[1] + 5)
    box_rect = pygame.Rect((0, 0), border_dimensions)
    box_rect.center = self.background.center
    self.box_border = pygame.draw.rect(screen, self.border_colour, box_rect, 5)
    
    self.font = pygame.font.SysFont(None, 40)
    binary_box_text = self.font.render(self.current_binary, True, self.text_colour)
    binary_box_text_rect = binary_box_text.get_rect()
    binary_box_text_rect.center = self.background.center
    screen.blit(binary_box_text, binary_box_text_rect)
  
  def update_binary(self):
    if self.current_binary == "0":
      self.current_binary = "1"
      self.bg_colour = binary_box_text_colour
      self.text_colour = binary_box_bg_colour
    else:
      self.current_binary = "0"
      self.text_colour = binary_box_text_colour
      self.bg_colour = binary_box_bg_colour
    self.create_box()


positionx = 50
positiony = 50
dimensions = (40, 40)
distance_between = 50

binary_box_1 = binary_box((positionx, positiony), dimensions)
binary_box_2 = binary_box((positionx + distance_between, positiony), dimensions)
binary_box_3 = binary_box((positionx + 2*distance_between, positiony), dimensions)
binary_box_4 = binary_box((positionx + 3*distance_between, positiony), dimensions)
binary_box_5 = binary_box((positionx + 4*distance_between, positiony), dimensions)
binary_box_6 = binary_box((positionx + 5*distance_between, positiony), dimensions)
binary_box_7 = binary_box((positionx + 6*distance_between, positiony), dimensions)
binary_box_8 = binary_box((positionx + 7*distance_between, positiony), dimensions)

pygame.display.flip()

while True:
  for event in pygame.event.get():
    match event.type:
      case pygame.QUIT:
        pygame.quit()
      case pygame.KEYDOWN:
        match event.key:
          case pygame.K_z | pygame.K_a | pygame.K_q | pygame.K_1:
            binary_box_1.update_binary()
          case pygame.K_x | pygame.K_s | pygame.K_w | pygame.K_2:
            binary_box_2.update_binary()
          case pygame.K_c | pygame.K_d | pygame.K_e | pygame.K_3:
            binary_box_3.update_binary()
          case pygame.K_v | pygame.K_f | pygame.K_r | pygame.K_4:
            binary_box_4.update_binary()
          case pygame.K_b | pygame.K_g | pygame.K_t | pygame.K_5:
            binary_box_5.update_binary()
          case pygame.K_n | pygame.K_h | pygame.K_y | pygame.K_6:
            binary_box_6.update_binary()
          case pygame.K_m | pygame.K_j | pygame.K_u | pygame.K_7:
            binary_box_7.update_binary()
          case pygame.K_COMMA | pygame.K_l | pygame.K_o | pygame.K_9:
            binary_box_8.update_binary()

  pygame.display.update()