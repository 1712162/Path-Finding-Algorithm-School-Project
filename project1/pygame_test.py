import pygame

YELLOW = (255,255,0)
WHITE  = (255,255,255)
screen = pygame.display.set_mode((800, 600))
screen.fill(YELLOW)
pygame.display.update()
pygame.display.set_caption("Test")
running = True
while running :
  pygame.time.delay(1000)
  for event in pygame.event.get(): 
    if event.type == pygame.QUIT:
      running = False
  for i in range(1,10) : pygame.draw.polygon(screen,WHITE,[(i*10,170),(i*10,190),(30,190),(30,170)])
  pygame.display.update()

pygame.quit()
