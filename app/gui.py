import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from processing import run_processing


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
        file_path = filedialog.askopenfilename(
            title="Select Template File",
            filetypes=[("Excel files", "*.xlsx *.xlsm")])
        if file_path:
            self.template_file.set(file_path)

    def select_mapping_file(self):
        file_path = filedialog.askopenfilename(title="Select Mapping CSV", filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.mapping_file.set(file_path)


class OutputTab(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.suffix_entry = None
        self.output_folder = tk.StringVar(value="")
        self.spinner = None
        self.start_stop_button = None  # Track the Start/Stop button

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

        # Suffix Entry Box
        tk.Label(frame, text="Output File Suffix:").grid(
            row=2, column=0, sticky="w", padx=5, pady=(10, 5)
        )
        self.suffix_entry = tk.Entry(frame)
        self.suffix_entry.insert(0, "_processed")  # Default value
        self.suffix_entry.grid(row=3, column=0, sticky="w", padx=5, pady=(0, 10))

        # Start/Stop Button
        self.start_stop_button = tk.Button(frame, text="Start Processing", command=self.toggle_processing)
        self.start_stop_button.grid(row=4, column=0, sticky="w", padx=5, pady=(50, 0))

        # Spinner (hidden by default)
        self.spinner = ttk.Progressbar(frame, mode='indeterminate')
        self.spinner.grid(row=5, column=0, sticky="w", padx=5, pady=(5, 10))
        self.spinner.grid_remove()  # Hide initially

    def select_output_folder(self):
        folder_path = filedialog.askdirectory(title="Select Output Folder")
        if folder_path:
            self.output_folder.set(folder_path)

    def toggle_processing(self):
        if self.app.is_processing:
            # Stop processing
            self.app.stop_processing()
            self.start_stop_button.config(text="Start Processing")
        else:
            # Start processing in a new thread
            self.start_stop_button.config(text="Stop Processing")
            self.start_processing_thread()

    def start_processing_thread(self):
        # Start the spinner
        self.spinner.grid()  # Show spinner
        self.spinner.start()

        # Run the processing in a separate thread
        processing_thread = threading.Thread(target=self.app.start_processing)
        processing_thread.start()


class MapperApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mapper")
        self.geometry("400x315")

        # Create Tab Control
        self.tab_control = ttk.Notebook(self)
        self.input_tab = InputTab(self.tab_control)
        self.output_tab = OutputTab(self.tab_control, self)

        self.tab_control.add(self.input_tab, text="Input")
        self.tab_control.add(self.output_tab, text="Output")
        self.tab_control.pack(expand=1, fill="both")

        self.is_processing = False  # Track processing state
        self.stop_requested = False  # Track if a stop is requested

    def start_processing(self):
        # Set processing state
        self.is_processing = True
        self.stop_requested = False  # Reset stop flag

        # Fetch user inputs from both tabs
        input_folder = self.input_tab.input_folder.get()
        template_file = self.input_tab.template_file.get()
        mapping_file = self.input_tab.mapping_file.get()
        output_folder = self.output_tab.output_folder.get()
        append_text = self.output_tab.suffix_entry.get()

        # Check if all fields are provided
        if not input_folder or not template_file or not mapping_file or not output_folder:
            messagebox.showerror("Missing Input", "Please ensure all input fields are filled.")
            self.stop_processing_ui_update()
            return

        try:
            # Call the processing logic with stop check
            run_processing(
                input_folder,
                template_file,
                mapping_file,
                output_folder,
                append_text,
                self.stop_requested_check,
            )

            # Display success message if completed
            if not self.stop_requested:
                messagebox.showinfo("Success", "Processing complete! Files have been saved to the output folder.")

        except Exception as e:
            # Handle any errors
            messagebox.showerror("Error", f"An error occurred during processing: {str(e)}")

        finally:
            # Stop processing UI update
            self.stop_processing_ui_update()

    def stop_processing_ui_update(self):
        """UI cleanup after processing stops."""
        self.output_tab.spinner.stop()
        self.output_tab.spinner.grid_remove()
        self.output_tab.start_stop_button.config(text="Start Processing")
        self.is_processing = False

    def stop_processing(self):
        """Sets stop_requested flag to true to signal the processing loop to stop."""
        self.stop_requested = True

    def stop_requested_check(self):
        """Check if stop has been requested and stop processing if true."""
        return self.stop_requested


if __name__ == "__main__":
    app = MapperApp()
    app.mainloop()
