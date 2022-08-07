# csv importing
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
import importlib
import csv
import os.path


class Notebook:
    def __init__(self):
        self.root = Tk()
        self.root.title("Traitement fichier csv")
        self.build_Menu()
        self.build_NoteBook()
        self.build_page_1()
        self.build_page_2()
        self.root.mainloop()

    def build_Menu(self):
        # MENU WIDGET CONFIGURATION
        self.menu = Menu(self.root)
        self.root.configure(menu=self.menu)
        self.filemenu = [None] * 3
        for f in range(1, 3):
            self.filemenu[f] = Menu(self.menu, tearoff=False)
        # FILE MENU
        self.menu.add_cascade(label="File", menu=self.filemenu[1])
        for i in ["New", "Open", "Exit"]:
            if i == "New":
                self.filemenu[1].add_command(label=i, command=self.Add_New_Tab)
            elif i == "open":
                self.filemenu[1].add_command(label=i, command=self.filedialog)
            elif i == "Exit":
                self.filemenu[1].add_command(label=i, command=quit)
            else:
                self.filemenu[1].add_command(label=i)

    # ADD NEW TAG CODE
    def Add_New_Tab(self):
        for k in range(2, 3):
            self.notebook.add(self.tab[k], text=f"Page {k}")

    def build_NoteBook(self):
        # NOTEBOOK WIDGET CONFIGURATION
        self.notebook = ttk.Notebook(self.root, height=400, width=800)

        self.tab = [None] * 10
        global t
        for t in range(1, 10):
            self.tab[t] = ttk.Frame(self.notebook)

        self.notebook.add(self.tab[1], text="Importation des donnees", underline=0)
        self.notebook.add(self.tab[2], text="Affichage des donnees apres traitement ")
        # self.notebook.add(self.tab[3], text='Page 3')
        # self.notebook.add(self.tab[4], text='Page 4')
        self.notebook.pack(fill=BOTH, expand=YES, padx=5, pady=5)

        # PAGE ONE CONTENTS

    def build_page_1(self):
        ttk.Button(self.tab[1], text="Ouvrir un fichier csv", command=self.filedialog).pack(side=LEFT, anchor=CENTER, padx=90, pady=5, fill=X, expand=1)
        # ttk.Button(self.tab[1], text='close', command=quit).pack(side=LEFT, padx=90, fill=X, anchor=CENTER,expand=1)

    def filedialog(self):
        self.filename = filedialog.askopenfilename(initialdir="/", title="Select a file", filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
        print(self.filename)
        # os.system('python deleteNull.py')
        # global filename
        # filename=self.filename
        importlib.import_module("deleteNull")

    def build_page_2(self):
        data = []
        path = "C:/Users/ThinkPad/Desktop/Python/fout.csv"
        if os.path.exists(path):
            input_file = "fout.csv"
            with open(input_file, "r") as source:
                reader = csv.reader(source)
                next(reader, None)  # skip the headers
                for row in reader:
                    data.append([row[0], row[1], row[2], row[3], row[4]])

            tree = ttk.Treeview(self.tab[2], columns=(1, 2, 3, 4, 5), height=50, show="headings")
            tree.pack(side="left")
            tree.heading(1, text="Matricule")
            tree.heading(2, text="Date Inscription")
            tree.heading(3, text="Cycle")
            tree.heading(4, text="Specialité")
            tree.heading(5, text="Durée cursus")

            tree.column(1, width=150)
            tree.column(2, width=150)
            tree.column(3, width=150)
            tree.column(4, width=150)
            tree.column(5, width=180)

            scroll = ttk.Scrollbar(self.tab[2], orient="vertical", command=tree.yview)
            scroll.pack(side="right", fill="y")

            tree.configure(yscrollcommand=scroll.set)

        for val in data:
            tree.insert("", "end", values=(val[0], val[1], val[2], val[3], val[4]))


if __name__ == "__main__":
    Notebook()

# grid may be usefull for the future
# ttk.Label(tab1,text ="Welcome to GeeksForGeeks").grid(column = 0, row = 0,padx = 30,pady = 30)
# ttk.Label(tab2,text ="Lets dive into the world of computers").grid(column = 0,row = 0, padx = 30,pady = 30)
