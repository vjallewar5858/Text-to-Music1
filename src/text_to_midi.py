"""
text_to_midi.py - Main application for text-to-music conversion
"""

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from midiutil import MIDIFile
import random
import os
import argparse

# Download required NLTK data
try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')
    nltk.download('punkt')


class TextAnalyzer:
    """Analyzes text to extract musical parameters."""
    
    def __init__(self):
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
    
    def analyze(self, text):
        """Analyze text and convert to musical parameters."""
        text = text.strip()
        
        # Analyze sentiment
        sentiment = self.sentiment_analyzer.polarity_scores(text)
        
        # Split into sentences and words
        sentences = nltk.sent_tokenize(text)
        words = nltk.word_tokenize(text.lower())
        
        # Calculate statistics
        avg_sentence_len = sum(len(nltk.word_tokenize(s)) for s in sentences) / max(len(sentences), 1)
        avg_word_len = sum(len(w) for w in words) / max(len(words), 1)
        
        # Calculate tempo (60-180 BPM)
        base_tempo = 100
        tempo = base_tempo + (10 - avg_sentence_len) * 3
        tempo += sentiment['pos'] * 30 - sentiment['neg'] * 30
        tempo = max(60, min(180, int(tempo)))
        
        # Determine key/mode
        if sentiment['compound'] > 0:
            mode = 'major'
            key_note = 60  # C major
        else:
            mode = 'minor'
            key_note = 57  # A minor
        
        # Note density (0.3-1.0)
        note_density = 1.0 - (avg_word_len - 3) / 10
        note_density = max(0.3, min(1.0, note_density))
        
        return {
            'tempo': tempo,
            'mode': mode,
            'key_note': key_note,
            'note_density': note_density,
            'num_bars': max(8, len(sentences) * 2),
            'sentiment': sentiment,
        }


class MusicGenerator:
    """Generates MIDI music from text analysis parameters."""
    
    # Musical scales
    MAJOR_SCALE = [0, 2, 4, 5, 7, 9, 11]
    MINOR_SCALE = [0, 2, 3, 5, 7, 8, 10]
    
    # Chord progressions
    MAJOR_PROGRESSIONS = [
        [0, 7, 9, 5],    # I-V-vi-IV
        [0, 5, 7, 0],    # I-IV-V-I
        [0, 9, 5, 7],    # I-vi-IV-V
    ]
    
    MINOR_PROGRESSIONS = [
        [0, 5, 10, 7],   # i-iv-VII-V
        [0, 7, 5, 0],    # i-V-iv-i
        [0, 10, 5, 7],   # i-VII-iv-V
    ]
    
    def __init__(self, params):
        """Initialize with analysis parameters."""
        self.params = params
        self.midi = MIDIFile(2)  # 2 tracks
        
        self.melody_track = 0
        self.chord_track = 1
        
        # Set tempo
        self.midi.addTempo(self.melody_track, 0, params['tempo'])
        self.midi.addTempo(self.chord_track, 0, params['tempo'])
        
        # Set track names
        self.midi.addTrackName(self.melody_track, 0, "Melody")
        self.midi.addTrackName(self.chord_track, 0, "Chords")
        
        # Set instruments (piano)
        self.midi.addProgramChange(self.melody_track, 0, 0, 0)
        self.midi.addProgramChange(self.chord_track, 1, 0, 0)
        
        # Select scale and progression
        if params['mode'] == 'major':
            self.scale = self.MAJOR_SCALE
            self.progression = random.choice(self.MAJOR_PROGRESSIONS)
        else:
            self.scale = self.MINOR_SCALE
            self.progression = random.choice(self.MINOR_PROGRESSIONS)
    
    def generate(self):
        """Generate the full musical piece."""
        num_bars = self.params['num_bars']
        self._generate_chords(num_bars)
        self._generate_melody(num_bars)
        return self.midi
    
    def _generate_chords(self, num_bars):
        """Generate chord progression."""
        time = 0
        beats_per_bar = 4
        
        for bar in range(num_bars):
            chord_root_interval = self.progression[bar % len(self.progression)]
            chord_root = self.params['key_note'] + chord_root_interval
            
            # Create triad
            if self.params['mode'] == 'major':
                chord_notes = [0, 4, 7]
            else:
                chord_notes = [0, 3, 7]
            
            for note_offset in chord_notes:
                pitch = chord_root + note_offset - 12
                self.midi.addNote(self.chord_track, 1, pitch, time, beats_per_bar, 70)
            
            time += beats_per_bar
    
    def _generate_melody(self, num_bars):
        """Generate melody over chords."""
        time = 0
        beats_per_bar = 4
        note_density = self.params['note_density']
        
        for bar in range(num_bars):
            notes_in_bar = max(2, int(note_density * 8))
            rhythm = self._generate_rhythm(beats_per_bar, notes_in_bar)
            
            for duration in rhythm:
                scale_degree = random.randint(0, 6)
                octave_offset = random.choice([-12, 0, 12])
                pitch = self.params['key_note'] + self.scale[scale_degree] + octave_offset
                
                volume = 100 if time % beats_per_bar == 0 else random.randint(70, 90)
                self.midi.addNote(self.melody_track, 0, pitch, time, duration, volume)
                time += duration
    
    def _generate_rhythm(self, total_beats, num_notes):
        """Generate rhythmic pattern."""
        durations = [0.25, 0.5, 1.0, 1.5, 2.0]
        rhythm = []
        beats_used = 0
        
        for i in range(num_notes):
            remaining = total_beats - beats_used
            
            if i == num_notes - 1:
                rhythm.append(remaining)
            else:
                possible = [d for d in durations if d <= remaining]
                if possible:
                    duration = random.choice(possible)
                    rhythm.append(duration)
                    beats_used += duration
                else:
                    rhythm.append(remaining)
                    break
        
        return rhythm
    
    def save(self, filename):
        """Save MIDI file."""
        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
        with open(filename, "wb") as output_file:
            self.midi.writeFile(output_file)
        return filename


def main():
    parser = argparse.ArgumentParser(description="Convert text to music (MIDI)")
    parser.add_argument("--text", type=str, help="Text to convert")
    parser.add_argument("--file", type=str, help="Text file to convert")
    parser.add_argument("--output", type=str, default="output/music.mid", help="Output MIDI file")
    
    args = parser.parse_args()
    
    # Get text
    text = args.text
    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            text = f.read()
    
    if not text:
        print("=== Text to Music Converter ===\n")
        text = input("Enter your text (poem, lyrics, etc.):\n")
    
    print("\n📝 Analyzing text...")
    analyzer = TextAnalyzer()
    params = analyzer.analyze(text)
    
    print(f"\n🎼 Musical Parameters:")
    print(f"   Tempo: {params['tempo']} BPM")
    print(f"   Mode: {params['mode']}")
    print(f"   Sentiment: {params['sentiment']['compound']:.2f}")
    print(f"   Number of bars: {params['num_bars']}")
    print(f"   Note density: {params['note_density']:.2f}")
    
    print("\n🎵 Generating music...")
    generator = MusicGenerator(params)
    generator.generate()
    
    output_file = generator.save(args.output)
    print(f"\n✅ Music saved to: {os.path.abspath(output_file)}")
    print("\n🎹 To listen:")
    print("   - Use VLC, Windows Media Player, or GarageBand")
    print("   - Or upload to: https://onlinesequencer.net/import")

if __name__ == "__main__":
    main()
```

### 4. examples/sample_poem.txt
```
Roses are red,
Violets are blue,
Music is sweet,
And so are you.
```

### 5. examples/happy_text.txt
```
Sunshine on my face,
Birds singing in the trees,
Life is full of grace,
Dancing in the breeze.

Joy fills every heart,
Laughter everywhere,
A brand new start,
Happiness we share.
```

### 6. examples/sad_text.txt
```
Rain falls on empty streets,
Memories fade away,
Silent heart that beats,
Longing for yesterday.

Shadows grow so long,
Echoes of the past,
Where did we go wrong,
Nothing seems to last.
```

### 7. .gitignore
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Output files
output/*.mid
output/*.wav
output/*.mp3

# NLTK data (downloaded at runtime)
nltk_data/
```
