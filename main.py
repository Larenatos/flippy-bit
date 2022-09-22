import pygame
pygame.init()

pygame.display.set_mode(size=(500, 400))
surface = pygame.display.get_surface()


pygame.draw.rect(surface, "yellow", pygame.Rect(30, 30, 60, 60), 5)
pygame.draw.rect(surface, "blue", pygame.Rect(35, 35, 50, 50))
pygame.display.flip()

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT: pygame.quit()