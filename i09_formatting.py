# -*- coding: utf-8 -*- 
"""
Created on Tue Jul  7 15:25:21 2026

@author: bramc44
"""

import tkinter as tk
from tkinter import colorchooser
import json
import os
print("Starting...")
class LabbookFormattingDialog(tk.Toplevel):

    DEFAULT_REGION_COLOURS = {
        "c1s_xsw": "#FFC000",
        "n1s_xsw": "#11C1FF",
        "ru2p_xsw": "#DA64EE",
        "o1s_xsw": "#70AD47",
    }
    DEFAULT_PREP_COLOUR = "#FFFFFF"
    DEFAULT_PREP_COLOURS = [
        "#E2EFD9",
        "#E5E0EC",  
        "#FFF2CC",  
        "#FADBD2",  
        "#FBE5D5",  
        "#DEEBF6",  
        "#D6DCE4",
        "#C5E0B3",
        "#CCC1D9",  
        "#FEE599",  
        "#F5B7A6",  
        "#F7CBAC",  
        "#BDD7EE",  
        "#ADB9CA",
    ]
    SETTINGS_FILE = os.path.join(
        os.path.dirname(__file__),
        "i09_formatting_settings.json"
    )
    def __init__(self, parent, detected_regions):
        saved = self.load_settings()
        super().__init__(parent)

        self.title("Labbook Formatting")

        self.result = None
        self.cancelled = True

        self.region_widgets = {}

        #self.transient(parent)
        self.prep_widgets = []
        self.update_idletasks()
        self.deiconify()
        self.lift()
        self.focus_force()
        
        self.grab_set()

        tk.Label(
            self,
            text="XSW Region Colours",
            font=("Arial", 12, "bold")
        ).grid(row=0, column=0, columnspan=4, pady=10)

        row = 1

        for region in sorted(detected_regions):

            key = region.lower()

            saved_colours = saved.get("xsw_colours", {})

            default = saved_colours.get(
                key,
                self.DEFAULT_REGION_COLOURS.get(key, "#FFFFFF")
            )
            tk.Label(self, text=region).grid(
                row=row,
                column=0,
                sticky="w",
                padx=5,
                pady=2
            )

            entry = tk.Entry(self, width=10)
            entry.insert(0, default)
            entry.grid(row=row, column=1)

            preview = tk.Label(
                self,
                width=4,
                bg=default,
                relief="sunken"
            )
            preview.grid(row=row, column=2, padx=5)

            button = tk.Button(
                self,
                text="Choose",
                command=lambda e=entry, p=preview:
                    self.choose_colour(e, p)
            )
            button.grid(row=row, column=3)

            entry.bind(
                "<KeyRelease>",
                lambda event, p=preview, e=entry:
                    self.update_preview(e, p)
            )

            self.region_widgets[region] = (entry, preview)

            row += 1
        tk.Label(
            self,
            text="Preparation Blocks",
            font=("Arial", 12, "bold")
        ).grid(row=row, column=0, columnspan=6, pady=(20,5))

        row += 1
        tk.Label(self, text="Start", width=8, anchor="w").grid(
            row=row, column=0, sticky="w"
        )

        tk.Label(self, text="End", width=8, anchor="w").grid(
            row=row, column=1, sticky="w"
        )

        tk.Label(self, text="Colour", width=10, anchor="w").grid(
            row=row, column=2, sticky="w"
        )

        tk.Label(self, text="Description", width=35, anchor="w").grid(
            row=row, column=4, sticky="w"
        )

        row += 1
        # Scrollable prep area
        prep_canvas = tk.Canvas(
            self,
            height=250,
            width=700
        )
        prep_scrollbar = tk.Scrollbar(
            self,
            orient="vertical",
            command=prep_canvas.yview
        )

        self.prep_frame = tk.Frame(prep_canvas)

        self.prep_frame.bind(
            "<Configure>",
            lambda e: prep_canvas.configure(
                scrollregion=prep_canvas.bbox("all")
            )
        )

        prep_canvas.create_window(
            (0, 0),
            window=self.prep_frame,
            anchor="nw"
        )
        
        prep_canvas.configure(
            yscrollcommand=prep_scrollbar.set
        )

        prep_canvas.grid(
            row=row,
            column=0,
            columnspan=5,
            sticky="ew"
        )

        prep_scrollbar.grid(
            row=row,
            column=5,
            sticky="ns"
        )
        prep_canvas.bind_all(
            "<MouseWheel>",
            lambda e: prep_canvas.yview_scroll(
                int(-e.delta/120),
                "units"
            )
        )
        row += 1

        tk.Button(
            self,
            text="Add Prep",
            command=self.add_prep_row
        ).grid(row=row,column=0,pady=10)

        row += 1
        tk.Button(
            self,
            text="OK",
            command=self.on_ok
        ).grid(row=row, column=1, pady=15)

        tk.Button(
            self,
            text="Cancel",
            command=self.destroy
        ).grid(row=row, column=2)
        # Calculate required size
        self.update_idletasks()

        # Centre over parent
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_w = parent.winfo_width()
        parent_h = parent.winfo_height()

        dialog_w = self.winfo_width()
        dialog_h = self.winfo_height()

        x = parent_x + (parent_w - dialog_w) // 2
        y = parent_y + (parent_h - dialog_h) // 2
        
        self.geometry(f"+{x}+{y}")

        # Bring to front
        self.lift()
        self.focus_force()

        # Make modal
        self.grab_set()
        for prep in saved.get("prep_allocations",[]):
            self.add_prep_row(prep)
        if not saved.get("prep_allocations"):
            self.add_prep_row()
    def choose_colour(self, entry, preview):

        colour = colorchooser.askcolor(
            color="#808080"
        )[1]

        if colour is None:
            return

        entry.delete(0, tk.END)
        entry.insert(0, colour)

        preview.configure(bg=colour)
    def get_next_prep_colour(self):

        used_colours = []

        for prep in self.prep_widgets:
            used_colours.append(
                prep["colour"].get()
            )

        for colour in self.DEFAULT_PREP_COLOURS:
            if colour not in used_colours:
                return colour
            
        # fallback if you run out
        return self.DEFAULT_PREP_COLOUR
    def update_preview(self, entry, preview):

        colour = entry.get()

        if len(colour) == 7 and colour.startswith("#"):
            try:
                preview.configure(bg=colour)
            except:
                pass

    def on_ok(self):

        colours = {}

        for region, (entry, preview) in self.region_widgets.items():

            colours[region.lower()] = entry.get()

        self.result = {
            "xsw_colours": colours,
            "prep_allocations": []
        }
        self.save_settings(self.result)
        self.cancelled = False

        
        preps = []
        
        for prep in self.prep_widgets:
            
            try:
                start = int(prep["start"].get())
                end = int(prep["end"].get())
            except ValueError:
                continue

            preps.append({

                "start": start,
                "end": end,
                "colour": prep["colour"].get(),
                "description": prep["description"].get()

            })

        self.result = {

            "xsw_colours": colours,

        "prep_allocations": preps

        }

        self.save_settings(self.result)
        self.cancelled = False

        self.destroy()
    @classmethod
    def load_settings(cls):

        if os.path.exists(cls.SETTINGS_FILE):
            try:
                with open(cls.SETTINGS_FILE, "r") as f:
                    return json.load(f)
            except Exception:
                pass

        return {
            "xsw_colours": {},
            "prep_allocations": []
        }

    def save_settings(self, settings):

        try:
            with open(self.SETTINGS_FILE, "w") as f:
                json.dump(settings, f, indent=4)
        except Exception:
            pass
    def add_prep_row(self, prep=None):

        prep = prep or {}

        row = tk.Frame(self.prep_frame)
        row.pack(anchor="w", pady=2)

        start = tk.Entry(row,width=8)
        start.insert(0,str(prep.get("start","")))
        start.pack(side="left",padx=2)

        end = tk.Entry(row,width=8)
        end.insert(0,str(prep.get("end","")))
        end.pack(side="left",padx=2)

        colour = tk.Entry(row,width=10)

        if "colour" in prep:
            default_colour = prep["colour"]
        else:
            default_colour = self.get_next_prep_colour()

        colour.insert(
            0,
            default_colour
        )
        colour.pack(side="left",padx=2)

        preview = tk.Label(
            row,
            width=3,
            bg=colour.get(),
            relief="sunken"
        )
        preview.pack(side="left",padx=2)

        tk.Button(
            row,
            text="Choose",
            command=lambda:
                self.choose_colour(colour,preview)
            ).pack(side="left",padx=2)

        description = tk.Entry(row,width=35)
        description.insert(
            0,
            prep.get("description","")
        )
        description.pack(side="left",padx=2)

        remove_button = tk.Button(
            row,
            text="✕",
            command=lambda r=row:self.remove_prep_row(r)
        )
        remove_button.pack(side="left")

        colour.bind(
            "<KeyRelease>",
            lambda e:self.update_preview(colour,preview)
        )

        self.prep_widgets.append({
            "frame":row,
            "start":start,
            "end":end,
            "colour":colour,
            "description":description
        })
    def remove_prep_row(self, frame):

        for prep in self.prep_widgets:
            
            if prep["frame"] is frame:
                
                prep["frame"].destroy()
                
                self.prep_widgets.remove(prep)

                break