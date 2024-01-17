from random import randint 
# notes is a list of lists of octaves. It is used to check if a note is C or C-sharp or ...
notes = []
for i in range(12):
	note = [(i + 12*j) for j in range(0,11)]
	notes.append(note)


def C_MAJ(freq):
	# notes which are not in C_MAJ
	not_scale = [1,3,6,8,10]
	# set melody range to be 60-84 so that it can be heard of chords - which are lower
	while (freq > 84):
		freq -= 12
	while (freq < 60):
		freq += 12

	# Approximate note to nearest note in C_MAJ
	for i in not_scale:
		if freq in notes[i]:
			return freq-1
	return freq
# dictionary containing note as key and its C_MAJ chord as value
CMAJ_chords = {0:[0,4,7], 2:[2,5,8], 4:[4,7,11], 5:[5,9,12], 7:[7,11,14],9:[9,12,16], 11:[11,14,17]}

def CMAJ_chord(freq):
	# freq is reduced down to under 13 so that dictionary can remain small in size
	# which octave the original freq note belonged to is not relevant since
	# all chord notes are chosen to be in a specefic range
	while freq>=12:
		freq -= 12
	return CMAJ_chords[freq]


# same as C_MAJ
def C_MIN(freq):
	not_scale = [1,4,6,9,11]
	while (freq > 84):
		freq -= 12
	while (freq < 60):
		freq += 12

	for i in not_scale:
		if freq in notes[i]:
			return freq-1
	return freq

CMIN_chords = {0:[0,3,7], 2:[2,5,8], 3:[3,7,10], 5:[5,8,12], 7:[7,10,14],8:[8,12,15], 10:[10,14,17]}
def CMIN_chord(freq):
	while freq>= 12:
		freq -= 12
	return CMIN_chords[freq]

def C_PENTA(freq):
	# pentatonic c scale is in code but not used
	not_scale = [1,3,5,6,8,10,11]
	while (freq > 84):
		freq -= 12
	while (freq < 48):
		freq += 12
	for i in not_scale:
		if freq in notes[i]:
			if i == 6 or i == 11:
				return freq-2
			elif i == 7:
				return freq-3
			else:
				return freq-1
	return freq


def get_key(key):
	# return functions to approximate notes in chosen key_signature
	if key == "C_Major":
		key_note = C_MAJ
		key_chord = CMAJ_chord
	elif key == "C_Minor":
		key_note = C_MIN
		key_chord = CMIN_chord
	elif key == "C_Pentatonic":
		key_note = C_PENTA
		key_chord = CMAJ_chord
	return key_note, key_chord



def round_dur_chords(dur):
	# for each range of values, return a duration
	# chords are chosen to be longer and have less variation that melody notes
	if 0 <= dur and dur <= 100:
		return 2
		return 1.25
	elif 100 < dur and dur <= 200:
		return 1.5
	elif 200 < dur and dur <= 255:
		return 1 


def round_dur(dur):
	# return duration of melody note based on its "dur" value
	if 0 <= dur and dur <= 6.25:
		return 2
	elif 6.25 < dur and dur <12.5:
		return 1.75
	elif 12.5 < dur and dur <= 25:
		return 1.5
	elif 25 < dur and dur  < 37.5:
		return 1.25
	elif 37.5 < dur and dur <= 50:
		return 1.25
	elif 50 < dur and dur <= 72.5:
		return 1
	elif 72.5 < dur and dur <= 85:
		return 0.75
	elif 85 < dur and dur <= 97.5:
		return 0.5
	elif 97.5 < dur and dur <= 110:
		return 0.25
	else:
		return 0.125


# dictionary containing instrument as key and its value as the general midi instrument
gm = {
    "Piano": 0,
    "Harpsichord": 6,
    "Organ": 19,
    "Guitar": 24,
    "Violin": 40,
    "Harp": 46,
    "String_Ensemble": 48,
    "Choir": 52,
    "French_Horn": 60,
    "Oboe": 68,
    "Flute": 73,
    "Melodic_Tom": 117,
}



