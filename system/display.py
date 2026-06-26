import pygame

from system import ui


pygame.init()

screen = pygame.display.set_mode(
    (ui.SCREEN_WIDTH, ui.SCREEN_HEIGHT),
    pygame.RESIZABLE
)
pygame.display.set_caption("Adventure Game")


def _clamp_scroll(scroll_y, min_scroll, max_scroll=0):
    if scroll_y > max_scroll:
        return max_scroll
    if scroll_y < min_scroll:
        return min_scroll
    return scroll_y


def _build_dynamic_choice_buttons(choice_texts, panel_rect):
    buttons = []

    panel_padding_x = 24
    panel_bottom_padding = 12
    gap = 10

    button_x = panel_rect.x + panel_padding_x
    button_width = panel_rect.width - panel_padding_x * 2

    y = panel_rect.y + 44

    for index, text in enumerate(choice_texts, start=1):
        button_text = f"{index}. {text}"

        text_height = ui.get_wrapped_text_height(
            button_text,
            ui.CHOICE_FONT,
            button_width - 28,
            line_spacing=4,
            paragraph_spacing=4
        )

        button_height = max(44, text_height + 18)

        button = ui.Button(
            (button_x, y, button_width, button_height),
            button_text,
            style="choice"
        )
        buttons.append(button)

        y += button_height + gap

    total_height = (
        44 +
        sum(button.rect.height for button in buttons) +
        gap * max(0, len(buttons) - 1) +
        panel_bottom_padding
    )

    return buttons, total_height


def _draw_clipped_wrapped_text(screen, text, font, color, rect, scroll_y=0):
    old_clip = screen.get_clip()
    screen.set_clip(rect)

    ui.draw_text_wrapped(
        screen,
        text,
        font,
        color,
        rect,
        scroll_y=scroll_y
    )

    screen.set_clip(old_clip)


def _show_confirmation_popup(title, text, confirm_text="Yes", cancel_text="No"):
    clock = pygame.time.Clock()

    while True:
        screen_width = screen.get_width()
        screen_height = screen.get_height()

        panel_rect = pygame.Rect(
            screen_width // 2 - 300,
            screen_height // 2 - 170,
            600,
            340
        )

        body_rect = pygame.Rect(
            panel_rect.x + 36,
            panel_rect.y + 90,
            panel_rect.width - 72,
            110
        )

        confirm_button = ui.Button(
            (panel_rect.centerx - 160, panel_rect.bottom - 72, 130, 44),
            confirm_text,
            style="small"
        )

        cancel_button = ui.Button(
            (panel_rect.centerx + 30, panel_rect.bottom - 72, 130, 44),
            cancel_text,
            style="small"
        )

        mouse_pos = pygame.mouse.get_pos()
        confirm_button.update(mouse_pos)
        cancel_button.update(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_y):
                    return True
                if event.key in (pygame.K_ESCAPE, pygame.K_n, pygame.K_BACKSPACE):
                    return False

            if confirm_button.handle_event(event):
                return True
            if cancel_button.handle_event(event):
                return False

        ui.draw_background(screen, mode="node")
        ui.draw_panel(screen, panel_rect)

        ui.draw_text(
            screen,
            title,
            ui.HEADING_FONT,
            ui.DANGER,
            panel_rect.centerx,
            panel_rect.y + 48,
            center=True
        )

        ui.draw_text_wrapped(
            screen,
            text,
            ui.BODY_FONT,
            ui.TEXT,
            body_rect
        )

        confirm_button.draw(screen)
        cancel_button.draw(screen)

        pygame.display.flip()
        clock.tick(ui.FPS)


def _show_save_slot_popup(player, current_scenario):
    clock = pygame.time.Clock()

    while True:
        screen_width = screen.get_width()
        screen_height = screen.get_height()

        panel_rect = pygame.Rect(
            screen_width // 2 - 340,
            screen_height // 2 - 220,
            680,
            440
        )

        slot_buttons = [
            ui.Button((panel_rect.centerx - 110, panel_rect.y + 140, 220, 48), "Save to Slot 1", style="menu"),
            ui.Button((panel_rect.centerx - 110, panel_rect.y + 205, 220, 48), "Save to Slot 2", style="menu"),
            ui.Button((panel_rect.centerx - 110, panel_rect.y + 270, 220, 48), "Save to Slot 3", style="menu"),
        ]

        cancel_button = ui.Button(
            (panel_rect.centerx - 90, panel_rect.bottom - 64, 180, 42),
            "Cancel",
            style="small"
        )

        mouse_pos = pygame.mouse.get_pos()
        for button in slot_buttons:
            button.update(mouse_pos)
        cancel_button.update(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 1
                if event.key == pygame.K_2:
                    return 2
                if event.key == pygame.K_3:
                    return 3
                if event.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
                    return None

            for index, button in enumerate(slot_buttons, start=1):
                if button.handle_event(event):
                    return index

            if cancel_button.handle_event(event):
                return None

        ui.draw_background(screen, mode="node")
        ui.draw_panel(screen, panel_rect)

        ui.draw_text(
            screen,
            "SAVE GAME",
            ui.HEADING_FONT,
            ui.GOLD,
            panel_rect.centerx,
            panel_rect.y + 48,
            center=True
        )

        preview = (
            f"{player['name']} | Node: {current_scenario} | "
            f"HP: {player['current_hp']}/{player['max_hp']}"
        )

        ui.draw_text(
            screen,
            preview,
            ui.SMALL_FONT,
            ui.MUTED,
            panel_rect.centerx,
            panel_rect.y + 92,
            center=True
        )

        for button in slot_buttons:
            button.draw(screen)

        cancel_button.draw(screen)

        pygame.display.flip()
        clock.tick(ui.FPS)


def show_message(title, text, title_color=None):
    clock = pygame.time.Clock()
    scroll_y = 0

    while True:
        screen_width = screen.get_width()
        screen_height = screen.get_height()

        panel_rect = pygame.Rect(
            30,
            20,
            screen_width - 60,
            screen_height - 40
        )

        title_rect = pygame.Rect(
            panel_rect.x + 25,
            panel_rect.y + 20,
            panel_rect.width - 50,
            60
        )

        body_rect = pygame.Rect(
            panel_rect.x + 30,
            panel_rect.y + 105,
            panel_rect.width - 60,
            panel_rect.height - 200
        )

        continue_button = ui.Button(
            (
                panel_rect.centerx - 110,
                panel_rect.bottom - 78,
                220,
                48
            ),
            "Continue",
            style="small"
        )

        content_height = ui.get_wrapped_text_height(
            text,
            ui.BODY_FONT,
            body_rect.width
        )

        min_scroll = min(0, body_rect.height - content_height)

        mouse_pos = pygame.mouse.get_pos()
        continue_button.update(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return
                if event.key == pygame.K_UP:
                    scroll_y += 35
                if event.key == pygame.K_DOWN:
                    scroll_y -= 35

            if event.type == pygame.MOUSEWHEEL:
                scroll_y += event.y * 35

            if continue_button.handle_event(event):
                return

        scroll_y = _clamp_scroll(scroll_y, min_scroll)

        ui.draw_background(screen, mode="node")
        ui.draw_panel(screen, panel_rect)

        ui.draw_text(
            screen,
            title,
            ui.HEADING_FONT,
            title_color or ui.TITLE,
            title_rect.centerx,
            title_rect.centery,
            center=True
        )

        pygame.draw.line(
            screen,
            ui.PANEL_BORDER,
            (panel_rect.x + 25, panel_rect.y + 85),
            (panel_rect.right - 25, panel_rect.y + 85),
            2
        )

        _draw_clipped_wrapped_text(
            screen,
            str(text),
            ui.BODY_FONT,
            ui.TEXT,
            body_rect,
            scroll_y=scroll_y
        )

        ui.draw_text(
            screen,
            "Mouse wheel / ↑ ↓ to scroll",
            ui.SMALL_FONT,
            ui.MUTED,
            panel_rect.x + 30,
            panel_rect.bottom - 62
        )

        continue_button.draw(screen)

        pygame.display.flip()
        clock.tick(ui.FPS)


def show_popup(title, text, title_color=None, width=620, min_height=240):
    clock = pygame.time.Clock()

    while True:
        screen_width = screen.get_width()
        screen_height = screen.get_height()

        body_width = width - 80
        content_height = ui.get_wrapped_text_height(
            str(text),
            ui.BODY_FONT,
            body_width
        )

        panel_height = max(min_height, content_height + 170)
        max_height = screen_height - 80
        panel_height = min(panel_height, max_height)

        panel_rect = pygame.Rect(
            (screen_width - width) // 2,
            (screen_height - panel_height) // 2,
            width,
            panel_height
        )

        title_rect = pygame.Rect(
            panel_rect.x + 24,
            panel_rect.y + 18,
            panel_rect.width - 48,
            44
        )

        body_rect = pygame.Rect(
            panel_rect.x + 36,
            panel_rect.y + 82,
            panel_rect.width - 72,
            panel_rect.height - 160
        )

        continue_button = ui.Button(
            (
                panel_rect.centerx - 100,
                panel_rect.bottom - 62,
                200,
                42
            ),
            "Continue",
            style="small"
        )

        mouse_pos = pygame.mouse.get_pos()
        continue_button.update(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return

            if continue_button.handle_event(event):
                return

        ui.draw_background(screen, mode="node")
        ui.draw_panel(screen, panel_rect)

        ui.draw_text(
            screen,
            title,
            ui.HEADING_FONT,
            title_color or ui.TITLE,
            title_rect.centerx,
            title_rect.centery,
            center=True
        )

        pygame.draw.line(
            screen,
            ui.PANEL_BORDER,
            (panel_rect.x + 24, panel_rect.y + 62),
            (panel_rect.right - 24, panel_rect.y + 62),
            2
        )

        ui.draw_text_wrapped(
            screen,
            str(text),
            ui.BODY_FONT,
            ui.TEXT,
            body_rect
        )

        continue_button.draw(screen)

        pygame.display.flip()
        clock.tick(ui.FPS)


def get_player_name():
    clock = pygame.time.Clock()
    name = ""
    max_length = 20

    while True:
        screen_width = screen.get_width()
        screen_height = screen.get_height()

        panel_rect = pygame.Rect(
            screen_width // 2 - 340,
            screen_height // 2 - 210,
            680,
            420
        )

        input_rect = pygame.Rect(
            panel_rect.x + 40,
            panel_rect.y + 140,
            panel_rect.width - 80,
            64
        )

        confirm_button = ui.Button(
            (
                panel_rect.centerx - 110,
                panel_rect.bottom - 80,
                220,
                50
            ),
            "Confirm Name",
            style="menu",
            enabled=bool(name.strip())
        )

        mouse_pos = pygame.mouse.get_pos()
        confirm_button.update(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name.strip():
                    return name.strip()
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if (
                        event.unicode
                        and event.unicode.isprintable()
                        and len(name) < max_length
                    ):
                        name += event.unicode

            if confirm_button.handle_event(event):
                return name.strip()

        ui.draw_background(screen, mode="menu")
        ui.draw_panel(screen, panel_rect)

        ui.draw_text(
            screen,
            "ENTER YOUR NAME",
            ui.HEADING_FONT,
            ui.TITLE,
            panel_rect.centerx,
            panel_rect.y + 55,
            center=True
        )

        ui.draw_text(
            screen,
            "This is the identity your bad decisions will be attached to.",
            ui.SMALL_FONT,
            ui.MUTED,
            panel_rect.centerx,
            panel_rect.y + 95,
            center=True
        )

        pygame.draw.rect(
            screen,
            ui.INPUT_BG,
            input_rect,
            border_radius=12
        )
        pygame.draw.rect(
            screen,
            ui.ACCENT,
            input_rect,
            width=2,
            border_radius=12
        )

        display_name = name if name else "Type here..."
        name_color = ui.TEXT if name else ui.MUTED

        ui.draw_text(
            screen,
            display_name,
            ui.BODY_FONT,
            name_color,
            input_rect.x + 18,
            input_rect.y + 17
        )

        char_count = f"{len(name)}/{max_length}"
        ui.draw_text(
            screen,
            char_count,
            ui.SMALL_FONT,
            ui.MUTED,
            input_rect.right - 70,
            input_rect.bottom + 12
        )

        confirm_button.draw(screen)

        pygame.display.flip()
        clock.tick(ui.FPS)


def show_player(player):
    text = (
        f"Name: {player['name']}\n"
        f"Knowledge: {player['knowledge']}\n"
        f"Influence: {player['influence']}\n"
        f"Trust: {player['trust']}\n"
        f"Skill: {player['skill']}\n"
        f"HP Stat: {player['hp_stat']}\n"
        f"HP: {player['current_hp']}/{player['max_hp']}"
    )

    show_popup("CHARACTER CREATED", text, title_color=ui.ACCENT, width=640, min_height=320)


def show_scenario(player, node, current_scenario):
    clock = pygame.time.Clock()
    choices = node.get("choices", [])

    story_scroll_y = 0
    choice_scroll_y = 0
    active_panel = "story"

    while True:
        screen_width = screen.get_width()
        screen_height = screen.get_height()

        outer_margin = 24

        stat_bar_rect = pygame.Rect(
            outer_margin,
            18,
            screen_width - outer_margin * 2,
            52
        )

        # right-side persistent action panel
        action_panel_width = 210
        gap_between_main_and_side = 16

        main_width = screen_width - outer_margin * 2 - action_panel_width - gap_between_main_and_side

        story_panel_rect = pygame.Rect(
            outer_margin,
            stat_bar_rect.bottom + 14,
            main_width,
            390
        )

        action_panel_rect = pygame.Rect(
            story_panel_rect.right + gap_between_main_and_side,
            story_panel_rect.y,
            action_panel_width,
            screen_height - story_panel_rect.y - 20
        )

        title_rect = pygame.Rect(
            story_panel_rect.x + 24,
            story_panel_rect.y + 16,
            story_panel_rect.width - 48,
            42
        )

        text_rect = pygame.Rect(
            story_panel_rect.x + 28,
            story_panel_rect.y + 72,
            story_panel_rect.width - 56,
            story_panel_rect.height - 118
        )

        story_height = ui.get_wrapped_text_height(
            node["text"],
            ui.BODY_FONT,
            text_rect.width
        )
        story_min_scroll = min(0, text_rect.height - story_height)

        choice_panel_y = story_panel_rect.bottom + 14
        choice_panel_height = screen_height - choice_panel_y - 20

        choice_panel_rect = pygame.Rect(
            outer_margin,
            choice_panel_y,
            main_width,
            choice_panel_height
        )

        buttons, total_choice_content_height = _build_dynamic_choice_buttons(
            [choice["text"] for choice in choices],
            choice_panel_rect
        )

        choice_view_rect = pygame.Rect(
            choice_panel_rect.x + 18,
            choice_panel_rect.y + 42,
            choice_panel_rect.width - 36,
            choice_panel_rect.height - 56
        )

        choice_min_scroll = min(
            0,
            choice_view_rect.height - (total_choice_content_height - 44)
        )

        save_button = ui.Button(
            (action_panel_rect.x + 20, action_panel_rect.y + 80, action_panel_rect.width - 40, 52),
            "Save Game",
            style="menu"
        )

        exit_button = ui.Button(
            (action_panel_rect.x + 20, action_panel_rect.y + 150, action_panel_rect.width - 40, 52),
            "Exit Game",
            style="menu"
        )

        mouse_pos = pygame.mouse.get_pos()

        scrolled_buttons = []
        for button in buttons:
            moved_rect = button.rect.move(0, choice_scroll_y)
            temp_button = ui.Button(
                moved_rect,
                button.text,
                style=button.style,
                enabled=button.enabled
            )
            temp_button.hovered = (
                moved_rect.collidepoint(mouse_pos)
                and choice_view_rect.collidepoint(mouse_pos)
            )
            scrolled_buttons.append(temp_button)

        save_button.update(mouse_pos)
        exit_button.update(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                confirmed = _show_confirmation_popup(
                    "Exit Game?",
                    "Are you sure you want to exit to the main menu without making another choice?"
                )
                if confirmed:
                    return {"action": "exit"}

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    active_panel = "choices" if active_panel == "story" else "story"

                elif event.key == pygame.K_UP:
                    if active_panel == "story":
                        story_scroll_y += 35
                    else:
                        choice_scroll_y += 35

                elif event.key == pygame.K_DOWN:
                    if active_panel == "story":
                        story_scroll_y -= 35
                    else:
                        choice_scroll_y -= 35

                elif event.key == pygame.K_BACKSPACE:
                    confirmed = _show_confirmation_popup(
                        "Exit Game?",
                        "Leave the current run and return to the main menu?",
                        confirm_text="Exit",
                        cancel_text="Stay"
                    )
                    if confirmed:
                        return {"action": "exit"}

                elif event.key == pygame.K_1 and len(choices) >= 1:
                    return {"action": "choice", "value": 1}
                elif event.key == pygame.K_2 and len(choices) >= 2:
                    return {"action": "choice", "value": 2}
                elif event.key == pygame.K_3 and len(choices) >= 3:
                    return {"action": "choice", "value": 3}
                elif event.key == pygame.K_4 and len(choices) >= 4:
                    return {"action": "choice", "value": 4}
                elif event.key == pygame.K_5 and len(choices) >= 5:
                    return {"action": "choice", "value": 5}

            if event.type == pygame.MOUSEWHEEL:
                if active_panel == "story":
                    story_scroll_y += event.y * 35
                else:
                    choice_scroll_y += event.y * 35

            if save_button.handle_event(event):
                slot_id = _show_save_slot_popup(player, current_scenario)
                if slot_id is not None:
                    return {"action": "save", "slot_id": slot_id}

            if exit_button.handle_event(event):
                confirmed = _show_confirmation_popup(
                    "Exit Game?",
                    "Leave the current run and return to the main menu?",
                    confirm_text="Exit",
                    cancel_text="Stay"
                )
                if confirmed:
                    return {"action": "exit"}

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for index, button in enumerate(scrolled_buttons, start=1):
                    if (
                        button.rect.collidepoint(event.pos)
                        and choice_view_rect.collidepoint(event.pos)
                    ):
                        return {"action": "choice", "value": index}

        story_scroll_y = _clamp_scroll(story_scroll_y, story_min_scroll)
        choice_scroll_y = _clamp_scroll(choice_scroll_y, choice_min_scroll)

        ui.draw_background(screen, mode="node")

        ui.draw_game_stat_bar(screen, player, stat_bar_rect)

        # STORY PANEL
        ui.draw_panel(
            screen,
            story_panel_rect,
            border_color=ui.ACCENT if active_panel == "story" else ui.PANEL_BORDER,
            border_width=3 if active_panel == "story" else 2
        )

        ui.draw_text(
            screen,
            node["title"],
            ui.HEADING_FONT,
            ui.TITLE,
            title_rect.centerx,
            title_rect.centery,
            center=True
        )

        pygame.draw.line(
            screen,
            ui.PANEL_BORDER,
            (story_panel_rect.x + 24, story_panel_rect.y + 62),
            (story_panel_rect.right - 24, story_panel_rect.y + 62),
            2
        )

        _draw_clipped_wrapped_text(
            screen,
            node["text"],
            ui.BODY_FONT,
            ui.TEXT,
            text_rect,
            scroll_y=story_scroll_y
        )

        story_hint = "TAB: switch panel | ↑ ↓: scroll"
        story_hint_surface = ui.SMALL_FONT.render(story_hint, True, ui.MUTED)
        screen.blit(
            story_hint_surface,
            (
                story_panel_rect.right - 24 - story_hint_surface.get_width(),
                story_panel_rect.bottom - 12 - story_hint_surface.get_height()
            )
        )

        # CHOICE PANEL
        ui.draw_panel(
            screen,
            choice_panel_rect,
            border_color=ui.ACCENT if active_panel == "choices" else ui.PANEL_BORDER,
            border_width=3 if active_panel == "choices" else 2
        )

        ui.draw_text(
            screen,
            "Choices",
            ui.SMALL_FONT,
            ui.MUTED,
            choice_panel_rect.x + 24,
            choice_panel_rect.y + 12
        )

        old_clip = screen.get_clip()
        screen.set_clip(choice_view_rect)

        for button in scrolled_buttons:
            button.draw(screen)

        screen.set_clip(old_clip)

        # ACTION PANEL
        ui.draw_panel(screen, action_panel_rect, fill_color=ui.PANEL_ALT, border_color=ui.PANEL_BORDER)

        ui.draw_text(
            screen,
            "Menu",
            ui.HEADING_FONT,
            ui.TITLE,
            action_panel_rect.centerx,
            action_panel_rect.y + 34,
            center=True
        )

        save_button.draw(screen)
        exit_button.draw(screen)

        pygame.display.flip()
        clock.tick(ui.FPS)


def show_event(event):
    show_message(event["title"], event["text"])


def show_ending(ending):
    show_message(
        ending["title"],
        ending["text"],
        title_color=ui.DANGER
    )


def show_save_preview(player, current_scenario):
    text = (
        f"{player['name']}\n"
        f"Scenario: {current_scenario}\n"
        f"HP: {player['current_hp']}/{player['max_hp']}"
    )

    show_popup("SAVE FILE", text, title_color=ui.GOLD, width=520, min_height=240)


def show_stats(player):
    text = (
        f"Knowledge: {player['knowledge']}\n"
        f"Influence: {player['influence']}\n"
        f"Trust: {player['trust']}\n"
        f"Skill: {player['skill']}\n"
        f"HP: {player['current_hp']}/{player['max_hp']}"
    )

    show_popup("PLAYER STATS", text, title_color=ui.ACCENT, width=520, min_height=260)


def show_stat_gain(stat, amount):
    show_popup(
        "STAT INCREASED",
        f"{stat.upper()} +{amount}",
        title_color=ui.SUCCESS,
        width=460,
        min_height=220
    )


def show_result(result):
    show_popup(
        "RESULT",
        result,
        title_color=ui.ACCENT,
        width=620,
        min_height=240
    )


def show_artifact_result(result):
    show_popup(
        "ARTIFACT RESULT",
        result,
        title_color=ui.GOLD,
        width=620,
        min_height=240
    )


def show_class_unlock(player_class):
    show_popup(
        "CLASS UNLOCKED",
        player_class,
        title_color=ui.GOLD,
        width=520,
        min_height=220
    )