import pygame

WIDTH = 555
HEIGHT = 655
background_color = (251, 247, 245)


class button:
    def __init__(self, position, size, clr=[100, 100, 100], cngclr=None, func=None, text='', font="Segoe Print",
                 font_size=16, font_clr=[0, 0, 0]):
        self.clr = clr
        self.size = size
        self.func = func
        self.surf = pygame.Surface(size)
        self.rect = self.surf.get_rect(center=position)

        if cngclr:
            self.cngclr = cngclr
        else:
            self.cngclr = clr

        if len(clr) == 4:
            self.surf.set_alpha(clr[3])

        self.font = pygame.font.SysFont(font, font_size)
        self.txt = text
        self.font_clr = font_clr
        self.txt_surf = self.font.render(self.txt, 1, self.font_clr)
        self.txt_rect = self.txt_surf.get_rect(center=[wh // 2 for wh in self.size])

    def draw(self, screen):
        self.mouseover()

        self.surf.fill(self.curclr)
        self.surf.blit(self.txt_surf, self.txt_rect)
        screen.blit(self.surf, self.rect)

    def mouseover(self):
        self.curclr = self.clr
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.curclr = self.cngclr

    def call_back(self, *args):
        if self.func:
            return self.func(*args)


class text:
    def __init__(self, msg, position, clr=[100, 100, 100], font="Segoe Print", font_size=15, mid=False):
        self.position = position
        self.font = pygame.font.SysFont(font, font_size)
        self.txt_surf = self.font.render(msg, 1, clr)

        if len(clr) == 4:
            self.txt_surf.set_alpha(clr[3])

        if mid:
            self.position = self.txt_surf.get_rect(center=position)

    def draw(self, screen):
        screen.blit(self.txt_surf, self.position)


# call back functions
def fn1():
    print('check')


def fn2():
    print('solution')


def main():
    pygame.init()
    SCHERMO = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sudoku")
    SCHERMO.fill(background_color)
    for i in range(0, 10):
        if i % 3 == 0:
            pygame.draw.line(SCHERMO, (10, 10, 10), (50 + 50 * i, 50), (50 + 50 * i, 500), 4)
            pygame.draw.line(SCHERMO, (10, 10, 10), (50, 50 + 50 * i), (500, 50 + 50 * i), 4)
        pygame.draw.line(SCHERMO, (100, 10, 10), (50 + 50 * i, 50), (50 + 50 * i, 500), 2)
        pygame.draw.line(SCHERMO, (100, 10, 10), (50, 50 + 50 * i), (500, 50 + 50 * i), 2)
    button1 = button((200, 600), (100, 50), (220, 220, 220), (255, 0, 0), fn1, 'CHECK')
    button2 = button((350, 600), (100, 50), (220, 220, 220), (255, 0, 0), fn2, 'SOLUTION')

    button_list = [button1, button2]

    for b in button_list:
        b.draw(SCHERMO)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                pygame.quit()
                return


main()
