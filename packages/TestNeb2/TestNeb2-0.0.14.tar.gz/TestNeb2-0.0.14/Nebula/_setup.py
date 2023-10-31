try:
    from ._obj import *
    from ._utils import *
except ModuleNotFoundError:
    mnf = str(input("~| SCRIPT IMPORT ERROR...\nThere was an error while gathering _setup core\nPlease check that your installation directory contains the 'core' sub-directory.\nIf so, type 'fix' to open the Nebula Console.\nWhen the command line appears, type 'neb -fix ~core' to run the appropriate repair script.\nIf the problem persists, contact setoichi.\n~| ")) #cmd, flg, mod
    if mnf in {"fix",}:
        print("open Abyss Console\n")
    import os
    os.sys.exit()

class Main:
    def __init__(self, projectName:str="MyNebulaProject", projectType:str="pt", projectPath:str=os.path.join(os.getcwd(), "MyNebulaProject"), autoNCFG:bool=True, manNCFG:bool=False):    
        
        if autoNCFG and not manNCFG:
            self.autoNCFG(projectName=projectName, projectPath=projectPath)
        if manNCFG and not autoNCFG:
            self.manNCFG(projectName=projectName, projectPath=projectPath)

    def genProjectDir(self, projectName:str="MyNebulaProject", projectPath:str=os.path.join(os.getcwd(), "MyNebulaProject")):
        # Create the project directory
        project_dir = os.path.join(projectPath, projectName)
        if not os.path.exists(project_dir):
            os.makedirs(project_dir)

        # Create assets directory
        assets_dir = os.path.join(project_dir, 'assets')
        if not os.path.exists(assets_dir):
            os.makedirs(assets_dir)

        # Create game directory
        game_dir = os.path.join(project_dir, 'game')
        if not os.path.exists(game_dir):
            os.makedirs(game_dir)

        # Create nenv directory
        nenv_dir = os.path.join(project_dir, 'nenv')
        if not os.path.exists(nenv_dir):
            os.makedirs(nenv_dir)

        # Create _dat directory
        dat_dir = os.path.join(nenv_dir, '_dat')
        if not os.path.exists(dat_dir):
            os.makedirs(dat_dir)
        
        # Create _bin directory
        bin_dir = os.path.join(nenv_dir, '_bin')
        if not os.path.exists(bin_dir):
            os.makedirs(bin_dir)
        
        # Create _lib directory
        lib_dir = os.path.join(nenv_dir, '_lib')
        if not os.path.exists(lib_dir):
            os.makedirs(lib_dir)

        # Create the notes.txt + settings.json in game directory
        for file_name in ['notes.txt', 'settings.json']:
            with open(os.path.join(game_dir, file_name), 'w') as f:
                f.write("{}")
                f.close()

        # Create the .ncfg in nenv directory
        with open(os.path.join(nenv_dir, '.ncfg'), 'w') as ncfg:
            ncfg.write("ncfg")
            ncfg.close()
        
        # Create nebula.log in _dat directory
        with open(os.path.join(dat_dir, 'nebula.log'), 'w') as logfile:
            logfile.write("Nebula Log")
            logfile.close()

        return True

    def genCFG(self, projectName:str="MyNebulaProject", projectPath:str=os.path.join(os.getcwd(), "MyNebulaProject")):
        ncfgTemplate = {
            "env": {
                "debug": "False",
                "update": "False",
                "configured": "False"
            },
            "project": {
                "cfg":"auto",
                "build ver": "v0.0.1",
                "abyss ver": "v0.0.1",
                "project name": "",
                "project type": "",
                "project path": f"{projectPath}{projectName}",
                "tilesize": 16,
                "tilemap size": [5000,5000],
                "screen size": [1400, 800],
                "canvas size": [700, 400],
                "target FPS": 60
            }
        }
        
        with open(f"{projectPath}/{projectName}/nenv/.ncfg", "w") as f:
            json.dump(
                ncfgTemplate,
                f,
                indent=4
            )
            f.close()

    def autoNCFG(self, projectName:str="MyNebulaProject", projectPath:str=os.path.join(os.getcwd(), "MyNebulaProject")):
        if self.genProjectDir(projectName=projectName, projectPath=projectPath):
            self.genCFG(projectName=projectName, projectPath=projectPath)

            from ._autoCFG import projectName as apn
            from ._autoCFG import projectPath as appt
            from ._autoCFG import Main as autoMain
            apn = projectName
            appt = projectPath
            autoMain()

setup = Main(
    projectName="ExampleProject",
    projectType="pt",
    projectPath="C:\\",
    autoNCFG=True,
    manNCFG=False
)

