def apply_stat(player, stat, amount):
    if not stat:
        return

    if stat == "hp_stat":
        player["hp_stat"] += amount

        hp_gain = amount * 25
        player["max_hp"] += hp_gain
        player["current_hp"] += hp_gain
    else:
        player[stat] += amount