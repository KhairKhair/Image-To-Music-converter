import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import pygame
from createMIDI import generateMIDI
from playMIDI import show_pic2,play_midi,stop_playing
from helper import gm, find_key, find_tempo

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt


file_path = None
def open_file():
# chooes and open the image file
    global file_path
    f_types = [('Jpg Files', '*.jpg'),('PNG Files','*.png'), ('jpeg Files', '*.jpeg')]    
    file_path = filedialog.askopenfilename(title="Select Image",filetypes=f_types)
    if file_path:
        play_button.config(state=tk.NORMAL)
        setScale_button.config(state=tk.NORMAL)
        setTempo_button.config(state=tk.NORMAL)
        image = Image.open(file_path)
        # resizing the image to 300x300  for display purposes
        if image.size[0] > 300 or image.size[1] > 300:
            image = image.resize((300,100))
        photo = ImageTk.PhotoImage(image)
        # show the image on root instance
        label_img.config(image=photo)
        label_img.image = photo
    else:
        print("Didn't work")




def start_playing():
    # play music and open visualizer
    stop_button.config(state=tk.NORMAL)
    play_button.config(state=tk.DISABLED)


    # get key signature chosen by user
    key = key_var.get()
    # generates and save MIDI file and returns 16x16 image, full image and list containting duration of melody notes
    tempo = scale.get()
    sync = scale_sync.get()
    img, full_img, durations, sync_index = generateMIDI(file_path, key, tempo, sync)
    # MidiFile saved as following
    midi_name = "pic.mid"
    # setup and play midi file through pygame

    play_midi(midi_name, gm[melodyInstru_var.get()], gm[harmonyInstru_var.get()])
    # show visualizer using matplotlib
    show_pic2(root,img, full_img, durations, tempo, play_button, stop_button, sync_index)
    stop_button.config(state=tk.DISABLED)
    play_button.config(state=tk.NORMAL)

    pygame.mixer.music.stop()
    plt.close()

def set_scale():
    image = Image.open(file_path)
    image = image.resize((16,16))
    pixels = image.getdata()
    avg_pixels = []

    # get avg value of r,g, and b values
    for i in pixels:
        avg_pixels.append((i[0] + i[1] + i[2])/3)

    key_var.set(find_key(avg_pixels))

def set_tempo():
    image = Image.open(file_path)
    img2 = image.resize((50,50)).getdata()
    image = image.resize((16,16))
    pixels = image.getdata()

    scale.set(find_tempo(pixels))




def on_scale_change(value):
    # Convert the value to an integer
    int_value = int(float(value))

    # Snap the value to the nearest multiple of 60
    snapped_value = round(int_value/10) * 10

    # Update the scale's value
    scale.set(snapped_value)


def on_scaleSync_change(value):
    label_sync.config(text=("Snyc melody and chords\n every " + str(value) +" beat"))


def create(first=True):
    global root, key_var, label_img, play_button, stop_button, scale
    global melodyInstru_var, harmonyInstru_var, setScale_button, setTempo_button
    global label_sync,scale_sync

    root = tk.Tk()
    root.title("Image To Music Converter")
    root.geometry("800x400")


    # Create and set up GUI components using grid
    label_img = tk.Label(root, text="Selected Image will appear here")
    label_img.grid(row=1, column=3, columnspan=1, padx=5, pady=5)

    # Buttons
    image_button = tk.Button(root, text="Open Image File", command=open_file)
    image_button.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

    play_button = tk.Button(root, text="Start Playing", command=start_playing, state=tk.DISABLED)
    play_button.grid(row=1, column=1, padx=0, pady=0, sticky="ew")

    stop_button = tk.Button(root, text="Stop Playing", command=stop_playing, state=tk.DISABLED)
    stop_button.grid(row=1, column=2, padx=0, pady=0, sticky="ew")

    # Key Signature Menu
    label_scale = tk.Label(root, text="Key Signature: ", font=("Helvetica", 15))
    label_scale.grid(row=2,column=0)
    key_var = tk.StringVar(value="C_Major")
    key_menu = tk.OptionMenu(root, key_var, "C_Major", "C_Minor", "C_Sharp_Major", "C_Sharp_Minor", 
        "D_Major", "D_Minor", "D_Sharp_Major", "D_Sharp_Minor", 
        "E_Major", "E_Minor", "F_Major", "F_Minor", 
        "F_Sharp_Major", "F_Sharp_Minor", "G_Major", "G_Minor", 
        "G_Sharp_Major", "G_Sharp_Minor", "A_Major", "A_Minor", 
        "A_Sharp_Major", "A_Sharp_Minor", "B_Major", "B_Minor")

    key_menu.grid(row=2, column=1, columnspan=1, padx=0, pady=0, sticky="ew")

    # Scale for selecting values
    label_scale = tk.Label(root, text="Tempo (bpm): ", font=("Helvetica", 15))
    label_scale.grid(row=2,column=2)
    scale = tk.Scale(root, from_=60, to=180, orient='horizontal', command=on_scale_change, tickinterval=10, length=350)
    scale.grid(row=2, column=3, columnspan=1, padx=0, pady=0)

    setScale_button = tk.Button(root, text="Set Key Signature \n (Based on Given Image)", command=set_scale, state=tk.DISABLED)
    setScale_button.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

    setTempo_button = tk.Button(root, text="Set Tempo \n (Based on Given Image)", command=set_tempo, state=tk.DISABLED)
    setTempo_button.grid(row=3, column=1, padx=0, pady=5, sticky="ew")



    # slider to control sync of melody and harmony
    scale_sync = tk.Scale(root, from_=0, to=24, orient='horizontal', command=on_scaleSync_change, tickinterval=2, length=300)
    scale_sync.grid(row=3, column=3, columnspan=1, padx=0, pady=0)

    label_sync = tk.Label(root, text=("Snyc melody and chords\n every " + str(scale_sync.get()) +" beat(s)" ), font=("Helvetica", 13))
    label_sync.grid(row=3, column=2)




    label_scale = tk.Label(root, text="Melody Instrument: ", font=("Helvetica", 15))
    label_scale.grid(row=4,column=0)
    melodyInstru_var = tk.StringVar(value="Piano")
    melody_menu = tk.OptionMenu(root, melodyInstru_var, "Piano", "Violin", "Harpsichord", "Organ", "Guitar",\
            "Violin","Harp","String_Ensemble","Choir", "French_Horn", "Oboe", "Flute", "Melodic_Tom")
    melody_menu.grid(row=4, column=1, columnspan=1, padx=0, pady=0, sticky="ew")

    label_scale = tk.Label(root, text="  Harmony Instrument:  ", font=("Helvetica", 15))
    label_scale.grid(row=4,column=2, padx = 10)
    harmonyInstru_var = tk.StringVar(value="Piano")
    harmony_menu = tk.OptionMenu(root, harmonyInstru_var, "Piano", "Violin", "Harpsichord", "Organ", "Guitar",\
            "Violin","Harp","String_Ensemble","Choir", "French_Horn", "Oboe", "Flute", "Melodic_Tom")

    harmony_menu.grid(row=4, column=3, columnspan=1, sticky="ew")





    # Quit Button
    process_button = tk.Button(root, text="Quit Program", command=quit)
    process_button.grid(row=5, column=0, columnspan=4, padx=0, pady=0, sticky="ew")

    label_warn = tk.Label(root, text="Please only press Stop Playing to stop music and to close pixel visualizer window")
    label_warn.grid(row=6, column=0, columnspan=4, padx=5, pady=5)



    # Configure grid rows and columns
    root.grid_rowconfigure(2, weight=1)
    root.grid_rowconfigure(3, weight=1)
    root.grid_rowconfigure(4, weight=1)
    root.grid_rowconfigure(5, weight=1)
    root.grid_rowconfigure(6, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)
    root.grid_columnconfigure(3, weight=1)

    # tkinter main loop
    root.mainloop()

plt.show()
create()