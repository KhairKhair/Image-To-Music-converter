from createMIDI import start_melody, end_melody
import pygame
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import tkinter as tk
import pretty_midi
import pygame


def play_midi(midi_file, melody_instrument, harmony_instrument):

    # Load MIDI file
    midi_data = pretty_midi.PrettyMIDI(midi_file)

    # Check if the MIDI file has enough tracks
    if len(midi_data.instruments) >= 2:
        # Assign the melody instrument to the first track
        midi_data.instruments[0].program = melody_instrument

        # Assign the harmony instrument to the second track
        midi_data.instruments[1].program = harmony_instrument

    # Save the modified MIDI file
    modified_midi_file = "modified_midi.mid"
    midi_data.write(modified_midi_file)

    # Initialize pygame mixer
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(modified_midi_file)
    pygame.mixer.music.play()


def stop_playing():
    global playing
    playing = False
playing = True

import numpy as np
import time
import matplotlib.pyplot as plt

# Global variable to control the play/stop status
playing = True

def show_pic2(root, img, full_img, durations, tempo, play_button, stop_button):
    global playing
    playing = True

    tempo_scalar = 60/tempo
    # Convert PIL Images to numpy arrays for manipulation
    img_array = np.array(img)
    full_img_array = np.array(full_img)

    # Get height and width of img
    height, width = img_array.shape[:2]

    # Create a figure to display the images
    fig, (ax1, ax2) = plt.subplots(2, 1)

    # Function to handle the closing of the window
    def on_close(event):
        global playing
        playing = False
    fig.canvas.mpl_connect('close_event', on_close)

    # Set up initial display of images
    img_display = ax1.imshow(img_array)
    ax1.set_title("16x16 image")
    ax2.imshow(full_img_array)
    ax2.set_title("Full image")

    for i in range(start_melody, end_melody):
        a = time.time()
        if not playing:
            stop_button.config(state=tk.DISABLED)
            play_button.config(state=tk.NORMAL)
            pygame.mixer.music.stop()
            plt.close()
            return

        note_value = durations[0]
        durations = durations[1:]

        # Highlight pixel
        x = i % width
        y = i // width
        original_color = img_array[y, x].copy()  # Save original color
        img_array[y, x] = [255, 255, 255]  # Change color to white for highlight

        img_display.set_data(img_array)
        plt.draw()
        plt.pause((note_value*tempo_scalar)-0.003)

        # Wait for the duration of the note

        # Revert pixel to original color
        img_array[y, x] = original_color
        img_display.set_data(img_array)
        plt.draw()
        print(time.time()-a)




