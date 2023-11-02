import ctypes
def Administrate(File):
    if ctypes.windll.shell32.IsUserAnAdmin() == 0:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", "python", File, None, 1)
    else:
        return("Unable to administrate file: User is not Administrator.")