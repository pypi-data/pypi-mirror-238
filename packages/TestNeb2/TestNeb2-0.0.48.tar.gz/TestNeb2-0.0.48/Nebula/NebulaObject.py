try:
    from .NebulaCore import *
except ModuleNotFoundError:
    mnf = str(input("~| BASE IMPORT ERROR...\nThere was an error while gathering nebula.core\nPlease check that your installation directory contains the 'core' sub-directory.\nIf so, type 'fix' to open the Nebula Console.\nWhen the command line appears, type 'neb -fix ~core' to run the appropriate repair script.\nIf the problem persists, contact setoichi.\n~| ")) #cmd, flg, mod
    if mnf in {"fix",}:
        print("open Abyss Console\n")
    import os
    os.sys.exit()



"""
NEBULA CORE OBJECTS
"""

class Camera:
    
    def __init__(self, env, levelSize, screenSize, cameraSpeed, scrollInterpolation):
        self.env = env
        self.levelSize = VECTOR2(levelSize)
        self.screenSize = VECTOR2(screenSize)
        self.scroll = VECTOR2(0, 0)
        self.scrollInterpolation = scrollInterpolation
        self.scrollSpeed = cameraSpeed
        self.DEADZONERADIUS = 10
        self.inDeadzone = False
        self.panSpeed = cameraSpeed/2
        self.panning = False
        self.panTarget = None

    def scrollCamera(self, target):
        desiredScroll = VECTOR2(
            target.rect().centerx - self.screenSize.x / 2,
            target.rect().centery - self.screenSize.y / 2
        )

        distanceToTarget = (self.scroll - desiredScroll).length()
        if distanceToTarget >= self.DEADZONERADIUS:
            self.scroll += (desiredScroll - self.scroll) * self.scrollSpeed / self.scrollInterpolation * self.env.dt

    def panCamera(self, target):
        if type(target) == VECTOR2:
            desiredScroll = VECTOR2(
                target.x - self.screenSize.x / 2,
                target.y - self.screenSize.y / 2
            )
            # Use regular division for smoother interpolation
            self.scroll += (desiredScroll - self.scroll) * self.panSpeed / self.scrollInterpolation * self.env.dt
    
    def setTarget(self, target, screenSize, levelBound=False):
        self.screenSize = screenSize
        if not self.panning:
            self.scrollCamera(target)
        else:
            self.panTarget = target
            self.panCamera(self.panTarget)

        if levelBound:
            # Constrain camera within the level bounds
            self.scroll.x = max(0, min(self.scroll.x, self.levelSize.x - self.screenSize.x))
            self.scroll.y = max(0, min(self.scroll.y, self.levelSize.y - self.screenSize.y))

    def getOffset(self):
        return VECTOR2(int(self.scroll.x), int(self.scroll.y))


class Physics:
    def __init__(self, game, cellSize=16):
        self.env = game
        self.tilemap = None
        self.cellSize = cellSize
        self.spatialPartitioning = {}
        self.isTopdown = game.isTopdown
        self.isPlatformer = game.isPlatformer

    def setTilemap(self, tilemap):
        self.tilemap = tilemap
        self.cellSize = tilemap.tileSize
        self.createSpatialPartitioning(tilemap)

    def addEntity(self, entity):
        self.insertEntity(entity)

    def removeEntity(self, entity):
        self.removeEntityFromGrid(entity)

    def createSpatialPartitioning(self, tilemap):
        print('cellsize when gen spGrid',self.cellSize,"\n")
        self.spatialPartitioning = {}
        mapWidth = tilemap.mapSize.x
        mapHeight = tilemap.mapSize.y
        for x in range(0, int(mapWidth), self.cellSize):
            for y in range(0, int(mapHeight), self.cellSize):
                self.spatialPartitioning[f"{x};{y}"] = []

    def insertEntity(self, entity):
        entityCells = self.getCellsForEntity(entity)
        for cell in entityCells:
            self.spatialPartitioning[cell].append(entity)

    def removeEntityFromGrid(self, entity):
        entityCells = entity.spatialPartitioningCells
        for cell in entityCells:
            self.spatialPartitioning[cell].remove(entity)

    def getCellsForEntity(self, entity):
        print('cellsize when gen spGrid for entity',self.cellSize,"\n")
        entityRect = entity.rect()
        cells = set()
        left, top, right, bottom = entityRect.left, entityRect.top, entityRect.right, entityRect.bottom
        for x in range(left*self.cellSize, right*self.cellSize, self.cellSize):
            for y in range(top*self.cellSize, bottom*self.cellSize, self.cellSize):
                cells.add(f"{x};{y}")

        entity.spatialPartitioningCells = cells
        return entity.spatialPartitioningCells

    def update(self, dt):
        self.applyGravity(dt)
        self.handleEntityCollisions()

    def applyGravity(self, dt):
        for entity in self.env.entities:
            entity.velocity += pygame.pygame.math.Vector2(0, 16.8) * dt

    def handleEntityCollisions(self):
        for entity in self.env.entities:
            entityCells = entity.spatialPartitioningCells
            potentialColliders = set()
            for cell in entityCells:
                potentialColliders.update(self.spatialPartitioning[cell])
            for collider in potentialColliders:
                if entity.rect().colliderect(collider.rect()):
                    self.handleCollision(entity, collider)

    def handleCollision(self, entity, collider):
        if self.isPlatformer:
            if self.isCollidingFromAbove(entity, collider):
                entity.velocity.y = 0
                entity.position.y = collider.rect().bottom
            elif self.isCollidingFromBelow(entity, collider):
                entity.velocity.y = 0
                entity.position.y = collider.rect().top - entity.rectSize.y
            elif self.isCollidingFromLeft(entity, collider):
                entity.velocity.x = 0
                entity.position.x = collider.rect().right
            elif self.isCollidingFromRight(entity, collider):
                entity.velocity.x = 0
                entity.position.x = collider.rect().left - entity.rectSize.x
        elif self.isTopdown:
            pass

    def isCollidingFromAbove(self, entity, collider):
        return entity.rect().bottom > collider.rect().top and entity.rect().top < collider.rect().top

    def isCollidingFromBelow(self, entity, collider):
        return entity.rect().top < collider.rect().bottom and entity.rect().bottom > collider.rect().bottom

    def isCollidingFromLeft(self, entity, collider):
        return entity.rect().right > collider.rect().left and entity.rect().left < collider.rect().left

    def isCollidingFromRight(self, entity, collider):
        return entity.rect().left < collider.rect().right and entity.rect().right > collider.rect().right

    def updateSpatialPartitioning(self):
        for entity in self.env.entities:
            self.removeEntityFromGrid(entity)
            self.insertEntity(entity)


class Entity(pygame.sprite.Sprite):
    def __init__(self, game, _id:int=random.randint(999,9999), position:pygame.math.Vector2()=pygame.math.Vector2(), size:int=32, rectSize=pygame.math.Vector2(32, 32), spriteGroups:list=[], color:list=[10, 30, 20]):
        super().__init__(spriteGroups)
        self._id = _id
        self.Renderer = None
        self.rectSize = rectSize
        self.size = pygame.math.Vector2(size, size)
        self.spriteGroups = spriteGroups
        self.position = pygame.math.Vector2(position)
        self.velocity = pygame.math.Vector2()
        self.image = pygame.Surface((size, size))
        self.image.fill(color)

    def rect(self):
        return pygame.Rect((self.position.x, self.position.y), (self.rectSize[0], self.rectSize[1]))

    def setRenderer(self, renderer):
        self.Renderer = renderer

    def update(self):
        self.collisions = {"up": False, "down": False, "left": False, "right": False}
        self.position += self.velocity


class NebulaCache:
    def __init__(self, maxSize=100):
        self.cache = {"base": {"cache": {}, "frequency": {}}}
        self.usage = []
        self.maxSize = maxSize

    @outDebugReturn
    def addSubCache(self, name:str=""):
        if name not in self.cache:
            self.cache[name] = {"cache":{}, "frequency":{}}
            return True
        return False

    @outDebugReturn
    def get(self, key, subCache=None):
        subCache = subCache if subCache in self.cache else "base"
        cache = self.cache[subCache]["cache"]
        frequency = self.cache[subCache]["frequency"]

        if key in cache:
            frequency[key] += 1
            self.updateUsage(key, subCache)
            return cache[key]
        else:
            return 'Key Not Present'

    @outDebugReturn
    def put(self, key, value, subCache=None):
        if self.maxSize <= 0:
            return 'Cache is disabled'

        if subCache in self.cache:
            cache = self.cache[subCache]["cache"]
            frequency = self.cache[subCache]["frequency"]
        elif subCache not in self.cache:
            self.cache[subCache] = {"cache":{}, "frequency":{}}
            cache = self.cache[subCache]["cache"]
            frequency = self.cache[subCache]["frequency"]

        if self.checkSize(subCache) >= self.maxSize:
            minFrequencyKey = min(frequency, key=lambda k: (frequency[k], self.usage.index(k)))
            del cache[minFrequencyKey]
            del frequency[minFrequencyKey]

        try:
            cache[key] = value
            frequency[key] = 1
            self.updateUsage(key, subCache)
        except (KeyError, ValueError):
            return 'Key or Value was not given'

    def checkSize(self, subCache="base"):
        return len(self.cache[subCache]["cache"])

    def updateUsage(self, key, subCache="base"):
        if key in self.usage:
            self.usage.remove(key)
        self.usage.append(key)


class Animation:
    def __init__(self, images, frameCount=5, loop=True):
        self.images = images
        self.imageMasks = [pygame.mask.from_surface(image) for image in images]
        self.loop = loop
        self.frameCount = frameCount
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.frameCount, self.loop)

    def update(self):
        if not self.done:
            self.frame = (self.frame + 1) % (self.frameCount * len(self.images)) if self.loop else min(self.frame + 1, self.frameCount * len(self.images) - 1)

    def img(self):
        frameIndex = int(self.frame / self.frameCount)
        return [self.images[frameIndex], self.imageMasks]


class AssetManager:
    def __init__(self, env, maxCacheSize=100):
        self._env = env
        self.cache = NebulaCache(maxSize=maxCacheSize)

    def loadLiveAssets(self, assetsPath: str, animationLib: dict, frameCount: int, willLoop: bool, subCache=None):
        loadedAssets = {}
        for key, folderPath in animationLib.items():
            self.cache.put(key=key, value=Animation(loadAssetDir(assetsPath + f"{folderPath}"), frameCount=frameCount, loop=willLoop), subCache=subCache)
        return True

    def loadStaticAsset(self, assetName: str, assetPath: str, subCache=None):
        self.cache.put(key=assetName, value=loadAsset(assetPath))
        return True

    def putAsset(self, assetID, asset, subCache=None):
        self.cache.put(assetID, asset, subCache=subCache)

    def getAssetByID(self, assetID):
        return self.cache.get(assetID)

    def reloadAssetPosition(self, assetID, position, subCache=None):
        # Update the rendering position of an asset
        asset = self.getAssetByID(assetID)
        if asset:
            self._env.Renderer.addStaticRenderData(assetID, position)
        else:
            print(f"Asset not found: {assetID}")


class Renderer:
    def __init__(self, env, layerCount: int, assetManager: AssetManager):
        self.layerCount = layerCount
        self.renderLayers = [[] for _ in range(layerCount)]
        self.dirtyRects = []
        self.assetManager = assetManager
        self.renderData = []  # Store rendering data for static images

    def addStaticRenderData(self, assetID: str|int, position: pygame.math.Vector2(0, 0)=pygame.math.Vector2(0, 0), offset: pygame.math.Vector2(0, 0)=pygame.math.Vector2(0, 0)):
        # Add rendering data for static imagesz
        self.renderData.append((assetID, position, offset))
    
    def addLayer(self):
        self.layerCount += 1
        self.renderLayers.append([])

    def addAsset(self, assetID: str|int, asset: pygame.Surface, layerNumber: int=0):
        self.renderLayers[layerNumber].append(asset)
        self.dirtyRects.append(asset.get_rect())

    def addEntity(self, obj: Entity, layerNumber: int=0):
        self.renderLayers[layerNumber].append(obj)
        self.assetManager.putAsset(obj._id, obj, subCache="Entities")
        self.dirtyRects.append(obj.rect())

    def render(self, surface: pygame.Surface):
        # Render the layers and assets on them in order
        surface.fill((0, 0, 0))  # Clear the surface
        for layer in self.renderLayers:
            for item in layer:
                if isinstance(item, Entity):
                    item.render(surface)
                elif isinstance(item, pygame.Surface):
                    surface.blit(item, item.get_rect())
                else:
                    print(f"Unsupported item in render layer: {item}")

        # Render static images using the rendering data
        for assetID, position, offset in self.renderData:
            asset = self.assetManager.getAssetByID(assetID)
            try:
                assetImage = asset.img()
                surface.blit(assetImage[0], position - offset)
                self.dirtyRects.append(pygame.Rect(position.x, position.y, assetImage[0].get_width(), assetImage[0].get_height()))
            except AttributeError:
                surface.blit(asset, position - offset)
                self.dirtyRects.append(pygame.Rect(position.x, position.y, asset.get_width(), asset.get_height()))

    def clearDirtyRects(self):
        self.dirtyRects.clear()


class Tilemap:
    def __init__(self, mapDataPath, env, renderer, tileSize=32, physicsTilesIds=None):
        self.env = env
        self.Renderer = renderer
        self.AssetManager = self.Renderer.assetManager
        self.cache = self.AssetManager.cache
        self.tileSize = tileSize
        self.tilemap = {}
        self.physicsTileIDs = set(physicsTilesIds) if physicsTilesIds else set()
        self.load(mapDataPath)

    def load(self, path):
        with open(path, "r") as savefile:
            map_data = json.load(savefile)

        self.mapName = map_data["name"]
        self.tilemap = map_data["tileMap"]
        self.tileSize = map_data["tileSize"]
        self.offgridTiles = map_data["offGrid"]
        self.mapSize = pygame.math.Vector2(map_data['map width']*self.tileSize, map_data['map height']*self.tileSize)

        try:
            [self.AssetManager.putAsset(_id, tile, subCache="tiles") for _id, tile in enumerate(cLoadAssets(map_data["tilesetPath"], self.tileSize))]
        except (KeyError, ValueError):
            return 'unable to cache tileset\n'

    def getMapSize(self, in_tiles=True):
        return self.mapSize.x, self.mapSize.y

    def solidTileCheck(self, position, layer):
        tileLocation = f"{int(position[0] // self.tileSize)};{int(position[1] // self.tileSize)}"
        if layer in self.tilemap and tileLocation in self.tilemap[layer]:
            tile = self.tilemap[layer][tileLocation]
            if tile['id'] in self.physicsTileIDs:
                return tile

    def extractTileInfo(self, tileId, keep=False):
        matches = []
        for layer in self.tilemap.values():
            for location, tile in list(layer.items()):
                if tile['id'] in tileId:
                    matches.append(tile.copy())
                    if not keep:
                        del layer[location]
        
        return matches

    def tilesAround(self, position, layer):
        tiles = []
        tileLocation = (int(position[0] // self.tileSize), int(position[1] // self.tileSize))

        for offset in [(i, j) for i in [-1, 0, 1] for j in [-1, 0, 1]]:
            checkLocation = f"{tileLocation[0] + offset[0]};{tileLocation[1] + offset[1]}"
            if layer in self.tilemap and checkLocation in self.tilemap[layer]:
                tiles.append(self.tilemap[layer][checkLocation])
        
        return tiles

    def physicsRectsAround(self, position, layer):
        rects = []

        for tile in self.tilesAround(position, layer):
            if tile['id'] in self.physicsTileIDs:
                tileX, tileY = tile['position']
                rect = pygame.Rect(tileX * self.tileSize, tileY * self.tileSize, self.tileSize, self.tileSize)
                rects.append(rect)
        
        return rects

    def exportAsPng(self, savePath):
        mapSize = self.getMapSize(inTiles=False)
        exportSurface = pygame.Surface(mapSize)
        exportSurface.fill((255, 255, 255))

        for layer in self.tilemap.values():
            for location, tile in list(layer.items()):
                tileImage = self.cache.cache['tiles']['cache'][tile['id']]
                x, y = tile['position']
                position = (x * self.tileSize, y * self.tileSize)
                exportSurface.blit(tileImage, position)

        exportFilename = f'{self.mapName}.png'
        fullExportPath = os.path.join(savePath, exportFilename)
        pygame.image.save(exportSurface, fullExportPath)
        return f"Map exported as {fullExportPath}"

    def render(self, surface, offset=pygame.math.Vector2(), zoomFactor=1):
        visibleArea = pygame.Rect(1 / zoomFactor, 1 / zoomFactor, surface.get_width(), surface.get_height())
        # offset += pygame.math.Vector2(0.2, 0.4)
        for layer in self.tilemap.values():
            for location, tile in list(layer.items()):
                tileRect = pygame.Rect(
                    tile['position'][0] * self.tileSize - offset[0],
                    tile['position'][1] * self.tileSize - offset[1],
                    self.tileSize, self.tileSize
                )

                if tileRect.colliderect(visibleArea):
                    assetId = tile['id']
                    asset = self.cache.cache['tileset']['cache'][assetId]
                    position = pygame.math.Vector2(tileRect.topleft)
                    self.Renderer.render(surface)
                    # self.Renderer.renderAssets([assetId], surface, [position])
                    # self.Renderer.renderAssets([assetId], renderSurf, [position])




"""NEBULA"""
# [monitor := m for m in get_monitors()]
# os.environ['SDL_VIDEO_WINDOW_POS'] = f'{str(int(monitor.width)/2)},{str(int(monitor.height)/2)}'
# NebulaEnv(
#     int(input('Enter Desired Screen Width:\t')), int(input('Enter Desired Screen Height:\t'))
#     ).run()



