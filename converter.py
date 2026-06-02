import threading
import proglog
import time
import sys
import os

from moviepy import ImageSequenceClip
from moviepy.video.fx import Resize
from PIL import Image, ImageTk
from project import COLORS
from tkinter import messagebox


class ConvertLogger(proglog.ProgressBarLogger):
    def __init__(self, total_frames, on_progress, clip, on_preview):
        super().__init__()
        self.total_frames = total_frames
        self.on_progress = on_progress
        self.clip = clip
        self.on_preview = on_preview

    def bars_callback(self, bar, attr, value, old_value=None):
        if bar == "frame_index" and attr == "index":
            progress = value / self.total_frames
            self.on_progress(progress)
            if value % 25 == 0:
                frame = self.clip.get_frame(value / self.clip.fps)
                self.on_preview(frame)

def convert(clip, output_path, fps_value, preset_value, bitrate_value, logger=None):
    clip.write_videofile(
        output_path,
        fps=fps_value,
        bitrate=bitrate_value,
        preset=preset_value,
        logger=logger
    )

def run_convert(input_sequence,
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
                ):
    if not output_folder._full_path:
        messagebox.showerror("Missing Output", "Please configure the output")
        return

    img_list = getattr(input_sequence, "sequence_files", [])
    if not img_list:
        messagebox.showerror("Missing Input", "Please select an input sequence.")
        return

    fps_value = int(fps_val.value.get())
    total_frames = len(img_list)
    start_time = time.time()

    clip = ImageSequenceClip(img_list, fps=fps_value)
    if resolution_val.get_resize_params():
        clip = clip.with_effects([Resize(**resolution_val.get_resize_params())])

    def on_progress(progress):
        elapsed = time.time() - start_time
        remaining = (elapsed / progress * (1 - progress)) if progress > 0 else 0
        root.after(0, lambda: progress_bar.configure(progress_color=COLORS["dark_orange"]))
        root.after(0, lambda: progress_bar.set(progress))
        root.after(0, lambda: elapsed_label.configure(text=f"Elapsed Time:   {elapsed:.0f}s"))
        root.after(0, lambda: remaining_label.configure(text=f"Remaining Time: {remaining:.0f}s"))

    def on_preview(frame):
        img_copy = Image.fromarray(frame).copy()
        def update():
            prev_img.update_idletasks()
            w = prev_img.winfo_width()
            h = prev_img.winfo_height()
            img_copy.thumbnail((w, h))
            tk_img = ImageTk.PhotoImage(img_copy)
            prev_img._label.configure(image=tk_img)
            prev_img._label.image = tk_img
        root.after(0, update)

    logger = ConvertLogger(total_frames, on_progress, clip, on_preview)

    def job():
        convert(
            clip,
            output_folder._full_path,
            fps_value,
            preset_val.value.get(),
            bitrate_val.value.get(),
            logger=logger
        )
        root.after(0, lambda: convert_btn.configure(text="CONVERT", state="normal"))
        root.after(0, lambda: progress_bar.set(1.0))
        if sys.platform == "win32":
            import winsound
            tada = os.path.join(os.environ["WINDIR"], "Media", "tada.wav")
            winsound.PlaySound(tada, winsound.SND_FILENAME | winsound.SND_ASYNC)
        else:
            os.system("afplay /System/Library/Sounds/Glass.aiff &")

    root.after(0, lambda: convert_btn.configure(text="Rendering...", state="disabled"))
    thread = threading.Thread(target=job, daemon=True)
    thread.start()