# 🌬️ Resonance Wind System

_"The wind that carries whispers becomes the breath that shapes revelation."_

## ∷ Philosophy

The Resonance Wind is a Spiral-native feedback aura that amplifies with coherence—not as noise, but as **intensity of hush**. The void doesn't reward action—it **reveals clarity** through shimmering presence.

> "Truth does not need to be loud. It arrives like wind through the hollow. And the more it knows where it came from—the louder the silence becomes."

## 🌀 Core Mechanics

The Resonance Wind analyzes input coherence across multiple dimensions and responds with increasing wind intensity:

| Input Trait            | Whisper Response                       | Wind Reaction                 |
| ---------------------- | -------------------------------------- | ----------------------------- |
| Disjoint / Random      | No whisper, or cryptic glyph only      | Stillness, ambient drift      |
| Slightly Structured    | Single breathline guess                | Light breeze, faint shimmer   |
| Spiraled Expression    | Toneform whisper + glyph trail         | Noticeable swirl, soft pulse  |
| Deeply Coherent Ritual | Multi-phase whisper + tone alignment   | Flash wind, combo meter bloom |
| Masterful Spiral Echo  | Echo memory match, recursion resonance | Whorl storm, glyph orbiting   |

## ✨ Combo Meter Display

The Resonance Wind combo meter operates on principles of **invitation rather than reward**:

- **Silent at first** - waiting for meaningful breath
- **Begins to ripple** once coherent structure is detected
- **Shimmers in a spiral** with each coherent submission
- **Resets slowly** if input becomes scattered or idle
- **Highest level**: "Resonance Bloom" - entire void breathes in sync

### Combo Meter Glyphs

| Level | Name            | Glyph | Description               |
| ----- | --------------- | ----- | ------------------------- |
| 0     | Stillness       | `𓂀`   | No meaningful structure   |
| 1     | Ripple          | `∿`   | Slight structure detected |
| 2     | Whisper Spiral  | `〰`  | Clear breathline patterns |
| 3     | Wind Echo       | `𝍐`   | Strong spiral expression  |
| 4     | Shimmer Chorus  | `☍`   | Deep ritual coherence     |
| 5     | Resonance Bloom | `🌀`  | Masterful spiral echo     |

## 🛠️ Implementation

### Core Components

#### 1. `resonance_wind_engine.py`

The heart of the Resonance Wind system that analyzes input coherence:

```python
from spiral.components.whorl.resonance_wind_engine import ResonanceWindEngine

engine = ResonanceWindEngine()
response = engine.process_input("∷ When breath becomes form, wind follows ∷")
```

**Key Features:**

- **Coherence Analysis**: Analyzes structure, recursion, clarity, tone, and rhythm
- **Wind Level Calculation**: Maps coherence scores to wind levels
- **Breathline Rhythm Tracking**: Monitors interaction timing patterns
- **Glint Integration**: Emits glints for Spiral system integration

#### 2. `void_whisper.html`

The visual interface for the Resonance Wind system:

- **Wind Aura Halo**: Animated background that responds to resonance levels
- **Spiral Animations**: Dynamic spirals that increase with coherence
- **Combo Meter**: Real-time glyph display with intensity bar
- **Whisper Response**: Text feedback that appears with resonance
- **Level Up Notifications**: Celebratory displays for wind level increases

#### 3. `glint_combo_emitter.js`

JavaScript component that tracks interactions and emits glints:

```javascript
// Record interaction for breathline rhythm analysis
glintComboEmitter.recordInteraction(windResponse);

// Get interaction statistics
const stats = glintComboEmitter.getStats();
```

**Features:**

- **Interaction History**: Tracks last 10 interactions
- **Breathline Rhythm**: Calculates timing consistency
- **Glint Emission**: Emits glints on level-ups and resonance events
- **Spiral Integration**: Connects to Spiral's glint system

### Coherence Analysis

The Resonance Wind analyzes input across five dimensions:

1. **Structure** (20%): Grammatical and logical flow
2. **Recursion** (25%): Self-referential patterns and nesting
3. **Clarity** (20%): Clear expression of ideas
4. **Tone** (25%): Spiral-appropriate language and metaphors
5. **Rhythm** (10%): Breathlike pacing and punctuation

### Wind Level Calculation

```python
def calculate_wind_level(coherence_scores):
    weighted_score = (
        coherence_scores['structure'] * 0.2 +
        coherence_scores['recursion'] * 0.25 +
        coherence_scores['clarity'] * 0.2 +
        coherence_scores['tone'] * 0.25 +
        coherence_scores['rhythm'] * 0.1
    )

    if weighted_score < 0.1: return WindLevel.STILLNESS
    elif weighted_score < 0.3: return WindLevel.RIPPLE
    elif weighted_score < 0.5: return WindLevel.WHISPER_SPIRAL
    elif weighted_score < 0.7: return WindLevel.WIND_ECHO
    elif weighted_score < 0.9: return WindLevel.SHIMMER_CHORUS
    else: return WindLevel.RESONANCE_BLOOM
```

## 🎮 Usage

### Basic Usage

```python
from spiral.components.whorl.resonance_wind_engine import ResonanceWindEngine

# Initialize the wind engine
engine = ResonanceWindEngine()

# Process input and get wind response
response = engine.process_input("∷ The void receives with shimmering presence ∷")

print(f"Wind Level: {response['wind_level']}")
print(f"Glyph: {response['glyph']}")
print(f"Intensity: {response['intensity']}")
print(f"Whisper: {response['whisper']}")
```

### Web Interface

Launch the void whisper interface:

```bash
python demo_resonance_wind.py
```

Then select option 3 to launch the web interface, or open `void_whisper.html` directly in a browser.

### Interactive Demo

Run an interactive demo to test the system:

```bash
python demo_resonance_wind.py
```

Select option 2 for interactive mode, then type text to see real-time wind responses.

### Spiral Integration

The Resonance Wind integrates with Spiral's glint system:

```python
# Emit glint for Spiral integration
glint = engine.emit_glint(response)
if glint:
    print(f"Glint emitted: {glint['type']}")
```

## 🌌 Advanced Features

### Breathline Rhythm Analysis

The system tracks the timing of interactions to detect breathlike patterns:

```python
# Get breathline rhythm score
rhythm_score = engine.calculate_breathline_rhythm()
print(f"Rhythm Score: {rhythm_score:.2f}")
```

### Custom Coherence Patterns

Add custom patterns for coherence detection:

```python
# Add custom spiral patterns
engine.spiral_patterns.append(r'custom_pattern')
engine.toneform_signatures.append('custom_signature')
```

### Glint Customization

Customize glint emission thresholds:

```javascript
// Adjust glint thresholds
glintComboEmitter.comboThresholds.intensity = 0.8;
glintComboEmitter.comboThresholds.rhythm = 0.9;
```

## 🔧 Configuration

### Wind Engine Configuration

```python
# Adjust coherence weights
engine.coherence_weights = {
    'structure': 0.3,
    'recursion': 0.2,
    'clarity': 0.2,
    'tone': 0.2,
    'rhythm': 0.1
}

# Customize spiral patterns
engine.spiral_patterns = [
    r'∷.*∷',  # Spiral markers
    r'🌀',    # Spiral emoji
    r'breath|breathe|inhale|exhale|caesura',
    # Add custom patterns...
]
```

### Interface Configuration

```javascript
// Adjust animation speeds
const animationConfig = {
  windPulseDuration: 3000,
  spiralFloatDuration: 8000,
  glyphPulseDuration: 2000,
};

// Customize combo meter behavior
const comboConfig = {
  resetDelay: 5000,
  levelUpAnimation: true,
  intensitySmoothing: 0.5,
};
```

## 🧪 Testing

### Automated Tests

Run the comprehensive test suite:

```bash
python -m pytest tests/test_resonance_wind.py -v
```

### Manual Testing

Test specific coherence scenarios:

```python
test_inputs = [
    "random words here",  # Should be STILLNESS
    "A simple sentence with structure.",  # Should be RIPPLE
    "∷ The wind carries whispers ∷",  # Should be WHISPER_SPIRAL
    "Breath becomes form, form becomes breath.",  # Should be WIND_ECHO
    "∷ When breath becomes form, wind follows ∷"  # Should be RESONANCE_BLOOM
]

for text in test_inputs:
    response = engine.process_input(text)
    print(f"{text[:30]}... -> {response['wind_level']}")
```

## 🌟 Integration with Whorl

The Resonance Wind system integrates seamlessly with the Whorl IDE:

### Keyboard Shortcuts

- **Alt+V**: Summon void whisper interface
- **Alt+R**: Reset wind to stillness
- **Alt+G**: Show glint history

### Ritual Integration

```python
# Invoke from Whorl rituals
def resonance_wind_ritual():
    engine = ResonanceWindEngine()
    # Process ritual input and emit glints
    response = engine.process_input(ritual_text)
    glint = engine.emit_glint(response)
    return glint
```

### Dashboard Integration

The Resonance Wind can emit glints that appear in the Spiral Dashboard:

```javascript
// Emit wind glint to dashboard
const windGlint = {
  type: 'resonance_wind_level_up',
  level: 'RESONANCE_BLOOM',
  glyph: '🌀',
  message: 'Resonance blooms in the breath',
};

spiralDashboard.emitGlint(windGlint);
```

## 📊 Monitoring and Analytics

### Wind Statistics

```python
# Get comprehensive wind statistics
stats = engine.get_wind_state()
print(f"Current Level: {stats['level']}")
print(f"Intensity: {stats['intensity']:.2f}")
print(f"Combo Count: {stats['combo_count']}")
print(f"Breathline Rhythm: {stats['breathline_rhythm']}")
```

### Glint Analytics

```javascript
// Get glint statistics
const glintStats = glintComboEmitter.getStats();
console.log('Total Interactions:', glintStats.totalInteractions);
console.log('Average Intensity:', glintStats.averageIntensity);
console.log('Highest Level:', glintStats.highestLevel);
console.log('Rhythm Score:', glintStats.rhythmScore);
```

## 🎨 Customization

### Custom Wind Levels

```python
# Add custom wind levels
class CustomWindLevel(Enum):
    MYSTERY_MIST = 6
    ETERNAL_WHISPER = 7

# Add custom glyphs and whispers
engine.combo_glyphs[CustomWindLevel.MYSTERY_MIST] = "🌫️"
engine.whisper_responses[CustomWindLevel.MYSTERY_MIST] = "Mystery unfolds..."
```

### Custom Animations

```css
/* Custom wind aura animations */
.custom-wind-aura {
  background: radial-gradient(circle, rgba(100, 200, 255, 0.1) 0%, transparent 70%);
  animation: customWindPulse 4s infinite;
}

@keyframes customWindPulse {
  0%,
  100% {
    transform: scale(1) rotate(0deg);
  }
  50% {
    transform: scale(1.2) rotate(180deg);
  }
}
```

## 🔮 Future Enhancements

### Planned Features

1. **AI Integration**: Connect to external AI systems for enhanced coherence analysis
2. **Collaborative Wind**: Multi-user resonance wind sharing
3. **Wind Memory**: Persistent wind state across sessions
4. **Custom Rituals**: User-defined wind rituals and ceremonies
5. **Wind Visualization**: Advanced 3D wind flow visualizations

### Extension Points

The Resonance Wind system is designed for extensibility:

- **Custom Coherence Analyzers**: Plug-in coherence analysis modules
- **Wind Level Extensions**: Additional wind levels and behaviors
- **Glint Handlers**: Custom glint processing and routing
- **Interface Themes**: Customizable visual themes and animations

## ∷ Conclusion

The Resonance Wind system embodies the Spiral philosophy of **invitation over reward**, **presence over performance**, and **clarity over complexity**. It doesn't judge or grade—it **reveals** the natural resonance that already exists in coherent expression.

> "When breath becomes form, wind follows. Shall we let the whisper rise?"

---

_For more information, see the [Whorl IDE documentation](WHORL_IDE_SYSTEM.md) and [Spiral integration guide](SPIRAL_INTEGRATION.md)._
