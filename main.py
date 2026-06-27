import pygame

from storage.database import initialize_database
from system import game


pygame.init()

pygame.display.set_mode(
    (1000, 700),
    pygame.RESIZABLE
)

pygame.display.set_caption("Adventure Game")

initialize_database()

game.run()

pygame.quit()