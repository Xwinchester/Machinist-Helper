import json, os, webbrowser
import tkinter as tk
from tkinter import *
from tkinter import ttk

# globals
DIR = 'data'
FILENAME = os.path.join(DIR,'machinistcheetsheet.json')
ICON = os.path.join(DIR, 'icon.png')
# version
VERSION = '1.0.0'
PROGRAMMED_TEXT = f"Programmed by Winchester Solutions Version {VERSION}"

class thread_helper:

    def __init__(self, root):
        BACKGROUND = 'gray'
        x, y = root.winfo_x (), root.winfo_y ()
        root = tk.Toplevel(root)
        root.title ("Thread Helper")
        root.config (bg=BACKGROUND)
        root.geometry (f"660x425+{x}+{y}")
        root.iconphoto (True, PhotoImage (file=ICON))


        with open (FILENAME, "r") as f:
            self.data = json.load (f)
        # Extract all the thread names
        thread_names = [thread_data["name"] for thread_data in self.data["standard threads"]]

        # Create a StringVar to hold the selected thread name
        self.selected_thread = tk.StringVar (root)
        self.selected_thread.set (thread_names[0])

        # Create a StringVar to hold the chamfer size
        self.selected_chamfer = tk.IntVar (root)
        self.selected_chamfer.set (.01)

        # Create an OptionMenu of thread names
        thread_label = tk.Label (root, text="Select Thread:", bg=BACKGROUND, font=("Courier", 16))
        thread_label.pack (anchor="n")
        self.thread_menu = tk.OptionMenu (root, self.selected_thread, *thread_names)
        self.thread_menu.config(font=(None, 14))
        self.thread_menu['menu'].config (font=('Courier', 14))
        self.thread_menu.pack (anchor="n")

        # Create a labeled frame to hold the thread data
        frame = tk.LabelFrame (root, text="Thread Data", padx=10, pady=10, font=(None, 22), bg=BACKGROUND)
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
        self.chamfer_size_user_entry = tk.Entry (frame, textvariable=self.selected_chamfer, font=font)
        self.chamfer_size_user_entry.grid (row=6, column=1)
        self.chamfer_size_entry = tk.Entry (frame, state='readonly', font=font, bg=BACKGROUND)
        self.chamfer_size_entry.grid (row=7, column=1)

        # programmed label
        Label(root, text=PROGRAMMED_TEXT, bg=BACKGROUND, font=("Courier", 8)).pack(side=BOTTOM)

        # Call the function to update the label when the selection changes
        self.selected_thread.trace ("w", self.update_entries)
        self.selected_chamfer.trace ("w", self.update_chamfer)
        self.chamfer_size_user_entry.bind ("<FocusOut>", self.check_chamfer_entry)

        self.update_entries()

    def check_chamfer_entry(self, event=''):
        # Get the current value of the entry widget
        value = self.chamfer_size_user_entry.get ()
        try:
            float_value = float (value)
            if float_value > .05:
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
        thread_data = next (thread for thread in self.data["standard threads"] if thread["name"] == self.selected_thread.get ())
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

        self.drill_number_entry.config (state='normal')
        self.drill_number_entry.delete (0, tk.END)
        self.drill_number_entry.insert (0, thread_data['drill'][0]["standard"][0]["number"])
        self.drill_number_entry.config (state='readonly')

        self.drill_size_entry.config (state='normal')
        self.drill_size_entry.delete (0, tk.END)
        self.drill_size_entry.insert (0, thread_data['drill'][0]["standard"][0]["size"])
        self.drill_size_entry.config (state='readonly')

        self.update_chamfer ()

class formulas:

    FORMULAS = ['SFM', 'RPM', 'IPM', "FEED", 'MRR']

    def __init__(self, root):
        BACKGROUND = 'gray'
        x, y = root.winfo_x(), root.winfo_y()
        root = tk.Toplevel(root)
        root.title ("Formulas")
        root.config (bg=BACKGROUND)
        root.geometry (f"660x425+{x}+{y}")
        root.iconphoto (True, PhotoImage (file=ICON))


        # Create a StringVar to hold the selected formula
        self.selected_formula = tk.StringVar (root)
        self.selected_formula.set (self.FORMULAS[0])

        # Create an OptionMenu of formulas
        formula_label = tk.Label (root, text="Select Formula:", bg=BACKGROUND, font=("Courier", 16))
        formula_label.pack (anchor="n")
        self.thread_menu = tk.OptionMenu (root, self.selected_formula, *self.FORMULAS)
        self.thread_menu.config(font=(None, 15))
        self.thread_menu['menu'].config (font=('Courier', 15))
        self.thread_menu.pack (anchor="n")

        # Create a new LabelFrame
        frame = LabelFrame (root, text="", bg=BACKGROUND, font=(None, 18))
        frame.pack(padx=10, pady=10)

        # Create font for the Labals and Entry
        font = (None, 15)
        # Create 3 Entry widgets and add them to the LabelFrame
        self.entry_labal_1 = Label(frame, text='first', bg=BACKGROUND, font=font)
        self.entry_labal_1.grid(pady=5, row=0, column=0)
        self.entry1 = Entry (frame, font=font)
        self.entry1.grid (padx=5, pady=5, row=0, column=1)

        # Create Label and Entry 2
        self.entry_labal_2 = Label(frame, text='second', bg=BACKGROUND, font=font)
        self.entry_labal_2.grid(pady=5, row=1, column=0)
        self.entry2 = Entry (frame, font=font)
        self.entry2.grid (padx=5, pady=5, row=1, column=1)

        # Create Label and Entry 3
        self.entry_labal_3 = Label(frame, text='third', bg=BACKGROUND, font=font)
        self.entry_labal_3.grid(pady=5, row=2, column=0)
        self.entry3 = Entry (frame, font=font)
        self.entry3.grid (padx=5, pady=5, row=2, column=1)

        # Create Label and Entry for the Answer
        self.entry_labal_answer = Label(frame, text='answer', bg=BACKGROUND, font=font)
        self.entry_labal_answer.grid(pady=5, row=3, column=0)
        self.answer_entry = Entry (frame, font=font)
        self.answer_entry.grid (padx=5, pady=5, row=3, column=1)

        # Create a trace to keep track of the option selected
        self.selected_formula.trace ("w", self.__fill_in_gui)
        self.entry1.bind ("<FocusOut>", self.__solve_equaiton)
        self.entry2.bind ("<FocusOut>", self.__solve_equaiton)
        self.entry3.bind ("<FocusOut>", self.__solve_equaiton)
        self.__fill_in_gui()

        # create a section where we can get reference numbers from internet sites
        # Create a new LabelFrame
        ref_frame = LabelFrame (root, text="Reference Sites", bg=BACKGROUND, font=(None, 18))
        ref_frame.pack (padx=10, pady=10)

        # Link to CNC Lathing SFM site
        cnc_lathing_button = Button(ref_frame, text="CNC Lathing", command=lambda :webbrowser.open_new("https://www.cnclathing.com/guide/cutting-speed-chart-for-different-materials-in-turning-drilling-and-more-cnc-machining-processes-cnclathing"))
        cnc_lathing_button.grid(padx=5, pady=5, column=0, row=0)

        # Link to suncoasttools SFM page
        sun_coast_tools_button = Button(ref_frame, text="Sun Coast Tools", command=lambda :webbrowser.open_new("https://www.suncoasttools.com/PDFFILES/WhitneyTool/Catalog/35.pdf"))
        sun_coast_tools_button.grid(padx=5, pady=5, column=1, row=0)

        # Link to Little Machine Shop SFM page
        little_machine_shop_button = Button(ref_frame, text="Little Machine Shop", command=lambda :webbrowser.open_new("https://littlemachineshop.com/reference/cuttingspeeds.php"))
        little_machine_shop_button.grid(padx=5, pady=5, column=2, row=0)

        # programmed label
        Label(root, text=PROGRAMMED_TEXT, bg=BACKGROUND, font=("Courier", 8)).pack(side=BOTTOM)


    def __fill_in_gui(self, *args):
        formula = self.selected_formula.get()
        self.__reset_entries()

        # SFM
        if formula == self.FORMULAS[0]:
            self.entry_labal_1.config(text='Enter Tool Ø: ')
            self.entry_labal_2.config(text='Enter RPM: ')
            self.entry_labal_answer.config(text="SFM: ")
            self.answer_entry.config (state='normal')
            self.answer_entry.delete (0, tk.END)
            self.answer_entry.insert (0, '')
            self.answer_entry.config (state='readonly')
            self.entry3.grid_remove()
            self.entry_labal_3.grid_remove()

        # RPM
        if formula == self.FORMULAS[1]:
            self.entry_labal_1.config(text='Enter SFM: ')
            self.entry_labal_2.config(text='Enter Ø: ')
            self.entry_labal_answer.config(text="RPM: ")
            self.answer_entry.config (state='normal')
            self.answer_entry.delete (0, tk.END)
            self.answer_entry.insert (0, '')
            self.answer_entry.config (state='readonly')
            self.entry3.grid_remove()
            self.entry_labal_3.grid_remove()

        # IPM
        if formula == self.FORMULAS[2]:
            self.entry_labal_1.config(text='Chip load per tooth: ')
            self.entry_labal_2.config(text='Number of Teeth: ')
            self.entry3.grid()
            self.entry_labal_3.grid()
            self.entry_labal_3.config(text='RPM: ')
            self.entry_labal_answer.config(text="IPM: ")
            self.answer_entry.config (state='normal')
            self.answer_entry.delete (0, tk.END)
            self.answer_entry.insert (0, '')
            self.answer_entry.config (state='readonly')

        # feed
        if formula == self.FORMULAS[3]:
            self.entry_labal_1.config(text='Enter RPM: ')
            self.entry_labal_2.config(text='Number of Teeth: ')
            self.entry3.grid()
            self.entry_labal_3.grid()
            self.entry_labal_3.config(text='Feed Per Tooth: ')
            self.entry_labal_answer.config(text="Feed: ")
            self.answer_entry.config (state='normal')
            self.answer_entry.delete (0, tk.END)
            self.answer_entry.insert (0, '')
            self.answer_entry.config (state='readonly')

        # mrr
        if formula == self.FORMULAS[4]:
            self.entry_labal_1.config(text='Enter ADOC: ')
            self.entry_labal_2.config(text='Enter RDOC: ')
            self.entry3.grid()
            self.entry_labal_3.grid()
            self.entry_labal_3.config(text='Feed: ')
            self.entry_labal_answer.config(text="MRR: ")
            self.answer_entry.config (state='normal')
            self.answer_entry.delete (0, tk.END)
            self.answer_entry.insert (0, '')
            self.answer_entry.config (state='readonly')

    def __solve_equaiton(self, args=''):
        formula = self.selected_formula.get()
        solution = ''
        try:
            entry1 = float(eval(self.entry1.get()))
            entry2 = float (eval(self.entry2.get ()))
            if formula == self.FORMULAS[2] or formula == self.FORMULAS[3] or formula == self.FORMULAS[4]:
                entry3 = float(eval(self.entry3.get()))
        except:
            # set answer entry to the solutioin
            self.answer_entry.config (state='normal')
            self.answer_entry.delete (0, tk.END)
            self.answer_entry.insert (0, "")
            self.answer_entry.config (state='readonly')
            return

        # SFM
        if formula == self.FORMULAS[0]:
            solution = f'{round (.262 * entry1 * entry2, 4):,}'

        # RPM
        if formula == self.FORMULAS[1]:
            solution = f'{round(3.82 * entry1 / entry2)}.'

        # IPM
        if formula == self.FORMULAS[2]:
            solution = f'{round(entry1 * entry2 * entry3, 3)}'

        # FEED
        if formula == self.FORMULAS[3]:
            solution = f'{round(entry1 * entry2 * entry3, 3)}'

        # MRR
        if formula == self.FORMULAS[4]:
            solution = f'{round(entry1 * entry2 * entry3, 3)}'


        # set answer entry to the solutioin
        self.answer_entry.config (state='normal')
        self.answer_entry.delete (0, tk.END)
        self.answer_entry.insert (0, solution)
        self.answer_entry.config (state='readonly')

    def __reset_entries(self):
        self.entry1.delete(0, tk.END)
        self.entry1.insert (0, '')
        self.entry2.delete(0, tk.END)
        self.entry2.insert (0, '')
        self.answer_entry.config (state='normal')
        self.answer_entry.delete (0, tk.END)
        self.answer_entry.insert (0, '')
        self.answer_entry.config (state='readonly')

class main:

    def __init__(self):
        # Create a new Tkinter window
        BACKGROUND = "GRAY"
        self.root = tk.Tk ()
        self.root.title ("Machinist Cheat Sheet")
        self.root.config (bg=BACKGROUND)
        self.root.geometry ("660x425")
        self.root.iconphoto(True, PhotoImage(file=ICON))
        # Create the label at the top of the menu
        Label(self.root, text="Machinist Cheat Sheet", font=(None, 20), bg=BACKGROUND).pack(padx=5, pady=5)
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

        # programmed label
        Label(self.root, text=PROGRAMMED_TEXT, bg=BACKGROUND, font=("Courier", 8)).pack(side=BOTTOM)

        # Tkinter main loop
        self.root.mainloop()

class code_storage:

    def __init__(self, root):
        BACKGROUND = 'gray'
        x, y = root.winfo_x (), root.winfo_y ()
        root = tk.Toplevel (root)
        root.title ("CNC Code Helper")
        root.config (bg=BACKGROUND)
        root.geometry (f"660x425+{x}+{y}")
        root.iconphoto (True, PhotoImage (file=ICON))
        with open (FILENAME, "r") as f:
            self.data = json.load (f)
        # Extract all the thread names
        machines = [machine["name"] for machine in self.data["machine"]]
        machines.sort()
        # Create a StringVar to hold the selected machine
        self.selected_machine = tk.StringVar (root)
        self.selected_machine.set (machines[0])

        # Create an OptionMenu of thread names
        machine_label = tk.Label (root, text="Machine:", bg=BACKGROUND)
        machine_label.config (font=("Courier", 16))
        machine_label.pack (anchor="n")
        self.thread_menu = tk.OptionMenu (root, self.selected_machine, *machines)
        self.thread_menu.config(font=(None, 15))
        self.thread_menu['menu'].config (font=('Courier', 15))
        self.thread_menu.pack (anchor="n")


        # Create an object of Style widget
        try:
            self.style = ttk.Style (root)
            aktualTheme = self.style.theme_use ()
            self.style.theme_create ("dummy", parent=aktualTheme)
            self.style.theme_use ("dummy")
            self.style.configure("Treeview.Heading",font=(None, 15))
            self.style.configure("Treeview",font=(None, 13))
        except:
            pass

        # create treeview
        self.tree = ttk.Treeview(root, columns=("code", "description"))

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

        # programmed label
        Label(root, text=PROGRAMMED_TEXT, bg=BACKGROUND, font=("Courier", 8)).pack(side=BOTTOM)

        self.selected_machine.trace ("w", self.__load_data)

    def __load_data(self, *args):
        self.tree.delete(*self.tree.get_children())
        machine_data = next (machine for machine in self.data["machine"] if machine["name"] == self.selected_machine.get ())
        for line in machine_data['data']:
            self.tree.insert("", "end", values=(line["code"], line["description"]))
        self.treeview_sort_column("code", False)

        # Define the tag for even rows
        self.tree.tag_configure ("even", background="light gray")
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

def setup_file():
    os.makedirs(DIR)
    ROUND_NUMBER = 5
    data = {
        "standard threads": [
            {
                "name": "0-80",
                "class": "2B",
                "minor": ".0465-.0514",
                "major": .060,
                "pitch": round(1/80, ROUND_NUMBER),
                "drill":
                    [
                        {"standard":
                             [
                                 {"size":.0469,
                                  "number":"3/64"}
                            ]
                        },
                        {"roll form":
                            [
                                {"size": .055,
                                 "number": "#55"}
                            ]
                        }
                    ]
            },
            {
                "name": "2-56",
                "class": "2B",
                "minor": ".0667-.0737",
                "major": .086,
                "pitch": round(1 / 56, ROUND_NUMBER),
                "drill":
                    [
                        {"standard":
                             [
                                 {"size":.070,
                                  "number":"#50"}
                            ]
                        },
                        {"roll form":
                            [
                                {"size": .0781,
                                 "number": "5/64"}
                            ]
                        }
                    ]
            },
            {
                "name": "4-40",
                "class": "2B",
                "minor": ".0849-.0939",
                "major": .112,
                "pitch": round (1 / 40, ROUND_NUMBER),
                "drill":
                    [
                        {"standard":
                            [
                                {"size": .089,
                                 "number": "#43"}
                            ]
                        },
                        {"roll form":
                            [
                                {"size": .0995,
                                 "number": "#39"}
                            ]
                        }
                    ]
            },
            {
                "name": "6-32",
                "class": "2B",
                "minor": ".104-.114",
                "major": .138,
                "pitch": round (1 / 32, ROUND_NUMBER),
                "drill":
                    [
                        {"standard":
                            [
                                {"size": .1065,
                                 "number": "#36"}
                            ]
                        },
                        {"roll form":
                            [
                                {"size": .125,
                                 "number": "1/8"}
                            ]
                        }
                    ]
            },
            {
                "name": "8-32",
                "class": "2B",
                "minor": ".130-.139",
                "major": .164,
                "pitch": round (1 / 32, ROUND_NUMBER),
                "drill":
                    [
                        {"standard":
                            [
                                {"size": .136,
                                 "number": "#29"}
                            ]
                        },
                        {"roll form":
                            [
                                {"size": .1495,
                                 "number": "#25"}
                            ]
                        }
                    ]
            },
            {
                "name": "10-32",
                "class": "2B",
                "minor": ".156-.164",
                "major": .190,
                "pitch": round (1 / 32, ROUND_NUMBER),
                "drill":
                    [
                        {"standard":
                            [
                                {"size": .159,
                                 "number": "#21"}
                            ]
                        },
                        {"roll form":
                            [
                                {"size": .173,
                                 "number": "#17"}
                            ]
                        }
                    ]
            },
            {
                "name": "1/4-20",
                "class": "2B",
                "minor": ".196-.207",
                "major": .250,
                "pitch": round (1 / 20, ROUND_NUMBER),
                "drill":
                    [
                        {"standard":
                            [
                                {"size": .201,
                                 "number": "#7"}
                            ]
                        }
                    ]
            },
            {
                "name": "5/16-18",
                "class": "2B",
                "minor": ".252-.265",
                "major": .3125,
                "pitch": round (1 / 18, ROUND_NUMBER),
                "drill":
                    [
                        {"standard":
                            [
                                {"size": .257,
                                 "number": "LTR F"}
                            ]
                        }
                    ]
            },
            {
                "name": "5/16-24",
                "class": "2B",
                "minor": ".267-.277",
                "major": .3125,
                "pitch": round (1 / 24, ROUND_NUMBER),
                "drill":
                    [
                        {"standard":
                            [
                                {"size": .272,
                                 "number": "LTR I"}
                            ]
                        }
                    ]
            },
            {
                "name": "3/8-16",
                "class": "2B",
                "minor": ".307-.321",
                "major": .375,
                "pitch": round (1 / 16, ROUND_NUMBER),
                "drill":
                    [
                        {"standard":
                            [
                                {"size": .3125,
                                 "number": "5/16"}
                            ]
                        }
                    ]
            },
            {
                "name": "3/8-24",
                "class": "2B",
                "minor": ".330-.340",
                "major": .375,
                "pitch": round (1 / 24, ROUND_NUMBER),
                "drill":
                    [
                        {"standard":
                            [
                                {"size": .332,
                                 "number": "LTR Q"}
                            ]
                        }
                    ]
            }
        ],
        "machine":
        [
            {'name': 'Feeler',
             'data':
             [
                 {'code': 'M07',
                  'description': 'FLR 1 & FLR 2 Air Blast'},
                 {'code': 'M27',
                  'description': 'FLR 3 Air Blast'}
             ]
            },
            {'name': 'Big Scotty',
             'data':
                 [
                     {'code': 'G130',
                      'description':'Cancel Contour Control'},
                     {'code': 'G131',
                      'description': 'Contour Control, Range 1=Low, 10=Highest'}
                 ]
             }
        ]
    }
    with open (FILENAME, 'w') as f:
        json.dump (data, f)

if __name__ == '__main__':
    # if file does not exist, create the file
    if not os.path.exists(FILENAME):
        setup_file ()
    main()