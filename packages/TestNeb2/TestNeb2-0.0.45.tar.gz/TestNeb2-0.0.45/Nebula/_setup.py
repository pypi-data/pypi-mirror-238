try:
    from .NebulaObject import *
    from .NebulaCore import *
except ModuleNotFoundError:
    mnf = str(input("~| SCRIPT IMPORT ERROR...\nThere was an error while gathering _setup core\nPlease check that your installation directory contains the 'core' sub-directory.\nIf so, type 'fix' to open the Nebula Console.\nWhen the command line appears, type 'neb -fix ~core' to run the appropriate repair script.\nIf the problem persists, contact setoichi.\n~| ")) #cmd, flg, mod
    if mnf in {"fix",}:
        print("open Abyss Console\n")
    import os
    os.sys.exit()

class Main:
    def __init__(self, projectName:str="MyNebulaProject", projectType:str="pt", projectPath:str=os.path.join(os.getcwd(), "MyNebulaProject"), autoNCFG:bool=True, manNCFG:bool=False):    
        
        if autoNCFG and not manNCFG:
            self.autoNCFG(projectType=projectType, projectName=projectName, projectPath=projectPath)
        if manNCFG and not autoNCFG:
            return 'manual config specified\n\n'

        if not os.path.exists('C:\\.NebulaCache'):
            os.mkdir('C:\\.NebulaCache')

        if not os.path.exists('C:\\.NebulaCache\\nebula-cache.json'):
            with open('C:\\.NebulaCache\\nebula-cache.json', 'w') as f:
                f.write("")
                json.dump({"Nebula":{}}, f, indent=4)
                f.close()

    def genCFG(self,projectType:str="pt", projectName:str="MyNebulaProject", projectPath:str=os.path.join(os.getcwd(), "MyNebulaProject")):
        ncfgTemplate = {
            "env": {
                "debug": "False",
                "update": "False",
                "configured": "False"
            },
            "project": {
                "cfg":"auto",
                "build ver": "v0.0.1",
                "project name": f"{projectName}",
                "project type": f"{projectType}",
                "project path": f"{projectPath}{projectName}",
                "tilesize": 8,
                "tilemap size": [5000,5000],
                "screen size": [1400, 800],
                "canvas size": [700, 400],
                "target FPS": 60
            }
        }
        
        with open(f"{projectPath}{projectName}\\.ncfg", "r") as check:
            c = check.read()
            check.close()
        if "env" not in c:
            with open(f"{projectPath}{projectName}\\.ncfg", "w") as f:
                json.dump(
                    ncfgTemplate,
                    f,
                    indent=4
                )
                f.close()
        if "env" in c:
            with open(f"C:\\.NebulaCache\\nebula-cache.json", "r") as f:
                cache = json.load(f)
                f.close()
            cache['Nebula'][projectName] = {}
            cache['Nebula'][projectName]['path'] = projectPath
            cache['Nebula'][projectName]['project name'] = projectPath
            print("modified cache",cache,"\n\n\n")

            with open(f"{projectPath}{projectName}\\.ncfg", "r") as f:
                data = json.load(f)
                f.close()

            if data['env']['configured'] == 'True':
                return 'this Nebula project was already configured!\n\n'

    def autoNCFG(self,projectType:str="pt", projectName:str="MyNebulaProject", projectPath:str=os.path.join(os.getcwd(), "MyNebulaProject")):
        self.genCFG(projectType=projectType, projectName=projectName, projectPath=projectPath)

        from ._autoCFG import Main as autoMain
        autoMain(projectType=projectType, projectName=projectName, projectPath=projectPath)

setup = Main(
    projectName="ExampleProject",
    projectType="pt",
    projectPath="C:\\",
    autoNCFG=True,
    manNCFG=False
)

