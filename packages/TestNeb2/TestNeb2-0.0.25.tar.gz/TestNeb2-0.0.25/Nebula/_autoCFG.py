try:
    from .NebulaCore import *
except ModuleNotFoundError:
    mnf = str(input("~| SCRIPT IMPORT ERROR...\nThere was an error while gathering _autoCFG.core\nPlease check that your installation directory contains the 'core' sub-directory and in that is the '_scripts' sub-directory .\nIf so, type 'fix' to open the Nebula Console.\nWhen the command line appears, type 'neb -fix ~core' to run the appropriate repair script.\nIf the problem persists, contact setoichi.\n~| ")) #cmd, flg, mod
    if mnf in {"fix",}:
        print("open Abyss Console\n")
    import os
    os.sys.exit()


ncfg = False

def Main(projectType:str, projectName:str, projectPath:str) -> bool:
    print('Nebula project path ->',projectPath,"\n")
    projectDir = os.path.join(projectPath, projectName)
    print('Nebula project dir ->',projectDir,"\n")
    
    try:
        open(f"{projectDir}\\nenv\\.ncfg", "r")
        ncfg = True
    except FileNotFoundError:
        print('ncfg not found')
    
    if ncfg:
        print(ncfg, 'ncfg found!\n')
        
        with open(f"{projectDir}\\nenv\\.ncfg", "r") as cfgReader:
            cfgData = json.load(cfgReader)
            cfgReader.close()

        if cfgData['env']['configured'] == 'False':

            try:
                open(f"{projectDir}\\nenv\\.ncfg", "w")
            except FileNotFoundError:
                # os.makedirs()
                pass

            with open(f"{projectDir}\\nenv\\.ncfg", "w") as cfgWriter:
                # Implement Automatic Configuration Here LOL
                from ._ideps import Main   # install dependancies

                finalCFG = ncfgTemplate = {
                    "env": {
                        "debug": "False",
                        "update": "False",
                        "configured": "True"
                    },
                    "project": {
                        "cfg":"auto",
                        "build ver": "v0.0.1",
                        "abyss ver": "v0.0.1",
                        "project name": f"{projectName}",
                        "project type": f"{projectType}",
                        "project path": f"{projectDir}",
                        "tilesize": 8,
                        "tilemap size": [5000,5000],
                        "screen size": [1400, 800],
                        "canvas size": [700, 400],
                        "target FPS": 60
                    }
                }

                cfgWriter.write("")
                json.dump(finalCFG, cfgWriter, indent=4)
                cfgWriter.close()
            print('project was not pre-configured\n_autoCFG did so...\n')
            return True

        if cfgData['env']['configured'] == 'True':
            import _ideps # install dependancies
            print('project was pre-configured???\n')
            return True

    else:
        print('ncfg not found!\n')

    

