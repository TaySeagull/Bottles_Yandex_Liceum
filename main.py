import pygame
import random
import itertools
import sys
import os


FPS = 50
GRAVITY = 1
screen_rect = (0, 0, 860, 600)
pygame.init()
size = 860, 600
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Бутылочки")


def load_image(name: str, color_key=None):
    """
    param name: the name of the file
    param color_key: color key
    return: picture
    Is used to load the picture
    """
    thename = f"data/{name}"
    try:
        image = pygame.image.load(thename)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


# dictionary of pictures
tile_images = {
    'end': load_image("end_background.jpeg"),
    'background': load_image("back_start.jpg"),
    'black': load_image("black_tile_new.jpg"),
    'clear': load_image("clear_tile_new.jpg"),
    'yellow': load_image("yellow_tile_new.jpg"),
    'blue': load_image("blue_tile_new.jpg"),
    'orange': load_image("orange_tile_new.jpg"),
    'green': load_image("green_tile_new.jpg"),
    'pink': load_image("pink_tile_new.jpg")}

# dictionary of coordinates for water in level 1
bottles_dict_1 = {"bottle_1": [(2, 4), (2, 5), (2, 6), (2, 7), (2, 8)],
                  "bottle_2": [(5, 4), (5, 5), (5, 6), (5, 7), (5, 8)],
                  "bottle_3": [(8, 4), (8, 5), (8, 6), (8, 7), (8, 8)]}

# dictionary of colors of water in level 1
colors_dict_1 = {"bottle_1": ["clear", "yellow", "blue", "yellow", "blue"],
                 "bottle_2": ["clear", "blue", "yellow", "blue", "yellow"],
                 "bottle_3": ["clear", "clear", "clear", "clear", "clear"]}

# dictionary of coordinates for water in level 2
bottles_dict_2 = {"bottle_1": [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5)],
                  "bottle_2": [(3, 1), (3, 2), (3, 3), (3, 4), (3, 5)],
                  "bottle_3": [(5, 1), (5, 2), (5, 3), (5, 4), (5, 5)],
                  "bottle_4": [(7, 1), (7, 2), (7, 3), (7, 4), (7, 5)],
                  "bottle_5": [(1, 8), (1, 9), (1, 10), (1, 11), (1, 12)],
                  "bottle_6": [(4, 8), (4, 9), (4, 10), (4, 11), (4, 12)],
                  "bottle_7": [(7, 8), (7, 9), (7, 10), (7, 11), (7, 12)]}

# dictionary of colors of water in level 2
colors_dict_2 = {"bottle_1": ["clear", "green", "pink", "green", "blue"],
                 "bottle_2": ["clear", "orange", "orange", "orange", "yellow"],
                 "bottle_3": ["clear", "orange", "green", "yellow", "pink"],
                 "bottle_4": ["clear", "pink", "yellow", "pink", "green"],
                 "bottle_5": ["clear", "yellow", "blue", "blue", "blue"],
                 "bottle_6": ["clear", "clear", "clear", "clear", "clear"],
                 "bottle_7": ["clear", "clear", "clear", "clear", "clear"]}


class SpriteGroup(pygame.sprite.Group):
    """
    Is used for Sprites
    """
    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for sprite in self:
            sprite.get_event(event)


class Sprite(pygame.sprite.Sprite):
    """
    Is used for Sprites
    """
    def __init__(self, *groups):
        super().__init__(*groups)
        self.rect = None

    def get_event(self, event):
        pass


tile_width = tile_height = 45
sprite_group = SpriteGroup()
all_sprites = SpriteGroup()


def start_screen():
    """
    Is used to start the game
    """
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Вам предстоит перемешать воду в колбочки.",
                  "Удачи!",
                  "Представлены следующие уровни в порядке очереди:",
                  "Легкий",
                  "Средний",
                  "ВНИМАНИЕ!",
                  "После запуска окна нужно подождать,",
                  "пока ответит pygame",
                  "обещаю, что он ответит (за всё)"]

    fon = pygame.transform.scale(load_image('back_start.jpg'), (size[0], size[1]))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # starts the game
        pygame.display.flip()


def very_end_screen():
    """
    Is used to end the game. For real this time
    """
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    intro_text = ["СПАСИБО ЗА ИГРУ"]
    fon = pygame.transform.scale(load_image('end_background.jpeg'), (size[0], size[1]))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()


def end_screen():
    """
    Is used to relaaaaax
    """
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    fon = pygame.transform.scale(load_image('end_background.jpeg'), (size[0], size[1]))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                create_particles(pygame.mouse.get_pos())
        all_sprites.update()
        screen.blit(fon, (0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(50)


class Particle(pygame.sprite.Sprite):
    """
    Is used for particles
    """
    fire = [load_image("star.png")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = GRAVITY

    def update(self) -> None:
        """
        Is used to update the particles
        return: None
        """
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles(position: tuple) -> None:
    """
    Is used to create particles
    param position: coordinates
    return: None
    """
    particle_count = 20
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


class Tile(Sprite):
    """
    Is used to create tiles for water and background
    """
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(sprite_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.pos = (pos_x, pos_y)


class Board:
    """
    Is used for the board
    """
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 40
        self.top = 5
        self.cell_size = 45

    def render(self, screen) -> None:
        """
        Is used to render the screen
        """
        colors = [pygame.Color("black"), pygame.Color("red"), pygame.Color("blue")]
        for x, y in itertools.product(range(self.width), range(self.height)):
            pygame.draw.rect(screen, colors[self.board[y][x]], (
                x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                self.cell_size))
            pygame.draw.rect(screen, pygame.Color("white"), (
                x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                self.cell_size), 1)

    def set_view(self, left: int, top: int, cell_size: int) -> None:
        """
        Is used to set the view of the programme
        """
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def on_click(self, cell):
        """
        Is used as a plug
        """
        pass

    def get_cell(self, mouse_pos):
        """
        param mouse_pos: the position of the mouse
        return: coordinates of the cell
        Is used to get the coordinates of the cell clicked
        """
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def get_click(self, mouse_pos) -> tuple:
        """
        param mouse_pos: the position of the mouse
        return: None
        """
        cell = self.get_cell(mouse_pos)
        if cell:
            return cell


def check_in_bottle(pos: tuple, level_num: int) -> bool:
    """
    param pos: the position of the click
    param level_num: the number of the level
    return: True/False
    Is used to check whether the click is located on the bottle
    """
    if level_num == 1:
        for lis in bottles_dict_1.values():
            if pos in lis:
                return True
        return False
    else:
        for lis in bottles_dict_2.values():
            if pos in lis:
                return True
        return False


def check_num_bottle(l_pos: tuple, level_num: int) -> str:
    """
    param l_pos, level num: the last position of water, the number of the level
    return: the number of the bottle of the water
    Is used to identify the number of the bottle of water
    (I know it looks bad, sorry)
    """
    i = ""
    if level_num == 1:
        if l_pos[0] == 2:
            i = "1"
        elif l_pos[0] == 5:
            i = "2"
        else:
            i = "3"
    elif level_num == 2:
        if l_pos[0] == 1 and l_pos[1] < 6:
            i = "1"
        elif l_pos[0] == 3:
            i = "2"
        elif l_pos[0] == 5:
            i = "3"
        elif l_pos[0] == 7 and l_pos[1] < 6:
            i = "4"
        elif l_pos[0] == 1 and l_pos[1] > 7:
            i = "5"
        elif l_pos[0] == 4:
            i = "6"
        elif l_pos[0] == 7 and l_pos[1] > 7:
            i = "7"
    return i


def load_level(name: str) -> list:
    """
    param name: name of the file of the level's map
    return: list consisting of stings of the level
    Is used to read txt-files of the level and convert it into a list
    """
    filename = "data/" + name
    with open(filename, 'r') as mapFile:
        level_map = [list(line.strip()) for line in mapFile]
    return level_map


def generate_level(level: list, size_y: int, size_x: int) -> tuple:
    """
    param level: a list containing lists of special marks about the level
    return: coordinates
    Is used to generate the level
    """
    x, y = None, None
    for y in range(size_y):
        for x in range(size_x):
            if level[y][x] == '.':
                Tile('black', x, y)
            elif level[y][x] == 'c':
                Tile('clear', x, y)
            elif level[y][x] == 'y':
                Tile('yellow', x, y)
            elif level[y][x] == 'b':
                Tile('blue', x, y)
            elif level[y][x] == 'o':
                Tile('orange', x, y)
            elif level[y][x] == 'g':
                Tile('green', x, y)
            elif level[y][x] == 'p':
                Tile('pink', x, y)
    return x, y


def move_up_1(pos: tuple):
    """
    For level 1
    param pos: the position of the water
    return: 1)the color of the current water 2) the previous position 3) the previous index
    Is used in level_1 to move the water upwards and
    change the last position to the clear cell
    """
    current_color, ind, cleared_ind = "", 0, 0
    i = check_num_bottle(pos, 1)
    for ind, c in enumerate(colors_dict_1[f"bottle_{i}"], 0):
        if c != "clear":
            current_color = colors_dict_1[f"bottle_{i}"][ind]
            colors_dict_1[f"bottle_{i}"][ind] = "clear"
            cleared_ind = ind
            Tile("clear", pos[0] + 1, ind + 4)
            Tile(current_color, pos[0] + 1, 2)
            break
    return current_color, (pos[0] + 1, ind + 4), cleared_ind


def move_up_2(pos: tuple):
    """
    For level 2
    param pos: the position of the water
    return: 1)the color of the current water 2) the previous position 3) the previous index
    Is used in level_1 to move the water upwards and
    change the last position to the clear cell
    """
    current_color, ind, cleared_ind = "", 0, 0
    i = check_num_bottle(pos, 2)
    for ind, c in enumerate(colors_dict_2[f"bottle_{i}"], 0):
        if c != "clear":
            current_color = colors_dict_2[f"bottle_{i}"][ind]
            colors_dict_2[f"bottle_{i}"][ind] = "clear"
            cleared_ind = ind
            if int(i) <= 4:
                Tile("clear", pos[0] + 1, ind + 1)
                Tile(current_color, pos[0] + 1, 0)
            else:
                Tile("clear", pos[0] + 1, ind + 8)
                Tile(current_color, pos[0] + 1, 7)
            break
    if int(i) <= 4:
        return current_color, (pos[0], ind + 1), cleared_ind
    else:
        return current_color, (pos[0], ind + 8), cleared_ind


def move_to_bottle_1(pos_needed: tuple, l_pos: tuple, cleared_ind: int, color: str) -> None:
    """
    For level 1
    param pos_needed: the position of the click (needed bottle)
    param l_pos: the previous position of the water
    param cleared_ind: the index of cleared y-coord
    param color: the color of the current water
    return: None
    Is used to move the water to the right place in the bottle (or move it to the previous spot)
    """
    found = False
    i = check_num_bottle(pos_needed, 1)
    for ind, c in enumerate(colors_dict_1[f"bottle_{i}"], 0):
        if c != "clear":
            if c == color and ind != 1:
                Tile(color, pos_needed[0] + 1, ind + 3)
                colors_dict_1[f"bottle_{i}"][ind - 1] = color
                found = True
                break
            break
        if c == "clear" and ind == 4:
            Tile(color, pos_needed[0] + 1, ind + 3 + 1)
            colors_dict_1[f"bottle_{i}"][ind] = color
            found = True
            break
    if not found:
        Tile(color, l_pos[0], l_pos[1])
        x = check_num_bottle((l_pos[0] - 1, l_pos[1] - 1), 1)
        colors_dict_1[f"bottle_{x}"][cleared_ind] = color


def move_to_bottle_2(pos_needed: tuple, l_pos: tuple, cleared_ind: int, color: str) -> None:
    """
        For level 2
        param pos_needed: the position of the click (needed bottle)
        param l_pos: the previous position of the water
        param cleared_ind: the index of cleared y-coord
        param color: the color of the current water
        return: None
        Is used to move the water to the right place in the bottle (or move it to the previous spot)
        """
    found = False
    i = check_num_bottle(pos_needed, 2)
    for ind, c in enumerate(colors_dict_2[f"bottle_{i}"], 0):
        if c != "clear":
            if c == color and ind != 1:
                if int(i) <= 4:
                    Tile(color, pos_needed[0] + 1, ind)
                else:
                    Tile(color, pos_needed[0] + 1, ind + 7)
                colors_dict_2[f"bottle_{i}"][ind - 1] = color
                found = True
                break
            break
        if c == "clear" and ind == 4:
            if int(i) <= 4:
                Tile(color, pos_needed[0] + 1, ind + 1)
            else:
                Tile(color, pos_needed[0] + 1, ind + 8)
            colors_dict_2[f"bottle_{i}"][ind] = color
            found = True
            break
    if not found:
        Tile(color, l_pos[0] + 1, l_pos[1])
        x = check_num_bottle((l_pos[0], l_pos[1]), 2)
        colors_dict_2[f"bottle_{x}"][cleared_ind] = color


def finished(level_num: int) -> bool:
    """
    param: level_num: the number of the level
    return: bool
    Is used to check whether the level is finished
    """
    count = 0
    if level_num == 1:
        for c in colors_dict_1.values():
            if len(set(c[1:])) == 1:
                count += 1
        if count == 3:
            return True
        return False
    if level_num == 2:
        for c in colors_dict_2.values():
            if len(set(c[1:])) == 1:
                count += 1
        if count == 7:
            return True
        return False


def terminate() -> None:
    """
    return: None
    Is used to quit the programme
    """
    pygame.quit()
    sys.exit()


def level_1():
    """
    Is used to start the level 1
    """
    pygame.init()
    size = 600, 600
    size_y, size_x = 13, 13
    level_x, level_y = generate_level(load_level('level_1.txt'), size_y, size_x)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Легкий уровень")
    count_of_actions = 1
    clear_pos, current_color, cleared_ind = (0, 0), "", 0
    board = Board(13, 13)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = board.get_click(event.pos)
                if count_of_actions == 1 and check_in_bottle(pos, 1):
                    current_color, clear_pos, cleared_ind = move_up_1(pos)
                    count_of_actions = 2
                elif count_of_actions == 2 and check_in_bottle(pos, 1):
                    move_to_bottle_1(pos, clear_pos, cleared_ind, current_color)
                    Tile("black", clear_pos[0], 2)
                    count_of_actions = 1
                if finished(1):
                    running = False

        screen.fill(pygame.Color("black"))
        sprite_group.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()


def level_2():
    """
    Is used to start the level 2
    """
    pygame.init()
    size = 600, 600
    size_y, size_x = 13, 10
    level_x, level_y = generate_level(load_level('level_2.txt'), size_y, size_x)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Средний уровень")
    count_of_actions = 1
    clear_pos, current_color, cleared_ind = (0, 0), "", 0
    board = Board(10, 13)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = board.get_click(event.pos)
                if count_of_actions == 1 and check_in_bottle(pos, 2):
                    current_color, clear_pos, cleared_ind = move_up_2(pos)
                    count_of_actions = 2
                elif count_of_actions == 2 and check_in_bottle(pos, 2):
                    move_to_bottle_2(pos, clear_pos, cleared_ind, current_color)
                    i = check_num_bottle(clear_pos, 2)
                    if int(i) <= 4:
                        Tile("black", clear_pos[0] + 1, 0)
                    else:
                        Tile("black", clear_pos[0] + 1, 7)
                    count_of_actions = 1
                if finished(2):
                    running = False

        screen.fill(pygame.Color("black"))
        sprite_group.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    start_screen()
    level_1()
    level_2()
    end_screen()
    very_end_screen()
