# Python Standard Library
from fractions import Fraction, gcd
from numbers import Number
import re
import six

# Other dependencies
import librosa
import numpy as np
import pandas as pd


def clean(onst_file, tie):
    """



    Parameters
    ----------

    Returns
    -------

    """
    notes = list(np.loadtxt(onst_file, skiprows=1, delimiter=','))

    fixed = []
    for i in range(len(notes) - 1):
        # Take current note
        curr = notes[i]

        # Duration is 0
        if curr[2] == 0:
            continue

        # Take next note
        next = notes[i+1]

        j = 0
        # If silence is too short and same note (frequency), tie both notes
        # TODO change These numbers that are hardcoded
        # This could tie notes that are fast same notes...
        if tie:
            while next[1] - curr[1] - curr[2] < 2 and (next[0] - curr[0]) < 5:
                curr[2] = next[1] + next[2] - curr[1]
                next[2] = 0
                j += 1
                next = notes[i + j]

        fixed.append(curr)

    fixed.append(notes[-1])

    df = pd.DataFrame(fixed, columns=['freq', 'start', 'duration'])
    return df


def lily_pitch(note):
    """



    Parameters
    ----------

    Returns
    -------

    """
    if not isinstance(note, six.string_types):
        return np.array([lily_pitch(n) for n in note])

    if note == 'r':
        return note

    acc_map  = {'#': 's', '': '', 'b': 'f', '♯': 's'}
    oct_map  = {
        '': '',
        '0': ',,',
        '1': ',',
        '2': '',
        '3': '\'',
        '4': '\'\'',
        '5': '\'\'\'',
        '6': '\'\'\'\n'
    }
    match = re.match(r'^(?P<note>[A-Ga-g])'
                     r'(?P<accidental>[#b!♯]*)'
                     r'(?P<octave>[+-]?\d+)?',
                     note)

    pitch      = match.group('note').lower()
    accidental = acc_map[match.group('accidental')]
    octave     = oct_map[match.group('octave')]

    lily = pitch + accidental + octave

    return lily


def lily_duration(bpm, beat, subdivision, duration, pitch):
    def get_divisors(n):
        return [d for d in range(2, n+1) if n%d == 0]


    def check_composition(fraction, components):
        if fraction.numerator == 1:
            components.append(fraction)
            return

        else:
            for divisor in sorted(get_divisors(fraction.denominator), reverse=True):
                if fraction.numerator > divisor:
                    f1 = Fraction(divisor/fraction.denominator)
                    components.append(f1)
                    f2 = Fraction(fraction - f1)
                    return check_composition(f2, components)


    # Process
    bps = bpm/60
    whole_duration = beat/bps

    fraction = Fraction(
        int(round(subdivision*duration/whole_duration, 2)) / subdivision
    )

    components = []
    check_composition(fraction, components)

    if len(components) == 0:
        components = [Fraction(1/subdivision)]

    denominator = components[0].denominator

    notation = pitch + str(denominator)

    for component in components[1:]:
        if component.denominator == denominator*2:
            notation += '.'
        else:
            notation += f'~ {pitch}{component.denominator}'
        denominator = component.denominator

    return notation


def lily_notation(bpm, beat, subdivision, duration, pitch):
    if not isinstance(duration, Number):
        notation = [
            lily_duration(bpm, beat, subdivision, d, p)
            for d, p in zip(duration, pitch)
        ]
    else:
        notation, last_denominator = lily_duration(bpm, beat, subdivision,
                                                   duration, pitch)
    return notation


def _get_notes(df, bpm, beat, subdivision):
    """



    Parameters
    ----------

    Returns
    -------

    """
    df.onset      /= 100
    df.freq       /= 2
    df['duration'] = abs(df.start.diff(periods=-1))
    df.at[len(df)-1, 'duration'] = 4*bpm/60 # Fix last unbounded duration
    df['pitch']    = librosa.hz_to_note(df.freq)
    df['notation'] = lily_notation(bpm, beat, subdivision, df.duration,
                                   lily_pitch(df.pitch))
    return df

def get_notes(df, bpm, beat, subdivision):
    """



    Parameters
    ----------

    Returns
    -------

    """
    df['duration'] = abs(df.onset.diff(periods=-1))
    df.at[len(df)-1, 'duration'] = 4*bpm/60      # Fix last unbounded duration
    df['notation'] = lily_notation(bpm, beat, subdivision, df.duration,
                                   lily_pitch(df.pitch))
    return df


if __name__ == '__main__':
    duration = lily_duration(112.35, 4, 32, 0.19, 'f')
    print(duration); exit()
