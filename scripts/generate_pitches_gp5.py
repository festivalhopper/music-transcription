"""Open output file in TuxGuitar - Export - Export Audio File

File Encoding: PCM_SIGNED
Custom soundbank: $INSTALL_DIR\TuxGuitar\share\soundfont\MagicSFver2.sf2
"""

import os
import re

from music_transcription.fileformat.guitar_pro.gp5_writer import write_gp5
from music_transcription.fileformat.guitar_pro.utils import beat, Measure, note, Track
from music_transcription.string_fret_detection import plausibility

TUNING = (64, 59, 55, 50, 45, 40)
N_FRETS = 24
MIN_PITCH = min(TUNING)
MAX_PITCH = max(TUNING) + N_FRETS


def create_measure():
    return [([], [])]


def get_string_fret_possibilities(pitch):
    for string, string_pitch in enumerate(TUNING):
        if pitch >= string_pitch and pitch <= string_pitch + N_FRETS:
            yield string, pitch - string_pitch


def generate_mono(filename='generated_mono.gp5'):
    tracks = [
        Track(
            "Electric Guitar",
            len(TUNING), TUNING + (-1,),
            1, 1, 2, N_FRETS, 0, (200, 55, 55, 0), 27
        ),
    ]
    measures = []
    beats = []
    for pitch in range(MIN_PITCH, MAX_PITCH + 1):
        for string, fret in get_string_fret_possibilities(pitch):
            print('pitch={}, string={}, fret={}'.format(pitch, string, fret))

            if len(measures) == 0:
                measures.append(Measure(4, 4, False, 0, 0, "", (0, 0, 0, 0), 0, 0, False, (2, 2, 2, 2), 0))
            else:
                measures.append(Measure(0, 0, False, 0, 0, "", (0, 0, 0, 0), 0, 0, False, (0, 0, 0, 0), 0))

            beats_measure = create_measure()
            beats_measure[0][0].append(beat([None] * 7, pause=True))

            notes = [None] * 7
            notes[string] = note(fret)
            beats_measure[0][0].append(beat(notes))

            beats_measure[0][0].append(beat([None] * 7, pause=True))
            beats_measure[0][0].append(beat([None] * 7, pause=True))
            beats.append(beats_measure)

    path_to_gp5_file = os.path.join(r'..\tmp', filename)
    write_gp5(measures, tracks, beats, outfile=path_to_gp5_file)


def generate_poly(chord_type, filename='generated_poly.gp5', n_measures_per_file=10000):
    gp5_ending_regex = re.compile(r'\.gp5$')

    files = []
    tracks, measures, beats = create_tracks_measures_beats()

    # chords with 2 pitches
    if chord_type == 2:
        for pitch_1 in range(MIN_PITCH, MAX_PITCH + 1):
            for pitch_2 in range(pitch_1 + 1, MAX_PITCH + 1):
                if pitch_1 != pitch_2:
                    possibilities = plausibility.get_all_fret_possibilities((pitch_1, pitch_2), tuning=TUNING, n_frets=N_FRETS)
                    if len(possibilities) > 0:
                        measure, beats_measure, printable_notes = create_measure_beats_measure_printable_notes(
                            len(measures), possibilities[0]
                        )
                        measures.append(measure)
                        beats.append(beats_measure)
                        print('pitch_1={}, pitch_2={}, notes={}'.format(
                            pitch_1, pitch_2, printable_notes
                        ))

                        if len(measures) >= n_measures_per_file:
                            if len(files) == 0:
                                current_filename = filename
                            else:
                                current_filename = gp5_ending_regex.sub('', filename) + '.' + str(len(files)) + '.gp5'
                            files.append((current_filename, measures, tracks, beats))
                            tracks, measures, beats = create_tracks_measures_beats()

    # chords with 3 pitches
    elif chord_type == 3:
        for pitch_1 in range(MIN_PITCH, MAX_PITCH + 1):
            for pitch_2 in range(pitch_1 + 1, MAX_PITCH + 1):
                for pitch_3 in range(pitch_2 + 1, MAX_PITCH + 1):
                    if pitch_1 != pitch_2 and pitch_1 != pitch_3 and pitch_2 != pitch_3:
                        possibilities = plausibility.get_all_fret_possibilities((pitch_1, pitch_2, pitch_3),
                                                                                tuning=TUNING, n_frets=N_FRETS)
                        if len(possibilities) > 0:
                            measure, beats_measure, printable_notes = create_measure_beats_measure_printable_notes(
                                len(measures), possibilities[0]
                            )
                            measures.append(measure)
                            beats.append(beats_measure)
                            print('pitch_1={}, pitch_2={}, pitch_3={}, notes={}'.format(
                                pitch_1, pitch_2, pitch_3, printable_notes
                            ))

                            if len(measures) >= n_measures_per_file:
                                if len(files) == 0:
                                    current_filename = filename
                                else:
                                    current_filename = gp5_ending_regex.sub('', filename) + '.' + str(len(files)) + '.gp5'
                                files.append((current_filename, measures, tracks, beats))
                                tracks, measures, beats = create_tracks_measures_beats()

    # chords with 4 pitches
    elif chord_type == 4:
        for pitch_1 in range(MIN_PITCH, MAX_PITCH + 1):
            for pitch_2 in range(pitch_1 + 1, MAX_PITCH + 1):
                for pitch_3 in range(pitch_2 + 1, MAX_PITCH + 1):
                    for pitch_4 in range(pitch_3 + 1, MAX_PITCH + 1):
                        if (pitch_1 != pitch_2 and pitch_1 != pitch_3 and pitch_1 != pitch_4
                            and pitch_2 != pitch_3 and pitch_2 != pitch_4
                            and pitch_3 != pitch_4):
                            possibilities = plausibility.get_all_fret_possibilities((pitch_1, pitch_2, pitch_3, pitch_4),
                                                                                    tuning=TUNING, n_frets=N_FRETS)
                            if len(possibilities) > 0:
                                measure, beats_measure, printable_notes = create_measure_beats_measure_printable_notes(
                                    len(measures), possibilities[0]
                                )
                                measures.append(measure)
                                beats.append(beats_measure)
                                print('pitch_1={}, pitch_2={}, pitch_3={}, pitch_4={}, notes={}'.format(
                                    pitch_1, pitch_2, pitch_3, pitch_4, printable_notes
                                ))

                                if len(measures) >= n_measures_per_file:
                                    if len(files) == 0:
                                        current_filename = filename
                                    else:
                                        current_filename = gp5_ending_regex.sub('', filename) + '.' + str(len(files)) + '.gp5'
                                    files.append((current_filename, measures, tracks, beats))
                                    tracks, measures, beats = create_tracks_measures_beats()

    if len(measures) > 0:
        if len(files) == 0:
            current_filename = filename
        else:
            current_filename = gp5_ending_regex.sub('', filename) + '.' + str(len(files)) + '.gp5'
        files.append((current_filename, measures, tracks, beats))

    for filename, measures, tracks, beats in files:
        path_to_gp5_file = os.path.join(r'..\tmp', filename)
        write_gp5(measures, tracks, beats, outfile=path_to_gp5_file)


def create_tracks_measures_beats():
    return [
        Track(
            "Electric Guitar",
            len(TUNING), TUNING + (-1,),
            1, 1, 2, N_FRETS, 0, (200, 55, 55, 0), 27
        ),
    ], [], []


def create_measure_beats_measure_printable_notes(len_measures, notes):
    if len_measures == 0:
        measure = Measure(4, 4, False, 0, 0, "", (0, 0, 0, 0), 0, 0, False, (2, 2, 2, 2), 0)
    else:
        measure = Measure(0, 0, False, 0, 0, "", (0, 0, 0, 0), 0, 0, False, (0, 0, 0, 0), 0)

    beats_measure = create_measure()
    beats_measure[0][0].append(beat([None] * 7, pause=True))

    # [0, 3, 2, -1, -1, -1] -> [note(0), note(3), note(2), None, None, None, None]
    notes = [None if fret == -1 else note(fret) for fret in notes]
    notes.append(None)

    beats_measure[0][0].append(beat(notes))

    beats_measure[0][0].append(beat([None] * 7, pause=True))
    beats_measure[0][0].append(beat([None] * 7, pause=True))

    return measure, beats_measure, [None if my_note is None else my_note.fret for my_note in notes]

generate_mono()
generate_poly(2, filename='generated_poly_2.gp5')
generate_poly(3, filename='generated_poly_3.gp5')
# generate_poly(4, filename='generated_poly_4.gp5')
# generate_poly(5, filename='generated_poly_5.gp5')
# generate_poly(6, filename='generated_poly_6.gp5')