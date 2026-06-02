import customtkinter as ctk
import re

from project import parse_seq_name, COLORS, BORDERS
from pathlib import Path
from tkinter import filedialog


class Panel(ctk.CTkFrame):
    def __init__(self,master, title, **kwargs):
        super().__init__(master,
                         corner_radius=0,
                         fg_color="transparent",
                         border_width=BORDERS["b_thin"],
                         border_color=COLORS["orange"],
                         **kwargs
                         )       
        self.label = ctk.CTkLabel(self,
                                  text=title,
                                  anchor="center",
                                  fg_color=COLORS["dark_purple"],
                                  text_color=COLORS["text"]
                                  )       
        self.label.pack(padx=BORDERS["b_thin"], pady=BORDERS["b_thin"], fill="x")


class LabeledField(ctk.CTkFrame):
    def __init__(self, master, title, size=100, **kwargs):
        super().__init__(master,
                         fg_color="transparent",
                         corner_radius=0,
                         border_width=BORDERS["b_thin"],
                         border_color=COLORS["orange"],
                         height=40,
                         **kwargs)
        self.size = size
        self.label = ctk.CTkLabel(self, text=title, anchor="w", width=size)
        self.label.pack(side="left", padx=10, pady=4)


class PathField(LabeledField):
    def __init__(self, master, title, mode="file", on_file_selected=None, **kwargs):
        super().__init__(master, title, **kwargs)
        self.mode = mode
        self.on_file_selected = on_file_selected
        self.path = ctk.StringVar(value="None Selected")
        self._full_path = ""
        self.sequence_files = []
        self.path_label = ctk.CTkLabel(self, textvariable=self.path, anchor="w", width=self.size)
        self.path_label.pack(side="left", padx=(0, 10))
        self.button = ctk.CTkButton(self,
                                    text="Browse",
                                    font=ctk.CTkFont(size=14),
                                    command=self.browse,
                                    width=100,
                                    fg_color=COLORS["dark_orange"],
                                    hover_color=COLORS["orange"])
        self.button.pack(side="right", padx=10)

    def _truncate(self, path_str, max_chars=40):
        if len(path_str) <= max_chars:
            return path_str
        return "..." + path_str[-(max_chars - 3):]

    def browse(self):
        if self.mode == "file":
            path = filedialog.askopenfilename(
                filetypes=[
                    ("Image Files","*.png *.jpg *.jpeg *.tiff *.tif *.tga"),
                ]
            )
        else:
            path = filedialog.asksaveasfilename(
                title="Output To:",
                defaultextension=".mp4",
                filetypes=[("MP4", "*.mp4")]
            )
        if path:
            if self.mode == "file":
                p = Path(path)
                SUPPORTED = {".png", ".jpg", ".jpeg", ".tiff", ".tif", ".tga"}
                if Path(path).suffix.lower() not in SUPPORTED:
                    from tkinter import messagebox
                    messagebox.showerror("Invalid format", f"Format not supported.\nPlease select a PNG, JPG, TIFF or TGA file.")
                    return
                folder = p.parent
                files_in_folder = list(folder.iterdir())
                result = parse_seq_name(p.name)
                if result:
                    base, sep, padding, ext = result
                    sep_escaped = re.escape(sep) if sep else ''
                    pattern_str = f"^{re.escape(base)}{sep_escaped}(\\d{{{padding}}}){re.escape(ext)}$"
                    pattern = re.compile(pattern_str)
                    files = [f for f in files_in_folder if pattern.match(f.name)]
                    files_sorted = sorted(files, key=lambda f: int(pattern.match(f.name).group(1)))
                    self.sequence_files = [str(f) for f in files_sorted]
                    seq_pattern = str(folder / (f"{base}{sep}" + "#"*padding + ext))
                    self._full_path = seq_pattern
                    self.path.set(self._truncate(seq_pattern))
                else:
                    self.sequence_files = [str(p)]
                    self._full_path = str(p)
                    self.path.set(self._truncate(str(p)))
                if self.on_file_selected:
                    self.on_file_selected(self.sequence_files)
            else:
                self._full_path = path
                self.path.set(self._truncate(path))


class FpsField(LabeledField):
    def __init__(self, master, title, min_val, max_val, def_val, **kwargs):
        super().__init__(master, title, **kwargs)
        self.value = ctk.StringVar(value=str(def_val))
        self.min_val = min_val
        self.max_val = max_val
        self._def_val = def_val

        chek_val = (self.register(self._validate), "%P")

        self.entry = ctk.CTkEntry(self, textvariable=self.value, validate="key", validatecommand=chek_val, width=60)
        self.entry.pack(side="left")
        self.entry.bind("<FocusOut>", self._on_focus_out)

    def _validate(self, new_val):
        if new_val == "":
            return True
        if not new_val.isdigit():
            return False
        return self.min_val <= int(new_val) <= self.max_val

    def _on_focus_out(self, event):
        if self.entry.get() == "":
            self.value.set(str(self._def_val))


class DropField(LabeledField):
    def __init__(self, master, title, options, **kwargs):
        super().__init__(master, title, **kwargs)
        self.value = ctk.StringVar(value=options[0])
        self.dropdown = ctk.CTkOptionMenu(self,
                                          variable=self.value,
                                          values=options,
                                          fg_color=COLORS["dark_orange"],
                                          button_color=COLORS["dark_orange"],
                                          button_hover_color=COLORS["orange"])
        self.dropdown.pack(side="left")


class BitrateField(LabeledField):
    STEPS = [500, 1000, 1500, 2000, 3000, 4000, 6000, 8000, 10000, 15000, 20000, 30000, 50000]

    def __init__(self, master, title, **kwargs):
        super().__init__(master, title, **kwargs)

        self.value = ctk.StringVar(value="6000k")
        self._display = ctk.StringVar(value="6 Mbps")
        self._step = ctk.IntVar(value=self.STEPS.index(6000))

        self.slider = ctk.CTkSlider(self,
                                    button_color=COLORS["dark_orange"],
                                    button_hover_color=COLORS["orange"],
                                    from_=0,
                                    to=len(self.STEPS) - 1,
                                    number_of_steps=len(self.STEPS) - 1,
                                    variable=self._step,
                                    command=self._on_slide)
        self.slider.pack(side="left", expand=True, fill="x", padx=(0, 8))

        self.val_label = ctk.CTkLabel(self, textvariable=self._display, width=80, anchor="w")
        self.val_label.pack(side="left", padx=(0, 4))

    def _on_slide(self, val):
        kbps = self.STEPS[int(round(val))]
        self.value.set(f"{kbps}k")
        if kbps >= 1000:
            self._display.set(f"{kbps // 1000} Mbps" if kbps % 1000 == 0 else f"{kbps / 1000:.1f} Mbps")
        else:
            self._display.set(f"{kbps} kbps")


class ResolutionField(LabeledField):
    def __init__(self, master, title, min_val, max_val, **kwargs):
        super().__init__(master, title, **kwargs)
        self.min_val = min_val
        self.max_val = max_val
        self.width = ctk.IntVar(value=0)
        self._height_display = ctk.StringVar(value="—")
        self._aspect = None

        validate = (self.register(self._validate), "%P")

        self.width_entry = ctk.CTkEntry(self, textvariable=self.width, validate="key", validatecommand=validate, width=70)
        self.width_entry.pack(side="left", padx=(0, 4))
        self.width_entry.bind("<FocusOut>", self._on_focus_out)

        ctk.CTkLabel(self, text="×").pack(side="left")

        self.height_label = ctk.CTkLabel(self, textvariable=self._height_display, width=70, anchor="center")
        self.height_label.pack(side="left", padx=(4, 0))

        self.width.trace_add("write", self._on_width_change)

    def _validate(self, val):
        if val == "":
            return True
        if not val.isdigit():
            return False
        return int(val) <= self.max_val

    def _on_width_change(self, *args):
        if self._aspect:
            try:
                w = int(self.width.get())
                h = int(round(w * self._aspect))
                self._height_display.set(str(h))
            except Exception:
                self._height_display.set("—")

    def _on_focus_out(self, event):
        try:
            w = int(self.width.get())
            if w < self.min_val:
                self.width.set(self.min_val)
            elif w > self.max_val:
                self.width.set(self.max_val)
        except ValueError:
            pass

    def set_resolution(self, w, h):
        self._aspect = h / w if w else 1
        self.width.set(w)
        self._height_display.set(str(h))

    def get_resize_params(self):
        w = self.width.get()
        return {"width": w} if w else None
    
