try:
    from .NebulaCore import *
except ModuleNotFoundError:
    mnf = str(input("~| SCRIPT IMPORT ERROR...\nThere was an error while gathering _autoCFG.core\nPlease check that your installation directory contains the 'core' sub-directory and in that is the '_scripts' sub-directory .\nIf so, type 'fix' to open the Nebula Console.\nWhen the command line appears, type 'neb -fix ~core' to run the appropriate repair script.\nIf the problem persists, contact setoichi.\n~| ")) #cmd, flg, mod
    if mnf in {"fix",}:
        print("open Abyss Console\n")
    import os
    os.sys.exit()


ncfg = False

@outDebugReturn
def Main(projectType:str, projectName:str, projectPath:str) -> bool:
    try:
        open(f"{projectPath}\\.ncfg", "r")
        ncfg = True
    except FileNotFoundError:
        return 'ncfg not found'
    
    if ncfg:
        with open(f"{projectPath}\\.ncfg", "r") as cfgReader:
            cfgData = json.load(cfgReader)
            cfgReader.close()

        if cfgData['env']['configured'] == 'False':
            with open(f"{projectPath}\\.ncfg", "w") as cfgWriter:
                finalCFG = ncfgTemplate = {
                    "env": {
                        "debug": "False",
                        "update": "False",
                        "configured": "True"
                    },
                    "project": {
                        "cfg":"auto",
                        "build ver": "v0.0.1",
                        "project name": f"{projectName}",
                        "project type": f"{projectType}",
                        "project path": f"{projectPath}",
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
            return 'Nebula project configured!'

        elif cfgData['env']['configured'] == 'True':
            return 'Nebula Project Configured.'
    else:
        return 'ncfg not found!'