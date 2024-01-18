# notes is a list of lists of octaves. It is used to check if a note is C or C-sharp or ...
notes = []
for i in range(12):
    note = [(i + 12*j) for j in range(0,11)]
    notes.append(note)

# create all chords types for all notes
chords_major = {}
chords_minor = {}
chords_dim = {}
for i in range(12):
    chords_major[i] = [i, i+4, i+7]
    chords_minor[i] = [i, i+3,i+7]
    chords_dim[i] = [i, i+3, i+6]

# construct set chords for a given major key
def construct_chords_major(key):
    chords = {} 
    scale = [key, key+2, key+4,key+5,key+7,key+9,key+11]
    for i in range(len(scale)):
        while scale[i] >= 12:
            scale[i] = scale[i]-12

    for note in scale:
        # first, fourth, fifth degree are major chords
        if note == key or note == key+5 or note == key+7:
            chords[note] = chords_major[note]
        # second, third, sixth degree are minor chords
        elif note == key+2 or note == key+4 or note == key+9:
            chords[note] = chords_minor[note]
        else:
        # 7th degree is dim chord
            chords[note] = chords_dim[note]
    return chords

# construct set chords for a given minor key
def construct_chords_minor(key):
    chords = {} 
    scale = [key, key+2, key+3,key+5,key+7,key+8,key+10]
    for i in range(len(scale)):
        while scale[i] >= 12:
            scale[i] = scale[i]-12
    for note in scale:
        # first, fourth, fifth degree are minor chords
        if note == key or note == key+5 or note == key+7:
            chords[note] = chords_minor[note]
        # third, sixth, seventh degree are major chords
        elif note == key+3 or note == key+8 or note == key+10:
            chords[note] = chords_major[note]
        # 2nd degree is dim chord
        else:
            chords[note] = chords_dim[note]
    return chords

# return scale (list of notes in scale) and not scale (list of notes not in scale) for given minor key
def construct_notScale_major(key):
    scale = [key, key+2, key+4,key+5,key+7,key+9,key+11]
    for i in range(len(scale)):
        while scale[i] >= 12:
            scale[i] -= 12 
    not_scale = []
    for i in range(12):
        if i not in scale:
            not_scale.append(i)
    return scale,not_scale

# return scale (list of notes in scale) and not scale (list of notes not in scale) for given major key
def construct_notScale_minor(key):
    scale = [key, key+2, key+3,key+5,key+7,key+8,key+10]
    for i in range(len(scale)):
        while scale[i] >= 12:
            scale[i] -= 12 
    not_scale = []
    for i in range(12):
        if i not in scale:
            not_scale.append(i)
    return scale,not_scale

# dictionary of all key signatures as keys
keys = {
    "C_Major":[],
    "C_Minor":[],
    "C_Sharp_Major":[],
    "C_Sharp_Minor":[],
    "D_Major":[],
    "D_Minor":[],
    "D_Sharp_Major":[],
    "D_Sharp_Minor":[],
    "E_Major":[],
    "E_Minor":[],
    "F_Major":[],
    "F_Minor":[],
    "F_Sharp_Major":[],
    "F_Sharp_Minor":[],
    "G_Major":[],
    "G_Minor":[],
    "G_Sharp_Major":[],
    "G_Sharp_Minor":[],
    "A_Major":[],
    "A_Minor":[],
    "A_Sharp_Major":[],
    "A_Sharp_Minor":[],
    "B_Major":[],
    "B_Minor":[]
}

# create values for the key signatures
key_it = 0
for key in keys:
    if "Major" in key:
        scale,not_scale = (construct_notScale_major(key_it))
        # append to the empty list: scale, not_scale, and dictionary of chords
        keys[key].append(scale)
        keys[key].append(not_scale)
        keys[key].append(construct_chords_major(key_it))
        # key_it not iterated here because there is still minor key of the same note
    if "Minor" in key:
        scale,not_scale = (construct_notScale_minor(key_it))
        keys[key].append(scale)
        keys[key].append(not_scale)
        keys[key].append(construct_chords_minor(key_it))
        # now iterated becaues next key siganture is different key
        key_it += 1


def round_to_key(freq, key):
    # reduced_note allows us to compare given freq with items in list scale
    reduced_note = freq
    while reduced_note >= 12:
        reduced_note -= 12

    scale = keys[key][0]

    # Find the closest note in the scale to the given frequency
    closest_note = min(scale, key=lambda note: abs(note - reduced_note))


    # set melody range to be 60-84 so that it can be heard of chords - which are lower
    while (closest_note > 84):
        closest_note -= 12
    while (closest_note < 60):
        closest_note += 12

    return closest_note


def key_note(freq, key_name):
    # return value of note in given key
    return round_to_key(freq, key_name)

def key_chord(freq, key_name):
    while freq >= 12:
        freq -= 12
    # return list of chords construced from key and note
    return keys[key_name][2][freq]

