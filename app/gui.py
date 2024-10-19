import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from app.processing import run_processing


class InputTab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.input_folder = tk.StringVar(value="")
        self.template_file = tk.StringVar(value="")
        self.mapping_file = tk.StringVar(value="")

        self.create_widgets()

    def create_widgets(self):
        frame = self

        # Input Folder Selection
        tk.Button(frame, text="Select Input Folder", command=self.select_input_folder).grid(
            row=0, column=0, sticky="w", padx=5, pady=(10, 5)
        )
        tk.Label(frame, textvariable=self.input_folder).grid(row=1, column=0, sticky="w", padx=5, pady=(0, 10))

        # Template File Selection
        tk.Button(frame, text="Select Template File", command=self.select_template_file).grid(
            row=2, column=0, sticky="w", padx=5, pady=(10, 5)
        )
        tk.Label(frame, textvariable=self.template_file).grid(row=3, column=0, sticky="w", padx=5, pady=(0, 10))

        # Mapping File Selection
        tk.Button(frame, text="Select Mapping CSV", command=self.select_mapping_file).grid(
            row=4, column=0, sticky="w", padx=5, pady=(10, 5)
        )
        tk.Label(frame, textvariable=self.mapping_file).grid(row=5, column=0, sticky="w", padx=5, pady=(0, 10))

    def select_input_folder(self):
        folder_path = filedialog.askdirectory(title="Select Input Folder")
        if folder_path:
            self.input_folder.set(folder_path)

    def select_template_file(self):
        file_path = filedialog.askopenfilename(title="Select Template File", filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            self.template_file.set(file_path)

    def select_mapping_file(self):
        file_path = filedialog.askopenfilename(title="Select Mapping CSV", filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.mapping_file.set(file_path)


class OutputTab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.output_folder = tk.StringVar(value="")

        self.create_widgets()

    def create_widgets(self):
        frame = self

        # Output Folder Selection
        tk.Button(frame, text="Select Output Folder", command=self.select_output_folder).grid(
            row=0, column=0, sticky="w", padx=5, pady=(10, 5)
        )
        tk.Label(frame, textvariable=self.output_folder).grid(
            row=1, column=0, sticky="w", padx=5, pady=(0, 10)
        )

        # Start Button
        tk.Button(frame, text="Start Processing", command=self.master.master.start_processing).grid(
            row=2, column=0, sticky="w", padx=5, pady=(50, 0)
        )

    def select_output_folder(self):
        folder_path = filedialog.askdirectory(title="Select Output Folder")
        if folder_path:
            self.output_folder.set(folder_path)


class MapperApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mapper")
        self.geometry("400x300")

        # Create Tab Control
        self.tab_control = ttk.Notebook(self)
        self.input_tab = InputTab(self.tab_control)
        self.output_tab = OutputTab(self.tab_control)

        self.tab_control.add(self.input_tab, text="Input")
        self.tab_control.add(self.output_tab, text="Output")
        self.tab_control.pack(expand=1, fill="both")

    def start_processing(self):
        # Fetch user inputs from both tabs
        input_folder = self.input_tab.input_folder.get()
        template_file = self.input_tab.template_file.get()
        mapping_file = self.input_tab.mapping_file.get()
        output_folder = self.output_tab.output_folder.get()

        # Check if all fields are provided
        if not input_folder or not template_file or not mapping_file or not output_folder:
            messagebox.showerror("Missing Input", "Please ensure all input fields are filled.")
            return

        append_text = "processed"

        try:
            # Call the processing logic
            run_processing(input_folder, template_file, mapping_file, output_folder, append_text)

            # Display success message
            messagebox.showinfo("Success", "Processing complete! Files have been saved to the output folder.")

        except Exception as e:
            # Handle any errors
            messagebox.showerror("Error", f"An error occurred during processing: {str(e)}")


if __name__ == "__main__":
    app = MapperApp()
    app.mainloop()
