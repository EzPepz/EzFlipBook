import customtkinter as ctk

from project import BORDERS, COLORS, update_recap, on_input_selected
from classes import *
from converter import run_convert


### ROOT ###
root = ctk.CTk()
root.title("EzFlipBook")
root.geometry("600x600")
root.configure(fg_color=COLORS["orange"])
root.resizable(False, False)

#------------#
# MAIN FRAME #
#------------#
mainframe = ctk.CTkFrame(
    root,
    fg_color=COLORS["dark_gray"],
    border_width=BORDERS["b_thin"],
    border_color=COLORS["orange"],
    corner_radius=0
)
mainframe.pack(fill="both", expand=True)
mainframe.grid_columnconfigure(0, weight=1)


#----------------------#
# INPUT / OUTPUT FRAME #
#----------------------#
io_frame = Panel(mainframe, "Input - Output:", height=130)
io_frame.grid(row=0, column=0, sticky="ew", padx=8, pady=(8,0))
io_frame.pack_propagate(False)

input_sequence = PathField(io_frame, "Input Sequence:", mode="file",
                           on_file_selected=lambda files: on_input_selected(files, resolution_val, prev_img,
                                                                            lambda: update_recap(fps_val,
                                                                                                resolution_val,
                                                                                                bitrate_val,
                                                                                                input_sequence,
                                                                                                set_info)
                                                                            )
                           )
input_sequence.pack(fill="x", padx=8, pady=(4,0))
input_sequence.pack_propagate(False)

output_folder = PathField(io_frame, "Output To:", mode="dir")
output_folder.pack(fill="x", padx=8, pady=(4,0))
output_folder.pack_propagate(False)


#----------------#
# SETTINGS FRAME #
#----------------#
set_frame = Panel(mainframe, "Settings:", height=218)
set_frame.grid(row=1, column=0, sticky="ew", padx=8, pady=(8, 0))
set_frame.pack_propagate(False)

set_content = ctk.CTkFrame(set_frame, fg_color="transparent")
set_content.pack(fill="x", expand=True, padx=8, pady=(0,8))
set_content.grid_columnconfigure(0, weight=2, uniform="col")
set_content.grid_columnconfigure(1, weight=1, uniform="col")
set_content.grid_rowconfigure(0, weight=1)

set_left = ctk.CTkFrame(set_content,
                        fg_color="transparent",
                        border_width=BORDERS["b_thin"],
                        border_color=COLORS["orange"],
                        corner_radius=0
                        )

set_right = ctk.CTkFrame(set_content,
                         fg_color="transparent",
                         border_width=BORDERS["b_thin"],
                         border_color=COLORS["orange"],
                         corner_radius=0
                        )

set_left.grid(row=0, column=0, sticky="nsew", padx=(0,2), pady=(4,0))
set_right.grid(row=0, column=1, sticky="nsew", padx=(2,0), pady=(4,0))

# settings
fps_val = FpsField(set_left, "FPS:", 1, 120, 25, size=60)
fps_val.pack(fill="x", padx=8, pady=(8,0))

preset_list = ["ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower", "veryslow", "placebo"]
preset_val = DropField(set_left, "Preset:", preset_list, size=60)
preset_val.pack(fill="x", padx=8, pady=(4,0))

bitrate_val = BitrateField(set_left, "Bitrate:", size=60)
bitrate_val.pack(fill="x", padx=8, pady=(4,0))

resolution_val = ResolutionField(set_left, "Size:", 144, 7680, size=60)
resolution_val.pack(fill="x", padx=8, pady=(4,8))

# info
set_info = ctk.CTkLabel(set_right, text="", anchor="nw", justify="left", font=ctk.CTkFont(family="Courier New", size=12))
set_info.pack(anchor="nw", padx=8, pady=4)

# update recap
fps_val.value.trace_add("write", lambda *a: update_recap(fps_val, resolution_val, bitrate_val, input_sequence, set_info))
bitrate_val._step.trace_add("write", lambda *a: update_recap(fps_val, resolution_val, bitrate_val, input_sequence, set_info))
resolution_val._height_display.trace_add("write", lambda *a: update_recap(fps_val, resolution_val, bitrate_val, input_sequence, set_info))

update_recap(fps_val, resolution_val, bitrate_val, input_sequence, set_info)

#---------------#
# CONVERT FRAME #
#---------------#
convert_frame = Panel(mainframe, "Convert:", height=200)
convert_frame.grid(row=2, column=0, sticky="ew", padx=8, pady=(8, 0))
convert_frame.pack_propagate(False)

convert_content = ctk.CTkFrame(convert_frame, fg_color="transparent")
convert_content.pack(fill="both", expand=True, padx=8, pady=(0,8))
convert_content.grid_columnconfigure(0, weight=1, uniform="col")
convert_content.grid_columnconfigure(1, weight=1, uniform="col")
convert_content.grid_rowconfigure(0, weight=1)


#preview (update every 25 frames)
convert_left = ctk.CTkFrame(convert_content,
                            fg_color="transparent",
                            border_width=BORDERS["b_thin"],
                            border_color=COLORS["orange"],
                            corner_radius=0
                            )

convert_left.grid(row=0, column=0, sticky="nsew", padx=(0,2), pady=(4,0))
convert_left.grid_columnconfigure(0, weight=1)
convert_left.grid_rowconfigure(0, weight=1)

prev_img = ctk.CTkLabel(convert_left, text="None Selected", anchor="center")
prev_img.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)


#convert
convert_right = ctk.CTkFrame(convert_content,
                             fg_color="transparent",
                             border_width=BORDERS["b_thin"],
                             border_color=COLORS["orange"],
                             corner_radius=0)

convert_right.grid(row=0, column=1, sticky="nsew", padx=(2,0), pady=(4,0))
convert_right.grid_columnconfigure(0, weight=1)
convert_right.grid_rowconfigure(0, weight=0) # button
convert_right.grid_rowconfigure(1, weight=0) # elapsed Time
convert_right.grid_rowconfigure(2, weight=0) # remaining Time
convert_right.grid_rowconfigure(3, weight=0) # progress


# button
convert_btn = ctk.CTkButton(convert_right,
                            text="CONVERT",
                            font=ctk.CTkFont(weight="bold", size=24),
                            fg_color=COLORS["dark_orange"],
                            hover_color=COLORS["orange"],
                            text_color=COLORS["text"],
                            height=60,
                            width=200,
                            command=lambda: run_convert(input_sequence,
                                                        output_folder,
                                                        fps_val,
                                                        preset_val,
                                                        bitrate_val,
                                                        resolution_val,
                                                        root,
                                                        progress_bar,
                                                        elapsed_label,
                                                        remaining_label,
                                                        prev_img,
                                                        convert_btn
                                                        )
                            )

convert_btn.grid(row=0, column=0, padx=10, pady=(8,4), sticky="ew")

elapsed_label = ctk.CTkLabel(convert_right,
                             text="Time elapsed: 0s",
                             anchor="w",
                             height=16,
                             font=ctk.CTkFont(family="Courier New", size=12)
                             )

elapsed_label.grid(row=1, column=0, padx=10, pady=(8,2), sticky="w")

remaining_label = ctk.CTkLabel(convert_right,
                               text="Time remaining: —",
                               anchor="w",
                               height=16,
                               font=ctk.CTkFont(family="Courier New", size=12)
                               )

remaining_label.grid(row=2, column=0, padx=10, pady=(2,8), sticky="w")

# progress bar
progress_bar = ctk.CTkProgressBar(convert_right, progress_color=COLORS["dark_orange"])
progress_bar.set(0.0)
progress_bar.configure(fg_color=COLORS["mid_gray"], progress_color=COLORS["mid_gray"])
progress_bar.grid(row=3, column=0, padx=10, pady=(8,0), sticky="ew")