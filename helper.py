from random import randint

from numpy import maximum 

from keys import keys

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



def find_key(avg_pixels):
    # reset keys_count
    keys_count = {}
    for key in keys.keys():
        keys_count[key] = 0
    # check if avg_pixel value when converted to musical note fits all key signature
    # if it fits given key signature, increment keys_count[key]
    for i in avg_pixels:
        freq = int(i)
        while freq >= 12:
            freq -= 12
        for key in keys_count.keys():
            if freq in keys[key][0]:
                keys_count[key] += 1
    # find key with highest count
    key =  max(keys_count, key=lambda k: keys_count[k])
    return key

def find_tempo(pixels):
    anger_value = 0
    for pixel in pixels:
        red = pixel[0]
        blue = pixel[1]
        green = pixel[2]
        # so if pixel is "angry"
        if red > (green+blue)/2:
            anger_value += red
        else:
            anger_value -= (green+blue)/2
    # Define the range of values to transform to.

    # below lines are generated through chatgpt
    if anger_value == 0:
        transformed_anger = 120
    elif anger_value < 0:
        # Normalize negative anger_value to the range of -255 to 0 for a single pixel.
        # For all pixels, it would be -255 * len(pixels) to 0.
        max_negative_anger = -255 * len(pixels)
        # Normalize and then linearly map it to the range 60-100.
        normalized_anger = (anger_value - max_negative_anger) / (-max_negative_anger) * 40 + 60
        # Find the closest value in the anger_range to the normalized_anger.
        transformed_anger = min([60, 70, 80, 90,100], key=lambda x: abs(x - normalized_anger))
    else:
        # Positive anger_value: Normalize to the range 0 to 255 for a single pixel.
        # For all pixels, it would be 0 to 255 * len(pixels).
        max_positive_anger = 255 * len(pixels)
        # Normalize and then linearly map it to the range 120-180.
        normalized_anger = (anger_value / max_positive_anger) * 60 + 120
        # Find the closest value in the anger_range to the normalized_anger.
        transformed_anger = min([120,130,140, 150,160, 170,180], key=lambda x: abs(x - normalized_anger))

    return transformed_anger


def calc_vol(rgb):
    """
    Convert an RGB value to a darkness score.

    Parameters:
    rgb (tuple): A tuple of (R, G, B) values (0-255).

    Returns:
    int: Darkness score (30-100), where 30 is the darkest and 100 is the lightest.
    """
    # Unpack the RGB values
    if len(rgb) == 4:
        r,g,b,a = rgb
    else:
        r, g, b = rgb

    # Calculate luminance in a way that accounts for human perception
    luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b

    # Normalize luminance to a scale of 30 (dark) to 100 (light)
    # Assuming the luminance range is 0 (black) to 255 (white)
    darkness_score = 100 - (luminance / 255 * 70)

    return round(darkness_score)




