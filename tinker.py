import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import pygame
from createMIDI import generateMIDI
from playMIDI import show_pic2,play_midi,stop_playing

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
		root.geometry("600x600")
		play_button.config(state=tk.NORMAL)
		image = Image.open(file_path)
		# resizing the image to 300x300  for display purposes
		if image.size[0] > 300 or image.size[1] > 300:
			image = image.resize((300,300))
		photo = ImageTk.PhotoImage(image)
		# show the image on root instance
		label_img.config(image=photo)
		label_img.image = photo

def start_playing():
	# play music and open visualizer
	stop_button.config(state=tk.NORMAL)
	play_button.config(state=tk.DISABLED)


	# get key signature chosen by user
	key = key_var.get()
	# generates and save MIDI file and returns 16x16 image, full image and list containting duration of melody notes
	tempo = scale.get()
	img, full_img, durations = generateMIDI(file_path, key, tempo)
	# MidiFile saved as following
	midi_name = "pic.mid"
	# setup and play midi file through pygame
	play_midi(midi_name)
	# show visualizer using matplotlib
	show_pic2(root,img, full_img, durations, tempo)
	stop_button.config(state=tk.DISABLED)
	play_button.config(state=tk.NORMAL)




def on_scale_change(value):
    # Convert the value to an integer
    int_value = int(float(value))

    # Snap the value to the nearest multiple of 60
    snapped_value = round(int_value / 60) * 60

    # Update the scale's value
    scale.set(snapped_value)

# Create the main window
#def create(first = True):
#	global root
#	global key_var
#	global label_img
#	global play_button
#	global stop_button
#	global scale
#
#	root = tk.Tk()
#	root.title("Image To Music Converter")
#	root.geometry("600x600")
#
#	# Create and set up GUI components
#	label_img = tk.Label(root, text="Selected Image will appear here")
#	label_img.pack()
#
#	# used to upload image
#	image_button = tk.Button(root, text="Open Image File", command=open_file)
#	image_button.pack()
#
#	# used to start playing music and visualizer
#	play_button = tk.Button(root, text="Start Playing", command=start_playing, state=tk.DISABLED)
#	play_button.pack()
#	play_button.place(x=50,y=100)
#
#	stop_button = tk.Button(root, text="Stop Playing", command=stop_playing, state=tk.DISABLED)
#	stop_button.place(x=450,y=100)
#
#
#
#	# allows user to choose key signature
#	key_var = tk.StringVar()
#	# C Major set as default key signature
#	key_var.set("C_Major")
#	key_menu = tk.OptionMenu(root, key_var, "C_Major", "C_Minor")
#	key_menu.pack()
#
#	scale = tk.Scale(root, from_=60, to=360, orient='horizontal', command=on_scale_change)
#
#	# Set the tick interval to 1 so that each integer value has a label
#	scale.config(tickinterval=60, length = 200)
#
#	scale.pack()
#
#
#	#used to quit program
#	process_button = tk.Button(root, text="Quit Program", command=quit)
#	process_button.pack(pady=10)
#
#
#	# warning on how to exit
#	label_warn = tk.Label(root, text="If you have started playing the music and want to exit,\n \
#	 simply close the window with the two pictures", font=("Helvetica", 15))
#	label_warn.pack(padx=20)
#
#	label_warn.pack(padx=20)
#
#	# this line is very important - without it the pixel highlighting and the melody notes will not be in sync
#	# This line is also the reason why the user must close the program after every use
#	# Start the Tkinter main loop
#	root.mainloop()



def create(first=True):
    global root, key_var, label_img, play_button, stop_button, scale

    root = tk.Tk()
    root.title("Image To Music Converter")
    root.geometry("600x300")


    # Create and set up GUI components using grid
    label_img = tk.Label(root, text="Selected Image will appear here")
    label_img.grid(row=0, column=0, columnspan=3, padx=10, pady=5)

    # Buttons
    image_button = tk.Button(root, text="Open Image File", command=open_file)
    image_button.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

    play_button = tk.Button(root, text="Start Playing", command=start_playing, state=tk.DISABLED)
    play_button.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    stop_button = tk.Button(root, text="Stop Playing", command=stop_playing, state=tk.DISABLED)
    stop_button.grid(row=1, column=2, padx=10, pady=5, sticky="ew")

    # Key Signature Menu
    key_var = tk.StringVar(value="C_Major")
    key_menu = tk.OptionMenu(root, key_var, "C_Major", "C_Minor")
    key_menu.grid(row=2, column=0, columnspan=1, padx=10, pady=10, sticky="ew")

    # Scale for selecting values
    scale = tk.Scale(root, from_=60, to=360, orient='horizontal', command=on_scale_change, tickinterval=60, length=300)
    scale.grid(row=2, column=1, columnspan=2, padx=10, pady=5)

    # Quit Button
    process_button = tk.Button(root, text="Quit Program", command=quit)
    process_button.grid(row=3, column=0, columnspan=3, padx=10, pady=5, sticky="ew")


    # Configure grid rows and columns
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=1)
    root.grid_rowconfigure(3, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)

    root.mainloop()

plt.show()
create()