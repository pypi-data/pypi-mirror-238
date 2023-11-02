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
                "project path": f"{projectPath}",
                "tilesize": 8,
                "tilemap size": [5000,5000],
                "screen size": [1400, 800],
                "canvas size": [700, 400],
                "target FPS": 60
            }
        }
        
        with open(f"{projectPath}\\.ncfg", "r") as check:
            c = check.read()
            check.close()
        if "env" not in c:
            with open(f"C:\\.NebulaCache\\nebula-cache.json", "r") as f:
                cache = json.load(f)
                f.close()
            cache['Nebula'][projectName] = {}
            cache['Nebula']['current project'] = projectName
            cache['Nebula'][projectName]['path'] = projectPath
            cache['Nebula'][projectName]['project name'] = projectName
            with open(f"C:\\.NebulaCache\\nebula-cache.json", "w") as f:
                json.dump(cache, f, indent=4)
                f.close()
            
            with open(f"{projectPath}\\.ncfg", "w") as f:
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
            cache['Nebula']['current project'] = projectName
            cache['Nebula'][projectName]['path'] = projectPath
            cache['Nebula'][projectName]['project name'] = projectName
            with open(f"C:\\.NebulaCache\\nebula-cache.json", "w") as f:
                json.dump(cache, f, indent=4)
                f.close()

            with open(f"{projectPath}\\.ncfg", "r") as f:
                data = json.load(f)
                f.close()

            if data['env']['configured'] == 'True':
                return 'Nebula Project Configured.'

    def autoNCFG(self,projectType:str="pt", projectName:str="MyNebulaProject", projectPath:str=os.path.join(os.getcwd(), "MyNebulaProject")):
        self.genCFG(projectType=projectType, projectName=projectName, projectPath=projectPath)

        from ._autoCFG import Main as autoMain
        autoMain(projectType=projectType, projectName=projectName, projectPath=projectPath)


if not os.path.exists('C:\\.NebulaCache'):
    os.mkdir('C:\\.NebulaCache')

if not os.path.exists('C:\\.NebulaCache\\nebula-cache.json'):
    with open('C:\\.NebulaCache\\nebula-cache.json', 'w') as f:
        f.write("")
        json.dump({"Nebula":{}}, f, indent=4)
        f.close()

with open(f"C:\\.NebulaCache\\nebula-cache.json", "r") as f:
    cache = json.load(f)
    f.close()


def configRecentProject(choice:str):
    projectPath=cache['Nebula'][choice]['path']
    print(f'~| Configuring {choice}...')
    Main(
        projectName=choice,
        projectType="pt",
        projectPath=projectPath,
        autoNCFG=True,
        manNCFG=False
    )

def configLoadProject(choice:str):
    if choice in list(cache['Nebula'].keys()):
        projectPath=cache['Nebula'][choice]['path']
        print(f'~| Configuring {choice}...')
        Main(
            projectName=choice,
            projectType="pt",
            projectPath=projectPath,
            autoNCFG=True,
            manNCFG=False
        )
    else:
        print(f'~| Unable to locate {choice}!\n~| You can navigate to your project\'s .ncfg and take a look at the name if need be!\n')
        time.sleep(1.3)
        projectConfig()

def configNewProject():
    print('~| New project...\n~| Lets get it set up!\n')
    Main(
        projectName=str(input('~| Please enter a name for this project: ')),
        projectType="pt",
        projectPath=str(input('~| Please enter the path where your project\'s .ncfg is located:    ')),
        autoNCFG=True,
        manNCFG=False
    )

def projectConfig():
    os.system('cls')
    if len(cache['Nebula']) != 0:
        recentProject = list(cache['Nebula'].keys())[len(cache['Nebula'])-1]
        configChoice = str(input(f'~|(y/yes/n/no/new/exit)\n~| Configure {recentProject}?: '))
        if configChoice in {'', 'y', 'Y', 'yes', 'Yes'}:
            configRecentProject(choice=recentProject)
        elif configChoice in {'n', 'N', 'no', 'No'}:
            choice = str(input('~| Alright, name the project you wish to configure: '))
            configLoadProject(choice=choice)
        elif configChoice in {'new', 'New'}:
            configNewProject()
        elif configChoice in {'exit', 'Exit'}:
            print('~| Quitting Nebula Project Configuration...\n')
            os.sys.exit()
        else:
            print('~| Invalid option!')
            time.sleep(0.8)
            projectConfig()

projectConfig()