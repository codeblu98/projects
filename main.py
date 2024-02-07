import pygame
from sprites import *
from config import *
import sys

pygame.display.set_caption("BoardRPG")

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('Arial.ttf', 32)
        self.running = True

        self.character_spritesheet = Spritesheet('img/character.png')
        self.terrain_spritesheet = Spritesheet('img/terrain.png')
        self.enemy_spritesheet = Spritesheet('img/enemies.png')
        self.intro_background = pygame.image.load('./img/introbackground.png')

        self.inventory_window = pygame.Surface((250, 230))
        self.inventory_window.fill((GRAY))

        self.shop_row = None
        self.shop_col = None

        self.player = None

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
            self.draw_shop_window()

            if not self.playing:
            # Reset the player's position if the game is not playing
                self.player.rect.x = 0
                self.player.rect.y = 0
                break 
        
            # Check for player interaction with the shop
            if self.shop_row is not None and self.shop_col is not None:
                shop_tile_position = (
                    self.shop_col * TILESIZE + TILESIZE // 2,
                    self.shop_row * TILESIZE + TILESIZE // 2,
                )
                distance_to_shop = self.calculate_distance(
                    self.player.rect.center, shop_tile_position
                )
            
                if distance_to_shop < TILESIZE:
                    if pygame.mouse.get_pressed()[0]:
                        self.shop.interact()
    def createTilemap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == "V":
                    self.shop = Shop(self, j, i, SHOP_ITEMS)
                    self.shop_row = i  # Store the row of the shop tile
                    self.shop_col = j  # Store the column of the shop tile
                if column == "X":
                    Castle(self, j, i)
                if column == "B":
                    Block(self, j, i)
                if column == "Z":
                    Grass(self, j, i)
                if column == "E":
                    Enemy(self, j, i)
                if column == "P":
                    Player(self, j, i)
                if column == "D":
                    WildDog(self, j, i)
                if column == "S":
                    Slime(self, j, i)
                if column == "W":
                    Wolf(self, j, i)
                if column == "L":
                    Shadowwolf(self, j, i)
                if column == "G":
                    Goblin(self, j, i)
                if column == "T":
                    Bandit(self, j, i)
                if column == "N":
                    Skeleton(self, j, i)
                if column == "A":
                    Garmy(self, j, i)
                if column == "C":
                    Cultist(self, j, i)
                if column == "O":
                    Orc(self, j, i)
                if column == "R":
                    Eliteorc(self, j, i)
                if column == "M":
                    Golem(self, j, i)
                if column == "I":
                    Siren(self, j, i)
                if column == "K":
                    Kraken(self, j, i)
                if column == "H":
                    Hydra(self, j, i)
                if column == "F":
                    Dragon(self, j, i)

        for sprite in self.all_sprites:
            if isinstance(sprite, Player):
                self.player = sprite
                break

    def new(self):
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.createTilemap()

        # Find the player sprite and reset their position within tilemap boundaries
        for sprite in self.all_sprites:
            if isinstance(sprite, Player):
                player_start_pos = self.find_player_start_position() 
                sprite.rect.x = player_start_pos[0]
                sprite.rect.y = player_start_pos[1]


    def find_player_start_position(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                if column == "P":
                    return j * TILESIZE, i * TILESIZE

    # If starting position not found, default to (0, 0)
        return 0, 0
    
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        # Game loop update
        self.all_sprites.update()

    def calculate_distance(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def draw(self):
        self.screen.fill(BLUE)
        self.all_sprites.draw(self.screen)

        player_sprite = None

        # Find the player sprite
        for sprite in self.all_sprites:
            if isinstance(sprite, Player):
                player_sprite = sprite
                break

        if player_sprite:
            player_position = player_sprite.rect.center

            # Check if the player is hovering over the shop tile
            if self.shop_row is not None and self.shop_col is not None:
                shop_tile_position = (
                    self.shop_col * TILESIZE + TILESIZE // 2,
                    self.shop_row * TILESIZE + TILESIZE // 2,
                )
                distance_to_shop = self.calculate_distance(player_position, shop_tile_position)

                if distance_to_shop < TILESIZE:
                    # Display the shop window
                    self.draw_shop_window()

            # Display enemy stats under the enemy sprite
            for sprite in self.all_sprites:
                if isinstance(sprite, Enemy):
                    enemy_position = sprite.rect.center
                    distance = self.calculate_distance(player_position, enemy_position)
                    if distance < 50: 
                        stats_text = f"HP: {sprite.hp}  Atk: {sprite.attack}  Def: {sprite.defence}"
                        stats_font = pygame.font.Font('Arial.ttf', 10)
                        stats_surface = stats_font.render(stats_text, True, BLACK)
                        stats_rect = stats_surface.get_rect(centerx=enemy_position[0], y=enemy_position[1] + 20)
                        self.screen.blit(stats_surface, stats_rect)

            # Display player stats on the bottom left of the screen
            player_stats_text = f"Player HP: {player_sprite.hp}  Attack: {player_sprite.attack}  Defense: {player_sprite.defence}  Gold: {player_sprite.gold}"
            player_stats_font = pygame.font.Font('Arial.ttf', 16)
            player_stats_surface = player_stats_font.render(player_stats_text, True, WHITE)
            player_stats_rect = player_stats_surface.get_rect(topleft=(10, WIN_HEIGHT - 30))
            self.screen.blit(player_stats_surface, player_stats_rect)

        # Draw the inventory window in the bottom right corner
        inventory_x = WIN_WIDTH - self.inventory_window.get_width()
        inventory_y = WIN_HEIGHT - self.inventory_window.get_height()
        self.screen.blit(self.inventory_window, (inventory_x, inventory_y))

        # Render the items and their images in the player's inventory
        inventory_font = pygame.font.Font('Arial.ttf', 10)
        inventory_text_y = inventory_y + 10

        for item in self.player.inventory:
            item_name = item['name']
            item_text = f"- {item_name}"
            item_surface = inventory_font.render(item_text, True, BLACK)
            item_rect = item_surface.get_rect(topleft=(inventory_x + 10, inventory_text_y))
            self.screen.blit(item_surface, item_rect)

            # Load and render the item's image
            item_image_path = item['image']
            item_image = pygame.image.load(item_image_path)
            item_image = pygame.transform.scale(item_image, (16, 16))
            item_image_rect = item_image.get_rect(
                topleft=(inventory_x + 80, inventory_text_y)
            )
            self.screen.blit(item_image, item_image_rect)

            inventory_text_y += 20

        self.clock.tick(FPS)
        pygame.display.update()

    def draw_shop_window(self):
        pygame.draw.rect(self.screen, WHITE, (WIN_WIDTH - 250, 0, 250, 250))
    
        for i, shop_item in enumerate(SHOP_ITEMS):
            item_name = shop_item['name']
            item_cost = shop_item['cost']
            item_image_path = shop_item['image']
            item_image = pygame.image.load(item_image_path)
            item_image = pygame.transform.scale(item_image, (32, 32))
    
            item_rect = item_image.get_rect(
                top=5 + i * 35, right=WIN_WIDTH - 210, width=32, height=32
            )
            self.screen.blit(item_image, item_rect)
    
            font = pygame.font.Font(None, 20)
    
            text_name = font.render(item_name, True, BLACK)
            text_name_rect = text_name.get_rect(
                top=10 + i * 35, left=WIN_WIDTH - 200
            )
            self.screen.blit(text_name, text_name_rect)
    
            text_cost = font.render(f"{item_cost}g", True, GOLDEN)
            text_cost_rect = text_cost.get_rect(
                top=10 + i * 35, left=WIN_WIDTH - 50
            )
            self.screen.blit(text_cost, text_cost_rect)

            # Check if the mouse is over an item in the shop
            mouse_pos = pygame.mouse.get_pos()
            if item_rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, GRAY, item_rect, 2)

            # Check if the mouse is over the buy button for this item
            buy_button_rect = pygame.Rect(WIN_WIDTH - 90, item_rect.top, 80, item_rect.height)
            if buy_button_rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, GRAY, buy_button_rect, 2)

                # Check if the item can be bought
                if self.player.gold >= item_cost:
                    buy_text = font.render("Buy", True, BLACK)
                    self.screen.blit(buy_text, buy_button_rect.move(5, 5))

                    # Check if the mouse is clicked on the buy button
                    if pygame.mouse.get_pressed()[0] and self.player.gold >= item_cost:
                        # Call the buy_from_shop method of the player with the selected item
                        self.player.buy_from_shop([shop_item])

    def game_over(self):
        pass

    def intro_screen(self):
        intro = True

        title = self.font.render('BoardRPG', True, BLACK)
        title_rect = title.get_rect(x=10, y=10)

        play_button = Button(10, 50, 100, 50, WHITE, BLACK, 'Play', 32)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False

            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()