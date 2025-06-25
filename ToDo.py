import tkinter as tk
from tkinter import ttk
from tkinter import Listbox

def create_todo_list_tab(parent):
    entry_var = tk.StringVar()
    selected_index = tk.IntVar(value=-1)

    # Input de texto
    entry = ttk.Entry(parent, textvariable=entry_var, font=('Helvetica', 14), width=50)
    entry.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    # Botón Añadir
    add_button = ttk.Button(parent, text="Añadir", command=lambda: add_task(entry_var, listbox, selected_index), style="success.TButton")
    add_button.grid(row=0, column=1, padx=5, pady=10)

    # Botón Eliminar
    remove_button = ttk.Button(parent, text="Eliminar", command=lambda: remove_task(listbox, selected_index), style="danger.TButton")
    remove_button.grid(row=0, column=2, padx=5, pady=10)

    # Botón Editar
    edit_button = ttk.Button(parent, text="Editar", command=lambda: edit_task(entry_var, listbox, selected_index), style="info.TButton")
    edit_button.grid(row=0, column=3, padx=5, pady=10)

    # Lista de tareas
    listbox = Listbox(parent, font=('Helvetica', 14))
    listbox.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

    # Evento para seleccionar y editar
    def on_select(event):
        selection = listbox.curselection()
        if selection:
            idx = selection[0]
            selected_index.set(idx)
            entry_var.set(listbox.get(idx))
        else:
            selected_index.set(-1)
            entry_var.set("")

    listbox.bind("<<ListboxSelect>>", on_select)

    parent.rowconfigure(1, weight=1)
    for i in range(4):
        parent.columnconfigure(i, weight=0)

def add_task(entry_var, listbox, selected_index):
    task = entry_var.get().strip()
    if task:
        listbox.insert(tk.END, task)
        entry_var.set("")
        selected_index.set(-1)

def remove_task(listbox, selected_index):
    selection = listbox.curselection()
    if selection:
        index = selection[0]
        listbox.delete(index)
        selected_index.set(-1)

def edit_task(entry_var, listbox, selected_index):
    idx = selected_index.get()
    new_text = entry_var.get().strip()
    if idx >= 0 and new_text:
        listbox.delete(idx)
        listbox.insert(idx, new_text)
        entry_var.set("")
        selected_index.set(-1)
