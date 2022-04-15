import random
level_map = [
'                            ',
'                            ',
'                            ',
' XX    XXX            XX    ',
' XX P                       ',
' XXXX         XX         XX ',
' XXXX       XX              ',
' XX    X  XXXX    XX  XX    ',
'       X  XXXX    XX  XXX   ',
'    XXXX  XXXXXX  XX  XXXX  ',
'XXXXXXXX  XXXXXX  XX  XXXX  ']
n = 1000
for y in range(3,10):
    for x in range(n):
        if random.randint(0,5) == 0:
            level_map[y] = level_map[y] + "X"
        else:
            level_map[y] = level_map[y] + " "

tile_size = 64
screen_width = 1200
screen_height = len(level_map) * tile_size