import os
try:
    import pygame
    import sqlite3
except:
    os.system("pip install -r {}".format(os.path.join(os.path.dirname(__file__), "requirements.txt")))
    print("\nWe have installed missing dependencies, please restart the program to start it properly with the required dependencies.")
    input("Please click any key to continue... ")
    os.exit()
    quit()

pygame.init()

# Start game class ✔?
# - main menu
# - history
# - settings
# - play vs comp
# - play locally
# - play on network

# Color palette
## Main         - #A9F0D1/(169, 240, 209)
## Secondary    - #FFA69E/(255, 166, 158)

class Essentials:
    def __init__(self, *args, **kwargs):
        pass
    
    def ShowButton( 
                    self,  
                    text="Button", 
                    position=(0, 0), 
                    size=(200, 100), 
                    color=None, 
                    hover_color=None, 
                    border=None, 
                    hover_border=None, 
                    callback=None
                ):
        pass
    

class Game(Essentials):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("systemui", 20)
    def __init__(self, ip=None, size=(600, 600)):
        self.win = pygame.display.set_mode(size) # set window with size of 600px / 600px by default
        self.StartLoop()
    
    # Updating screen logic (Will be looped every frame)
    def Update(self):
        # fill screen based on preferences
        self.win.fill((170, 170, 170))

        # display main menu
        
        # update screen with all changes
        pygame.display.update()

    def MainMenu(self):
        pass

    def StartLoop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            self.Update()


g = Game()