import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk  # For icons (Pillow library)

# Create the main window
root = tk.Tk()
root.title("Mapper")
root.geometry("500x400")

# Create Notebook (for tabs)
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both')

# Define the icons (assuming you have 'folder.png' and 'excel.png' icons in the same folder)
folder_icon = ImageTk.PhotoImage(Image.open("resources/folder.png").resize((20, 20)))
excel_icon = ImageTk.PhotoImage(Image.open("resources/excel.png").resize((20, 20)))

# --- Input Tab ---
input_tab = ttk.Frame(notebook)
notebook.add(input_tab, text="Input")


# Input Folder Section
def select_input_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        input_folder_label.config(text=folder_selected)
        input_folder_label_img.config(image=folder_icon)


input_folder_btn = ttk.Button(input_tab, text="Select Input Folder", command=select_input_folder)
input_folder_btn.pack(pady=10)

input_folder_frame = tk.Frame(input_tab)
input_folder_frame.pack(pady=5)
input_folder_label_img = tk.Label(input_folder_frame)
input_folder_label_img.pack(side="left")
input_folder_label = tk.Label(input_folder_frame, text="No folder selected")
input_folder_label.pack(side="left")


# Template File Section
def select_template_file():
    file_selected = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    if file_selected:
        template_file_label.config(text=file_selected)
        template_file_label_img.config(image=excel_icon)


template_file_btn = ttk.Button(input_tab, text="Select Template File", command=select_template_file)
template_file_btn.pack(pady=10)

template_file_frame = tk.Frame(input_tab)
template_file_frame.pack(pady=5)
template_file_label_img = tk.Label(template_file_frame)
template_file_label_img.pack(side="left")
template_file_label = tk.Label(template_file_frame, text="No file selected")
template_file_label.pack(side="left")

# --- Add the remaining tabs for Mappings and Output ---
mappings_tab = ttk.Frame(notebook)
notebook.add(mappings_tab, text="Mappings")

output_tab = ttk.Frame(notebook)
notebook.add(output_tab, text="Output")

root.mainloop()
