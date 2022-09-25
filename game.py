from __future__ import annotations
from dataclasses import dataclass , field
import json

def create_teams():
    """Function which loads team data"""
    with open("players.json" , mode = "r+" , encoding = "utf-8") as f:
        team_data = json.load(f).get("Players")

    blue_team = Team("blue" , [Player(**data) for data in team_data.get("blue_team")])
    red_team = Team("red" , [Player(**data) for data in team_data.get("red_team")])
    return blue_team , red_team

@dataclass
class Player:

    health : float
    damage : float
    armor : float
    name : str
    max_health : float = field(init = False , repr = False)
    target : Player = field(init = False , default = None , repr = False)

    def __post_init__(self):
        self.max_health = self.health

    @staticmethod
    def damage_reduction(armor : float , cap : float = 1):
        return 1 - min( cap , armor/(armor + 100)) if armor >= 0 else 0

    def is_alive(self):
        return self.health > 0

    def attack(self):
        self.target.health -= self.damage*Player.damage_reduction(self.target.armor)

@dataclass
class Team:

    name : str
    combatants : list[Player]

    def is_alive(self):
        return any([player.is_alive() for player in self.combatants])

class Game:

    def __init__(self , teams):
        pass

    def start(self):
        pass


if __name__ == "__main__":
    teams = create_teams()
    game = Game(teams)
