#!/usr/bin/env python3
# @author Nathan Ulmen
from Helper_Functions import prompt_for_int, prompt_for_float
import Upgrade_Strategies

BundledEffect = ("ore.forge.Strategies.OreEffects.BundledEffect", "Bundled Effect", 0, '')
burning = ("ore.forge.Strategies.OreEffects.Burning", "Burning", 1,
           "Ore is lit on fire, causing its temperature to increase over time. Ore is doomed/destroyed when effect ends/runs out")
FrostBite = ("ore.forge.Strategies.OreEffects.FrostBite", "FrostBite", 2,
             'Ore is slowed down while under the effect and has its temperature decreased.')
invincible = ("ore.forge.Strategies.OreEffects.Invulnerability", "Invulnerability", 3,
              "While under the influence of this effect Ore is invincible.")
upgrade_over_time = ("ore.forge.Strategies.OreEffects.UpgradeOverTimeEffect", "Upgrade Over Time Effect", 4,
                     "The selected upgrade is applied to the ore on the interval that you specify.")

effects = [BundledEffect, burning, FrostBite, invincible, upgrade_over_time]


def prompt_for_ore_strategy():
    while True:
        print()
        for effect in effects:
            print(effect[2], "-", effect[1], "\t", effect[3])
        user_input = prompt_for_int("Which type of effect do you want? ")
        if user_input == 0:
            return "null"
        for effect in effects:
            if user_input == effect[2]:
                if effect == BundledEffect:
                    return create_bundled_effect()
                elif effect == burning or effect == FrostBite:
                    return create_basic_strategy(effect)
                elif effect == invincible:
                    bundle = {"name": invincible[0]}
                    return bundle
                elif effect == upgrade_over_time:
                    return create_upgrade_over_time_effect()
        print(user_input, " is an invalid input")


def create_bundled_effect():
    bundle = {
        "effectName": BundledEffect[0],
        "effect1": prompt_for_ore_strategy(),
    }

    if bundle["effect1"] == "null":
        del bundle["effect1"]
        return bundle

    bundle["effect2"] = prompt_for_ore_strategy()
    if bundle["effect2"] == "null":
        del bundle["effect2"]
        return bundle

    bundle["effect3"] = prompt_for_ore_strategy()
    if bundle["effect3"] == "null":
        del bundle["effect3"]
        return bundle

    bundle["effect4"] = prompt_for_ore_strategy()
    if bundle["effect4"] == "null":
        del bundle["effect4"]

    return bundle


def create_basic_strategy(effect):
    data = {
        "effectName": effect[0],
        "duration": prompt_for_float("How long would you like" + effect[1] + " to last? "),
    }

    if effect is FrostBite:
        data["tempDecrease"] = prompt_for_float(
            "How much would you like the ore's temperature to decrease each second? ")
    elif effect is burning:
        data["tempIncrease"] = prompt_for_float(
            "How much would you like the ore's temperature to increase each second? ")

    return data


def create_upgrade_over_time_effect():
    data = {
        "effectName": upgrade_over_time[0],
        "upgrade": Upgrade_Strategies.prompt_for_upg_type("Which upgrade would you like this effect to apply? "),
        "duration": prompt_for_float("How long would you like this effect to last? "),
        "interval": prompt_for_float("Enter the interval that you want the upgrade to applied on: ")
    }

    return data
