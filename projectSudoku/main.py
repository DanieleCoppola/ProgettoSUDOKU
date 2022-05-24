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


def set_text(string, coordx, coordy, fontSize):
    font = pygame.font.Font('freesansbold.ttf', fontSize)
    text = font.render(string, True, (0, 0, 0))
    textRect = text.get_rect()
    textRect.center = (coordx, coordy)
    return text, textRect


def valid_row(row, grid):
    temp = grid[row]
    # Removing 0's.
    temp = list(filter(lambda a: a != 0, temp))
    # Checking for invalid values.
    if any(0 > i > 9 for i in temp):
        print("Invalid value")
        return -1
    # Checking for repeated values.
    elif len(temp) != len(set(temp)):
        return 0
    else:
        return 1


def valid_col(col, grid):
    # Extracting the column.
    temp = [row[col] for row in grid]
    # Removing 0's.
    temp = list(filter(lambda a: a != 0, temp))
    # Checking for invalid values.
    if any(i < 0 and i > 9 for i in temp):
        print("Invalid value")
        return -1
    # Checking for repeated values.
    elif len(temp) != len(set(temp)):
        return 0
    else:
        return 1


def valid_subsquares(grid):
    for row in range(0, 9, 3):
        for col in range(0, 9, 3):
            temp = []
            for r in range(row, row + 3):
                for c in range(col, col + 3):
                    if grid[r][c] != 0:
                        temp.append(grid[r][c])
            # Checking for invalid values.
            if any(i < 0 and i > 9 for i in temp):
                print("Invalid value")
                return -1
            # Checking for repeated values.
            elif len(temp) != len(set(temp)):
                return 0
    return 1


def valid_board(grid):
    for i in range(9):
        res1 = valid_row(i, grid)
        res2 = valid_col(i, grid)

        if (res1 < 1 or res2 < 1):
            return

    res3 = valid_subsquares(grid)
    if (res3 < 1):
        return False
    else:
        return True


def insert(win, position):
    i, j = position[1], position[0]
    myfont = pygame.font.SysFont('Comic Sans MS', 35)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:

                if grid_original[i - 1][j - 1] != 0:
                    return
                if event.key == 48:
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

def insert2(win, position,num):
    i, j = position[1], position[0]
    myfont = pygame.font.SysFont('Comic Sans MS', 35)
    grid[i - 1][j - 1] = num
    pygame.draw.rect(win, background_color, (
        position[0] * 50 + buffer, position[1] * 50 + buffer, 50 - 2 * buffer, 50 - 2 * buffer))
    pygame.display.update()
    pygame.draw.rect(win, background_color, (
        position[0] * 50 + buffer, position[1] * 50 + buffer, 50 - 2 * buffer, 50 - 2 * buffer))
    value = myfont.render(str(num), True, (0, 0, 0))
    win.blit(value, (position[0] * 50 + 15, position[1] * 50))
    grid[i - 1][j - 1] = num
    pygame.display.update()

def sudoku_solver(win):
    myfont = pygame.font.SysFont('Comic Sans MS', 35)
    for i in range(0, len(grid[0])):
        for j in range(0, len(grid[0])):
            if isEmpty(grid[i][j]):
                for k in range(1, 10):
                    if valid_board(grid):
                        grid[i][j] = k
                        pygame.draw.rect(win, (245, 255, 0), (
                            (j + 1) * 50 + buffer, (i + 1) * 50 + buffer, 50 - 2 * buffer, 50 - 2 * buffer))
                        value = myfont.render(str(k), True, (0, 0, 0))
                        win.blit(value, ((j + 1) * 50 + 15, (i + 1) * 50))
                        pygame.display.update()
                        pygame.time.delay(11)

                        sudoku_solver(win)
                        # if sudoku_solver returns, there's a mismatch
                        grid[i][j] = 0
                        pygame.draw.rect(win, background_color, (
                            (j + 1) * 50 + buffer, (i + 1) * 50 + buffer, 50 - 2 * buffer, 50 - 2 * buffer))
                        pygame.display.update()
                        # pygame.time.delay(50)
                    else:
                        return

                return


def main():
    pygame.init()
    win = pygame.display.set_mode((570, WIDTH))
    pygame.display.set_caption("Sudoku")
    win.fill(background_color)
    myfont = pygame.font.SysFont('Comic Sans MS', 35)
    text = set_text("SUDOKUUU!", 280, 25, 30)
    text2 = set_text("Premi r per verificare il sudoku!", 270, 600, 30)
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
                pos = pygame.mouse.get_pos()
                insert(win, (pos[0] // 50, pos[1] // 50))
                if valid_board(grid):
                    pygame.draw.rect(win, (245, 255, 0), (
                        pos[0] * 50 + buffer, pos[1] * 50 + buffer, 50 - 2 * buffer, 50 - 2 * buffer))
                    insert(win, (pos[0] // 50, pos[1] // 50))
                    pygame.draw.rect(win, (245,255,0), (
                        pos[0] * 50 + buffer, pos[1] * 50 + buffer, 50 - 2 * buffer, 50 - 2 * buffer))
                    pygame.display.update()
                else:
                    insert2(win, (pos[0] // 50, pos[1] // 50),0)
                    pygame.draw.rect(win, (255, 255, 0), (
                        pos[0] * 50 + buffer, pos[1] * 50 + buffer, 50 - 2 * buffer, 50 - 2 * buffer))
                    pygame.display.update()
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    if valid_board(grid):
                        text4 = set_text("correct", 270, 650, 30)
                        win.blit(text4[0], text4[1])
                        pygame.display.update()
                    else:
                        text4 = set_text("incorrect", 270, 650, 30)
                        win.blit(text4[0], text4[1])
                        pygame.display.update()

main()
