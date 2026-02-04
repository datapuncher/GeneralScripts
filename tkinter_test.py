#!/usr/bin/python

import tkinter as tk

# Create main window
window = tk.Tk()
window.title("RivEM Color Code Generator")

# Create entry fields
chain_label = tk.Label(window, text="Chain ID:")
chain_label.pack()
chain_entry = tk.Entry(window)
chain_entry.pack()

residues_label = tk.Label(window, text="Residues:")
residues_label.pack()
residues_entry = tk.Entry(window)
residues_entry.pack()

rgb_label = tk.Label(window, text="RGB Code:")
rgb_label.pack()
rgb_entry = tk.Entry(window)
rgb_entry.pack()

# Function to get entry values
def get_values():
    chain = chain_entry.get()
    residues = residues_entry.get()
    rgb = rgb_entry.get()
    print("Chain ID:", chain)
    print("Residues:", residues)
    print("RGB Code:", rgb)

# Create button
submit_button = tk.Button(window, text="Submit", command=get_values)
submit_button.pack()

# Run the main loop
window.mainloop()
