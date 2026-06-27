def create_player():

    return {
        "name": "",

        # core stats
        "knowledge": 0,
        "trust": 0,
        "influence": 0,
        "skill": 0,

        # combat / survival
        "hp_stat": 0,
        "max_hp": 100,
        "current_hp": 100,

        # job system
        "job": None,
        "job_focus": None,
        "job_checks": 0,
        "job_success": 0,
        "job_rank": 0,

        # explorer system
        "artifact": None,
        "class": None,

        "promotion_return": None,
        "route": None
    }

def register_job_result(player, is_aligned):
    player["job_checks"] += 1

    if is_aligned:
        player["job_success"] += 1


def is_dead(player):
    return player["current_hp"] <= 0


def determine_explorer_class(player):
    classes = {
        "Chronicler": player["knowledge"],
        "Emissary": player["trust"],
        "Kingmaker": player["influence"],
        "Pilgrim": player["hp_stat"],
        "Pathfinder": player["skill"]
    }

    return max(classes, key=classes.get)
