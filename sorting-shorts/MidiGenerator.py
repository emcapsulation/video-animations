from midiutil.MidiFile import MIDIFile
import math

class MidiGenerator:
    def __init__(self, filename, track, channel, volume, tempo, default_duration):
        self.filename = filename
        self.track = track
        self.channel = channel
        self.volume = volume
        self.tempo = tempo
        self.default_duration = default_duration

        # Create MIDI object with one track
        self.mf = MIDIFile(1)

        # The first track
        self.time = 0
        self.mf.addTrackName(self.track, self.time, self.filename)
        self.mf.addTempo(self.track, self.time, self.tempo)

        # Eb major pentatonic
        self.notes = [i+60 for i in range(0, 12)]


    def write_int(self, i, duration):
        note = self.notes[i%len(self.notes)] + 12*math.floor(i/len(self.notes))
        self.mf.addNote(self.track, self.channel, note, self.time, duration, self.volume)
        self.time += duration


    def write_chord(self, notes, duration):
        for i in notes:
            this_note = self.notes[i%len(self.notes)] + 12*math.floor(i/len(self.notes))
            self.mf.addNote(self.track, self.channel, this_note, self.time, duration, self.volume)
        self.time += duration


    def write_pause(self, duration):
        self.time += duration


    def write_file(self, outf):
        self.mf.writeFile(outf)