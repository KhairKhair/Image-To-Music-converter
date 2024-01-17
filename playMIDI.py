from createMIDI import start_melody, end_melody
import pygame
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

def play_midi(midi_file):
    # set up midi player in pygame
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(midi_file)
    # play pygame music
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

def show_pic2(root, img, full_img, durations, tempo):
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
        pygame.mixer.music.stop()
    fig.canvas.mpl_connect('close_event', on_close)

    # Set up initial display of images
    img_display = ax1.imshow(img_array)
    ax1.set_title("16x16 image")
    ax2.imshow(full_img_array)
    ax2.set_title("Full image")

    for i in range(start_melody, end_melody):
        a = time.time()
        if not playing:
            break

        note_value = durations[0]
        durations = durations[1:]

        # Highlight pixel
        x = i % width
        y = i // width
        original_color = img_array[y, x].copy()  # Save original color
        img_array[y, x] = [255, 255, 255]  # Change color to white for highlight

        img_display.set_data(img_array)
        plt.draw()
        plt.pause((note_value*tempo_scalar)-0.002)

        # Wait for the duration of the note

        # Revert pixel to original color
        img_array[y, x] = original_color
        img_display.set_data(img_array)
        plt.draw()
        print(a-time.time())

    pygame.mixer.music.stop()
    plt.close(fig)



