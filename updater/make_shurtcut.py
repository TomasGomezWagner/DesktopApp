import os
from pathlib import Path
import win32com.client


def make_shortcut(dest:str, name:str) -> None:
    """Make shortcut of `source` path to file in `dest_dir` target folder.
    If `name` is None, will use `source`'s filename.
    """
    source = dest + r'\dist\vista\vista.exe'
    icon = dest + r'\dist\vista\img\logo.ico'
    dest_dir = os.path.join(os.environ['HOMEPATH'], 'Desktop')

    # process user input
    if name is None:
        name = Path(source).name
    dest_path = str(Path(dest_dir, name)) + '.lnk'
    
    # make shortcut
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(dest_path)
    shortcut.IconLocation = icon
    shortcut.Targetpath = source
    shortcut.WorkingDirectory = str(Path(source).resolve().parent)
    shortcut.save()
    

#make_shortcut(r'C:\Users\hcapra\Desktop\arreglo_csv_exe\versiones\win\1.2.1_windows', name='Procesos')