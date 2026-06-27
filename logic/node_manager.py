from storage import node_repository
from logic import stat_manager
from logic import player_manager
from system import display
import os


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def promotion_check(player, next_node):
    if player["job_rank"] == 0 and player["job_success"] >= 2:
        player["job_rank"] = 1
        player["promotion_return"] = next_node
        return "first_promotion_event"

    if player["job_rank"] == 1 and player["job_success"] >= 4:
        player["job_rank"] = 2
        player["promotion_return"] = next_node
        return "second_promotion_event"

    return next_node


def play_node(player, node_id):
    if node_id == "SETTLER_PROMOTION_CHECK_11":
        return promotion_check(player, "11_settler")

    if node_id == "SETTLER_PROMOTION_CHECK_13":
        return promotion_check(player, "13_settler")

    if node_id == "SETTLER_PROMOTION_CHECK_HEAD":
        return promotion_check(player, "head_conflict")

    if node_id == "PROMOTION_RETURN":
        print("[PROMOTION RETURN HANDLER HIT]")
        print(player["promotion_return"])
        return player["promotion_return"]

    if node_id == "settler_ending_check":
        knowledge = player["knowledge"]
        influence = player["influence"]
        trust = player["trust"]

        if knowledge >= influence and knowledge >= trust:
            return "settler_scholar_ending"

        if influence >= knowledge and influence >= trust:
            return "settler_leader_ending"

        return "settler_community_ending"

    if node_id == "EXPLORER_CLASS_CHECK":
        player_class = player_manager.determine_explorer_class(player)
        player["class"] = player_class
        display.show_class_unlock(player_class)
        return "class_event"

    node = node_repository.get_node(node_id)

    if not node:
        print(f"[BROKEN NODE] {node_id}")
        return "EXIT"

    node_type = node.get("type")

    if node_type not in ["scenario", "event", "ending"]:
        print(f"[INVALID NODE TYPE] {node_id}")
        return "EXIT"

    if node_type == "event":
        display.show_event(node)
        return node.get("next")

    if node_type == "ending":
        display.show_ending(node)
        return "EXIT"

    if node_type == "scenario":
        result = handle_scenario(player, node, node_id)

        if result is None:
            print("[CRITICAL] play_node returned None, forcing EXIT")
            return "EXIT"

        return result


def handle_scenario(player, node, node_id):
    from system import pause_menu

    while True:

        scenario_result = display.show_scenario(
            player,
            node,
            node_id
        )

        choices = node.get("choices", [])

        if scenario_result is None:
            return node_id

        if isinstance(scenario_result, dict):

            action = scenario_result.get("action")

            if action == "pause":

                pause_result = pause_menu.show_pause_menu(
                    player,
                    node_id
                )

                if pause_result == "RESUME":
                    continue

                if pause_result == "EXIT":
                    return "EXIT"

                continue

            elif action == "choice":
                choice_number = scenario_result.get("value")

            elif action == "save":
                pause_menu.show_save_menu(
                    player,
                    node_id
                )
                continue

            elif action == "exit":
                return "EXIT"

            else:
                print("[UNKNOWN SCENARIO ACTION]", scenario_result)
                return node_id

        else:
            choice_number = scenario_result

        if choice_number is None:
            return node_id

        if not isinstance(choice_number, int):
            print("[INVALID CHOICE RETURN]", choice_number)
            return node_id

        if choice_number < 1 or choice_number > len(choices):
            print("Invalid choice")
            return node_id

        selected_choice = choices[choice_number - 1]

        artifact = selected_choice.get("artifact")
        if artifact:
            player["artifact"] = artifact

        if selected_choice.get("job_focus"):
            is_aligned = (
                selected_choice["job_focus"] ==
                player["job_focus"]
            )
            player_manager.register_job_result(
                player,
                is_aligned
            )

        stat = selected_choice.get("stat")
        amount = selected_choice.get("amount", 0)

        stat_manager.apply_stat(
            player,
            stat,
            amount
        )

        job = selected_choice.get("job")

        if job:
            player["job"] = job
            player["job_focus"] = job

        if stat:
            display.show_stat_gain(stat, amount)

        if player_manager.is_dead(player):
            return "DEATH"

        result = selected_choice.get("result")

        if result:
            display.show_result(result)

        artifact_text = node_repository.get_artifact_result(
            selected_choice["id"],
            player.get("artifact")
        )

        if artifact_text:
            display.show_artifact_result(
                artifact_text
            )

        next_node = selected_choice.get("next")

        if next_node is None:
            print("[BROKEN DATA DETECTED]")
            print("Choice was:", selected_choice)
            print("Node was:", node_id)
            return node_id

        return next_node