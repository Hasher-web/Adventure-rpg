import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Adventure Game")

title_font = pygame.font.Font(None, 60)
text_font = pygame.font.Font(None, 32)
choice_font = pygame.font.Font(None, 28)


def show_scenario(node):

    choices = node.get("choices", [])

    running = True

    while running:

        # EVENTS
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_1 and len(choices) >= 1:
                    return 1

                if event.key == pygame.K_2 and len(choices) >= 2:
                    return 2

                if event.key == pygame.K_3 and len(choices) >= 3:
                    return 3

                if event.key == pygame.K_4 and len(choices) >= 4:
                    return 4

                if event.key == pygame.K_5 and len(choices) >= 5:
                    return 5

        # CLEAR SCREEN
        screen.fill((121, 171, 228))

        # CREATE SURFACES
        title_surface = title_font.render(
            node["title"],
            True,
            (255, 255, 255)
        )

        text_surface = text_font.render(
            node["text"],
            True,
            (255, 255, 255)
        )

        # DRAW TITLE
        screen.blit(title_surface, (50, 30))

        # DRAW STORY TEXT
        screen.blit(text_surface, (50, 100))

        # DRAW CHOICES
        y = 300

        for i, choice in enumerate(choices, 1):

            choice_surface = choice_font.render(
                f"{i}. {choice['text']}",
                True,
                (255, 255, 255)
            )

            screen.blit(choice_surface, (50, y))

            y += 40

        # UPDATE WINDOW
        pygame.display.flip()