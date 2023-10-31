try:
    from .NebulaCore import *
    from .NebulaObject import *
except ModuleNotFoundError:
    mnf = str(input("~| ENGINE IMPORT ERROR...\nThere was an error while gathering Nebula\nIf the problem persists, contact setoichi.\n~| "))
    import os
    os.sys.exit()

class Nebula:
    def __init__(self):
        self.DT = 0.0
        self.Clock = pygame.time.Clock()
        self.cfg = loadCFG(path=__file__, name=__name__)
        self.Display = pygame.display.set_mode(self.cfg['project']['screen size'])
        self.AssetManager = AssetManager(env=self, maxCacheSize=450)
        self.Camera = Camera(
            env=self,
            level_size=self.cfg['project']['tilemap size'],
            screen_size=self.cfg['project']['screen size'],
            camera_speed=30,
            scroll_interpolation=40
        )
        self.Renderer = Renderer(
            env=self,
            display=self.Display,
            layerCount=2,
            assetManager=self.AssetManager
        )
    
    def sendFrame(self):
        self.DT = self.Clock.tick(self.cfg['project']['target FPS']) / 1000.0
        pygame.display.update()
        # pygame.display.update(self.Renderer.dirtyRects)

Nebula = Nebula()