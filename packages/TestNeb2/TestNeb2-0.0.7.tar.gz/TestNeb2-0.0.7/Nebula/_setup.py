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
    def __init__(self, projectName:str="MyNebulaProject", projectType:str="pt", projectPath:str=core.os.path.join(core.os.getcwd(), "MyNebulaProject"), autoNCFG:bool=True, manNCFG:bool=False):    
        
        if autoNCFG and not manNCFG:
            self.autoNCFG(projectName=projectName, projectPath=projectPath)
        if manNCFG and not autoNCFG:
            self.manNCFG(projectName=projectName, projectPath=projectPath)

    def genProjectDir(self, projectName:str="MyNebulaProject", projectPath:str=core.os.path.join(core.os.getcwd(), "MyNebulaProject")):
        # Create the project directory
        project_dir = core.os.path.join(projectPath, projectName)
        if not core.os.path.exists(project_dir):
            core.os.makedirs(project_dir)

        # Create assets directory
        assets_dir = core.os.path.join(project_dir, 'assets')
        if not core.os.path.exists(assets_dir):
            core.os.makedirs(assets_dir)

        # Create game directory
        game_dir = core.os.path.join(project_dir, 'game')
        if not core.os.path.exists(game_dir):
            core.os.makedirs(game_dir)

        # Create nenv directory
        nenv_dir = core.os.path.join(project_dir, 'nenv')
        if not core.os.path.exists(nenv_dir):
            core.os.makedirs(nenv_dir)

        # Create _dat directory
        dat_dir = core.os.path.join(nenv_dir, '_dat')
        if not core.os.path.exists(dat_dir):
            core.os.makedirs(dat_dir)
        
        # Create _bin directory
        bin_dir = core.os.path.join(nenv_dir, '_bin')
        if not core.os.path.exists(bin_dir):
            core.os.makedirs(bin_dir)
        
        # Create _lib directory
        lib_dir = core.os.path.join(nenv_dir, '_lib')
        if not core.os.path.exists(lib_dir):
            core.os.makedirs(lib_dir)

        # Generate Templates
        template_path = os.path.dirname(os.path.abspath(__file__))+"\\_templates"
        main_code = open(template_path+"\\main.txt", "r").read()
        Nebula_code = open(template_path+"\\Nebula.txt", "r").read()
        _utils_code = open(template_path+"\\_utils.txt", "r").read()
        _obj_code = open(template_path+"\\_obj.txt", "r").read()
        
        # Create other required files
        # Create the main.py in game directory
        with open(core.os.path.join(game_dir, 'main.py'), 'w') as main_file:
            main_file.write(main_code)

        # Create the notes.txt + settings.json in game directory
        for file_name in ['notes.txt', 'settings.json']:
            with open(core.os.path.join(game_dir, file_name), 'w') as f:
                f.write("{}")
                f.close()

        # Create the .ncfg in nenv directory
        with open(core.os.path.join(nenv_dir, '.ncfg'), 'w') as ncfg:
            ncfg.write("ncfg")
            ncfg.close()
        
        # Create nenv.py in nenv directory
        with open(core.os.path.join(nenv_dir, 'nenv.py'), 'w') as nenv:
            nenv.write("nenv")
            nenv.close()

        # Create _utils.py in _lib directory
        with open(core.os.path.join(lib_dir, '_utils.py'), 'w') as logfile:
            logfile.write(_utils_code)
            logfile.close()
        
        # Create _obj.py in _lib directory
        with open(core.os.path.join(lib_dir, '_obj.py'), 'w') as logfile:
            logfile.write(_obj_code)
            logfile.close()

        # Create Nebula.py in _lib directory
        with open(core.os.path.join(lib_dir, 'Nebula.py'), 'w') as logfile:
            logfile.write(Nebula_code)
            logfile.close()

        # Create nebula.log in _dat directory
        with open(core.os.path.join(dat_dir, 'nebula.log'), 'w') as logfile:
            logfile.write("Nebula Log")
            logfile.close()

        return True

    def genCFG(self, projectName:str="MyNebulaProject", projectPath:str=core.os.path.join(core.os.getcwd(), "MyNebulaProject")):
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
            core.json.dump(
                ncfgTemplate,
                f,
                indent=4
            )
            f.close()

    def manNCFG(self, projectName:str="MyNebulaProject", projectPath:str=core.os.path.join(core.os.getcwd(), "MyNebulaProject")):
        if self.genProjectDir(projectName=projectName, projectPath=projectPath):
            self.genCFG(projectName=projectName, projectPath=projectPath)

            from _scripts import _manCFG
            _manCFG.projectName = projectName
            _manCFG.projectPath = projectPath
            _manCFG.main()  

    def autoNCFG(self, projectName:str="MyNebulaProject", projectPath:str=core.os.path.join(core.os.getcwd(), "MyNebulaProject")):
        if self.genProjectDir(projectName=projectName, projectPath=projectPath):
            self.genCFG(projectName=projectName, projectPath=projectPath)

            from _scripts import _autoCFG
            _autoCFG.projectName = projectName
            _autoCFG.projectPath = projectPath
            print(_autoCFG.__file__)
            _autoCFG.main()

setup = Main(
    projectName="ExampleProject",
    projectType="pt",
    projectPath="C:\\",
    autoNCFG=True,
    manNCFG=False
)

