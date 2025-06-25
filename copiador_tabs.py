from tkinter import ttk
import tkinter as tk

def create_copiador_tabs(parent):
    notebook = ttk.Notebook(parent)

    proc_tab = ttk.Frame(notebook)
    mods_tab = ttk.Frame(notebook)
    pruebas_tab = ttk.Frame(notebook)

    notebook.add(proc_tab, text="ProC")
    notebook.add(mods_tab, text="Mods")
    notebook.add(pruebas_tab, text="Pruebas")
    notebook.pack(expand=1, fill="both")

    # Añadir contenido de ejemplo
    tk.Label(proc_tab, text="Sección ProC").pack(pady=20)
    tk.Label(mods_tab, text="Sección Mods").pack(pady=20)
    tk.Label(pruebas_tab, text="Sección Pruebas").pack(pady=20)
