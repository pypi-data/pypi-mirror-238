try:
    from .NebulaCore import *
except ModuleNotFoundError:
    mnf = str(input("~| SCRIPT IMPORT ERROR...\nThere was an error while gathering _ideps.core\nPlease check that your installation directory contains the 'core' sub-directory and in that is the '_scripts' sub-directory .\nIf so, type 'fix' to open the Nebula Console.\nWhen the command line appears, type 'neb -fix ~core' to run the appropriate repair script.\nIf the problem persists, contact setoichi.\n~| ")) #cmd, flg, mod
    if mnf in {"fix",}:
        print("open Abyss Console\n")
    import os
    os.sys.exit()


@outDebugReturn
def Main():
    dependencies = ["python"]
    pyDeps = ["pygame-ce", "pygame-gui"]
    installed_dependencies = []

    for dep in dependencies:
        try:
            # Check if the dependency is installed
            subprocess.check_output(f"{dep} --version", shell=True, stderr=subprocess.STDOUT)
            installed_dependencies.append(dep)
        except subprocess.CalledProcessError:
            print(f"{dep} is not installed. Installing {dep}...")

            if platform.system() == "Windows":
                # Use PowerShell to install dependencies on Windows
                subprocess.call(f"powershell -Command \"Start-Process 'https://www.python.org/ftp/python/3.11.6/python-3.11.6-arm64.exe' -ArgumentList '/quiet InstallAllUsers=1 PrependPath=1' -Wait\"", shell=True)
                
    if "python" in installed_dependencies:
        for dep in pyDeps:
            try:    
                subprocess.call(f"powershell -Command \"python -m pip install {dep}\"", shell=True)
            except subprocess.CalledProcessError:
                print("python is not installed properly.\nTry running this script again or visiting this link:\nhttps://www.python.org/ftp/python/3.11.6/python-3.11.6-arm64.exe")
            
    return "Nebula has installed its own dependencies."

Main()