import sqlite3
import tkinter as tk
from tkinter import scrolledtext

def fetch_events():
    conn = sqlite3.connect("security_events.db")
    c = conn.cursor()
    c.execute("SELECT time, type, details FROM events ORDER BY id DESC LIMIT 10")
    events = c.fetchall()
    conn.close()
    return events

def update_gui(text_widget):
    events = fetch_events()
    text_widget.delete(1.0, tk.END)
    for event in events:
        text_widget.insert(tk.END, f"{event[0]} | {event[1]} | {event[2]}\n")

def start_gui():
    root = tk.Tk()
    root.title("Security Event Logger")
    text_area = scrolledtext.ScrolledText(root, width=60, height=20)
    text_area.pack(pady=10)
    update_gui(text_area)
    root.mainloop()

if __name__ == "__main__":
    start_gui()
