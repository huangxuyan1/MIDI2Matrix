import math

import mido
import os
import MIDIHandler

import numpy
import numpy as np

input_path_ = r'/Users/alvin/Downloads/MIDI Chord Dataset'
output_path_ = r'/Users/alvin/PycharmProjects/VAE-GAN Chords/dataset.npy'

def get_appropriate_note_range(note_range):
    """Change the note range to the nearest octave"""
    lowest_note = int(note_range[0] / 12) * 12
    highest_note = math.ceil(note_range[1] / 12) * 12
    return lowest_note, highest_note if highest_note < 127 else 127


def get_2D_matrix_from_MIDI(file, rows, cols, max_length, note_range, time_steps, include_stops):
    """Generate a 2d numpy array based on a MIDI file"""
    matrix = np.zeros(shape=(rows, cols))
    time = 0
    ticks_per_beat = time_steps[0]
    units_per_beat = time_steps[2]
    note_velocity = [0] * rows  # - 1 if include_stops else 0
    # print('note range', note_range)
    print(file.filename)
    while time < max_length:
        for msg in file.tracks[0]:
            if not msg.is_meta and msg.type == 'note_on' or msg.type == 'note_off':
                time += msg.time
                time_frame = int(time / ticks_per_beat * units_per_beat)
                pitch = rows - (msg.note - note_range[0]) - 1
                # print(time_frame, pitch)
                if msg.type == 'note_on':
                    # if time_frame >= cols:
                    #     break
                    matrix[0][time_frame] = 127
                    matrix[pitch][time_frame] = msg.velocity
                    note_velocity[pitch] = msg.velocity
                else:
                    # if time_frame > cols:
                    #     break
                    while time_frame > 0 and matrix[pitch][time_frame-1] == 0:
                        time_frame -= 1
                        matrix[pitch][time_frame] = note_velocity[pitch]
    # print(rows, cols)
    # print(matrix.shape)
    # print(matrix[0])
    return matrix


def generate_dataset(input_path, output_path, file_count=0, max_length=0,
                     note_range=(-1, 128), time_steps=(0, 0, 0), include_stops=True):
    """Generate a dataset (np.ndarray) based on the MIDI files from the input directory"""
    if file_count <= 0:
        file_count = MIDIHandler.getTotalMIDICountFromDir(input_path)
    if max_length <= 0:
        max_length = MIDIHandler.getMaxLengthFromDir(input_path)
    if note_range[0] < 0 or note_range[1] > 127:
        note_range = MIDIHandler.getNoteRangeFromDir(input_path)
    note_range = get_appropriate_note_range(note_range)
    if time_steps[0] == 0 or time_steps[1] == 0 or time_steps[2] == 0:
        time_steps = MIDIHandler.getMaxTimeStepsFromDir(input_path)
    matrix_rows = note_range[1] - note_range[0] + 1 if include_stops else 0
    print('Matrix pitches ranges from ', MIDIHandler.getNoteNameFromNoteNumber(note_range[0]),
          ' to ', MIDIHandler.getNoteNameFromNoteNumber(note_range[1]))
    matrix_cols = int(max_length / time_steps[0] * time_steps[2])  # Assuming time signature is 4/4 and file is 8 bars long
    print('Matrix based on 32th note, length ', matrix_cols)
    dataset = np.zeros(shape=(file_count, matrix_rows, matrix_cols))
    index = 0
    for root, dirs, files in os.walk(input_path, topdown=True):
        for file in files:
            if file.endswith('.mid'):
                path = os.path.join(root, file)
                midi_object = mido.MidiFile(path, clip=True)
                dataset[index] = get_2D_matrix_from_MIDI(midi_object, matrix_rows, matrix_cols, max_length,
                                                         note_range, time_steps, include_stops)
                index += 1

    np.save(output_path, dataset)
    # dataset[index] = get_2D_matrix_from_MIDI(mido.MidiFile(r'/Users/alvin/Downloads/MIDI Chord Dataset/Tropical_House/AbMaj_FMin/Set_1/Absus2-Ab-Cm7-Db(add2)-Dbsus2-Ab_Niko_Kotoulas.mid', clip=True), matrix_rows, matrix_cols, max_length,
    #                                                      note_range, time_steps, include_stops)
    # for row in dataset[index]:
    #     print(row)
    return dataset


generate_dataset(input_path_, output_path_, 126000, int(512 / 8 * 96), (18, 89), (96, 36, 8), True)

# testfile = mido.MidiFile('/Users/alvin/Downloads/MIDI Chord Dataset/Drill/DbMaj_BbMin/Set_21/Ebm-Bbm-C7sus4-Bbm_Niko_Kotoulas.mid')
# print(testfile)
