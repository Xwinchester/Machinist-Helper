import tkinter as tk
from tkinter import  messagebox
import os
import AutoUpdate
from win32com.client import Dispatch

class Update:

    GITHUB_URL = "https://raw.githubusercontent.com/Xwinchester/Machinist-Helper/main/"
    C_DRIVE = os.path.join ("C:\\", "Users", os.getlogin (), "Machinist Cheat Sheet")
    FILES = {}
    FILES_NAMES = ["icon.ico", "Machinist_Cheat_Sheet.exe", "drill_chart.html", "icon.png", "machinistcheatsheet.json", "styles.css", "version.txt"]
    VERSION = None
    DIRECTORY = None
    START_MENU = os.path.join ("C:\\", "Users", os.getlogin (), "AppData", "Roaming", "Microsoft", "Windows",
                                  "Start Menu", "Programs", "Machinist Cheat Sheet.lnk")

    @classmethod
    def CheckForUpdate(cls):
        cls.__create_filepaths()
        # sets url to github version file that stores current version
        AutoUpdate.set_url (cls.GITHUB_URL + "version.txt")
        try:
            AutoUpdate.set_current_version(open(cls.FILES['txt']).read().strip())
        except:
            AutoUpdate.set_current_version("-1")

        # stores current version

        cls.VERSION = AutoUpdate.get_latest_version()
        return AutoUpdate.is_up_to_date()

    @classmethod
    def ForceUpdate(cls):
            cls.__create_filepaths ()
            root = tk.Tk()
            root.withdraw()
            answer = messagebox.askyesnocancel("Update", "New update available, update files?")
            if answer:
                cls.delete_files()
                # update files
                for key, filepath in cls.FILES.items():
                    file_name = filepath.split('\\')[-1]
                    print(f"Downloading {file_name}")
                    AutoUpdate.set_download_link (cls.GITHUB_URL + file_name)
                    AutoUpdate.download (filepath)
                    if key == "exe":
                       cls.create_shortcut()
                       cls.create_desktop_shortcut()

                root = tk.Tk()
                root.withdraw()
                messagebox.showinfo("Update", "File Updated, Please Reopen file.")

    @classmethod
    def create_shortcut(cls):
        # Check if the shortcut file already exists, and delete it if necessary
        if os.path.exists (cls.START_MENU):
            os.remove (cls.START_MENU)

        shell = Dispatch ("WScript.Shell")
        shortcut = shell.CreateShortCut (cls.START_MENU)
        shortcut.Targetpath = cls.FILES['exe']
        shortcut.WorkingDirectory = os.path.dirname (cls.FILES['exe'])
        shortcut.IconLocation = cls.FILES['exe']
        shortcut.save ()

    @classmethod
    def create_desktop_shortcut(cls):
        # Get the path to the desktop folder
        shortcut_name = "Machinist Cheat Sheet"
        desktop_path = os.path.join (os.path.expanduser ("~"), "Desktop")

        # Create a full path to the shortcut file
        shortcut_path = os.path.join (desktop_path, f"{shortcut_name}.lnk")

        # Check if the shortcut file already exists, and delete it if necessary
        if os.path.exists (shortcut_path):
            os.remove (shortcut_path)

        # Create a new shortcut
        shell = Dispatch ("WScript.Shell")
        shortcut = shell.CreateShortCut (shortcut_path)

        # Set the properties of the shortcut
        shortcut.Targetpath = cls.FILES['exe']
        shortcut.WorkingDirectory = os.path.dirname (cls.FILES['exe'])
        shortcut.IconLocation = cls.FILES['exe'] + ",0"

        # Save the shortcut
        shortcut.save ()

    @classmethod
    def delete_files(cls):
        for filepath in cls.FILES.values ():
            if os.path.exists (filepath):
                os.remove (filepath)
                print (f"Deleted file: {filepath}")
            else:
                print (f"File not found: {filepath}")

    @classmethod
    def __create_filepaths(cls):
        cls.FILES.clear()
        for filename in cls.FILES_NAMES:
            extension = os.path.splitext (filename)[1][1:].lower ()  # Get file extension in lowercase
            filepath = os.path.join (cls.C_DRIVE, filename)  # Get full file path
            cls.FILES[extension] = filepath  # Add to FILES dictionary

if __name__ == '__main__':
    print('Working on updates')
    Update.ForceUpdate()
