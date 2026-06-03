# EzFlipBook

#### Description:

EzFlipBook is a small, light-weight app to convert image-sequences in .mp4 video file.
It accepts 4 different image formats (tif, jpg, tga and png) and allows the user to specify some basic settings like bitrate, fps and resolution.


## How to Use it

- Select the input image sequence (you just need to select a randome file from the correct sequence)
- Select the output folder and name
- Choose your export settings
- Press the Convert Button

## Parameters

### Input - Output

- **Input Sequence**: your image sequence. Accepted formats are: .tif , .jpg , .tga, .png.  
I recommend using **jpg** for smallest file size and **tif** for fastest conversion time, and avoid **png** due to longer preload time.
- **Output To**: destination folder and output file name. The resulting file will be an **mp4** using the default code **libx264**

### Settings
- **FPS**: Frames Per Seconds. It accepts values from 1 to 120.
- **Presets**: these are the standard **ffmpeg** presets, as per doc:
>Sets the time that FFMPEG will spend optimizing the compression. Note that this does not impact the quality of the video, only the size of the video file.
- **Bitrate**: video bitrate value. It accepts values from **500Kbps** to **50Mbps** (which should be way overkill in most of the cases)
- **Size**: the output resolution. It automatically detect the sequence original resolution.  
It accepts values from **144** to **7680**.  
**there's no real upscaling feature, so be mindful of your input resolution.*
- **Recap**: on the left side of the settings you have the info recap with the chosen settings, the duration of the output clip and its estimated size.

### Convert
- **Preview**: on the left side there's a "live" preview of the rendering, it updates each 25 frames.
- **Convert Button and Progress Bar**: on the right side, the button to launch the render, with the Elapsed and Remaining time info, along with the progress bar.


## Project Structure
- **project.py**: entry point of the app. Contains the `main` function, the UI theme constants (colors and borders), and the core logic functions: `parse_seq_name`, `calc_dur`, `calc_est_size`, `update_recap` and `on_input_selected`.
- **classes.py**: contains all the custom CTk widgets used in the UI: `Panel`, `PathField`, `FpsField`, `DropField`, `BitrateField` and `ResolutionField`.
- **converter.py**: handles the video conversion pipeline. Contains the `ConvertLogger` class for progress tracking, and the `convert` and `run_convert` functions that manage the ffmpeg conversion on a separate thread.
- **gui.py**: builds and lays out the entire user interface using the classes and functions defined in the other modules.

## Notes
While building the project I had a different structure in mind, with a utils.py file containing all the functions, but for submission requirements, I reformatted with some functions ready to test in the project.py main file. I also did a lot of testing with different sequence name formats and the regex seems pretty robust, handling different padding and special characters.

As for the libraries, MoviePy seemed a good choice to handle the video conversion with ffmpeg. For the GUI, I chose CustomTkinter because it seemed a pretty easy and basic UI library for beginners, but both choices ended up presenting two issues:

- The live preview and progress bar were a little tricky to set up because Tkinter is not thread-safe. The solution was to run the conversion on a separate thread using Python's `threading` library, and use `root.after()` to safely pass UI updates back to the main thread. Some more dynamic UI behavior could still be difficult to implement without switching to a more thread-friendly library like PyQt.
- The preload time with heavily compressed formats like .png becomes a little annoying with long sequences. This is apparently due to the fact that MoviePy reads all the metadata from all the sequence files before starting the conversion, and sadly this cannot be avoided.

## Future Improvements
For the previously mentioned issues, the best improvements would be to use different libraries to better address the dynamic aspects of the app and achieve some performance gains.

Besides that, I would probably add a crop feature and the possibility to add optional overlay text as a title.
