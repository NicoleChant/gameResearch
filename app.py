import sys
import numpy as np
from collections import OrderedDict
import argparse

def damage_reduction(armor : float , cap : float = 1) -> float:
    return 1 - min( cap , armor/(armor + 100) ) if armor >= 0.0 else 0.0

def calculate_damage(armor : float , reduced_amount : float , damage : float , history : str) -> float:
    total_damage = 0
    for action in history:
        if action == "a":
            armor -= reduced_amount
        elif action == "d":
            total_damage += damage*damage_reduction(armor)
    return total_damage

def find_sequences(epochs : int) -> list[str]:
    if epochs == 1:
        return ["a","d"]
    else:
        return [seq + action for seq in find_sequences(epochs - 1) for action in ["a","d"] ]

def find_exact_sequences(epochs : int) -> list[str]:
    if epochs == 1:
        return ["a","d"]
    else:
        for seq in find_exact_sequences(epochs - 1):
            if seq.count("a") > max_a:
                return

def find_sequences_improved(epochs : int) -> list[str]:
    return ["a"*i + "d"*(epochs - i) for i in range(epochs) ]

def calculate_all(armor : float , reduced_amount : float , damage : float , epochs : int) -> tuple[str,float]:
    possible_histories = find_sequences_improved(epochs)
    outcomes = []
    for history in possible_histories:
        outcomes.append( (history ,  calculate_damage(armor , reduced_amount , damage , history) ) )
    return max( outcomes , key = lambda x : x[1] )

if __name__ == "__main__":
    armor = 100
    reduced_amount = 10
    damage = 5
    outcomes = {}

    parser = argparse.ArgumentParser()
    parser.add_argument("epochs")

    args = parser.parse_args()
    num_epochs = int(args.epochs)
    epochs = np.arange(1,num_epochs,1)

    for epoch in epochs:
        outcome = calculate_all(armor , reduced_amount , damage , epoch)
        outcomes.update({outcome[0] : outcome[1]})
    print(outcomes)

    active_armor = []
    for key , value in outcomes.items():
        if "a" in key:
            active_armor.append( armor - (key.index("d") - 1)*reduced_amount )
        else:
            active_armor.append( armor )

    import matplotlib.pyplot as plt
    plt.style.use("seaborn")
    plt.plot(active_armor)
    plt.xticks(epochs)
    plt.show()
