import pygame
import itertools
import sys
import os


pygame.init()
size = 860, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Bottles")


def load_image(name, color_key=None):
    thename = f"data/{name}"
    try:
        image = pygame.image.load(thename)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key is -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


tile_images = {
    'bottle': load_image("bottle.PNG"),
    'background': load_image("back_start.jpg")
}


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
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
                return  # начинаем игру
        pygame.display.flip()


def load_level(name: str) -> list:
    """
    :param name: name of the file of the level's map
    :return: list consisting of stings of the level
    Is used to read txt-files of the level and convert it into a list
    """
    filename = "data/" + name
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    return level_map


def generate_level(level):
    x, y = None, None
    for y in range(16):
        for x in range(13):
            if level[y][x] == '.':
                Tile('black', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                level[y][x] = "."
    return x, y


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 40
        self.top = 5
        self.cell_size = 45

    def render(self, screen):
        colors = [pygame.Color("black"), pygame.Color("red"), pygame.Color("blue")]
        for x, y in itertools.product(range(self.width), range(self.height)):
            pygame.draw.rect(screen, colors[self.board[y][x]], (
                x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                self.cell_size))
            pygame.draw.rect(screen, pygame.Color("white"), (
                x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                self.cell_size), 1)

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def on_click(self, cell):
        print(cell)
        self.board[cell[1]][cell[0]] = (self.board[cell[1]][cell[0]] + 1) % 3

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)


def main():
    pygame.init()
    size = 800, 600
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Легкий уровень")

    board = Board(16, 13)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)

        screen.fill((0, 0, 0))
        board.render(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    start_screen()