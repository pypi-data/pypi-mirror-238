try:
    from .NebulaCore import *
    from .NebulaObject import *
except ModuleNotFoundError:
    mnf = str(input("~| ENGINE IMPORT ERROR...\nThere was an error while gathering Nebula\nIf the problem persists, contact setoichi.\n~| "))
    import os
    os.sys.exit()

cache = "C:\\"
try:
    with open('C:\\.NebulaCache\\nebula-cache.json', 'r') as f:
        cache = json.load(f)
        f.close()
except FileNotFoundError:
    print('Nebula Cache Not Present!\n')

class Nebula:
    def __init__(self):
        self.DT = 0.0
        self.Clock = pygame.time.Clock()
        currentProject = cache['Nebula']['current project']
        self.cfg = loadCFG(path=cache['Nebula'][currentProject]['path'], name=cache['Nebula'][currentProject]['project name'])
        self.Display = pygame.display.set_mode(self.cfg['project']['screen size'])
        self.AssetManager = AssetManager(env=self, maxCacheSize=450)
        self.Camera = Camera(
            env=self,
            levelSize=self.cfg['project']['tilemap size'],
            screenSize=self.cfg['project']['screen size'],
            cameraSpeed=30,
            scrollInterpolation=40
        )
        self.Renderer = Renderer(
            env=self,
            layerCount=2,
            assetManager=self.AssetManager
        )
    
    def sendFrame(self):
        self.DT = self.Clock.tick(self.cfg['project']['target FPS']) / 1000.0
        pygame.display.update()
        # pygame.display.update(self.Renderer.dirtyRects)

Nebula = Nebula()
with open(f"C:\\.NebulaCache\\nebula-cache.json", "r") as f:
    cache = json.load(f)
    f.close()
cache['Nebula']['current project'] = ""
with open(f"C:\\.NebulaCache\\nebula-cache.json", "w") as f:
    json.dump(cache, f, indent=4)
    f.close()