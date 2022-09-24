import pygame
pygame.init()

screen = pygame.display.set_mode(size=(500, 400))
screen.fill("grey")

rect_colour = "blue"
rectangle = pygame.draw.rect(screen, rect_colour, pygame.Rect(35, 35, 50, 50))
binary_box_background = pygame.draw.rect(screen, "#06001a", pygame.Rect(150, 150, 70, 70))

binary_rect = pygame.Rect(0, 0, 80, 80)
binary_rect.center = binary_box_background.center
binary_box_border = pygame.draw.rect(screen, "#8c8c8c", binary_rect, 5)

current_binary = "0"
font = pygame.font.SysFont(None, 70)
binary_box_text = font.render(current_binary, True, "white")
binary_box_text_rect = binary_box_text.get_rect()
binary_box_text_rect.center = binary_box_background.center
screen.blit(binary_box_text, binary_box_text_rect)
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
          pygame.draw.rect(screen, rect_colour, pygame.Rect(35, 35, 50, 50))
      case pygame.KEYDOWN:
        if event.key == pygame.K_a:
          if current_binary == "0":
            current_binary = "1"
          else:
            current_binary = "0"
          pygame.draw.rect(screen, "#06001a", pygame.Rect(150, 150, 70, 70))
          binary_box_text = font.render(current_binary, True, "white")
          screen.blit(binary_box_text, binary_box_text_rect)

    pygame.display.update()