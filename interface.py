import sqlite3
import tkinter as tk
from tkinter import scrolledtext
import threading
import time
from logger import monitor_events
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import Counter

def fetch_events():
    conn = sqlite3.connect("security_events.db")
    c = conn.cursor()
    c.execute("SELECT time, type, details FROM events ORDER BY id DESC LIMIT 10")
    events = c.fetchall()
    conn.close()
    return events

def fetch_event_counts():
    conn = sqlite3.connect("security_events.db")
    c = conn.cursor()
    c.execute("SELECT type FROM events WHERE time > datetime('now', '-1 hour')")
    events = c.fetchall()
    conn.close()
    return Counter(e[0] for e in events)

def update_gui(text_widget):
    events = fetch_events()
    text_widget.delete(1.0, tk.END)
    for event in events:
        text_widget.insert(tk.END, f"{event[0]} | {event[1]} | {event[2]}\n")

def update_graph(canvas, fig):
    fig.clear()
    counts = fetch_event_counts()
    ax = fig.add_subplot(111)
    ax.bar(counts.keys(), counts.values())
    ax.set_title("Event Frequency (Last Hour)")
    ax.set_xlabel("Event Type")
    ax.set_ylabel("Count")
    canvas.draw()

def gui_loop(root, text_widget, canvas, fig):
    def refresh():
        update_gui(text_widget)
        update_graph(canvas, fig)
        root.after(2000, refresh)
    refresh()

def start_gui():
    root = tk.Tk()
    root.title("Security Event Logger")
    
    text_area = scrolledtext.ScrolledText(root, width=60, height=10)
    text_area.pack(pady=10)
    
    fig = plt.Figure(figsize=(6, 4))
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(pady=10)
    
    threading.Thread(target=monitor_events, daemon=True).start()
    gui_loop(root, text_area, canvas, fig)
    root.mainloop()

if __name__ == "__main__":
    start_gui()
