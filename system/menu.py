import pygame

from system import display, ui
from storage import save_repository


def show_main_menu():
    screen = display.screen
    clock = pygame.time.Clock()

    while True:
        screen_width = screen.get_width()
        screen_height = screen.get_height()

        panel_width = 700
        panel_height = 460
        panel_rect = pygame.Rect(
            (screen_width - panel_width) // 2,
            (screen_height - panel_height) // 2,
            panel_width,
            panel_height
        )

        title_y = panel_rect.y + 70
        button_width = 280
        button_height = 58
        button_x = panel_rect.centerx - button_width // 2
        first_button_y = panel_rect.y + 170
        button_gap = 22

        new_game_button = ui.Button(
            (button_x, first_button_y, button_width, button_height),
            "New Game",
            style="menu"
        )

        load_game_button = ui.Button(
            (
                button_x,
                first_button_y + button_height + button_gap,
                button_width,
                button_height
            ),
            "Load Game",
            style="menu"
        )

        exit_button = ui.Button(
            (
                button_x,
                first_button_y + (button_height + button_gap) * 2,
                button_width,
                button_height
            ),
            "Exit",
            style="menu"
        )

        buttons = [
            (new_game_button, 1),
            (load_game_button, 2),
            (exit_button, 3)
        ]

        mouse_pos = pygame.mouse.get_pos()
        for button, _ in buttons:
            button.update(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 3

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 1
                if event.key == pygame.K_2:
                    return 2
                if event.key == pygame.K_3:
                    return 3

            for button, value in buttons:
                if button.handle_event(event):
                    return value

        ui.draw_background(screen, mode="menu")

        ui.draw_panel(
            screen,
            panel_rect,
            fill_color=ui.PANEL,
            border_color=ui.PANEL_BORDER,
            border_width=2
        )

        ui.draw_text(
            screen,
            "ADVENTURE GAME",
            ui.TITLE_FONT,
            ui.TITLE,
            panel_rect.centerx,
            title_y,
            center=True
        )

        ui.draw_text(
            screen,
            "Choose your path into suffering.",
            ui.SMALL_FONT,
            ui.MUTED,
            panel_rect.centerx,
            title_y + 50,
            center=True
        )

        for button, _ in buttons:
            button.draw(screen)

        pygame.display.flip()
        clock.tick(ui.FPS)


def show_load_menu():
    screen = display.screen
    clock = pygame.time.Clock()

    while True:
        screen_width = screen.get_width()
        screen_height = screen.get_height()

        panel_width = 700
        panel_height = 520
        panel_rect = pygame.Rect(
            (screen_width - panel_width) // 2,
            (screen_height - panel_height) // 2,
            panel_width,
            panel_height
        )

        title_y = panel_rect.y + 60
        button_width = 360
        button_height = 56
        button_x = panel_rect.centerx - button_width // 2
        first_button_y = panel_rect.y + 150
        button_gap = 18

        slot_1_button = ui.Button(
            (button_x, first_button_y, button_width, button_height),
            "Save Slot 1",
            style="menu"
        )

        slot_2_button = ui.Button(
            (
                button_x,
                first_button_y + (button_height + button_gap),
                button_width,
                button_height
            ),
            "Save Slot 2",
            style="menu"
        )

        slot_3_button = ui.Button(
            (
                button_x,
                first_button_y + (button_height + button_gap) * 2,
                button_width,
                button_height
            ),
            "Save Slot 3",
            style="menu"
        )

        back_button = ui.Button(
            (
                button_x,
                first_button_y + (button_height + button_gap) * 3 + 10,
                button_width,
                button_height
            ),
            "Back",
            style="menu"
        )

        buttons = [
            (slot_1_button, 1),
            (slot_2_button, 2),
            (slot_3_button, 3),
            (back_button, "BACK")
        ]

        mouse_pos = pygame.mouse.get_pos()
        for button, _ in buttons:
            button.update(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "BACK"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 1
                if event.key == pygame.K_2:
                    return 2
                if event.key == pygame.K_3:
                    return 3
                if event.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
                    return "BACK"

            for button, value in buttons:
                if button.handle_event(event):
                    return value

        ui.draw_background(screen, mode="menu")

        ui.draw_panel(
            screen,
            panel_rect,
            fill_color=ui.PANEL,
            border_color=ui.PANEL_BORDER,
            border_width=2
        )

        ui.draw_text(
            screen,
            "LOAD GAME",
            ui.HEADING_FONT,
            ui.TITLE,
            panel_rect.centerx,
            title_y,
            center=True
        )

        ui.draw_text(
            screen,
            "Choose a save slot.",
            ui.SMALL_FONT,
            ui.MUTED,
            panel_rect.centerx,
            title_y + 42,
            center=True
        )

        for button, _ in buttons:
            button.draw(screen)

        pygame.display.flip()
        clock.tick(ui.FPS)

def show_new_game_slot_menu():
    screen = display.screen
    clock = pygame.time.Clock()

    while True:
        screen_width = screen.get_width()
        screen_height = screen.get_height()

        panel_width = 700
        panel_height = 520

        panel_rect = pygame.Rect(
            (screen_width - panel_width) // 2,
            (screen_height - panel_height) // 2,
            panel_width,
            panel_height
        )

        title_y = panel_rect.y + 60

        button_width = 420
        button_height = 56
        button_x = panel_rect.centerx - button_width // 2
        first_button_y = panel_rect.y + 145
        button_gap = 18

        buttons = []

        for slot in (1, 2, 3):

            save = save_repository.load_game(slot)

            if save:
                text = f"Slot {slot} - {save['player']['name']}"
            else:
                text = f"Slot {slot} - Empty"

            button = ui.Button(
                (
                    button_x,
                    first_button_y + (slot - 1) * (button_height + button_gap),
                    button_width,
                    button_height
                ),
                text,
                style="menu"
            )

            buttons.append((button, slot))

        back_button = ui.Button(
            (
                button_x,
                first_button_y + 3 * (button_height + button_gap) + 10,
                button_width,
                button_height
            ),
            "Back",
            style="menu"
        )

        buttons.append((back_button, "BACK"))

        mouse_pos = pygame.mouse.get_pos()

        for button, _ in buttons:
            button.update(mouse_pos)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return "BACK"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 1
                if event.key == pygame.K_2:
                    return 2
                if event.key == pygame.K_3:
                    return 3
                if event.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
                    return "BACK"

            for button, value in buttons:

                if button.handle_event(event):

                    if value == "BACK":
                        return "BACK"

                    save = save_repository.load_game(value)

                    if save:
                        overwrite = display._show_confirmation_popup(
                            "Overwrite Save?",
                            f"Slot {value} already contains {save['player']['name']}.\n\nStart a new game anyway?",
                            confirm_text="Overwrite",
                            cancel_text="Cancel"
                        )

                        if not overwrite:
                            break

                    return value

        ui.draw_background(screen, "menu")

        ui.draw_panel(screen, panel_rect)

        ui.draw_text(
            screen,
            "NEW GAME",
            ui.HEADING_FONT,
            ui.TITLE,
            panel_rect.centerx,
            title_y,
            center=True
        )

        ui.draw_text(
            screen,
            "Choose a save slot.",
            ui.SMALL_FONT,
            ui.MUTED,
            panel_rect.centerx,
            title_y + 42,
            center=True
        )

        for button, _ in buttons:
            button.draw(screen)

        pygame.display.flip()
        clock.tick(ui.FPS)