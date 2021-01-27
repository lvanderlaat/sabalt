# Semi-Automatic Bass Lines Transcription

# Installation & settings

## Clone the repository

    $ git clone https://github.com/lvanderlaat/sabalt.git

## Conda environment

    $ conda create -n sabalt -c conda-forge spleeter
    $ cd sabalt
    $ conda activate sabalt
    (sabalt) $ pip install -e .

## SoX command line tool 

`sox` is a command line tool we use to get the bass an active up.

    $ brew install sox

## Audacity

Dowload [Audacity](https://www.audacityteam.org/download/mac/).

Change your audacity default settings in `Audacity > Preferences > Track > Spectrogram`:
* Frequency range between 70 and 220 Hz:
* Algorithm = Pitch (EAC)
* Window size: 4096

To check different frequency ranges do:
    (sabalt) $ ipython
    In [1]: import librosa
    In [2]: librosa.note_to_hz(['E2', 'E4'])

## Lilypond

Download and install [Lilypond](http://lilypond.org/download.html)

# Run

## Pre-process

We split the song in 4 tracks: bass, voice, drums and other using `spleeter`. Then we get an active up version of the bass.

    $ conda activate sabalt
    (sabalt) $ sabalt-pre-process [PATH TO AUDIO FILE] [PATH TO OUTPUT FOLDER]

## Manual label

* Load `bass_8ve.wav` in Audacity.

* In the track drop-down menu:
    * `Multi-view`
    * `Split Stereo to Mono`
* Close one of the channels
* Pick: 
    1. First the precise frequency in the spectrogram
    2. Then adjust the duration in the waveform
    3. Then hit command + b

Export the labels (`File > Export > Export Labels...`)

## Create notes labels

Once the notes are picked we transform the frequencies to musical notes (A-G):

    (sabalt) $ sabalt-pitches [PATH TO LABELS FILE]

## Check (with bass)

Load the labels file in Audacity, grab your bass and check. If something is wrong, correct the picking and run `sabalt-pitches` again.

## Export to Lilypond

In order to set the right note duration (quarter, eight, etc.) we need to know the exact tempo of the song (use the original record):

    (sabalt) $ ipython
    In [1]: y, sr = librosa.load(mp3_file)
    In [2]: librosa.beat.tempo(y=y, sr=sr)

Use this tempo and the labels file (`sabalt-pitches` output) to convert to musical notation:

    (sabalt) $ sabalt-score [PATH TO LABELS FILE] [TEMPO]

## Compile the score

    $ lilypond score.ly

This is not a perfect score, just a starting point, you'll have to check.
