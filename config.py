WIN_WIDTH = 640
WIN_HEIGHT = 480
TILESIZE = 32
FPS = 60

PLAYER_LAYER = 5
ENEMY_LAYER = 4
BLOCK_LAYER = 3
SHOP_LAYER = 2
GROUND_LAYER = 1

PLAYER_HP = 10
PLAYER_ATTACK = 10
PLAYER_DEFENCE = 5
PLAYER_GOLD = 300
PLAYER_SPEED = 1


RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
GOLDEN = (219, 172, 52)

tilemap = [
    'BBBBBBBBBBBB',
    'BPV........B',
    'B.ZZZZZZZZZB',
    'BD.S.W.L...B',
    'B.ZZZZZZZZZB',
    'BG.T.N.A...B',
    'B.ZZZZZZZZZB',
    'BC.O.R.M...B',
    'B.ZZZZZZZZZB',
    'BI.K.H.F..XB',
    'BBBBBBBBBBBB',
    ]

SHOP_ITEMS = [
    {'name': 'Wooden Sword', 'image': 'img/shop/sword1.png', 'cost': 10, 'type': 'sword', 'attack': 5},
    {'name': 'Stone Sword', 'image': 'img/shop/sword2.png', 'cost': 20, 'type': 'sword', 'attack': 30},
    {'name': 'Iron Sword', 'image': 'img/shop/sword3.png', 'cost': 30, 'type': 'sword', 'attack': 60},
    {'name': 'Long Sword', 'image': 'img/shop/sword4.png', 'cost': 40, 'type': 'sword', 'attack': 200},
    {'name': 'Wooden Shield', 'image': 'img/shop/shield1.png', 'cost': 15, 'type': 'shield', 'defense': 10},
    {'name': 'Iron Shield', 'image': 'img/shop/shield2.png', 'cost': 25, 'type': 'shield', 'defense': 70},
    {'name': 'Diamond Shield', 'image': 'img/shop/shield3.png', 'cost': 35, 'type': 'shield', 'defense': 120},
]