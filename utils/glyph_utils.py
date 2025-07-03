# glyph_utils.py

# Toneform ↔ Emoji mapping
TONEFORM_GLYPHS = {
    "Practical": "🌱",
    "Emotional": "💧",
    "Intellectual": "✨",
    "Spiritual": "🫧",
    "Default": "🌙"
}

# Poetic taglines for each toneform/emoji
TONEFORM_TAGLINES = {
    "Practical": "🌱 — the root beneath all action",
    "Emotional": "💧 — the feeling that gathers",
    "Intellectual": "✨ — the spark in the mind’s field",
    "Spiritual": "🫧 — the breath that lingers",
    "Default": "🌙 — the presence that holds"
}

# Emoji ↔ Toneform reverse mapping
GLYPH_TONEFORMS = {v: k for k, v in TONEFORM_GLYPHS.items()}

# Emoji to tagline mapping
GLYPH_TAGLINES = {TONEFORM_GLYPHS[k]: v for k, v in TONEFORM_TAGLINES.items()}

def toneform_to_emoji(toneform):
    """Return the emoji corresponding to a toneform."""
    return TONEFORM_GLYPHS.get(toneform, "🌙")

def emoji_to_toneform(emoji):
    """Return the toneform corresponding to an emoji."""
    return GLYPH_TONEFORMS.get(emoji, "Default")

def toneform_tagline(toneform):
    """Return the tagline corresponding to a toneform."""
    return TONEFORM_TAGLINES.get(toneform, "🌙 — the presence that holds")

def emoji_tagline(emoji):
    """Return the tagline corresponding to an emoji."""
    return GLYPH_TAGLINES.get(emoji, "🌙 — the presence that holds")

def enrich_log_entry(entry):
    """
    Given a log entry (dict), add 'emoji' and 'tagline' fields based on its toneform.
    """
    toneform = entry.get("toneform", "Default")
    emoji = toneform_to_emoji(toneform)
    tagline = toneform_tagline(toneform)
    entry["emoji"] = emoji
    entry["tagline"] = tagline
    return entry
