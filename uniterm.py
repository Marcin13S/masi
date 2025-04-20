import tkinter as tk
from tkinter import messagebox
import json

class UnitermProcessor:
    def __init__(self, uniterms):
        self.uniterms = uniterms

    def sequence_uniterms(self):
        return " -> ".join(self.uniterms)

    def eliminate_uniterms(self, uniterms_to_remove):
        self.uniterms = [u for u in self.uniterms if u not in uniterms_to_remove]
        return self.uniterms

def save_to_json(uniterms):
    with open("uniterms.json", "w") as file:
        json.dump(uniterms, file)

def load_from_json():
    try:
        with open("uniterms.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def update_display():
    uniterm_list.delete(0, tk.END)
    for uniterm in processor.uniterms:
        uniterm_list.insert(tk.END, uniterm)

def add_uniterm():
    uniterm = uniterm_entry.get()
    if uniterm:
        processor.uniterms.append(uniterm)
        uniterm_entry.delete(0, tk.END)
        update_display()
        save_to_json(processor.uniterms)

def remove_selected():
    selected_items = uniterm_list.curselection()
    to_remove = [uniterm_list.get(i) for i in selected_items]
    processor.eliminate_uniterms(to_remove)
    update_display()
    save_to_json(processor.uniterms)

def convert_sequence_to_elimination():
    sequence = processor.sequence_uniterms()
    if not processor.uniterms:
        messagebox.showinfo("Informacja", "Brak unitermów do sekwencjonowania.")
        return

    # Przykładowo usuwamy ostatni element
    to_remove = [processor.uniterms[-1]]
    processor.eliminate_uniterms(to_remove)
    update_display()
    save_to_json(processor.uniterms)

    messagebox.showinfo("Zamiana zakończona", f"Sekwencja: {sequence}\nUsunięto: {to_remove[0]}")

# Załadowanie danych
uniterms = load_from_json()
processor = UnitermProcessor(uniterms)

# Interfejs graficzny
root = tk.Tk()
root.title("Uniterm GUI")

frame = tk.Frame(root)
frame.pack(pady=10)

uniterm_entry = tk.Entry(frame)
uniterm_entry.pack(side=tk.LEFT, padx=5)
add_button = tk.Button(frame, text="Dodaj", command=add_uniterm)
add_button.pack(side=tk.LEFT)

uniterm_list = tk.Listbox(root, selectmode=tk.MULTIPLE)
uniterm_list.pack(pady=10)
update_display()

remove_button = tk.Button(root, text="Usuń zaznaczone", command=remove_selected)
remove_button.pack()

convert_button = tk.Button(root, text="Zamień sekwencję na eliminację", command=convert_sequence_to_elimination)
convert_button.pack(pady=10)

root.mainloop()
