#!/usr/bin/env python3
# @author Nathan Ulmen
from Helper_Functions import prompt_for_float, list_prompt, prompt_for_int
from CLI import CLI_Upgrade_Strategies

# BundledEffect = ("ore.forge.Strategies.OreEffects.BundledEffect", "Bundled Effect", 0, '')
# burning = ("ore.forge.Strategies.OreEffects.Burning", "Burning", 1,
#            "Ore is lit on fire, causing its temperature to increase over time. Ore is doomed/destroyed when effect ends/runs out")
# FrostBite = ("ore.forge.Strategies.OreEffects.FrostBite", "FrostBite", 2,
#              'Ore is slowed down while under the effect and has its temperature decreased.')
# invincible = ("ore.forge.Strategies.OreEffects.Invulnerability", "Invulnerability", 3,
#               "While under the influence of this effect Ore is invincible.")
# upgrade_over_time = ("ore.forge.Strategies.OreEffects.UpgradeOverTimeEffect", "Upgrade Over Time Effect", 4,
#                      "The selected upgrade is applied to the ore on the interval that you specify.")

bundled_effect = (1, "Bundled Effect", "Used to bundle up multiple different effects into one.",
                  "ore.forge.Strategies.OreEffects.BundledOreEffect")

burning = (2, "Burning",
           "Ore is lit on fire, causing its temperature to increase over time. Ore is doomed/destroyed when this effect expires.",
           "ore.forge.Strategies.OreEffects.Burning")

frost_bite = (3, "Frost Bite", "Ore is frozen, causing it to be slowed down and its temperature decreased.",
              "ore.forge.Strategies.OreEffects.FrostBite")

invincible = (4, "Invulnerability",
              "While under the influence of this effect the ore, the ore is saved from a doomed state as long as there are charges left",
              "ore.forge.Strategies.OreEffects.Invulnerability")

upgrade_over_time = (5, "Upgrade Over Time", "Applies an upgrade to the ore on an interval.",
                     "ore.forge.Strategies.OreEffects.UpgradeOreEffect")

effects = [bundled_effect, burning, frost_bite, invincible, upgrade_over_time]


def prompt_for_ore_strategy(prompt, can_return_zero):
    while True:
        effect = list_prompt(effects, prompt, can_return_zero)
        if effect == 0 and can_return_zero:
            return "null"
        if effect == bundled_effect:
            return create_bundled_effect()
        elif effect == burning or effect == frost_bite:
            return create_basic_strategy(effect)
        elif effect == invincible:
            return create_invulnerability_effect()
        elif effect == upgrade_over_time:
            return create_upgrade_over_time_effect()


# TODO: Update so that its not limited to only 4 values.
def create_bundled_effect():
    count = 1
    bundle = {
        "effectName": bundled_effect[3],
        "effect" + str(count): prompt_for_ore_strategy("What would you like + effect " + str(count) + " to be? ",
                                                       False),
    }
    while True:
        count += 1
        result = prompt_for_ore_strategy("What would you like effect" + str(count) + "to be? ", True)
        if result == "null":
            return bundle
        else:
            bundle["effect" + str(count)] = result


def create_basic_strategy(effect):
    data = {
        "effectName": effect[3],
        "duration": prompt_for_float("How long would you like" + effect[1] + " to last? "),
    }

    if effect is frost_bite:
        data["tempDecrease"] = prompt_for_float(
            "How much would you like the ore's temperature to decrease each second? ")
    elif effect is burning:
        data["tempIncrease"] = prompt_for_float(
            "How much would you like the ore's temperature to increase each second? ")

    return data


def create_upgrade_over_time_effect():
    data = {
        "effectName": upgrade_over_time[3],
        "upgrade": Upgrade_Strategies.prompt_for_upg_type("Which upgrade would you like this effect to apply? ", False),
        "duration": prompt_for_float("How long would you like this effect to last? "),
        "interval": prompt_for_float("Enter the interval that you want the upgrade to applied on: ")
    }

    return data


def create_invulnerability_effect():
    data = {
        "effectName": invincible[3],
        "charges": prompt_for_int("How many charges do you want this effect to have? "),
        "duration": prompt_for_float("How long would you like this invulnerability effect to last? ")
    }

    return data
