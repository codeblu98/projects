import pygame
from config import *
import math
import random
import time

class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0,0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.hp = PLAYER_HP
        self.attack = PLAYER_ATTACK
        self.defence = PLAYER_DEFENCE
        self.gold = PLAYER_GOLD

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 1

        self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.inventory = []

    def update(self):
        self.movement()
        self.animate()
        self.collide_enemy()

        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_RIGHT]:
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_UP]:
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_DOWN]:
            self.y_change += PLAYER_SPEED
            self.facing = 'down'

    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            player_stats = self.hp + self.attack + self.defence
            enemy_stats = hits[0].hp + hits[0].attack + hits[0].defence

            player_percentage = player_stats / (player_stats + enemy_stats)
            enemy_percentage = enemy_stats / (player_stats + enemy_stats)

            player_win = random.random() < player_percentage

            if player_win:
                hits[0].kill()
                self.gold += hits[0].gold_drop
                win_text = f"You won the battle and got {hits[0].gold_drop} gold!"
                win_font = pygame.font.Font('Arial.ttf', 20)
                win_surface = win_font.render(win_text, True, BLACK)
                win_rect = win_surface.get_rect(centerx=self.game.screen.get_width() / 2 - 125, y=self.game.screen.get_height() - 80)
                self.game.screen.blit(win_surface, win_rect)
                pygame.display.update()
                time.sleep(3)
            else:
             # Player loses, display message and reset after a delay
                loss_text = "You lost the battle!"
                loss_font = pygame.font.Font('Arial.ttf', 24)
                loss_surface = loss_font.render(loss_text, True, BLACK)
                loss_rect = loss_surface.get_rect(centerx=self.game.screen.get_width() / 2 - 125, y=self.game.screen.get_height() - 80)
                self.game.screen.blit(loss_surface, loss_rect)
                pygame.display.update()
                time.sleep(3)
            
            # Reset player position to the starting point within the tilemap
                player_start_pos = self.game.find_player_start_position()
                self.rect.x = player_start_pos[0]
                self.rect.y = player_start_pos[1]

                pygame.display.update()

    def collide_blocks(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right

        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.width
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

    def animate(self):
        down_animations = [self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(35, 2, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(68, 2, self.width, self.height)]

        up_animations = [self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(35, 34, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(68, 34, self.width, self.height)]

        left_animations = [self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(35, 98, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(68, 98, self.width, self.height)]

        right_animations = [self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(35, 66, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(68, 66, self.width, self.height)]
        
        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height)
            else:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "up":
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height)
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

    def buy_from_shop(self, items):
        if self.game.shop_row is not None and self.game.shop_col is not None:
            shop_tile_position = (
                self.game.shop_col * TILESIZE + TILESIZE // 2,
                self.game.shop_row * TILESIZE + TILESIZE // 2,
            )
            distance_to_shop = self.game.calculate_distance(self.rect.center, shop_tile_position)

            if distance_to_shop < TILESIZE:
                mouse_pos = pygame.mouse.get_pos()
                relative_mouse_pos = (
                    mouse_pos[0] - (WIN_WIDTH - 250),
                    mouse_pos[1] - self.game.shop.rect.top
                )
            
            # Calculate the clicked item index using integer division and an offset
                clicked_item_index = (relative_mouse_pos[1] + 20) // 35

                if 0 <= clicked_item_index < len(items):
                    selected_item = items[clicked_item_index]

                    if self.gold >= selected_item['cost']:
                        item_already_in_inventory = any(item['name'] == selected_item['name'] for item in self.inventory)

                        if not item_already_in_inventory:
                            self.gold -= selected_item['cost']
                            self.inventory.append(selected_item.copy())
                            # Update player's attack and defense based on the bought item's attributes
                            if 'attack' in selected_item:
                                self.attack += selected_item['attack']
                            if 'defense' in selected_item:
                                self.defence += selected_item['defense']
                            
                            self.game.draw()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.image = self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.hp = 100
        self.attack = 10
        self.defence = 5
        

    def update(self):

        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0

class WildDog(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.hp = 5
        self.attack = 5
        self.defence = 3
        self.gold_drop = random.randint(3,10)
        self.image = self.game.enemy_spritesheet.get_sprite(0.5, 2, self.width, self.height)
        self.image.set_colorkey(WHITE)

class Slime(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.hp = 1
        self.attack = 1
        self.defence = 7
        self.gold_drop = random.randint(5,11)
        self.image = self.game.enemy_spritesheet.get_sprite(32, 2, self.width, self.height)
        self.image.set_colorkey(WHITE)

class Wolf(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.hp = 7
        self.attack = 8
        self.defence = 4
        self.gold_drop = random.randint(8,13)
        self.image = self.game.enemy_spritesheet.get_sprite(64, 2, self.width, self.height)
        self.image.set_colorkey(WHITE)

class Shadowwolf(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.hp = 10
        self.attack = 13
        self.defence = 6
        self.gold_drop = random.randint(10,17)
        self.image = self.game.enemy_spritesheet.get_sprite(96, 2, self.width, self.height)
        self.image.set_colorkey(WHITE)

class Goblin(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.hp = 10
        self.attack = 15
        self.defence = 5
        self.gold_drop = random.randint(11,16)
        self.image = self.game.enemy_spritesheet.get_sprite(128, 2, self.width, self.height)
        self.image.set_colorkey(WHITE)

class Bandit(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.hp = 10
        self.attack = 17
        self.defence = 6
        self.gold_drop = random.randint(12,17)
        self.image = self.game.enemy_spritesheet.get_sprite(160, 2, self.width, self.height)
        self.image.set_colorkey(WHITE)

class Skeleton(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.hp = 14
        self.attack = 19
        self.defence = 7
        self.gold_drop = random.randint(13,18)
        self.image = self.game.enemy_spritesheet.get_sprite(192, 3, self.width, self.height)
        self.image.set_colorkey(WHITE)

class Garmy(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.hp = 40
        self.attack = 50
        self.defence = 15
        self.gold_drop = random.randint(16,20)
        self.image = self.game.enemy_spritesheet.get_sprite(224, 2, self.width, self.height)
        self.image.set_colorkey(WHITE)

class Cultist(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.hp = 30
        self.attack = 70
        self.defence = 20
        self.gold_drop = random.randint(15,20)
        self.image = self.game.enemy_spritesheet.get_sprite(260, 2, self.width, self.height)
        self.image.set_colorkey(WHITE)

class Orc(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.hp = 50
        self.attack = 50
        self.defence = 35
        self.gold_drop = random.randint(16,21)
        self.image = self.game.enemy_spritesheet.get_sprite(292, 2, self.width, self.height)
        self.image.set_colorkey(WHITE)

class Eliteorc(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.hp = 55
        self.attack = 55
        self.defence = 40
        self.gold_drop = random.randint(17,23)
        self.image = self.game.enemy_spritesheet.get_sprite(324, 2, self.width, self.height)
        self.image.set_colorkey(WHITE)

class Golem(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.hp = 90
        self.attack = 60
        self.defence = 60
        self.gold_drop = random.randint(20,30)
        self.image = self.game.enemy_spritesheet.get_sprite(356, 2, self.width, self.height)
        self.image.set_colorkey(WHITE)

class Siren(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.hp = 60
        self.attack = 100
        self.defence = 55
        self.gold_drop = random.randint(22,33)
        self.image = self.game.enemy_spritesheet.get_sprite(388, 2, self.width, self.height)
        self.image.set_colorkey(WHITE)

class Kraken(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.hp = 100
        self.attack = 110
        self.defence = 95
        self.gold_drop = random.randint(25,37)
        self.image = self.game.enemy_spritesheet.get_sprite(420, 2, self.width, self.height)
        self.image.set_colorkey(WHITE)

class Hydra(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.hp = 130
        self.attack = 110
        self.defence = 100
        self.gold_drop = random.randint(30,45)
        self.image = self.game.enemy_spritesheet.get_sprite(452, 2, self.width, self.height)
        self.image.set_colorkey(WHITE)

class Dragon(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.hp = 180
        self.attack = 150
        self.defence = 120
        self.gold_drop = random.randint(40,60)
        self.image = self.game.enemy_spritesheet.get_sprite(484, 2, self.width, self.height)
        self.image.set_colorkey(WHITE)

class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(24, 642, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Grass(Block):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.image = self.game.terrain_spritesheet.get_sprite(32, 810, self.width, self.height)



class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(64, 352, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Shop(pygame.sprite.Sprite):
    def __init__(self, game, x, y, items):
        self.game = game
        self._layer = SHOP_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.image = pygame.image.load('img/shop.png')
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.items = items

    def interact(self):
        self.game.player.buy_from_shop(self.items)
class Castle(Ground):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)

class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font('Arial.ttf', fontsize)
        self.content = content

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fg = fg
        self.bg = bg

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False
