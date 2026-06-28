import pygame

from system import display, ui
from storage import save_repository


def show_pause_menu(player, current_scenario):
    screen = display.screen
    clock = pygame.time.Clock()

    while True:

        screen_width = screen.get_width()
        screen_height = screen.get_height()

        panel_rect = pygame.Rect(
            (screen_width - 600) // 2,
            (screen_height - 420) // 2,
            600,
            420
        )

        button_width = 280
        button_height = 56
        button_x = panel_rect.centerx - button_width // 2
        first_y = panel_rect.y + 120
        gap = 18

        resume_button = ui.Button(
            (button_x, first_y, button_width, button_height),
            "Resume",
            style="menu"
        )

        save_button = ui.Button(
            (
                button_x,
                first_y + button_height + gap,
                button_width,
                button_height
            ),
            "Save Game",
            style="menu"
        )

        exit_button = ui.Button(
            (
                button_x,
                first_y + (button_height + gap) * 2,
                button_width,
                button_height
            ),
            "Exit to Menu",
            style="menu"
        )

        buttons = [
            (resume_button, "RESUME"),
            (save_button, "SAVE"),
            (exit_button, "EXIT")
        ]

        mouse_pos = pygame.mouse.get_pos()

        for button, _ in buttons:
            button.update(mouse_pos)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return "EXIT"

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    return "RESUME"

                if event.key == pygame.K_1:
                    return "RESUME"

                if event.key == pygame.K_2:
                    show_save_menu(player, current_scenario)

                if event.key == pygame.K_3:
                    return "EXIT"

            for button, action in buttons:

                if button.handle_event(event):

                    if action == "RESUME":
                        return "RESUME"

                    if action == "SAVE":
                        show_save_menu(
                            player,
                            current_scenario
                        )

                    if action == "EXIT":
                        return "EXIT"

        ui.draw_background(screen, mode="node")

        ui.draw_panel(screen, panel_rect)

        ui.draw_text(
            screen,
            "GAME PAUSED",
            ui.HEADING_FONT,
            ui.TITLE,
            panel_rect.centerx,
            panel_rect.y + 55,
            center=True
        )

        for button, _ in buttons:
            button.draw(screen)

        pygame.display.flip()
        clock.tick(ui.FPS)


def show_save_menu(player, current_scenario):
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

        buttons = []

        for slot in (1, 2, 3):

            existing = save_repository.load_game(slot)

            text = f"Save Slot {slot}"

            if existing:
                text += f" ({existing['player']['name']})"

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

        cancel_button = ui.Button(
            (
                button_x,
                first_button_y + 3 * (button_height + button_gap) + 10,
                button_width,
                button_height
            ),
            "Cancel",
            style="menu"
        )

        buttons.append((cancel_button, "BACK"))

        mouse_pos = pygame.mouse.get_pos()

        for button, _ in buttons:
            button.update(mouse_pos)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    return

                if event.key == pygame.K_1:
                    value = 1
                elif event.key == pygame.K_2:
                    value = 2
                elif event.key == pygame.K_3:
                    value = 3
                else:
                    continue

                existing = save_repository.load_game(value)

                if existing:
                    confirm = display._show_confirmation_popup(
                        "Overwrite Save?",
                        f"Slot {value} already contains {existing['player']['name']}.\n\nOverwrite this save?",
                        confirm_text="Overwrite",
                        cancel_text="Cancel"
                    )

                    if not confirm:
                        continue

                save_repository.save_game(
                    player,
                    current_scenario,
                    value
                )

                display.show_message(
                    "Game Saved",
                    f"Saved to Slot {value}"
                )

                return

        ui.draw_background(screen, "menu")

        ui.draw_panel(screen, panel_rect)

        ui.draw_text(
            screen,
            "SAVE GAME",
            ui.HEADING_FONT,
            ui.TITLE,
            panel_rect.centerx,
            title_y,
            center=True
        )

        for button, _ in buttons:
            button.draw(screen)

        pygame.display.flip()
        clock.tick(ui.FPS)