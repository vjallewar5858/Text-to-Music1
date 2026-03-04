# 🎵 Text to Music Converter

Convert any text (poems, lyrics, stories) into beautiful MIDI music using AI-powered text analysis and algorithmic music generation.

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

## 🌟 Features

- **Sentiment Analysis**: Analyzes the emotional tone of your text to determine major/minor key
- **Tempo Mapping**: Converts text rhythm and pacing into musical tempo
- **Automatic Composition**: Generates melody and chord progressions based on text structure
- **Multiple Output Formats**: Creates MIDI files playable on any device
- **100% Free**: No API keys, no subscriptions, completely open-source
- **Offline Capable**: Works without internet connection

## 🚀 Quick Start
```bash
# Clone the repository
git clone https://github.com/yourusername/text-to-music.git
cd text-to-music

# Install dependencies
pip install -r requirements.txt

# Run the application
python src/text_to_midi.py --text "Your text here"
```

## 📖 Usage

### Basic Usage

**Convert text directly:**
```bash
python src/text_to_midi.py --text "Twinkle twinkle little star"
```

**Convert from a file:**
```bash
python src/text_to_midi.py --file examples/sample_poem.txt
```

**Specify output location:**
```bash
python src/text_to_midi.py --file poem.txt --output my_music.mid
```

## 🧠 How It Works

1. **Text Analysis**: Uses NLP to analyze sentiment, rhythm, and structure
2. **Musical Mapping**: Converts text features to musical parameters
3. **Composition**: Generates melody and chords based on analysis
4. **MIDI Export**: Creates playable MIDI files

## 📁 Project Structure
```
text-to-music/
├── src/
│   ├── text_to_midi.py          # Main application
│   ├── text_analyzer.py         # Text analysis module
│   └── music_generator.py       # Music generation module
├── examples/
│   ├── sample_poem.txt
│   ├── happy_text.txt
│   └── sad_text.txt
├── output/                      # Generated MIDI files
├── requirements.txt
├── LICENSE
└── README.md
```

## 🎹 Playing Your Music

- **Windows**: Windows Media Player, VLC
- **macOS**: GarageBand, QuickTime
- **Linux**: TiMidity++, VLC
- **Online**: [Online Sequencer](https://onlinesequencer.net/import)

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- NLTK for text analysis
- MIDIUtil for MIDI generation

---

Made with ❤️ and 🎵
```

### 2. requirements.txt
```
midiutil>=1.2.1
nltk>=3.8
