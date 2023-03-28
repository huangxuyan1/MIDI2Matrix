import mido
import os

noteRef = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


def getTotalMIDICountFromDir(dir):
    """Returns total number of MIDI files in a directory"""
    count = 0
    for root, dirs, files in os.walk(dir, topdown=True):
        for name in files:
            if name.endswith('.mid'):
                count += 1
    print('Total MIDI Files Found: ', count)
    return count


def getMaxTimeStepsFromDir(dir):
    """
    Call this function to get maximum time steps of MIDI files in a directory
    Returns a tuple (ticks_per_beat, clocks_per_click, 32nd_notes_per_beat)
    ticks_per_beat:`        time steps per beat(1/4 note)
    clocks_per_click:       time between each metronome clicks, in clocks
    32nd_notes_per_beat:    indicate how many 32nd notes are in a beat(1/4 note)
    """
    max_ticks_per_beat = 0
    max_clocks_per_click = 36
    max_notated_32nd_notes_per_beat = 8
    for root, dirs, files in os.walk(dir, topdown=True):
        for name in files:
            if name.endswith('.mid'):
                path = os.path.join(root, name)
                file = mido.MidiFile(path, clip=True)
                metaMsg = mido.MetaMessage.copy(file.tracks[0][1])
                clocks_per_click = metaMsg.bytes()[-2]
                notated_32nd_notes_per_beat = metaMsg.bytes()[-1]
                max_ticks_per_beat = max(max_ticks_per_beat, file.ticks_per_beat)
                max_clocks_per_click = max(max_clocks_per_click, clocks_per_click)
                max_notated_32nd_notes_per_beat = max(max_notated_32nd_notes_per_beat, notated_32nd_notes_per_beat)
    print('Maximum Clocks Per Click: ', max_clocks_per_click)
    print('Maximum Notated 32nd Notes Per Beat: ', max_notated_32nd_notes_per_beat)
    return max_ticks_per_beat, max_clocks_per_click, max_notated_32nd_notes_per_beat


def getNoteNameFromNoteNumber(number):
    """Returns a String that contains the note name"""
    octave = int(number / 12) - 2
    note = number % 12
    return noteRef[note] + str(octave)


def getMaxLengthFromDir(dir):
    """Returns the maximum length of midi files from a directory"""
    max_length = 0
    for root, dirs, files in os.walk(dir, topdown=True):
        for name in files:
            if name.endswith('.mid'):
                path = os.path.join(root, name)
                file = mido.MidiFile(path, clip=True)
                length = 0
                for msg in file.tracks[0]:
                    length += msg.time
                max_length = max(max_length, length)
    return max_length


def getNoteRangeFromDir(dir):
    """Returns a tuple that contains the lowest note and highest note"""
    lowestNote = 127
    highestNote = 0
    for root, dirs, files in os.walk(dir, topdown=True):
        for name in files:
            if name.endswith('.mid'):
                path = os.path.join(root, name)
                file = mido.MidiFile(path, clip=True)
                for msg in file.tracks[0]:
                    if not msg.is_meta:
                        lowestNote = min(lowestNote, msg.bytes()[1])
                        highestNote = max(highestNote, msg.bytes()[1])
    print('Lowest Note: ', getNoteNameFromNoteNumber(lowestNote))
    print('Highest Note: ', getNoteNameFromNoteNumber(highestNote))
    return lowestNote, highestNote


# sample = mido.MidiFile(r'/Users/alvin/Downloads/MIDI Chord Dataset/Tropical_House/AbMaj_FMin/Set_1/Absus2-Ab-Cm7-Db(add2)-Dbsus2-Ab_Niko_Kotoulas.mid', clip=True)
# time = 0
# for msg in sample.tracks[0]:
#     # if not msg.is_meta:
#         # print(getNoteNameFromNoteNumber(msg.bytes()[1]))
#         # time += msg.time
#         # print(msg.time)
#     print(msg)
# print(time)
# print(sample.ticks_per_beat)

# getNoteRangeFromDir(r'/Users/alvin/Downloads/MIDI Chord Dataset')
# Lowest: B-1 Highest A5

# getMaxTimeStepsFromDir(r'/Users/alvin/Downloads/MIDI Chord Dataset')
# Maximum Clocks Per Click:  36
# Maximum Notated 32nd Notes Per Beat:  8
