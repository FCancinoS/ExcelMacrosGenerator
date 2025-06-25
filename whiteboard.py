import tkinter as tk
from tkinter import ttk, filedialog
from PIL import ImageGrab, Image
import io
import win32clipboard

def create_drawing_board(parent):
    color_var = tk.StringVar(value="black")
    size_var = tk.IntVar(value=3)
    tool_var = tk.StringVar(value="Pincel")
    dark_mode = tk.BooleanVar(value=False)

    canvas = tk.Canvas(parent, bg='white')
    canvas.pack(expand=1, fill="both", padx=10, pady=(0, 10))

    last_x, last_y = [None], [None]
    start_x = tk.IntVar()
    start_y = tk.IntVar()

    def draw(event):
        r = size_var.get()
        current_tool = tool_var.get()

        # El color del borrador siempre debe ser el color del fondo
        if current_tool == "Borrador":
            color = canvas["bg"]
        else:
            color = color_var.get()

        if last_x[0] is not None:
            canvas.create_line(
                last_x[0], last_y[0], event.x, event.y,
                fill=color, width=r, capstyle=tk.ROUND, smooth=True
            )
        last_x[0], last_y[0] = event.x, event.y


    def reset_line(event):
        last_x[0], last_y[0] = None, None

    def start_shape(event):
        start_x.set(event.x)
        start_y.set(event.y)

    def draw_shape(event):
        canvas.delete("preview")
        x0, y0 = start_x.get(), start_y.get()
        x1, y1 = event.x, event.y
        shape = tool_var.get()
        outline = color_var.get()

        if shape == "Rectángulo":
            canvas.create_rectangle(x0, y0, x1, y1, outline=outline, width=2, tags="preview")
        elif shape == "Círculo":
            canvas.create_oval(x0, y0, x1, y1, outline=outline, width=2, tags="preview")
        elif shape == "Triángulo":
            triangle = [x0, y1, (x0 + x1)//2, y0, x1, y1]
            canvas.create_polygon(triangle, outline=outline, fill="", width=2, tags="preview")

    def finalize_shape(event):
        draw_shape(event)
        canvas.dtag("preview")

    def bind_tools():
        canvas.unbind("<B1-Motion>")
        canvas.unbind("<Button-1>")
        canvas.unbind("<B1-ButtonRelease>")
        canvas.unbind("<ButtonRelease-1>")
        canvas.unbind("<Motion>")

        tool = tool_var.get()
        if tool in ["Pincel", "Borrador"]:
            canvas.bind("<B1-Motion>", draw)
            canvas.bind("<ButtonRelease-1>", reset_line)
        elif tool in ["Rectángulo", "Círculo", "Triángulo"]:
            canvas.bind("<Button-1>", start_shape)
            canvas.bind("<B1-Motion>", draw_shape)
            canvas.bind("<B1-ButtonRelease>", finalize_shape)

    def toggle_dark_mode():
        is_dark = dark_mode.get()
        bg_color = "#2e2e2e" if is_dark else "white"
        canvas.config(bg=bg_color)

        # Si el usuario tenía el color por defecto (negro o blanco), lo invertimos
        if is_dark and color_var.get() == "black":
            color_var.set("white")
        elif not is_dark and color_var.get() == "white":
            color_var.set("black")


    def save_as_image():
        x = parent.winfo_rootx() + canvas.winfo_x()
        y = parent.winfo_rooty() + canvas.winfo_y()
        w = x + canvas.winfo_width()
        h = y + canvas.winfo_height()
        img = ImageGrab.grab(bbox=(x, y, w, h))
        file = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file:
            img.save(file)

    def copy_to_clipboard():
        x = parent.winfo_rootx() + canvas.winfo_x()
        y = parent.winfo_rooty() + canvas.winfo_y()
        w = x + canvas.winfo_width()
        h = y + canvas.winfo_height()
        img = ImageGrab.grab(bbox=(x, y, w, h))

        output = io.BytesIO()
        img.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()

        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()

    # UI superior
    tools = ttk.Frame(parent)
    tools.pack(fill="x", padx=10, pady=10)

    ttk.Label(tools, text="Herramienta:").pack(side="left")
    ttk.OptionMenu(tools, tool_var, "Pincel", "Pincel", "Borrador", "Rectángulo", "Círculo", "Triángulo", command=lambda _: bind_tools()).pack(side="left", padx=5)

    ttk.Label(tools, text="Color:").pack(side="left")
    ttk.OptionMenu(tools, color_var, "black", "black", "red", "blue", "green", "purple", "orange").pack(side="left", padx=5)

    ttk.Label(tools, text="Tamaño:").pack(side="left")
    ttk.Scale(tools, from_=1, to=15, orient="horizontal", variable=size_var, length=120).pack(side="left", padx=5)

    ttk.Button(tools, text="Borrar todo", command=lambda: canvas.delete("all"), style="danger.TButton").pack(side="right", padx=5)
    ttk.Button(tools, text="Guardar PNG", command=save_as_image, style="info.TButton").pack(side="right", padx=5)
    ttk.Button(tools, text="Copiar Imagen", command=copy_to_clipboard, style="secondary.TButton").pack(side="right", padx=5)

    ttk.Checkbutton(tools, text="Modo oscuro", variable=dark_mode, command=toggle_dark_mode).pack(side="right", padx=5)

    bind_tools()
