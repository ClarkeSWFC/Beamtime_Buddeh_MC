import tkinter as tk
from tkinter import filedialog, messagebox
from convert_nexus_folder import convert_nexus_folder_i09, convert_data_folder_flexpes,convert_nexus_folder_b07_1
from txt_file_handler import normaliser, load_spectra_from_folder
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from create_labbook_i09 import create_labbook_i09
from create_labbook_flexpes  import create_labbook_flexpes 
from create_labbook_i06_2 import create_labbook_i06_2
from create_labbook_b07_1 import create_labbook_b07_1
import numpy as np
import threading
from tkinter import ttk
import os

#MC woz ere ☭

class BEAMTIMEBUDDEH:

    def __init__(self, root):
        self.root = root
        self.root.title("Beamtime Buddeh")

        self.data_dict = {}
        self.shift_entries = {}

        self.setup_frames()
        self.setup_conversion_section()
        self.setup_loading_section()
        self.setup_plot_area()
        self.setup_shift_panel()
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()

        self.root.geometry(f"{int(screen_w*0.8)}x{int(screen_h*0.8)}")
        self.root.maxsize(screen_w, screen_h)

        self.root.columnconfigure(1, weight=3)
        self.root.columnconfigure(2, weight=1)

    # ==============================
    # Layout
    # ==============================

    def setup_frames(self):
        self.root.columnconfigure(0, weight=0)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=0)

        self.root.rowconfigure(0, weight=1)

        self.left_frame = tk.Frame(self.root, padx=10, pady=10)
        self.left_frame.grid(row=0, column=0, sticky="ns")

        self.middle_frame = tk.Frame(self.root, padx=10, pady=10)
        self.middle_frame.grid(row=0, column=1, sticky="nsew")

        self.right_frame = tk.Frame(self.root, padx=10, pady=10)
        self.right_frame.grid(row=0, column=2, sticky="ns")
    # ==============================
    # Detect which beamline
    # ==============================
    def detect_beamline(self, folder):

        files = os.listdir(folder)

        # =====================================
        # CASE 1: .nxs files (Diamond Standard)
        # =====================================
        nxs_files = sorted([f for f in files if f.endswith(".nxs")])

        if nxs_files:
            first_file = nxs_files[0]
            prefix = first_file[:5]

            if prefix.startswith("i09-"):
                return "i09"

            elif prefix.startswith("i06-2"):
                return "i06-2"

            elif prefix.startswith("b07-1"):
                return "b07-1"

            else:
                messagebox.showwarning(
                    "Unsupported",
                    f"new beamline '{prefix}' not yet supported"
                )
                return None

        # ==============================
        # CASE 2: FLEXPES (possibly) (.txt)
        # ==============================
        txt_files = [f for f in files if f.startswith("XPS") and f.endswith(".txt")]

        if txt_files:
            txt_path = os.path.join(folder, txt_files[0])

            try:
                with open(txt_path, "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        if line.startswith("Location="):
                            location = line.split("=", 1)[1].strip()

                            if location == "FlexPES":
                                return "flexpes"
                            else:
                                messagebox.showwarning(
                                    "Unsupported",
                                    f"new beamline, probable MAX IV, '{location}' not yet supported"
                                )
                                return None

            except Exception as e:
                messagebox.showerror("Error", str(e))
                return None

        # ==============================
        # CASE 3: Nothing found
        # ==============================
        messagebox.showwarning(
            "Error",
            "cannot identify beamline data in selected location"
        )
        return None
    # ==============================
    # Conversion Section
    # ==============================

    def setup_conversion_section(self):

        tk.Label(self.left_frame, text="Data Handling").pack(pady=(0, 5))

        # ---------------- Folder Selection ----------------


        tk.Button(
            self.left_frame,
            text="Select Input Folder",
            command=self.select_input_folder
        ).pack(fill="x")

        tk.Button(
            self.left_frame,
            text="Select Output Folder",
            command=self.select_output_folder
        ).pack(fill="x", pady=(0, 10))

        # -----------------------------
        # Unified Buttons
        # -----------------------------
        self.beamline_label = tk.Label(self.left_frame, text="Beamline: None")
        self.beamline_label.pack(pady=(5, 10))
        tk.Button(
            self.left_frame,
            text="Convert Spectra Data to .txt",
            command=self.auto_convert_data
        ).pack(fill="x", pady=2)

        tk.Button(
            self.left_frame,
            text="Create Labbook",
            command=self.auto_create_labbook
        ).pack(fill="x", pady=2)
    def select_input_folder(self):
        folder = filedialog.askdirectory()
        if not folder:
            return

        self.input_dir = folder

        # Detect beamline immediately
        self.beamline = self.detect_beamline(folder)

        if self.beamline:
            messagebox.showinfo("Beamline Detected", f"Detected: {self.beamline}")
        if self.beamline:
            self.beamline_label.config(text=f"Beamline: {self.beamline}")
        else:
            self.beamline_label.config(text="Beamline: Unsupported/Unknown")
    def select_output_folder(self):
        self.output_dir = filedialog.askdirectory()
    def auto_convert_data(self):

        if not hasattr(self, 'input_dir') or not hasattr(self, 'output_dir'):
            messagebox.showwarning("Error", "Select both folders first.")
            return

        if not hasattr(self, 'beamline') or self.beamline is None:
            messagebox.showwarning("Error", "Beamline not identified.")
            return

        if self.beamline == "i09":
            self.run_conversion_i09()

        elif self.beamline == "flexpes":
            self.run_conversion_flexpes()
        
        elif self.beamline == "i06-2":
            messagebox.showwarning("Error", "i06-2 does not produce line spectra")
            
        elif self.beamline == "b07-1":
            self.run_conversion_b07_1()   
        
    
    def auto_create_labbook(self):

        if not hasattr(self, 'input_dir') or not hasattr(self, 'output_dir'):
            messagebox.showwarning("Error", "Select both folders first.")
            return

        if not hasattr(self, 'beamline') or self.beamline is None:
            messagebox.showwarning("Error", "Beamline not identified.")
            return

        if self.beamline == "i09":
            self.create_labbook_i09_gui()

        elif self.beamline == "flexpes":
            self.create_labbook_flexpes_gui()
            
        elif self.beamline == "i06-2":
            self.create_labbook_i06_2_gui()
        
        elif self.beamline == "b07-1":
            self.create_labbook_b07_1_gui()
    def run_conversion_i09(self):

        if not hasattr(self, 'input_dir') or not hasattr(self, 'output_dir'):
            messagebox.showwarning("Error", "Select both folders first.")
            return

        file_list = [f for f in os.listdir(self.input_dir) if f.endswith(".nxs")]
        total_files = len(file_list)
        if total_files == 0:
            messagebox.showinfo("No Files", "No matching files found.")
            return
        progress_window = ProgressWindow(self.root, total_files, "Converting i09 Data")

        def progress_callback(message):
            def update_ui():
                progress_window.update_status(message)
                progress_window.step()

            self.root.after(0, update_ui)

        def task():
            try:
                convert_nexus_folder_i09(
                    self.input_dir,
                    self.output_dir,
                    progress_callback=progress_callback
                )
                progress_window.close()
                messagebox.showinfo("Done", "Conversion complete.")
            except Exception as e:
                progress_window.close()
                messagebox.showerror("Error", str(e))

        threading.Thread(target=task).start()
    def run_conversion_b07_1(self):

        if not hasattr(self, 'input_dir') or not hasattr(self, 'output_dir'):
            messagebox.showwarning("Error", "Select both folders first.")
            return

        file_list = [f for f in os.listdir(self.input_dir) if f.endswith(".nxs")]
        total_files = len(file_list)
        if total_files == 0:
            messagebox.showinfo("No Files", "No matching files found.")
            return
        progress_window = ProgressWindow(self.root, total_files, "Converting b07 Data")

        def progress_callback(message):
            def update_ui():
                progress_window.update_status(message)
                progress_window.step()

            self.root.after(0, update_ui)

        def task():
            try:
                convert_nexus_folder_b07_1(
                    self.input_dir,
                    self.output_dir,
                    progress_callback=progress_callback
                )
                progress_window.close()
                messagebox.showinfo("Done", "Conversion complete.")
            except Exception as e:
                progress_window.close()
                messagebox.showerror("Error", str(e))

        threading.Thread(target=task).start()
    def run_conversion_flexpes(self):

        if not hasattr(self, 'input_dir') or not hasattr(self, 'output_dir'):
            messagebox.showwarning("Error", "Select both folders first.")
            return

        all_files = os.listdir(self.input_dir)

        # Count XPS files
        xps_files = [
            f for f in all_files
            if f.startswith("XPS_") and f.endswith(".txt")
        ]

        # Count H5 files
        h5_files = [
            f for f in all_files
            if f.endswith(".h5")
        ]

        file_list = xps_files + h5_files
        total_files = len(file_list)
        if total_files == 0:
            messagebox.showinfo("No Files", "No matching files found.")
            return
        progress_window = ProgressWindow(self.root, total_files, "Converting flexpes Data")

        def status_callback(message):
            self.root.after(0, lambda: progress_window.update_status(message))

        def file_done_callback():
            self.root.after(0, progress_window.step)

        def task():
            try:
                convert_data_folder_flexpes(
                    self.input_dir,
                    self.output_dir,
                    file_done_callback=file_done_callback,
                    status_callback=status_callback
                )
                progress_window.close()
                messagebox.showinfo("Done", "Conversion complete.")
            except Exception as e:
                progress_window.close()
                messagebox.showerror("Error", str(e))

        threading.Thread(target=task).start()
    def create_labbook_i09_gui(self):

        if not hasattr(self, 'input_dir') or not hasattr(self, 'output_dir'):
            messagebox.showwarning("Error", "Select both folders first.")
            return

        file_list = [f for f in os.listdir(self.input_dir) if f.endswith(".nxs")]
        total_files = len(file_list)
        if total_files == 0:
            messagebox.showinfo("No Files", "No matching files found.")
            return
        progress_window = ProgressWindow(self.root, total_files, "Creating i09 Labbook")

        def progress_callback(message):
            def update_ui():
                progress_window.update_status(message)
                progress_window.step()

            self.root.after(0, update_ui)

        def task():
            try:
                create_labbook_i09(
                    self.input_dir,
                    self.output_dir,
                    progress_callback=progress_callback
                )
                progress_window.close()
                messagebox.showinfo("Success", " Excel sheet produced by hardworking script goblins: ლ༼ ಥ 益 ಥ ༽ლ")
            except Exception as e:
                progress_window.close()
                messagebox.showerror("Error", str(e))

        threading.Thread(target=task).start()
    def create_labbook_i06_2_gui(self):

        if not hasattr(self, 'input_dir') or not hasattr(self, 'output_dir'):
            messagebox.showwarning("Error", "Select both folders first.")
            return

        file_list = [f for f in os.listdir(self.input_dir) if f.endswith(".nxs")]
        total_files = len(file_list)
        if total_files == 0:
            messagebox.showinfo("No Files", "No matching files found.")
            return
        progress_window = ProgressWindow(self.root, total_files, "Creating i06_2 Labbook")

        def progress_callback(message):
            def update_ui():
                progress_window.update_status(message)
                progress_window.step()

            self.root.after(0, update_ui)

        def task():
            try:
                create_labbook_i06_2(
                    self.input_dir,
                    self.output_dir,
                    progress_callback=progress_callback
                )
                progress_window.close()
                messagebox.showinfo("Success", " Excel sheet produced by hardworking script goblins: ლ༼ ಥ 益 ಥ ༽ლ")
            except Exception as e:
                progress_window.close()
                messagebox.showerror("Error", str(e))

        threading.Thread(target=task).start()
    def create_labbook_b07_1_gui(self):

        if not hasattr(self, 'input_dir') or not hasattr(self, 'output_dir'):
            messagebox.showwarning("Error", "Select both folders first.")
            return

        file_list = [f for f in os.listdir(self.input_dir) if f.endswith(".nxs")]
        total_files = len(file_list)
        if total_files == 0:
            messagebox.showinfo("No Files", "No matching files found.")
            return
        progress_window = ProgressWindow(self.root, total_files, "Creating b07-1 Labbook")

        def progress_callback(message):
            def update_ui():
                progress_window.update_status(message)
                progress_window.step()

            self.root.after(0, update_ui)

        def task():
            try:
                create_labbook_b07_1(
                    self.input_dir,
                    self.output_dir,
                    progress_callback=progress_callback
                )
                progress_window.close()
                messagebox.showinfo("Success", " Excel sheet produced by hardworking script goblins: ლ༼ ಥ 益 ಥ ༽ლ")
            except Exception as e:
                progress_window.close()
                messagebox.showerror("Error", str(e))

        threading.Thread(target=task).start()
    def create_labbook_flexpes_gui(self):

        if not hasattr(self, 'input_dir') or not hasattr(self, 'output_dir'):
            messagebox.showwarning("Error", "Select both folders first.")
            return
        all_files = os.listdir(self.input_dir)
        # Count XPS files
        xps_files = [
            f for f in all_files
            if f.startswith("XPS_") and f.endswith(".txt")
        ]

        # Count H5 files
        h5_files = [
            f for f in all_files
            if f.endswith(".h5")
        ]

        file_list = xps_files + h5_files
        total_files = len(file_list)
        if total_files == 0:
            messagebox.showinfo("No Files", "No matching files found.")
            return
        progress_window = ProgressWindow(self.root, total_files, "Creating flexpes Labbook")

        def progress_callback(message):
            def update_ui():
                progress_window.update_status(message)
                progress_window.step()

            self.root.after(0, update_ui)

        def task():
            try:
                create_labbook_flexpes(
                    self.input_dir,
                    self.output_dir,
                    progress_callback=progress_callback
                )
                progress_window.close()
                messagebox.showinfo("Success", " Excel sheet produced by hardworking script goblins: ლ༼ ಥ 益 ಥ ༽ლ")
            except Exception as e:
                progress_window.close()
                messagebox.showerror("Error", str(e))

        threading.Thread(target=task).start()
    # ==============================
    # Loading Section
    # ==============================

    def setup_loading_section(self):
        tk.Label(self.left_frame, text="Load Spectra").pack(pady=(20, 0))

        tk.Button(self.left_frame, text="Select Spectra .txt Folder",
                  command=self.load_spectra).pack(fill="x")

        self.setup_spectra_scroll_panel()

    def setup_spectra_scroll_panel(self):

        tk.Label(self.left_frame, text="Select Spectra").pack(pady=(10, 0))

        # --- Search Box ---
        search_frame = tk.Frame(self.left_frame)
        search_frame.pack(fill="x", pady=(2, 5))

        tk.Label(search_frame, text="Search:").pack(side="left")

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.filter_spectra())

        search_entry = tk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side="left", fill="x", expand=True, padx=3)

        # --- Deselect All Button ---
        tk.Button(
            self.left_frame,
            text="Deselect All",
            command=self.deselect_all_spectra
        ).pack(fill="x", pady=(0, 5))
        # --- Clear All Spectra Button ---
        tk.Button(
            self.left_frame,
            text="Clear All Spectra",
            command=self.clear_all_spectra
        ).pack(fill="x", pady=(0, 5))
        # --- Scrollable Canvas ---
        self.spectra_canvas = tk.Canvas(self.left_frame, width=250, height=300)
        self.spectra_canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(
            self.left_frame,
            orient="vertical",
            command=self.spectra_canvas.yview
        )
        self.scrollbar.pack(side="right", fill="y")

        self.spectra_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.spectra_check_frame = tk.Frame(self.spectra_canvas)
        self.spectra_canvas.create_window((0, 0),
                                          window=self.spectra_check_frame,
                                          anchor="nw")

        self.spectra_check_frame.bind(
            "<Configure>",
            lambda e: self.spectra_canvas.configure(
                scrollregion=self.spectra_canvas.bbox("all"))
        )

        self.spectra_vars = {}
 
    def deselect_all_spectra(self):

        for var in self.spectra_vars.values():
            var.set(False)

        self.replot()
    def clear_all_spectra(self):

        # Clear stored data
        self.data_dict.clear()
        self.spectra_vars.clear()
        self.shift_entries.clear()

        # Remove all checkboxes
        for widget in self.spectra_check_frame.winfo_children():
            widget.destroy()

        # Clear shift panel
        for widget in self.shift_panel.winfo_children():
            widget.destroy()

        # Clear plot
        self.ax.clear()
        self.canvas.draw()

        messagebox.showinfo("Cleared", "All spectra have been removed.")
    def load_spectra(self):

        folder = filedialog.askdirectory()
        if not folder:
            return

        txt_files = [f for f in os.listdir(folder) if f.endswith(".txt")]
        total_files = len(txt_files)

        if total_files == 0:
            messagebox.showwarning("No Data", "No spectra found in folder.")
            return

        progress_window = ProgressWindow(
            self.root,
            total_files,
            "Loading Spectra"
        )

        def progress_callback(message):
            def update_ui():
                progress_window.update_status(message)
                progress_window.step()

            self.root.after(0, update_ui)

        def task():
            try:
                new_data = load_spectra_from_folder(
                    folder,
                    progress_callback=progress_callback
                )

                def finish():
                    progress_window.close()

                    added = 0
                    skipped = 0

                    for key, value in new_data.items():
                        if key in self.data_dict:
                            skipped += 1
                        else:
                            self.data_dict[key] = value
                            added += 1

                    if added == 0:
                        messagebox.showinfo(
                            "No New Spectra",
                            "All loaded spectra already exist."
                        )
                    else:
                        messagebox.showinfo(
                            "Spectra Loaded",
                            f"Added {added} new spectra.\nSkipped {skipped} duplicates."
                        )

                    self.populate_spectra_checkboxes()

                self.root.after(0, finish)

            except Exception as e:
                self.root.after(0, progress_window.close)
                self.root.after(0, lambda err=e: messagebox.showerror("Error", str(err)))

        threading.Thread(target=task).start()
    def populate_spectra_checkboxes(self):

        # Save current states
        old_states = {
            key: var.get() for key, var in self.spectra_vars.items()
        }

        for widget in self.spectra_check_frame.winfo_children():
            widget.destroy()

        for key in self.data_dict.keys():

            var = tk.BooleanVar(value=old_states.get(key, False))

            cb = tk.Checkbutton(
                self.spectra_check_frame,
                text=key,
                variable=var,
                command=self.on_checkbox_change  # important
            )

            cb.pack(anchor="w")

            self.spectra_vars[key] = var
    def filter_spectra(self):
        search_text = self.search_var.get().lower()

        for widget in self.spectra_check_frame.winfo_children():
            widget.destroy()

        for key in self.data_dict.keys():
            if search_text in key.lower():
                var = self.spectra_vars.get(key, tk.BooleanVar(value=False))
                self.spectra_vars[key] = var

                cb = tk.Checkbutton(
                    self.spectra_check_frame,
                    text=key,
                    variable=var,
                    command=self.on_checkbox_change  # <--- ensure shift panel updates
                )
                cb.pack(anchor="w")

        
        self.on_checkbox_change()
    def on_checkbox_change(self):
        selected_keys = [
            key for key, var in self.spectra_vars.items() if var.get()
        ]

        MAX_SELECTED = 40
        if len(selected_keys) > MAX_SELECTED:
            messagebox.showwarning(
                "Limit Reached",
                "Select up to 40 spectra."
            )
            for key in selected_keys[MAX_SELECTED:]:
                self.spectra_vars[key].set(False)
            selected_keys = selected_keys[:MAX_SELECTED]

        
        self.update_shift_panel(selected_keys)
        self.update_plot(selected_keys)

    # ==============================
    # Plot Area
    # ==============================

    def setup_plot_area(self):
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.middle_frame)

        widget = self.canvas.get_tk_widget()
        widget.grid(row=0, column=0, sticky="nsew")

        self.middle_frame.rowconfigure(0, weight=1)
        self.middle_frame.columnconfigure(0, weight=1)

        self.canvas.draw()
        

    def update_plot(self, selected_keys):

        self.ax.clear()

        for key in selected_keys:

            spectra = self.data_dict[key]

            try:
                x_shift = float(self.shift_entries[key]["x"].get())
                y_shift = float(self.shift_entries[key]["y"].get())
            except (ValueError, KeyError):
                x_shift = 0
                y_shift = 0

            if key in self.shift_entries and self.shift_entries[key]["norm"].get():
                y_data = normaliser(spectra)
            else:
                y_data = spectra[:, 1]

            shifted_x = spectra[:, 0] + x_shift
            shifted_y = y_data + y_shift

            file_number = key.split("_")[0]
            self.ax.plot(shifted_x, shifted_y, label=file_number)

        if selected_keys:
            self.ax.legend()

        # ---------------- Axis Logic ----------------

        lower_keys = [key.lower() for key in selected_keys]

        is_kinetic = any("kinetic" in key for key in lower_keys)
        is_nexafs = any(
            any(term in key for term in ["kll", "lmm", "raes", "nexafs"])
            for key in lower_keys
        )

        if is_nexafs:
            self.ax.set_xlabel("Photon Energy (eV)")
            base_invert = False

        elif is_kinetic:
            self.ax.set_xlabel("Kinetic Energy (eV)")
            base_invert = False

        else:
            self.ax.set_xlabel("Binding Energy (eV)")
            base_invert = True


        # Apply RESPES/NEXAFS override
        if self.respes_var.get():
            invert = not base_invert
        else:
            invert = base_invert

        if invert:
            self.ax.invert_xaxis()
        self.ax.set_ylabel("Intensity")
        self.canvas.draw()
    def replot(self):
        selected_keys = [
            key for key, var in self.spectra_vars.items()
            if var.get()
        ]
        self.update_plot(selected_keys)
        
    # ==============================
    # Shift Panel
    # ==============================

    def setup_shift_panel(self):
        tk.Label(self.right_frame, text="Shifts").pack()

        self.shift_panel = tk.Frame(self.right_frame)
        self.shift_panel.pack(fill="both", expand=True)

        self.respes_var = tk.BooleanVar(value=False)

        tk.Checkbutton(
            self.right_frame,
            text="Flip X axis",
            variable=self.respes_var,
            command=self.replot
        ).pack(pady=5)

        tk.Button(self.right_frame,
                  text="Sum",
                  command=self.sum_selected_spectra).pack(pady=5)

        tk.Button(self.right_frame,
                  text="Fermi Finder",
                  command=self.find_step_centers).pack(pady=5)

        tk.Button(self.right_frame,
                  text="Save Figure",
                  command=self.save_figure).pack(pady=5)

    def update_shift_panel(self, selected_keys):

        for widget in self.shift_panel.winfo_children():
            widget.destroy()

        self.shift_entries = {}

        if not selected_keys:
            return

        # ==============================
        # Norm All Checkbox (Master)
        # ==============================

        self.norm_all_var = tk.BooleanVar(value=False)

        def toggle_all_norms():
            for key in self.shift_entries:
                self.shift_entries[key]["norm"].set(self.norm_all_var.get())
            self.replot()

        master_frame = tk.Frame(self.shift_panel)
        master_frame.pack(fill="x", pady=(0, 5))

        tk.Checkbutton(
            master_frame,
            text="Norm All",
            variable=self.norm_all_var,
            command=toggle_all_norms
        ).pack(anchor="e")

        tk.Label(self.shift_panel, text="--------------------").pack()

        # ==============================
        # Individual Shift Rows
        # ==============================

        for key in selected_keys:

            row = tk.Frame(self.shift_panel)
            row.pack(fill="x", pady=2)

            tk.Label(row, text=key.split("_")[0],
                     width=10, anchor="w").pack(side="left")
            
            tk.Label(row, text="X:").pack(side="left")
            x_entry = tk.Entry(row, width=6)
            x_entry.insert(0, "0")
            x_entry.pack(side="left", padx=3)
            tk.Label(row, text="Y:").pack(side="left")
            y_entry = tk.Entry(row, width=6)
            y_entry.insert(0, "0")
            y_entry.pack(side="left", padx=3)

            norm_var = tk.BooleanVar()

            tk.Checkbutton(
                row,
                text="Norm",
                variable=norm_var,
                command=self.replot
            ).pack(side="left", padx=3)

            x_entry.bind("<KeyRelease>", lambda e: self.replot())
            y_entry.bind("<KeyRelease>", lambda e: self.replot())

            self.shift_entries[key] = {
                "x": x_entry,
                "y": y_entry,
                "norm": norm_var
            }

    # ==============================
    # Analysis Tools
    # ==============================

    def find_step_centers(self):

        selected_keys = [
            key for key, var in self.spectra_vars.items()
            if var.get()
        ]

        if not selected_keys:
            messagebox.showwarning("No Selection", "Select spectra first.")
            return

        for key in selected_keys:

            spectra = self.data_dict[key]

            x_data = spectra[:, 0]
            y_data = spectra[:, 1]

            dy_dx = np.gradient(y_data, x_data)
            max_slope_idx = np.argmax(np.abs(dy_dx))
            step_center = x_data[max_slope_idx]

            self.ax.axvline(step_center,
                            color='r',
                            linestyle=':',
                            label=f"{step_center:.3f} eV")

        self.ax.legend()
        self.canvas.draw()

    def sum_selected_spectra(self):
        selected_keys = [key for key, var in self.spectra_vars.items() if var.get()]

        if len(selected_keys) < 2:
            messagebox.showwarning(
                "Selection Error",
                "Select at least two spectra to sum."
            )
            return

        reference_x = None
        summed_y = None

        for key in selected_keys:
            spectra = self.data_dict[key]
            x_data = spectra[:, 0]
            y_data = spectra[:, 1]

            if reference_x is None:
                reference_x = x_data
                summed_y = np.zeros_like(y_data)

            if not np.allclose(reference_x, x_data, atol=1e-6):
                messagebox.showerror(
                    "X-axis mismatch",
                    f"Spectra '{key}' has mismatched X values."
                )
                return

            summed_y += y_data

        # ---------------- Add summed spectrum to data_dict ----------------
        first_region = selected_keys[0].split("_", 1)[0] if "_" in selected_keys[0] else "region"
        summed_name = f"summed_{first_region}+"
        self.data_dict[summed_name] = np.column_stack((reference_x, summed_y))
        
        # ---------------- Deselect all other spectra ----------------
        for key, var in self.spectra_vars.items():
            var.set(False)

        # ---------------- Add a checkbox for the summed spectrum ----------------
        var = self.spectra_vars.get(summed_name, tk.BooleanVar())
        var.set(True)
        self.spectra_vars[summed_name] = var
        
        cb = tk.Checkbutton(
            self.spectra_check_frame,
            text=summed_name,
            variable=var,
            command=self.replot
        )
        cb.pack(anchor="w")

        # ---------------- Plot the summed spectrum ----------------
        current_xlabel = self.ax.get_xlabel()
        is_inverted = self.ax.xaxis_inverted()
        
        self.ax.clear()
        self.ax.plot(reference_x, summed_y, linewidth=2, label=summed_name)
        
        # Restore previous axis label and direction
        self.ax.set_xlabel(current_xlabel)
        self.ax.set_ylabel("Intensity")
        if is_inverted != self.ax.xaxis_inverted():
            self.ax.invert_xaxis()

        self.ax.set_title("Summed Spectrum")
        self.ax.legend()
        self.canvas.draw()
    # ==============================
    # Save Figure
    # ==============================

    def save_figure(self):

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"),
                       ("SVG files", "*.svg")]
        )

        if not file_path:
            return

        self.figure.savefig(file_path)
        messagebox.showinfo("Saved", f"Figure saved to:\n{file_path}")


class ProgressWindow(tk.Toplevel):

    def __init__(self, parent, total_steps, title="Processing..."):
        super().__init__(parent)

        self.title(title)
        self.geometry("400x150")
        self.transient(parent)
        self.grab_set()

        self.total_steps = total_steps
        self.current_step = 0

        # ---- Widgets ----
        self.label = tk.Label(self, text="Starting...")
        self.label.pack(pady=10)

        self.progress = ttk.Progressbar(
            self,
            orient="horizontal",
            length=350,
            mode="determinate",
            maximum=total_steps
        )
        self.progress.pack(pady=10)

        self.percent_label = tk.Label(self, text="0%")
        self.percent_label.pack()

        # ---- Center Window ----
        self.update_idletasks()

        width = self.winfo_width()
        height = self.winfo_height()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))

        self.geometry(f"{width}x{height}+{x}+{y}")

    # ---- Methods ----

    def update(self, message):
        if not self.winfo_exists():
            return
        self.update_status(message)

    def update_status(self, message):
        if self.winfo_exists():
            self.label.config(text=message)

    def step(self):
        if not self.winfo_exists():
            return

        self.current_step += 1
        self.progress["value"] = self.current_step

        if self.total_steps > 0:
            percent = int((self.current_step / self.total_steps) * 100)
        else:
            percent = 100

        self.percent_label.config(text=f"{percent}%")
        self.update_idletasks()

    def close(self):
        if self.winfo_exists():
            self.destroy()