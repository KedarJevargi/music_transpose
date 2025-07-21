import re

class HindustaniTransposer:
    def __init__(self):
        self.chromatic_scale = [
            'S', 'r', 'R', 'g', 'G', 'm', 'M',
            'P', 'd', 'D', 'n', 'N'
        ]

        self.western_notes = [
            'C', 'C#', 'D', 'D#', 'E', 'F', 'F#',
            'G', 'G#', 'A', 'A#', 'B'
        ]

        self.western_aliases = {
            'Db': 'C#', 'Eb': 'D#', 'Gb': 'F#',
            'Ab': 'G#', 'Bb': 'A#'
        }

    def normalize_note(self, note):
        return note.strip()

    def normalize_western_note(self, note):
        note = note.strip()
        if note in self.western_notes:
            return note
        if note in self.western_aliases:
            return self.western_aliases[note]
        raise ValueError(f"Invalid Western note: {note}")

    def get_semitone_index(self, note):
        normalized = self.normalize_note(note)
        
        if normalized in self.chromatic_scale:
            return self.chromatic_scale.index(normalized)
        
        upper_octave_match = re.match(r"^([a-zA-Z]+)'+$", normalized)
        if upper_octave_match:
            base_note = upper_octave_match.group(1)
            if base_note in self.chromatic_scale:
                return self.chromatic_scale.index(base_note)
        
        lower_octave_match = re.match(r"^([a-zA-Z]+),+$", normalized)
        if lower_octave_match:
            base_note = lower_octave_match.group(1)
            if base_note in self.chromatic_scale:
                return self.chromatic_scale.index(base_note)

        raise ValueError(f"Invalid Hindustani note: {note}")

    def get_western_index(self, note):
        normalized = self.normalize_western_note(note)
        return self.western_notes.index(normalized)

    def calculate_semitone_difference_western(self, from_note, to_note):
        from_index = self.get_western_index(from_note)
        to_index = self.get_western_index(to_note)
        return from_index - to_index

    def transpose_note(self, note, semitones):
        octaves = ""
        base_note = note.strip()

        upper_octave_match = re.match(r"^([a-zA-Z]+)('+)$", base_note)
        if upper_octave_match:
            base_note = upper_octave_match.group(1)
            octaves = upper_octave_match.group(2)

        lower_octave_match = re.match(r"^([a-zA-Z]+)(,+)$", base_note)
        if lower_octave_match:
            base_note = lower_octave_match.group(1)
            octaves = lower_octave_match.group(2)

        current_index = self.get_semitone_index(base_note)
        new_index = (current_index + semitones % 12 + 12) % 12
        
        return self.chromatic_scale[new_index] + octaves

    def transpose_sequence(self, notes, semitones):
        if isinstance(notes, str):
            notes = notes.replace(',', ' ').split()

        transposed = []
        for note in notes:
            if note.strip():
                try:
                    transposed_note = self.transpose_note(note.strip(), semitones)
                    transposed.append(transposed_note)
                except ValueError as e:
                    print(f"Warning: {e}")
                    transposed.append(note)
        return transposed
