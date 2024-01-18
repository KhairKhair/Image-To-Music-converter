
## Image to Music Converter

This program converts images into music by interpreting pixel colors as musical notes and chords. It features a visualizer that highlights the progression of the melody in sync with the music.

### Installing Libraries

Before running the program, ensure you have the following libraries installed. Use `pip` or `pip3` depending on your Python installation:

1. `pip install tk` - For the graphical user interface.
2. `pip install pretty_midi` - Allows MIDI files to be played with various instrument sounds.
3. `pip install matplotlib` - For data visualization.
4. `pip install pygame` - Used for sound playback and additional functionality.
5. `pip install midiutil` - For MIDI file creation and manipulation.
6. `pip install pillow` - For image processing.

### Instructions for Use

1. Run `tinker.py`.
2. In the Tkinter window, upload an image.
3. Choose the tempo and key signature, or use the 'Set Tempo' and 'Set Key Signature' buttons for automatic settings.
4. Select the instrument for the melody and harmony parts.
5. Click 'Play Music' to start the playback.
6. Use the 'Stop Playing' button to stop the music and close the matplotlib window.

### How It Works

- The uploaded image is resized to 16x16 pixels. The first and last 4 rows are used to generate continuous chords, while the middle 8 rows are used for the melody.
- The visualizer window (matplotlib) turns a pixel white when the corresponding melody note is played.
- The music and visualizer window close automatically after the melody finishes playing. Note that the complete MIDI file may include some chords beyond the last melody note.
- A note is determined by the average RGB values of a pixel, rounded to the nearest note in the selected key signature. Chords are similarly generated based on the average RGB values.
- The tempo is set automatically based on the overall "redness" of the image: the redder the image, the faster the tempo.
- The key signature is determined by finding which key has the highest number of pixel-generated notes fitting its scale without rounding.
