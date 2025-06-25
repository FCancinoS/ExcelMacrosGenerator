import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
import json
import os

def create_schedule_table(parent):
    columns = ("Fecha", "Evento", "Responsable", "Completado")

    
    # ==== Frame superior para controles ====
    control_frame = ttk.Frame(parent)
    control_frame.pack(fill="x", padx=10, pady=10)

    fecha_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
    evento_var = tk.StringVar()
    responsable_var = tk.StringVar()

    ttk.Label(control_frame, text="Fecha:").grid(row=0, column=0, padx=5, pady=5)
    ttk.Entry(control_frame, textvariable=fecha_var, width=12).grid(row=0, column=1, padx=5)

    ttk.Label(control_frame, text="Evento:").grid(row=0, column=2, padx=5, pady=5)
    ttk.Entry(control_frame, textvariable=evento_var, width=25).grid(row=0, column=3, padx=5)

    ttk.Label(control_frame, text="Responsable:").grid(row=0, column=4, padx=5, pady=5)
    ttk.Entry(control_frame, textvariable=responsable_var, width=25).grid(row=0, column=5, padx=5)

    def agregar_evento():
        if fecha_var.get() and evento_var.get() and responsable_var.get():
            tree.insert("", "end", values=(fecha_var.get(), evento_var.get(), responsable_var.get(), "❌"))
            evento_var.set("")
            responsable_var.set("")

    ttk.Button(control_frame, text="Añadir", command=agregar_evento, style="success.TButton").grid(row=0, column=6, padx=10)

    def guardar_tabla():
        data = [tree.item(i)["values"] for i in tree.get_children()]
        archivo = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("Archivos JSON", "*.json")])
        if archivo:
            with open(archivo, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            messagebox.showinfo("Guardado", "Agenda guardada correctamente.")

    def cargar_tabla():
        archivo = filedialog.askopenfilename(filetypes=[("Archivos JSON", "*.json")])
        if archivo and os.path.exists(archivo):
            with open(archivo, "r", encoding="utf-8") as f:
                data = json.load(f)
                tree.delete(*tree.get_children())
                for row in data:
                    tree.insert("", "end", values=row)

    ttk.Button(control_frame, text="Guardar", command=guardar_tabla).grid(row=0, column=7, padx=5)
    ttk.Button(control_frame, text="Cargar", command=cargar_tabla).grid(row=0, column=8, padx=5)

    # ==== Frame para la tabla ====
    table_frame = ttk.Frame(parent)
    table_frame.pack(expand=1, fill="both", padx=10)

    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=180)
    tree.pack(side="top", fill="both", expand=True)

    tree.column("Completado", width=100, anchor="center")
    # ==== Doble clic para editar ====
    def editar_celda(event):
        region = tree.identify("region", event.x, event.y)
        if region != "cell":
            return

        row_id = tree.identify_row(event.y)
        column_id = tree.identify_column(event.x)
        if not row_id or not column_id:
            return

        x, y, width, height = tree.bbox(row_id, column_id)
        col_index = int(column_id.replace("#", "")) - 1
        old_value = tree.item(row_id)['values'][col_index]

        edit_var = ttk.StringVar(value=old_value)
        entry = ttk.Entry(tree, textvariable=edit_var)
        entry.place(x=x, y=y, width=width, height=height)
        entry.focus()

        def guardar(event=None):
            new_value = edit_var.get()
            current_values = list(tree.item(row_id)["values"])
            current_values[col_index] = new_value
            tree.item(row_id, values=current_values)
            entry.destroy()

        entry.bind("<Return>", guardar)
        entry.bind("<FocusOut>", lambda e: entry.destroy())

    tree.bind("<Double-1>", editar_celda)
