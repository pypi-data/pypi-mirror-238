import platform, ctypes, pathlib, os

confFile = 'winLinux.cmd' # exist on "A:/miniProject/biobeee/Entrez/" for development stage
complition = "Installed WSL and edirect for machine: "

currentPath = str(pathlib.Path(__file__).parent.resolve())
# print("current path:", currentPath)

def Edirect_Config():

    if platform.platform().split('-')[0] == 'Windows':
        ctypes.windll.shell32.ShellExecuteW(None, u"runas", u"cmd.exe", f"/k {currentPath}\{confFile}", None, 1)
        os.system('wsl %s/EntrezConfig.sh'%currentPath.replace('\\', '/'))
        print(complition, platform.platform())
        pass

    elif platform.platform().split('-')[0] == 'Linux':
        os.system('sudo chmod 755 %s/EntrezConfig.sh'%currentPath.replace('\\', '/'))
        os.system('%s/EntrezConfig.sh'%currentPath.replace('\\', '/'))
        print("Build on",platform.platform())
        pass

    elif platform.platform().split('-')[0] == 'macOS':
        pass

# print(currentPath, "\config.py")

# "runas", "/noprofile", "/user:YADAV ANIKET\\administrator", "cmd"
#  subprocess.run(["powershell", "Start-Process cmd -Verb RunAs", "b:"], shell=True)
# "runas", "/user:ANIYD\\YADAV ANIKET\\administrator", "cmd" not working....
# "powershell", "Start-Process cmd -Verb RunAs B:/" working...

# powershell "Start-Process cmd -Verb RunAs"