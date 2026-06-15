# (c) 2026 Arhigis. All rights reserved. Licensed under the MIT License.

import os
import ctypes
import tkinter as tk
from tkinter import messagebox
import pyglet

FONT_FILE = "Sonarian.otf"
FONT_NAME = "Sonarian"

if os.path.exists(FONT_FILE):
    pyglet.font.add_file(FONT_FILE)
else:
    FONT_NAME = "Arial"

root = tk.Tk()
root.title("Sonarian Decoder")
root.geometry("950x400")

# --- ДОБАВЬТЕ ЭТУ СТРОЧКУ СЮДА ---
root.iconbitmap("icon.ico")
# ---------------------------------

entry = tk.Entry(root, font=("Arial", 16), width=50)
entry.pack(pady=20)

chars_upper = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
chars_lower = list("abcdefghijklmnopqrstuvwxyz")
buttons = []
is_top = False

def get_caps_state():
    try:
        return (ctypes.windll.user32.GetKeyState(0x14) & 1) != 0
    except:
        return False

def refresh_buttons(event=None):
    current_chars = chars_upper if get_caps_state() else chars_lower
    for i, btn in enumerate(buttons):
        if i < len(current_chars):
            btn.config(text=current_chars[i])

def press(idx):
    entry.insert(tk.END, buttons[idx].cget("text"))

def toggle_top():
    global is_top
    is_top = not is_top
    root.attributes("-topmost", is_top)
    btn_top.config(text="📌 LOCKED" if is_top else "📌 LOCK", bg="#a3ffb4" if is_top else "#ffaba3")

def clear_last():
    entry.delete(len(entry.get()) - 1, tk.END)

def copy_all():
    root.clipboard_clear()
    root.clipboard_append(entry.get())
    messagebox.showinfo("Success", "Copied to clipboard!")

grid = tk.Frame(root)
grid.pack()

for i, char in enumerate(chars_upper):
    btn = tk.Button(grid, text=char, font=(FONT_NAME, 20), width=3, height=1, command=lambda idx=i: press(idx))
    btn.grid(row=i // 10, column=i % 10, padx=4, pady=4)
    buttons.append(btn)

root.bind("<Motion>", refresh_buttons)
root.bind("<Key>", refresh_buttons)

controls = tk.Frame(root)
controls.pack(pady=25)

btn_top = tk.Button(controls, text="📌 LOCK", font=("Arial", 12), width=12, bg="#ffaba3", command=toggle_top)
btn_top.grid(row=0, column=0, padx=5)

tk.Button(controls, text="SPACE", font=("Arial", 12), width=10, command=lambda: entry.insert(tk.END, " ")).grid(row=0, column=1, padx=5)
tk.Button(controls, text="BACKSPACE", font=("Arial", 12), width=12, command=clear_last).grid(row=0, column=2, padx=5)
tk.Button(controls, text="COPY", font=("Arial", 12), width=12, bg="lightgreen", command=copy_all).grid(row=0, column=3, padx=5)

refresh_buttons()
root.mainloop()