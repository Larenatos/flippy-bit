import pygame
pygame.init()

pygame.display.set_mode(size=(500, 400))
surface = pygame.display.get_surface()

rect_colour = "blue"
pygame.draw.rect(surface, "yellow", pygame.Rect(30, 30, 60, 60), 5)
rectangle = pygame.draw.rect(surface, rect_colour, pygame.Rect(35, 35, 50, 50))
pygame.display.flip()

while True:
  for event in pygame.event.get():
    match event.type:
      case pygame.QUIT:
        pygame.quit()
      case pygame.MOUSEBUTTONDOWN:
        if rectangle.collidepoint(pygame.mouse.get_pos()):
          if rect_colour == "blue":
            rect_colour = "red"
          else:
            rect_colour = "blue"
          pygame.draw.rect(surface, rect_colour, pygame.Rect(35, 35, 50, 50))
          pygame.display.update()