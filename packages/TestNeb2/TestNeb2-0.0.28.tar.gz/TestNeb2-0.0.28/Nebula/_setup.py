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
            print('manual config specified\n\n')
            pass

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
        
        with open(f"{projectPath}\\.ncfg", "r") as check:
            data = json.load(check)
        print(data)
        if data['env']['configured'] == 'True':
            print('this Nebula project was already configured!\n\n')
        else:
            with open(f"{projectPath}\\.ncfg", "w") as f:
                json.dump(
                    ncfgTemplate,
                    f,
                    indent=4
                )
                f.close()

    def autoNCFG(self,projectType:str="pt", projectName:str="MyNebulaProject", projectPath:str=os.path.join(os.getcwd(), "MyNebulaProject")):
        self.genCFG(projectType=projectType, projectName=projectName, projectPath=projectPath)

            # from ._autoCFG import Main as autoMain
            # autoMain(projectType=projectType, projectName=projectName, projectPath=projectPath)

setup = Main(
    projectName="ExampleProject",
    projectType="pt",
    projectPath="C:\\",
    autoNCFG=True,
    manNCFG=False
)

