import json, os, webbrowser, urllib.request
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog, messagebox

# globals
DIR = os.path.join ('C:\\', 'Users', os.getlogin (), 'Machinist Cheat Sheet')
#CONFIG_DIR = os.path.join ('C:\\', 'Users', os.getlogin (), 'Machinist Cheat Sheet')
BACKGROUND = '#345760'
FILENAME = os.path.join(DIR,'machinistcheatsheet.json')
ICON = os.path.join(DIR, 'icon.png')
CSS = os.path.join(DIR, 'styles.css')
DRILL_CHART = os.path.join(DIR, 'drill_chart.html')
VERSION_FILE = os.path.join(DIR, 'config.json')
#EXE_FILE = os.path.join(DIR, 'Machinist Helper.exe')


BACKGROUND_IMAGE = os.path.join(DIR, 'background.png')
PROGRAM_TITLE = "Machinist Cheat Sheet"
# version
"""
version 1.1.0 Revisions:
    - Added A Option Menu to grab all taps involved in tap size
    - Added Tap Drill Chart to main function
version 1.2.0 Revision:
    - Added a Folder Creator to Create generic folders that Corning uses.
version 1.3.1 Revision:
    - Revised all classes to start from AppWindow and read everything from json file

***** IDEAS *****
TODO: Format numbers in the formulas to have commas: 15000 = 15,000
*****
"""


class AppUpdater:
    # Define the URL to the GitHub repository where the JSON file is located
    REPO_URL = "https://raw.githubusercontent.com/Xwinchester/Machinist-Helper/main/"
    # make sure version file is index 0
    # if skip == 1, will skip updated that item on force updates
    FILES = [{"name":"config.json", "skip":0},
             {"name":"drill_chart.html", "skip":0},
             {"name":"icon.png", "skip":0},
             {"name":"machinistcheatsheet.json", "skip":0},
             {"name":"styles.css", "skip":0}]
    LATEST_VERSION = ""
    LOCAL_VERSION = ""

    def __init__(self, root):
        global DIR
        self.DIR = DIR
        self.root = root
        self.__check_and_create_directory()
        self.get_local_version() # grabs local version
        self.get_latest_version ()  # grabs most recent version from Github
        #print(self.LATEST_VERSION, "|", self.LOCAL_VERSION)
        self.check_if_files_exist ()
        self.check_version ()

    def __check_and_create_directory(self):
        if not os.path.exists (self.DIR):
            os.makedirs (self.DIR)

    def check_version(self):
        # Compare local version to remote version
        if self.LOCAL_VERSION != self.LATEST_VERSION:
            self.force_update (self.LATEST_VERSION)

    def download_json(self):
        # Download the version JSON file from the GitHub repository
        try:
            with urllib.request.urlopen (self.REPO_URL + self.FILES[0]["name"]) as url:
                data = json.loads (url.read ().decode ())
                self.force_update (data)
        except urllib.error.URLError as e:
            messagebox.showerror ("Error", f"Unable to download version information: {e.reason}")

    def force_update(self, version_data):
        # Download and replace the main application file
        try:
            # Save the updated version JSON file
            for file in self.FILES:
                    # Download the file and save it to the destination directory
                    if file["skip"]>0:
                        continue
                    with urllib.request.urlopen (self.REPO_URL + file["name"]) as url, open (os.path.join (self.DIR, file["name"]),"wb") as f:
                        f.write (url.read ())
            # Notify the user that the update is complete and restart the application
            messagebox.showinfo ("Update", "The application has been updated. Please Reopen Program.")
        except urllib.error.URLError as e:
            messagebox.showerror ("Error", f"Unable to download update: {e.reason}")

    def get_local_version(self):
        # Check if the version JSON file exists locally
        if os.path.exists (os.path.join(self.DIR, self.FILES[0]["name"])):
            with open (os.path.join(self.DIR, self.FILES[0]["name"]), "r") as f:
                local_version_data = json.load (f)
            self.LOCAL_VERSION = local_version_data["version"]

    def get_latest_version(self):
        # Download the version JSON file from the GitHub repository
        try:
            with urllib.request.urlopen (self.REPO_URL + self.FILES[0]["name"]) as url:
                self.LATEST_VERSION = json.loads (url.read ().decode ())['version']
        except urllib.error.URLError as e:
            messagebox.showerror ("Error", f"Unable to download version information: {e.reason}")

    def check_if_files_exist(self):
        for file in self.FILES:
            if not os.path.exists (os.path.join(self.DIR ,file["name"])):
                # Download the file and save it to the destination directory
                with urllib.request.urlopen (self.REPO_URL + file["name"]) as url, open (os.path.join(self.DIR ,file["name"]), "wb") as f:
                    f.write (url.read ())

class AppWindow:

    VERSION = ""

    def __init__(self, parent=None, title=None):
        self.MAIN_ROOT = parent
        x, y = self.MAIN_ROOT.winfo_x(), self.MAIN_ROOT.winfo_y()

        # Hides the Main Root
        self.MAIN_ROOT.withdraw ()

        # Create a new Toplevel window
        self.TOP_LEVEL = tk.Toplevel(self.MAIN_ROOT)

        self.TOP_LEVEL.protocol ("WM_DELETE_WINDOW", self.__on_close)

        # Set the window title
        if title != None:
            self.TOP_LEVEL.title(PROGRAM_TITLE + " - " + title)
        else:
            self.TOP_LEVEL.title(PROGRAM_TITLE)

        # Set the window background color
        self.TOP_LEVEL.config(bg=BACKGROUND)

        # Set the window size and position
        self.TOP_LEVEL.geometry(f"660x425+{x}+{y}")

        # Set the window icon
        self.TOP_LEVEL.iconphoto(True, tk.PhotoImage(file=ICON))

        # Disable resizing of the window
        self.TOP_LEVEL.resizable(width=False, height=False)

        # Setup Footer
        self.__get_local_version()
        PROGRAMMED_TEXT = f"Powered by Winchester Automation Version {self.VERSION}"
        Label(self.TOP_LEVEL, text=PROGRAMMED_TEXT, bg=BACKGROUND, font=("Courier", 8)).pack(side=BOTTOM)


    def __on_close(self):
        self.MAIN_ROOT.deiconify()
        self.TOP_LEVEL.destroy()

    def __get_local_version(self):
        # Check if the version JSON file exists locally
        if os.path.exists (os.path.join(DIR, "config.json")):
            with open (os.path.join(DIR, "config.json"), "r") as f:
                local_version_data = json.load (f)
            self.VERSION = local_version_data["version"]

class thread_helper(AppWindow):

    THREAD_DATA = []
    SELECTED_THREAD = None
    TAP_TYPE = None
    CHAMFER_SIZE = None
    TAP_OPTIONS = None

    def __init__(self, root):
        super ().__init__ (root, title="Thread Helper")

        # load thread data
        # load file names & state form json file
        with open (FILENAME, "r") as f:
            self.data = json.load (f)
        # Extract all the thread names
        self.THREAD_DATA = [threads for threads in self.data["threads"]]

        # setup string var for drop down
        self.SELECTED_THREAD = StringVar(self.TOP_LEVEL)
        self.SELECTED_THREAD.set(self.THREAD_DATA[0]['name'])

        # Create a StringVar to hold the selected thread type
        self.TAP_TYPE = tk.StringVar (self.TOP_LEVEL)
        self.TAP_TYPE.set (self.THREAD_DATA[0]['drill'][0]['type'])

        # Create a IntVar to hold the chamfer size
        self.CHAMFER_SIZE = tk.IntVar (self.TOP_LEVEL)
        self.CHAMFER_SIZE.set (.01)

        # create thread label
        thread_label = tk.Label (self.TOP_LEVEL, text="Select Thread:", bg=BACKGROUND, font=("Courier", 16))
        thread_label.pack (anchor="n")

        # Create an OptionMenu of thread names
        self.option_frame = Frame(self.TOP_LEVEL, bg=BACKGROUND)
        self.option_frame.pack(padx=10, pady=10)
        self.thread_menu = tk.OptionMenu (self.option_frame, self.SELECTED_THREAD, *[thread_name['name'] for thread_name in self.THREAD_DATA])
        self.thread_menu.config(font=(None, 14))
        self.thread_menu['menu'].config (font=('Courier', 14))
        self.thread_menu.grid(padx=10,row=0, column=0)


        self.TAP_OPTIONS = [tap['type'] for tap in self.THREAD_DATA[0]['drill']]

        self.thread_menu_type = tk.OptionMenu (self.option_frame, self.TAP_TYPE, *self.TAP_OPTIONS)
        self.thread_menu_type.config(font=(None, 14))
        self.thread_menu_type['menu'].config (font=('Courier', 14))
        self.thread_menu_type.grid(padx=10, row=0, column=1)

        # Create a labeled frame to hold the thread data
        frame = tk.LabelFrame (self.TOP_LEVEL, text="Thread Data", padx=10, pady=10, font=(None, 22), bg=BACKGROUND)
        frame.pack ()
        font = ('Courier', 16)

        # Create labels to display the thread data
        class_label = tk.Label (frame, text="Class:", font=font, bg=BACKGROUND)
        class_label.grid (row=0, column=0)
        minor_label = tk.Label (frame, text="Minor Diameter:", font=font, bg=BACKGROUND)
        minor_label.grid (row=1, column=0)
        major_label = tk.Label (frame, text="Major Diameter:", font=font, bg=BACKGROUND)
        major_label.grid (row=2, column=0)
        feed_label = tk.Label (frame, text="Feed:", font=font, bg=BACKGROUND)
        feed_label.grid (row=3, column=0)
        drill_number_label = tk.Label (frame, text="Drill #:", font=font, bg=BACKGROUND)
        drill_number_label.grid (row=4, column=0)
        drill_size_label = tk.Label (frame, text="Drill Ø:", font=font, bg=BACKGROUND)
        drill_size_label.grid (row=5, column=0)
        chamfer_size_entry_label = tk.Label (frame, text="Enter Chamfer size:", font=font, bg=BACKGROUND)
        chamfer_size_entry_label.grid (row=6, column=0)
        chamfer_size_label = tk.Label (frame, text="Breakout Ø:", font=font, bg=BACKGROUND)
        chamfer_size_label.grid (row=7, column=0)

        # Create entries to display the thread data (the user can't alter them)
        self.class_entry = tk.Entry (frame, state='readonly', font=font, bg=BACKGROUND)
        self.class_entry.grid (row=0, column=1)
        self.minor_entry = tk.Entry (frame, state='readonly', font=font, bg=BACKGROUND)
        self.minor_entry.grid (row=1, column=1)
        self.major_entry = tk.Entry (frame, state='readonly', font=font, bg=BACKGROUND)
        self.major_entry.grid (row=2, column=1)
        self.feed_entry = tk.Entry (frame, state='readonly', font=font, bg=BACKGROUND)
        self.feed_entry.grid (row=3, column=1)
        self.drill_number_entry = tk.Entry (frame, state='readonly', font=font, bg=BACKGROUND)
        self.drill_number_entry.grid (row=4, column=1)
        self.drill_size_entry = tk.Entry (frame, state='readonly', font=font, bg=BACKGROUND)
        self.drill_size_entry.grid (row=5, column=1)
        self.chamfer_size_user_entry = tk.Entry (frame, textvariable=self.CHAMFER_SIZE, font=font)
        self.chamfer_size_user_entry.grid (row=6, column=1)
        self.chamfer_size_entry = tk.Entry (frame, state='readonly', font=font, bg=BACKGROUND)
        self.chamfer_size_entry.grid (row=7, column=1)

        # Call the function to update the label when the selection changes
        self.SELECTED_THREAD.trace ("w", self.__reset_tap_type_menu)
        self.CHAMFER_SIZE.trace ("w", self.update_chamfer)
        self.TAP_TYPE.trace('w', self.update_entries)
        self.chamfer_size_user_entry.bind ("<FocusOut>", self.check_chamfer_entry)

        self.update_entries()

    def check_chamfer_entry(self, event=''):
        # Get the current value of the entry widget
        value = self.chamfer_size_user_entry.get ()
        try:
            float_value = float (value)
            if float_value > .02:
                self.chamfer_size_user_entry.config (bg="pink")
            elif float_value < 0.:
                self.chamfer_size_user_entry.config (bg="pink")
            else:
                self.chamfer_size_user_entry.config (bg="white")
        except:
            self.chamfer_size_user_entry.config (bg="red")

    def update_chamfer(self, *args):
        self.check_chamfer_entry ()
        try:
            major = float (self.major_entry.get ())
            user_chamfer = float (self.chamfer_size_user_entry.get ())
            chamfer = round (major + (user_chamfer * 2), 4)
        except:
            chamfer = "ERROR"
        self.chamfer_size_entry.config (state='normal')
        self.chamfer_size_entry.delete (0, tk.END)
        self.chamfer_size_entry.insert (0, chamfer)
        self.chamfer_size_entry.config (state='readonly')

    def update_entries(self, *args):
        thread_data = next (thread for thread in self.data["threads"] if thread["name"] == self.SELECTED_THREAD.get ())
        self.class_entry.config (state='normal')
        self.class_entry.delete (0, tk.END)
        self.class_entry.insert (0, thread_data["class"])
        self.class_entry.config (state='readonly')

        self.minor_entry.config (state='normal')
        self.minor_entry.delete (0, tk.END)
        self.minor_entry.insert (0, thread_data["minor"])
        self.minor_entry.config (state='readonly')

        self.major_entry.config (state='normal')
        self.major_entry.delete (0, tk.END)
        self.major_entry.insert (0, thread_data["major"])
        self.major_entry.config (state='readonly')

        self.feed_entry.config (state='normal')
        self.feed_entry.delete (0, tk.END)
        self.feed_entry.insert (0, thread_data["pitch"])
        self.feed_entry.config (state='readonly')


        # get index
        index = self.TAP_OPTIONS.index(self.TAP_TYPE.get())

        size = thread_data['drill'][index]['data'][0]['size']
        number = thread_data['drill'][index]['data'][0]['number']

        self.drill_number_entry.config (state='normal')
        self.drill_number_entry.delete (0, tk.END)
        self.drill_number_entry.insert (0, number)
        self.drill_number_entry.config (state='readonly')

        self.drill_size_entry.config (state='normal')
        self.drill_size_entry.delete (0, tk.END)
        self.drill_size_entry.insert (0, size)
        self.drill_size_entry.config (state='readonly')

        self.update_chamfer ()

    def __reset_tap_type_menu(self, *args):
        thread_data = next (thread['drill'] for thread in self.data["threads"] if thread["name"] == self.SELECTED_THREAD.get ())
        # reset OptionMenu
        self.TAP_OPTIONS.clear()
        self.TAP_OPTIONS = [d['type'] for d in thread_data]
        self.TAP_TYPE.set(self.TAP_OPTIONS[0])
        self.thread_menu_type.destroy()
        self.thread_menu_type = tk.OptionMenu (self.option_frame, self.TAP_TYPE, *self.TAP_OPTIONS)
        self.thread_menu_type.config(font=(None, 14))
        self.thread_menu_type['menu'].config (font=('Courier', 14))
        self.thread_menu_type.grid(padx=10, row=0, column=1)
        self.update_entries()

class formulas(AppWindow):

    QUESTIONS = []
    ANSWER = None
    CURRENT_FORMULA = None

    def __init__(self, root):
        super ().__init__ (root, title="Formulas")

        # load formula data
        # load file names & state form json file
        with open (FILENAME, "r") as f:
            self.data = json.load (f)
        # Extract all the thread names
        self.FORMULAS = [formula for formula in self.data["formulas"]]

        # Create a StringVar to hold the selected formula
        self.selected_formula = tk.StringVar (self.TOP_LEVEL)
        self.selected_formula.set (self.FORMULAS[0]["name"])

        print(self.FORMULAS[0]["questions"])

        # Create an OptionMenu of formulas
        formula_label = tk.Label (self.TOP_LEVEL, text="Select Formula:", bg=BACKGROUND, font=("Courier", 16))
        formula_label.pack (anchor="n")
        self.thread_menu = tk.OptionMenu (self.TOP_LEVEL, self.selected_formula, *[name["name"] for name in self.FORMULAS])
        self.thread_menu.config(font=(None, 15))
        self.thread_menu['menu'].config (font=('Courier', 15))
        self.thread_menu.pack (anchor="n")

        # Create a new LabelFrame
        self.question_frame = LabelFrame (self.TOP_LEVEL, text="", bg=BACKGROUND, font=(None, 18))
        self.question_frame.pack (padx=10, pady=10)

        # Create a trace to keep track of the option selected
        self.selected_formula.trace ("w", self.__fill_in_questions)

        self.__fill_in_questions ()

    def __fill_in_questions(self, *args):
        for f in self.FORMULAS:
            if self.selected_formula.get() == f["name"]:
                self.CURRENT_FORMULA = f
                break
        self.__create_answer ()
        self.__set_answer ()


        # clear existing variables
        for ques in self.QUESTIONS:
            ques['lbl'].destroy()
            ques["entry"].destroy()
        self.QUESTIONS.clear()

        idx = 0
        for index, i in enumerate(self.CURRENT_FORMULA["questions"]):
            ques = self.__create_question(i)
            ques["lbl"].grid (pady=5, row=idx, column=0)
            ques["entry"].grid (pady=5, row=idx, column=1)
            self.QUESTIONS.append(ques)
            idx+= 1

        self.ANSWER["lbl"].grid (pady=5, row=idx, column=0)
        self.ANSWER["entry"].grid (pady=5, row=idx, column=1)

    def __create_question(self, name):
        label = Label (self.question_frame, text=name+":", bg=BACKGROUND, font=(None, 15))
        str_var = StringVar(self.TOP_LEVEL)
        str_var.set("0.")
        entry = Entry (self.question_frame, textvariable=str_var, font=(None, 15))

        entry.bind ("<FocusOut>", self.__solve_equaiton)
        return {"lbl":label, "entry":entry, 'var':str_var}

    def __create_answer(self):
        # Create Label and Entry for the Answer
        if self.ANSWER != None:
            self.ANSWER["lbl"].destroy()
            self.ANSWER["entry"].destroy()
        answer_label = Label (self.question_frame, text='answer', bg=BACKGROUND, font=(None, 15))
        answer_entry = Entry (self.question_frame, font=(None, 15))
        self.ANSWER = {'lbl':answer_label, "entry":answer_entry}

    def __solve_equaiton(self, args=''):
        solution = ''
        entry_data = []
        formula = None
        try:
            for q in self.QUESTIONS:
                entry = float(eval(q['entry'].get().replace(",", "")))
                try:
                    q['var'].set(f"{entry:,}")
                except:
                    pass
                entry_data.append(entry)
            formula = self.CURRENT_FORMULA["formula"]

        except:
            self.__set_answer()
            return

        for i in range(len(self.CURRENT_FORMULA['questions'])):
            formula = formula.replace(f"[{i}]", str(entry_data[i]))

        #print (f"Entry: {entry_data} | {formula}")
        solution = round(eval(formula), 4)

        # set answer entry to the solutioin
        self.__set_answer(solution)

    def __set_answer(self, answer=""):
        # set answer entry to the solutioin
        if self.CURRENT_FORMULA != None:
            self.ANSWER['lbl'].config(text=self.CURRENT_FORMULA['name'] + ":")
        try:
            answer = f"{answer:,}"
        except:
            pass
        self.ANSWER['entry'].config (state='normal')
        self.ANSWER['entry'].delete (0, tk.END)
        self.ANSWER['entry'].insert (0, answer)
        self.ANSWER['entry'].config (state='readonly')

    def __format_number(self, *args):
        try:
            for ques in self.QUESTIONS:
                value_float = float (ques['var'].get ())
                formatted_value = '{:,.0f}'.format (value_float)
                ques['var'].set (formatted_value)
        except:
            pass

class folder(AppWindow):

    FILE_PATH = ""

    def __init__(self, root):
        super ().__init__ (root, title="Folder Creator")

        # Create frame to hold labels
        label_frame = Frame (self.TOP_LEVEL, bg=BACKGROUND)
        label_frame.pack(padx=5, pady=5)

        # create label to show current path
        file_path_label = Label (label_frame, text="File:", bg=BACKGROUND, font=(None, 12))
        file_path_label.grid(padx=5, pady=5, row=0, column=0)

        # create entry widget for file path
        self.file_path_entry = tk.Entry(label_frame, state="readonly", font=(None, 12), width=50)
        self.file_path_entry.grid(padx=5, pady=5, row=0, column=1, columnspan=3)

        # load file names & state form json file
        with open (FILENAME, "r") as f:
            self.data = json.load (f)
        # Extract all the thread names
        self.folder_names = [{**folder, "var": tk.IntVar (self.TOP_LEVEL, value=folder["state"])} for folder in self.data["folders"]]

        # sort the list by the name
        self.folder_names.sort(key=lambda x: x["name"])

        # Create Checkbox Frame
        checkbox_frame = Frame (self.TOP_LEVEL, bg=BACKGROUND)
        checkbox_frame.pack(padx=5, pady=5)

        location = {"row":0, "column":0}
        for i, checkbox in enumerate (self.folder_names):
            cb = tk.Checkbutton (
                checkbox_frame,
                text=checkbox["name"],
                variable=checkbox["var"],
                bg=BACKGROUND,
                font=(None, 12)
            )
            if i%3 == 0:
                location["row"]+=1
                location["column"]=0
            else:
                location["column"]+=1
            cb.grid (padx=5, pady=5, row=location["row"], column=location["column"])

        # setup buttons
        button_frame = Frame (self.TOP_LEVEL, bg=BACKGROUND)
        button_frame.pack ()

        toggle_btn = Button (button_frame, text="Toggle All", command=self.__toggle_all, font=(None, 12))
        toggle_btn.grid (padx=5, pady=5, row=0, column=0)

        browse_btn = Button (button_frame, text="Browse", command=self.__save_file_path, font=(None, 12))
        browse_btn.grid (padx=5, pady=5, row=0, column=1)

        create_btn = Button (button_frame, text="Create", command=self.__create_folders, font=(None, 12))
        create_btn.grid (padx=5, pady=5, row=0, column=2)

    def __save_file_path(self):
        self.FILE_PATH = filedialog.askdirectory ()
        self.__alter_entry_text (text=self.FILE_PATH)

    def __create_folders(self):
        if not os.path.isdir (self.FILE_PATH):
            # File path is not valid
            print ("Invalid file path:", self.FILE_PATH)
            self.__alter_entry_text()
            return

        for folder in self.folder_names:
            if folder["var"].get() == 1:
                new_folder = os.path.join(self.FILE_PATH, folder["name"])
                if not os.path.exists (new_folder):
                    os.makedirs (new_folder)

        #self.__alter_entry_text(text="Folders Created.")
        #self.FILE_PATH = ""

    def __toggle_all(self):
        state = self.folder_names[0]["var"].get()
        for folder in self.folder_names:
            if state == 0:
                folder["var"].set(1)
            else:
                folder["var"].set (0)

    def __alter_entry_text(self, text=None):
        self.file_path_entry.config (state="normal")
        self.file_path_entry.delete(0, END)
        if text != None:
            self.file_path_entry.insert (0, text)
        else:
            self.file_path_entry.insert (0, "Invalid File Path.")
        self.file_path_entry.config (state="readonly")

class main:

    VERSION = ""
    PROGRAMMED_TEXT = ""

    def __init__(self):
        # Create a new Tkinter window
        self.root = tk.Tk ()
        self.UPDATER = AppUpdater(self.root)
        self.root.title (PROGRAM_TITLE)
        self.root.config (bg=BACKGROUND)
        self.root.geometry ("660x425")
        self.root.iconphoto(True, PhotoImage(file=ICON))
        self.root.resizable(width=False, height=False)

        # Create the label at the top of the menu
        lbl = Label(self.root, text="Machinist Cheat Sheet", font=(None, 20), bg=BACKGROUND).pack(padx=5, pady=5)
        button_font=(None, 16)

        # Create a button that opens the Thread Helper
        thread_helper_button = tk.Button (self.root, text="Thread Helper", command=lambda :thread_helper(self.root), font=button_font)
        thread_helper_button.pack (padx=5, pady=5)

        # Create a button that opens the Formulas
        formulas_button = tk.Button (self.root, text="Formulas", command=lambda :formulas(self.root), font=button_font)
        formulas_button.pack (padx=5, pady=5)

        # Create a button that opens the Code Helper
        formulas_button = tk.Button (self.root, text="CNC Codes", command=lambda :code_storage(self.root), font=button_font)
        formulas_button.pack (padx=5, pady=5)

        # Create a button that opens the Tap Drill Chart
        formulas_button = tk.Button (self.root, text="Drill Chart", command=lambda :webbrowser.open_new(DRILL_CHART), font=button_font)
        formulas_button.pack (padx=5, pady=5)

        # Create a button that opens the Tap Drill Chart
        formulas_button = tk.Button (self.root, text="Folder Creator", command=lambda :folder(self.root), font=button_font)
        formulas_button.pack (padx=5, pady=5)

        # programmed label

        PROGRAMMED_TEXT = f"Powered by Winchester Automation Version {self.UPDATER.LOCAL_VERSION}"
        Label(self.root, text=PROGRAMMED_TEXT, bg=BACKGROUND, font=("Courier", 8)).pack(side=BOTTOM)

        # Tkinter main loop
        self.root.mainloop()

class code_storage(AppWindow):

    FILE_PATH = ""
    MACHINE_DATA = []

    def __init__(self, root):
        super ().__init__ (root, title="Machine Code Database")

        # load data from json file
        with open (FILENAME, "r") as f:
            self.data = json.load (f)

        # Extract all the thread names
        self.MACHINE_DATA = [machine for machine in self.data["machine"]]
        self.MACHINE_DATA.sort(key=lambda x:x['name'])

        # Create a StringVar to hold the selected machine
        self.selected_machine = tk.StringVar (self.TOP_LEVEL)
        self.selected_machine.set (self.MACHINE_DATA[0]['name'])

        # Create an OptionMenu of thread names
        machine_label = tk.Label (self.TOP_LEVEL, text="Machine:", bg=BACKGROUND)
        machine_label.config (font=("Courier", 16))
        machine_label.pack (anchor="n")
        self.thread_menu = tk.OptionMenu (self.TOP_LEVEL, self.selected_machine, *[machine['name'] for machine in self.MACHINE_DATA])
        self.thread_menu.config(font=(None, 15))
        self.thread_menu['menu'].config (font=('Courier', 15))
        self.thread_menu.pack (anchor="n")

        # Create an object of Style widget
        try:
            self.style = ttk.Style (self.TOP_LEVEL)
            aktualTheme = self.style.theme_use ()
            self.style.theme_create ("dummy", parent=aktualTheme)
            self.style.theme_use ("dummy")
            self.style.configure("Treeview.Heading",font=(None, 15))
            self.style.configure("Treeview",font=(None, 13))
        except:
            pass

        # create treeview
        self.tree = ttk.Treeview(self.TOP_LEVEL, columns=("code", "description"))

        self.tree.heading('code', text="Code")
        self.tree.heading('description', text='Description')

        self.tree.column ("code", width=100, anchor="center")
        self.tree.column ("description", width=400, anchor="center")

        self.tree["show"] = "headings"

        # create the scrollbar and specify the Treeview as the parent
        scrollbar = Scrollbar (self.tree)

        # attach the scrollbar to the Treeview
        self.tree.config (yscrollcommand=scrollbar.set)

        # attach the Treeview to the scrollbar
        scrollbar.config (command=self.tree.yview)

        self.tree.pack(padx=5, pady=5)

        # place the scrollbar next to the Treeview
        scrollbar.place(relx=1.0, rely=0, relheight=1, relwidth=0.02)

        self.__load_data()

        self.selected_machine.trace ("w", self.__load_data)

    def __load_data(self, *args):
        self.tree.delete(*self.tree.get_children())
        machine_data = next (machine for machine in self.data["machine"] if machine["name"] == self.selected_machine.get ())
        for line in machine_data['data']:
            self.tree.insert("", "end", values=(line["code"], line["description"]))
        self.treeview_sort_column("code", False)

        # Define the tag for even rows
        self.tree.tag_configure ("even", background="gray")
        self.tree.tag_configure ("odd", background="white")

        # Apply the tag to the appropriate rows
        for i in range (self.tree.get_children ().__len__ ()):
            if i % 2 == 0:
                self.tree.item (self.tree.get_children ()[i], tags="even")
            else:
                self.tree.item (self.tree.get_children ()[i], tags="odd")

    def treeview_sort_column(self, col, reverse):
        l = [(self.tree.set (k, col), k) for k in self.tree.get_children ('')]
        l.sort (reverse=reverse)

        for index, (val, k) in enumerate (l):
            self.tree.move (k, '', index)

if __name__ == '__main__':
    main()
