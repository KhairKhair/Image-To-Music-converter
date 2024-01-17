from PIL import Image as I
from midiutil.MidiFile import *
from helper import round_dur, round_dur_chords, get_key
from random import randint

# written for 16x16 images
# image is broken up to 3 areas. 1 area is used to generate 1st set of chords.
# 2nd (middle area) is used to generate melody notes. # 3rd area is for 2nd set of chords.

start_chord1 = 0
end_chord1 = 4*16 
start_melody = 4*16
end_melody = 12*16
start_chord2 = 12*16
end_chord2 = 16*16

def generateMIDI(file_path, key, tempo):
    # writes midi file


    # get key signature functions
    key_note, key_chord= get_key(key)

    img = I.open(file_path)
    # full_img is not resized
    pixels = img.getdata()
    avg_pixels = []


    full_img = img
    img = img.resize((16,16))
    height,width = img.size


    # get avg value of r,g, and b values
    for i in pixels:
        avg_pixels.append((i[0] + i[1] + i[2])/3)


    # two channels, one for melody and one for chords
    midi = MIDIFile(2)
    time = 0
    midi.addTempo(0, time, tempo)
    midi.addTempo(1, time, tempo)
    midi.addTrackName(0,time, "Melody")
    midi.addTrackName(1,time, "Chord")

    channel = 0
    time = 0             # start on beat 0


    durations = []
    time_stamps = []

    for i in range(0,end_chord1):
        # a is the difference between the current pixel and the pixel next to it
        a = abs(avg_pixels[i] - avg_pixels[i+1])
        if a > 255:
           a = 255
        elif a < -255:
           a = -255

        # from a, get duration of chord
        dur = round_dur_chords(abs(a))


        # get note in key signature
        note = key_note(int(avg_pixels[i]))

        # add each chord note 
        for chord_note in key_chord(note):
            midi.addNote(1, channel, chord_note+60-12, time, dur, 0)

       # time_stamps used to keep track of when chords are played
       # so that sync with melody notes is possible
        time_stamps.append(time)
        time += dur

    for i in range(start_chord2,end_chord2):
       a = abs(avg_pixels[i] - avg_pixels[i+1])
       if a > 255:
           a = 255
       elif a < -255:
           a = -255


       note = key_note(int(avg_pixels[i]))
       dur = round_dur_chords(abs(a))
       for chord_note in key_chord(note):
           midi.addNote(1, channel, chord_note+60-12, time, dur, 0)



       # time_stamps used to keep track of when chords are played
       # so that sync with melody notes is possible
       time_stamps.append(time)
       time += dur


    time = 0
    for i in range(start_melody, end_melody):
        # generating melody notes

        # a is the difference between the current pixel and the average of the square it is in
        a = avg_pixels[i] - 0.125*(avg_pixels[i+1]+avg_pixels[i-1]+
                                   avg_pixels[i+width]+avg_pixels[i+width-1]+avg_pixels[i+width+1]+
                                   avg_pixels[i-width]+avg_pixels[i-width-1]+avg_pixels[i-width+1])
        if a > 255:
            a = 255
        elif a < -255:
            a = -255


        note = key_note(int(avg_pixels[i]))
        dur = round_dur(abs(a))
        midi.addNote(0, channel, note, time, dur, randint(80,100))
        durations.append(dur)
        time += dur


    with open("pic.mid", "wb") as output_file:
        midi.writeFile(output_file)

    return img, full_img, durations
