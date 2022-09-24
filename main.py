import pygame
pygame.init()

screen = pygame.display.set_mode(size=(500, 400))
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
    
    self.font = pygame.font.SysFont(None, 70)
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

binary_box_1 = binary_box((100, 100), (70, 70))

pygame.display.flip()

while True:
  for event in pygame.event.get():
    match event.type:
      case pygame.QUIT:
        pygame.quit()
      # case pygame.MOUSEBUTTONDOWN:
      #   if rectangle.collidepoint(pygame.mouse.get_pos()): 
      case pygame.KEYDOWN:
        if event.key == pygame.K_a:
          binary_box_1.update_binary()

  pygame.display.update()