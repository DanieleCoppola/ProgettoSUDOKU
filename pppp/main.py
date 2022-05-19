import pygame
import requests

WIDTH = 750
background_color = (251, 247, 245)
original_grid_element_color = (52, 31, 151)
buffer = 5

response = requests.get("https://sugoku.herokuapp.com/board?difficulty=easy")
grid = response.json()['board']
grid_original = [[grid[x][y] for y in range(len(grid[0]))] for x in range(len(grid))]


def isEmpty(num):
    if num == 0:
        return True
    return False


def isValid(position, num):
    for i in range(0, len(grid[0])):
        if grid[position[0]][i] == num:
            return False

    for i in range(0, len(grid[0])):
        if grid[i][position[1]] == num:
            return False
    x = position[0] // 3 * 3
    y = position[1] // 3 * 3


    for i in range(0, 3):
        for j in range(0, 3):
            if (grid[x + i][y + j] == num):
                return False
    return True


solved = 0


def set_text(string, coordx, coordy, fontSize):
    font = pygame.font.Font('freesansbold.ttf', fontSize)
    text = font.render(string, True, (0, 0, 0))
    textRect = text.get_rect()
    textRect.center = (coordx, coordy)
    return (text, textRect)


def insert(win, position):
    i, j = position[1], position[0]
    myfont = pygame.font.SysFont('Comic Sans MS', 35)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN :
                if grid_original[i - 1][j - 1] != 0:
                    return
                if (event.key == 48):
                    grid[i - 1][j - 1] = event.key - 48
                    pygame.draw.rect(win, background_color, (
                        position[0] * 50 + buffer, position[1] * 50 + buffer, 50 - 2 * buffer, 50 - 2 * buffer))
                    pygame.display.update()
                    return
                if 0 < event.key - 48 < 10:
                    pygame.draw.rect(win, background_color, (
                        position[0] * 50 + buffer, position[1] * 50 + buffer, 50 - 2 * buffer, 50 - 2 * buffer))
                    value = myfont.render(str(event.key - 48), True, (0, 0, 0))
                    win.blit(value, (position[0] * 50 + 15, position[1] * 50))
                    grid[i - 1][j - 1] = event.key - 48
                    pygame.display.update()
                    return
                return


def sudoku_solver(win):
    myfont = pygame.font.SysFont('Comic Sans MS', 35)
    for i in range(0, len(grid[0])):
        for j in range(0, len(grid[0])):
            if isEmpty(grid[i][j]):
                for k in range(1, 10):
                    if isValid((i, j), k):
                        grid[i][j] = k
                        pygame.draw.rect(win, (245,255,0), (
                        (j + 1) * 50 + buffer, (i + 1) * 50 + buffer, 50 - 2 * buffer, 50 - 2 * buffer))
                        value = myfont.render(str(k), True, (0, 0, 0))
                        win.blit(value, ((j + 1) * 50 + 15, (i + 1) * 50))
                        pygame.display.update()
                        pygame.time.delay(25)

                        sudoku_solver(win)

                        # Exit condition
                        global solved
                        if solved == 1:
                            return

                        # if sudoku_solver returns, there's a mismatch
                        grid[i][j] = 0
                        pygame.draw.rect(win, background_color, (
                        (j + 1) * 50 + buffer, (i + 1) * 50 + buffer, 50 - 2 * buffer, 50 - 2 * buffer))
                        pygame.display.update()
                        # pygame.time.delay(50)
                return
    solved = 1


def main():
    pygame.init()
    win = pygame.display.set_mode((570, WIDTH))
    pygame.display.set_caption("Sudoku")
    win.fill(background_color)
    myfont = pygame.font.SysFont('Comic Sans MS', 35)
    text = set_text("SUDOKUUU!", 280, 25, 30)
    text2 = set_text("Press r for solve the sudoku!", 270, 600, 30)
    win.blit(text[0], text[1])
    win.blit(text2[0], text2[1])
    for i in range(0, 10):
        if i % 3 == 0:
            pygame.draw.line(win, (0, 0, 0), (50 + 50 * i, 50), (50 + 50 * i, 500), 4)
            pygame.draw.line(win, (0, 0, 0), (50, 50 + 50 * i), (500, 50 + 50 * i), 4)

        pygame.draw.line(win, (0, 0, 0), (50 + 50 * i, 50), (50 + 50 * i, 500), 2)
        pygame.draw.line(win, (0, 0, 0), (50, 50 + 50 * i), (500, 50 + 50 * i), 2)
    pygame.display.update()
    for i in range(0, len(grid[0])):
        for j in range(0, len(grid[0])):
            if (0 < grid[i][j] < 10):
                value = myfont.render(str(grid[i][j]), True, original_grid_element_color)
                win.blit(value, ((j + 1) * 50 + 15, (i + 1) * 50))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pygame.draw.rect(win,(245,255,0),3)
                pos = pygame.mouse.get_pos()
                insert(win, (pos[0] // 50, pos[1] // 50))
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    sudoku_solver(win)


main()
