import pygame

from logic import node_manager, player_manager
from system import display, menu
from storage import save_repository
from storage.database import initialize_database


pygame.init()

screen = pygame.display.set_mode(
    (1000, 700),
    pygame.RESIZABLE
)
pygame.display.set_caption("Adventure Game")

initialize_database()


def run_game(player, current_scenario):
    while current_scenario not in ("EXIT", "DEATH", None):
        current_scenario = node_manager.play_node(player, current_scenario)

        if current_scenario == "DEATH":
            display.show_ending({
                "title": "Game Over",
                "text": "Your journey ends here."
            })
            break

        if current_scenario == "EXIT":
            break

        if current_scenario is None:
            print("[FIXED] prevented None state")
            break


while True:
    choice = menu.show_main_menu()

    if choice == 1:
        name = display.get_player_name()

        player = player_manager.create_player()
        player["name"] = name

        display.show_player(player)

        start_node = "1"
        run_game(player, start_node)

    elif choice == 2:
        selected_slot = menu.show_load_menu()

        if selected_slot == "BACK":
            continue

        save_data = save_repository.load_game(selected_slot)

        if not save_data:
            continue

        if "player" not in save_data:
            continue

        if "current_scenario" not in save_data:
            continue

        player = save_data["player"]
        current_scenario = save_data["current_scenario"]

        display.show_save_preview(player, current_scenario)
        run_game(player, current_scenario)

    elif choice == 3:
        pygame.quit()
        break