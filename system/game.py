import pygame

from logic import node_manager, player_manager
from storage import save_repository
from system import display, menu


def run_game(player, current_scenario):
    while current_scenario not in ("EXIT", "DEATH", None):

        current_scenario = node_manager.play_node(
            player,
            current_scenario
        )

        if current_scenario == "DEATH":
            display.show_ending({
                "title": "Game Over",
                "text": "Your journey ends here."
            })
            break

        if current_scenario in ("EXIT", None):
            break


def new_game():
    player = player_manager.create_player()

    slot = menu.show_new_game_slot_menu()

    if slot == "BACK":
        return

    player["save_slot"] = slot
    player["name"] = display.get_player_name()
    

    if slot == "BACK":
        return

    display.show_player(player)

    save_repository.save_game(
        player,
        "1",
        slot
    )

    run_game(player, "1")

    player["save_slot"] = slot

def load_game():
    player = new_game.player
    slot = menu.show_load_menu()

    if slot == "BACK":
        return

    save = save_repository.load_game(slot)

    if not save:
        return

    display.show_save_preview(
        save["player"],
        save["current_scenario"]
    )

    run_game(
        save["player"],
        save["current_scenario"]
    )

    player["save_slot"] = slot


def run():
    while True:

        match menu.show_main_menu():

            case 1:
                new_game()

            case 2:
                load_game()

            case 3:
                return