import pygame
import itertools
import sys
import os


FPS = 50
pygame.init()
size = 860, 600
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Bottles")


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
    'background': load_image("back_start.jpg"),
    'black': load_image("black_tile.jpg"),
    'clear': load_image("clear_tile.jpg"),
    'yellow': load_image("yellow_tile.jpg"),
    'blue': load_image("blue_tile.jpg"),
    'orange': load_image("orange_tile.jpg"),
    'green': load_image("green_tile.jpg"),
    'pink': load_image("pink_tile.jpg")
}

bottles_dict_1 = {"bottle_1": [(2, 4), (2, 5), (2, 6), (2, 7), (2, 8)],
                "bottle_2": [(5, 4), (5, 5), (5, 6), (5, 7), (5, 8)],
                "bottle_3": [(8, 4), (8, 5), (8, 6), (8, 7), (8, 8)]}

colors_dict_1 = {"bottle_1": ["clear", "yellow", "blue", "yellow", "blue"],
                "bottle_2": ["clear", "blue", "yellow", "blue", "yellow"],
                "bottle_3": ["clear", "clear", "clear", "clear", "clear"]}


class SpriteGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for sprite in self:
            sprite.get_event(event)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.rect = None

    def get_event(self, event):
        pass


tile_width = tile_height = 45
sprite_group = SpriteGroup()


def start_screen():
    """
    Is used to start the game
    """
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Вам предстоит перемешать шарики в колбочки.",
                  "Удачи!",
                  "Представлены следующие уровни в порядке очереди:",
                  "Легкий",
                  "Средний",
                  "Сложный"]

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


class Tile(Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(sprite_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(
            tile_width * self.pos[0] + 15, tile_height * self.pos[1] + 5)


class Board:
    """
    Is the class of the board
    """
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 40
        self.top = 5
        self.cell_size = 45

    def render(self, screen):
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

    def set_view(self, left, top, cell_size):
        """
        Is used to set the view of the programme
        """
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def on_click(self, cell):
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

    def get_click(self, mouse_pos):
        """
        param mouse_pos: the position of the mouse
        return: None
        """
        cell = self.get_cell(mouse_pos)
        if cell:
            return cell


def check_in_bottle(pos: tuple, level_num: int) -> bool:
    if level_num == 1:
        for lis in bottles_dict_1.values():
            if pos in lis:
                return True
        return False
    #else:
    #    for lis in bottles_dict_2.values():
    #        if pos in lis:
    #            return True
    #    return False


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


def generate_level(level: list):
    """
    param level: a list containing lists of special marks about the level
    return: coordinates
    """
    x, y = None, None
    for y in range(13):
        for x in range(13):
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


level_x, level_y = generate_level(load_level('level_1.txt'))


def terminate() -> None:
    """
    return: None
    Is used to quit the programme
    """
    pygame.quit()
    sys.exit()


def main():
    pygame.init()
    size = 800, 600
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Легкий уровень")

    board = Board(13, 13)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = board.get_click(event.pos)
                if check_in_bottle(pos, 1):
                    print(pos)
                    if pos[0] == 2:
                        current_water_pos = bottles_dict_1["bottle_1"].pop(1)
                        current_color = colors_dict_1["bottle_1"].pop(1)
                        Tile("clear", pos[0], pos[1])
                        Tile(current_color, pos[0], 3)
        screen.fill(pygame.Color("black"))
        sprite_group.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    start_screen()
    main()