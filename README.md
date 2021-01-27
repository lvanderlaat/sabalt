# Installation & settings

## Conda environment

    $ conda create -n sabalt -c conda-forge spleeter
    $ conda activate sabalt
    (sabalt) $ pip install -e .

## SoX command line tool 

    $ brew install sox

## Audacity

Dowload [Audacity](https://www.audacityteam.org/download/mac/).

Change your audacity default settings in `Audacity > Preferences > Track > Spectrogram`:
* Frequency range (use one octave up). open low E is `E1`:

    (sabalt) $ ipython
    In [1]: import librosa
    In [2]: librosa.note_to_hz(['E2', 'E4'])

* Algorithm = Pitch (EAC)
* Window size: 4096

# Run

## Pre-process

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

    (sabalt) $ sabalt-pitches [PATH TO LABELS FILE]

## Check (with bass)

Load the labels file in Audacity, grab your bass and check. If something is wrong, correct the picking and run `sabalt-pitches` again.

## Export to Lilypond

First get the exact tempo of the song:

    (sabalt) $ ipython
    In [1]: y, sr = librosa.load(mp3_file)
    In [2]: librosa.beat.tempo(y=y, sr=sr)

Use this tempo to convert to musical notation:

    (sabalt) $ sabalt-score [PATH TO LABELS FILE] [TEMPO]
