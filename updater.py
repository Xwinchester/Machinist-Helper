import os
import json
import urllib.request
import tkinter as tk
from tkinter import messagebox

class AppUpdater:
    # Define the URL to the GitHub repository where the JSON file is located
    REPO_URL = "https://raw.githubusercontent.com/Xwinchester/Machinist-Helper/main/version.json"
    DIR = os.path.join ('C:\\', 'Users', os.getlogin (), 'Machinist Cheat Sheet')
    JSON_FILE_PATH = "version.json"
    LATEST_VERSION = "1.0.0"
    LOCAL_VERSION = "0.0.0"
    
    def __init__(self, root):
        self.JSON_FILE_PATH = os.path.join(self.DIR, self.JSON_FILE_PATH)
        self.root = root
        self.get_latest_version() # grabs most recent version from Github
        self.check_version()

    
    
    def check_version(self):
        # Compare local version to remote version
        if self.LOCAL_VERSION != self.LATEST_VERSION:
            self.force_update(self.LATEST_VERSION)

        # If the version JSON file doesn't exist, download it
        else:
            self.download_json()

    def download_json(self):
        # Download the version JSON file from the GitHub repository
        try:
            with urllib.request.urlopen(self.REPO_URL) as url:
                data = json.loads(url.read().decode())
                self.force_update(data)
        except urllib.error.URLError as e:
            messagebox.showerror("Error", f"Unable to download version information: {e.reason}")

    def force_update(self, version_data):
        # Download and replace the main application file
        try:
            # Save the updated version JSON file
            with open(self.JSON_FILE_PATH, "w") as f:
                json.dump(version_data, f)

            # Notify the user that the update is complete and restart the application
            messagebox.showinfo("Update", "The application has been updated. Please restart it.")
            self.root.quit()
        except urllib.error.URLError as e:
            messagebox.showerror("Error", f"Unable to download update: {e.reason}")

    def get_local_version(self):
        # Check if the version JSON file exists locally
        if os.path.exists(self.JSON_FILE_PATH):
            with open(self.JSON_FILE_PATH, "r") as f:
                local_version_data = json.load(f)
            self.LOCAL_VERSION = local_version_data["version"]

    def get_latest_version(self):
        # Download the version JSON file from the GitHub repository
        try:
            with urllib.request.urlopen(self.REPO_URL) as url:
                self.LATEST_VERSION = json.loads(url.read().decode())['version']
        except urllib.error.URLError as e:
            messagebox.showerror("Error", f"Unable to download version information: {e.reason}")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    updater = AppUpdater(root)
    root.mainloop()
