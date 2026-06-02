import re

from pathlib import Path

#globals for borders and colors
BORDERS = {
    "b_thin": 1,
    "b_mid": 2,
    "b_thick": 3,
}

COLORS = {
    "dark_gray": "#1f1f1f",
    "mid_gray": "#404040",
    "orange": "#F18023",
    "dark_orange": "#dd6300",
    "mid_purple": "#5C3E94",
    "dark_purple": "#412B6B",
    "almost_black": "#0F0B16",
    "border_light": "#e0e0e0",
    "text": "#ffffff"
}


def main():
    import gui
    gui.root.mainloop()


def calc_dur(num_frames, fps):
    if fps <= 0:
        return 0
    return num_frames / fps


def calc_est_size(bitrate_kbps, duration):
    return (bitrate_kbps * duration) / 8 / 1024


def on_input_selected(files, resolution_val, prev_img, update_recap_fn):
    import customtkinter as ctk
    from PIL import Image
    if files:
        try:
            with Image.open(files[0]) as img:
                w, h = img.size
                preview = img.copy()
            resolution_val.set_resolution(w, h)

            prev_img.update_idletasks()
            max_w = prev_img.winfo_width()
            max_h = prev_img.winfo_height()

            preview.thumbnail((max_w, max_h))
            ctk_img = ctk.CTkImage(preview, size=preview.size)
            prev_img.configure(image=ctk_img, text="")
            prev_img._image = ctk_img

        except Exception as e:
            print(f"Error: {e}")
        update_recap_fn()

def parse_seq_name(filename):
    p = Path(filename)
    name = p.stem
    ext = p.suffix
    #regex
    match = re.match(r"(.+?)([._-]?)(\d+)$", name)
    if match:
        base, sep, frame = match.groups()
        padding = len(frame)
        return base, sep, padding, ext
    return None

def update_recap(fps_val, resolution_val, bitrate_val, input_sequence, set_info, *args):
    try:
        fps = int(fps_val.value.get())
        num_files = len(getattr(input_sequence, "sequence_files", []))
        duration = calc_dur(num_files, fps)

        w = resolution_val.width.get()
        h = resolution_val._height_display.get()
        resolution = f"{w} × {h}" if w else "—"

        bitrate_str = bitrate_val._display.get()
        bitrate_kbps = bitrate_val.STEPS[int(round(bitrate_val._step.get()))]
        estimated_mb = calc_est_size(bitrate_kbps, duration)

        set_info.configure(text=(
            f"Recap:\n"
            f"Duration:   {duration:.1f}s\n"
            f"FPS:        {fps}\n"
            f"Resolution: {resolution}\n"
            f"Bitrate:    {bitrate_str}\n"
            f"Est. Size:  {estimated_mb:.1f} MB"
        ))
    except Exception:
        pass






if __name__ == "__main__":
    main()