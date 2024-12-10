from character import Character
from enemy import Enemy
import random
from discord import Client, Message


class Combat:

    async def choose_craft(self, character: Character):
        for i in range(0, len(character.crafts)):
            await src_channel.send(f"{i}- " + character.crafts[i] + "\n")
        craft_chosen = int(input())
        return character.crafts[craft_chosen].damage

    async def character_turn(self, character: Character):
        await src_channel.send("Choose an action\n"
                               "1-Normal Attack\n"
                               "2-Crafts\n"
                               "3-Arts\n"
                               "4-Items\n")
        option = int(input)
        match option:
            # Normal Attack
            case 1:
                return character.STR
            # Crafts
            case 2:
                return self.choose_craft(character)
            # Arts
            case 3:
                return 0
            # Items
            case 4:
                return 0

    def enemy_turn(self, enemy: Enemy):
        choice = random.randint(0, 2)
        match choice:
            # Normal Attack
            case 0:
                return enemy.STR
            # Random craft
            case _:
                return enemy.crafts[choice]

    async def check_victory(self, enemy: Enemy):
        if enemy.HP <= 0:
            await src_channel.send("You won!\n")
            return True

    async def check_defeat(self, character: Character):
        if character.HP <= 0:
            await src_channel.send("You lost!\n")
            return True

    def start_fight(self, character: Character, enemy: Enemy):
        while character.HP > 0 or enemy.HP > 0:
            if character.SPD >= enemy.SPD:
                enemy.HP -= self.character_turn(character)

                # Check if the enemy is dead
                if self.check_victory(enemy): return

                character.HP -= self.enemy_turn(enemy)

                # Check if the player is dead
                if self.check_defeat(character): return

            else:
                character.HP -= self.enemy_turn(enemy)

                # Check if the player is dead
                if self.check_defeat(character): return
                enemy.HP -= self.character_turn(character)

                # Check if the enemy is dead
                if self.check_victory(enemy): return

        self.check_victory(enemy)
        self.check_defeat(character)
