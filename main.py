import tkinter as tk
from tkinter import ttk, simpledialog, Text
import pyperclip
from ttkbootstrap import Style
from whiteboard import *
from schedule_table import *
from values import *
from ToDo import *
from datetime import datetime


class KanbanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard")
        self.root.geometry("1000x500")

        # Estilo con ttkbootstrap
        style = Style(theme="litera")
        style.configure('.', font=("Helvetica", 12))
        style.configure('TEntry', font=('Helvetica', 12, 'bold'))
        style.configure('TButton', font=("Helvetica", 12))
        style.configure('Treeview', font=("Helvetica", 12), rowheight=28)
        style.configure('Treeview.Heading', font=('Helvetica', 13, 'bold'))
        ##style.configure('TNotebook.Tab', font=('Helvetica', 14))
        ##default_font = ("Helvetica", 14)


        # Crear el contenedor de pestañas (esto es lo que te faltaba)
        self.tabControl = ttk.Notebook(self.root)
        self.tabControl.pack(expand=1, fill="both")

        # Pestaña ToDo
        self.create_tab("ToDo List")

        # Pestaña Quick Copy
        self.create_tab("Quick Copy", subtabs=["Pizarra","ProC", "Mods",  "Otros"], drawing_board=True, proc_size=10, mods_size=18)

        # Pestaña Agenda
        self.create_tab("Agenda", schedule_table=True)

        # Pestaña Notepad
        notepad_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(notepad_tab, text="Notepad")
                # Frame superior para botones de guardar/cargar
        button_frame = ttk.Frame(notepad_tab)
        button_frame.pack(fill="x", pady=5)
        self.notepad_text = Text(notepad_tab, wrap=tk.WORD, font=('Helvetica', 14))
        self.notepad_text.pack(expand=1, fill="both")

        def guardar_nota():
            from tkinter import filedialog
            archivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")])
            if archivo:
                with open(archivo, "w", encoding="utf-8") as f:
                    f.write(self.notepad_text.get("1.0", "end-1c"))

        def cargar_nota():
            from tkinter import filedialog
            archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
            if archivo:
                with open(archivo, "r", encoding="utf-8") as f:
                    contenido = f.read()
                    self.notepad_text.delete("1.0", "end")
                    self.notepad_text.insert("1.0", contenido)

        ttk.Button(button_frame, text="Guardar", command=guardar_nota).pack(side="left", padx=10)
        ttk.Button(button_frame, text="Cargar", command=cargar_nota).pack(side="left")

        # Icono opcional (comentar si da error)
        icon_path = "assets/icon.png"
        try:
            icon_image = tk.PhotoImage(file=icon_path)
            root.iconphoto(True, icon_image) 
        except Exception as e:
            print("No se pudo cargar icon.png:", e)

    def create_tab(self, tab_name, subtabs=None, drawing_board=False, proc_size=None, mods_size=None, schedule_table=False):
        tab = ttk.Frame(self.tabControl)
        self.tabControl.add(tab, text=tab_name)

        if tab_name == "ToDo List":
            create_todo_list_tab(tab)
        elif subtabs:
            self.create_subtabs(tab, subtabs, drawing_board, proc_size, mods_size)
        if schedule_table:
            create_schedule_table(tab)

    def create_subtabs(self, parent, subtabs, drawing_board, proc_size, mods_size):
        subtab_copiador = ttk.Notebook(parent)
        subtab_copiador.pack(expand=1, fill="both")

        for subtab_name in subtabs:
            subtab_frame = ttk.Frame(subtab_copiador)
            subtab_copiador.add(subtab_frame, text=subtab_name)

            if subtab_name == "Pizarra" and drawing_board:
                create_drawing_board(subtab_frame)
            elif subtab_name == "ProC":
                entries = self.add_textboxes_and_buttons(subtab_frame, proc_size)
                self.insert_values_in_textboxes(entries, values_proc)
            elif subtab_name == "Mods":
                entries = self.add_textboxes_and_buttons(subtab_frame, mods_size)
                self.insert_values_in_textboxes(entries, values_mods)
            elif subtab_name == "Otros":
                self.create_otros_tab(subtab_frame)

    def add_textboxes_and_buttons(self, parent, size):
        entry_widgets = []
        for i in range(size):
            textbox = tk.Entry(parent, width=70, font=('Helvetica', 15))
            button = ttk.Button(parent, text="Copy", command=lambda tb=textbox: self.copy_textbox_content(tb), width=15)
            textbox.grid(row=i, column=0, padx=5, pady=5)
            button.grid(row=i, column=1, padx=5, pady=5)
            entry_widgets.append(textbox)
        return entry_widgets

    def insert_values_in_textboxes(self, entry_widgets, values):
        for entry, value in zip(entry_widgets, values):
            entry.insert(0, value)

    def copy_textbox_content(self, textbox):
        content = textbox.get()
        pyperclip.copy(content)

    def create_otros_tab(self, parent):
        label1 = ttk.Label(parent, text="Source tree", font=('Helvetica', 14))
        label2 = ttk.Label(parent, text="Listado", font=('Helvetica', 14))

        entry1 = tk.Entry(parent, width=60, font=('Helvetica', 14))
        entry2 = tk.Entry(parent, width=60, font=('Helvetica', 14))

        btn1 = ttk.Button(parent, text="Copiar", command=lambda: self.copy_textbox_content(entry1), style="info.TButton")
        btn2 = ttk.Button(parent, text="Copiar", command=lambda: self.copy_textbox_content(entry2), style="success.TButton")

        label1.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        entry1.grid(row=0, column=1, padx=10, pady=10)
        btn1.grid(row=0, column=2, padx=10, pady=10)

        label2.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        entry2.grid(row=1, column=1, padx=10, pady=10)
        btn2.grid(row=1, column=2, padx=10, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = KanbanApp(root)
    root.mainloop()
