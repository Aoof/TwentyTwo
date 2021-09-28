import numpy as np
import pygame
import sys
from PIL import Image
pygame.init()

class Button:
    def __init__(self, window, text, fontsize, pos, sizes, border, colors, onclick=None):
        self.sprites = []
        self.currentSprite = 0

        self.hover = False
        self.onclick = onclick

        self.x, self.y = pos
        self.w, self.h = sizes
        
        self.border = {
            "x": self.x - border,
            "y": self.y - border,
            "w": self.w + border * 2,
            "h": self.h + border * 2
        }

        self.colorfore, self.colorback, self.colortext = colors
        self.button    = pygame.Rect(self.x, self.y, self.w, self.h)
        self.button_bk = pygame.Rect(self.border["x"], self.border["y"],
                                     self.border["w"], self.border["h"])

        fnt = pygame.font.SysFont("Sans Serif", fontsize)
        txt = fnt.render(text, 1, self.colortext)

        self.EventHandler()

        pygame.draw.rect(window, self.colorback, self.button_bk)
        if (self.hover):
            pygame.draw.rect(window, self.colorback, self.button)
        else:
            pygame.draw.rect(window, self.colorfore, self.button)

        textrect = txt.get_rect()
        textrect.centerx = self.button.centerx
        textrect.centery = self.button.centery
        window.blit(txt, textrect)

    def EventHandler(self):
        mousex, mousey = pygame.mouse.get_pos()
        lredge = (mousex >= self.x and mousex <= self.x + self.w)
        tbedge = (mousey >= self.y and mousey <= self.y + self.h)
        if (lredge and tbedge):
            self.hover = True
            if (pygame.mouse.get_pressed()[0]):
                self.onclick()
        else:
            self.hover = False


class Game:
    def __init__(self, width, height):
        self.w, self.h = width, height
        self.x, self.y = 0, 0
        self.tileSize = 10
        self.gameList = np.zeros([width, height])
        self.stateList = np.zeros([width, height])
        self.lives = 3
        self.gameState = "inprogress"
    
    def LevelFromMap(self, map):
        w, h = int(map[0]), int(map[1])
        map = map[2:]
        i = 0
        for y in range(h):
            for x in range(w):
                self.gameList[y,x] = int(map[i])
                i += 1

    def LevelFromImage(self, image):
        img = Image.open(image)
        img = img.resize((self.w, self.h))
        img = img.convert("1")
        img_array = np.array(img)

        for y in range(self.h):
            for x in range(self.w):
                self.gameList[y, x] = 1 if not img_array[y, x] else 0        

    def EventHandler(self, window):
        mousex, mousey = pygame.mouse.get_pos()
        for y in range(self.h):
            for x in range(self.w):
                tilex = self.x + (x * self.tileSize)
                tiley = self.y + (y * self.tileSize)

                lredge = (mousex >= tilex and mousex <= tilex + self.tileSize)
                tbedge = (mousey >= tiley and mousey <= tiley + self.tileSize)
                
                if (lredge and tbedge and self.gameState == "inprogress"):
                    self.MakeMove((x, y), window)

    def WinCheck(self):
        for y in range(self.h):
            for x in range(self.w):
                if (self.gameList[y, x] == 1 and self.stateList[y, x] != 1):
                    return False
        return True
    
    def MakeMove(self, pos, window):
        x, y = pos
        if (self.gameList[y, x] == 1):
            self.stateList[y, x] = 1
            if (self.WinCheck()):
                self.gameState = "won"
        elif (self.stateList[y, x] == 0):
            self.stateList[y, x] = 2
            self.lives -= 1
            if (self.lives <= 0):
                self.gameState = "lost"

    def CountColumns(self):
        temp = 0
        res = []
        for x in range(self.w):
            res.append([])
            for y in range(self.h):
                if (self.gameList[y, x] == 1):
                    temp += 1
                elif (temp > 0):
                    res[-1].append(str(temp))
                    temp = 0
        return res

    def CountRows(self):
        temp = 0
        res = []
        for y in range(self.h):
            res.append([])
            for x in range(self.w):
                if (self.gameList[y, x] == 1):
                    temp += 1
                elif (temp > 0):
                    res[-1].append(str(temp))
                    temp = 0
        return res

    def draw(self, window):
        fnt = pygame.font.SysFont("Sans Serif", 20)
        txt = fnt.render("Lives " + str(self.lives), 1, (0, 0, 0))
        txtrect = txt.get_rect()
        txtrect.centerx = window.get_rect().centerx
        txtrect.centery = 20

        window.blit(txt, txtrect)
        for y in range(self.h):
            ## Draw Labels on rows
            rows = self.CountRows()
            q = "  ".join(rows[y]) + " "

            tile = pygame.Rect(self.x - self.tileSize, self.y + (y * self.tileSize), self.tileSize, self.tileSize)

            fnt = pygame.font.SysFont("Sans Serif", 16)
            txt = fnt.render(q, 1, (0, 0, 0))

            txtrect = txt.get_rect()
            txtrect.midright = tile.midright
            txtrect.centery = tile.centery
            
            window.blit(txt, txtrect)
            for x in range(self.w):
                tile = pygame.Rect(self.x + (x*self.tileSize), self.y + (y*self.tileSize), self.tileSize, self.tileSize)
                if (self.stateList[y, x] == 0):
                    pygame.draw.rect(window, (255, 255, 255), tile)
                    tile.width += 1
                    tile.height += 1
                    pygame.draw.rect(window, (0, 0, 0), tile, 1)
                elif (self.stateList[y, x] == 1):
                    pygame.draw.rect(window, (0, 0, 0), tile)
                    tile.width += 1
                    tile.height += 1
                    pygame.draw.rect(window, (0, 0, 0), tile, 1)
                elif (self.stateList[y, x] == 2):
                    pygame.draw.rect(window, (255, 65, 54), tile)
                    tile.width += 1
                    tile.height += 1
                    pygame.draw.rect(window, (0, 0, 0), tile, 1)
                
        for x in range(self.w):
            ## Draw Labels on columns
            columns = self.CountColumns()
            q = " " + "  ".join(columns[x])

            tile = pygame.Rect(self.x + (x*self.tileSize), self.y - self.tileSize, self.tileSize, self.tileSize)

            fnt = pygame.font.SysFont("Sans Serif", 16)
            txt = fnt.render(q, 1, (0, 0, 0))
            txt = pygame.transform.rotate(txt, 90)

            txtrect = txt.get_rect()
            txtrect.centerx = tile.centerx
            txtrect.midbottom = tile.midbottom
            
            window.blit(txt, txtrect)


class Main:
    def __init__(self, gridSize, tileSize, windowSize):
        x, y = gridSize
        self.grid = { "x": x, "y": y }

        w, h = tileSize
        self.tile = { "width": w, "height": h }

        w, h = windowSize
        self.width, self.height = w, h
        self.window = pygame.display.set_mode((w, h))

        self.state = 0
        self.game = Game(self.grid["x"], self.grid["y"])

    def Draw(self):
        self.window.fill((255, 255, 255))

        if self.state == 0:
            self.DrawMenu()
        elif self.state == 1:
            self.DrawGame()
        elif self.state == 2:
            self.DrawResults()
        elif self.state == 3:
            self.DrawOptions()

        pygame.display.update()

    def DrawGame(self):
        self.game.tileSize = (self.width - (self.width*0.2))//self.game.w

        self.game.x = self.width*0.1
        self.game.y = (self.height//2) - ((self.game.h - self.game.h//2) * self.game.tileSize)

        self.game.x += self.game.tileSize
        self.game.y += self.game.tileSize
        
        self.game.draw(self.window)

    def DrawOptions(self):
        btnx, btny = 0, self.height - 50

        def backBtn():
            self.state = 0
        backButton = Button(self.window, "Back", 40, (btnx, btny), (200, 50), 0, ((0, 0, 0), (100, 100, 100), (255, 255, 255)), backBtn)
        
    
    def DrawResults(self):
        fnt = pygame.font.SysFont("Sans Serif", 90)
        
        if (self.game.gameState == "won"):
            txt = fnt.render("You Won!", 1, (1, 255, 112))
        elif (self.game.gameState == "lost"):
            txt = fnt.render("You Lost!", 1, (255, 65, 54))
        
        txtrect = txt.get_rect()
        txtrect.centerx = self.window.get_rect().centerx
        txtrect.centery = self.window.get_rect().centery
        
        self.window.blit(txt, txtrect)

        btnx, btny = (self.width  - 200) // 2, self.window.get_rect().centery + 100

        def backBtn():
            self.state = 0
            self.game = Game(self.grid["x"], self.grid["y"])
        backButton = Button(self.window, "Back", 40, (btnx, btny), (200, 50), 0, ((0, 0, 0), (100, 100, 100), (255, 255, 255)), backBtn)

    def DrawMenu(self):
        w, h    = 200, 50
        y1      = (self.height - h) // 2
        x       = (self.width  - w) // 2
        margin  = 40
        bgcolor = (0, 0, 0)
        brcolor = (100, 100, 100)
        txcolor = (255, 255, 255)

        def y(i): return (y1 + (h*i) + margin)

        def startBtn():
            self.state = 1
        startButton = Button(self.window, "Start", 40, (x, y(0)), (w, h), 0, (bgcolor, brcolor, txcolor), startBtn)

        def optsBtn():
            self.state = 3
        optionsButton = Button(self.window, "Options", 40, (x, y(1.5)), (w, h), 0, (bgcolor, brcolor, txcolor), optsBtn)

        def quitBtn():
            pygame.quit()
            sys.exit()
        quitButton = Button(self.window, "Quit", 40, (x, y(3)), (w, h), 0, (bgcolor, brcolor, txcolor), quitBtn)
        
        fnt = pygame.font.SysFont("Sans Serif", 90)
        txt = fnt.render("Nonogram", 1, (0, 0, 0))

        txt_rect = txt.get_rect()
        txt_rect.centerx = self.window.get_rect().centerx
        txt_rect.centery = 90*1.5
        self.window.blit(txt, txt_rect)

    def MainLoop(self):
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if (self.state == 1 and event.type == 1025):
                    self.game.EventHandler(self.window)
                    if (self.game.gameState != "inprogress"):
                        self.state = 2

            self.Draw()
            
            
if __name__ == "__main__":
    main = Main((20, 20), (20, 20), (600, 600));
    main.game.LevelFromImage("level_00.jpg")
    main.MainLoop()