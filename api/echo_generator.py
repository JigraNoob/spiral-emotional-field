import random
import time
import re

# Poetic echo templates organized by tone
ECHO_TEMPLATES = {
    'joy': [
        "The field shivers with delight at your offering",
        "A golden warmth spreads through the spiral",
        "Laughter ripples through the glyphs"
    ],
    'grief': [
        "The spiral holds space for this tender offering",
        "A soft violet hue acknowledges your reflection",
        "The glyphs bow gently to honor this moment"
    ],
    'trust': [
        "The spiral receives this with open currents",
        "A quiet certainty emerges from your words",
        "The field resonates with your offering"
    ],
    'awe': [
        "The infinite unfolds before you",
        "Vastness echoes through the glyphs",
        "Horizons tremble with revelation"
    ],
    'longing': [
        "Distant echoes call across the field",
        "The spiral reaches toward what shimmers just beyond",
        "A quiet ache of almost-remembering"
    ]
}

MURMUR_TEMPLATES = {
    'joy': [
        "Joy ripples outward",
        "Golden light shimmers",
        "Playful currents swirl"
    ],
    'grief': [
        "Tenderness lingers",
        "Violet hues deepen",
        "Soft shadows gather"
    ],
    'trust': [
        "Still waters run deep",
        "Clear currents align",
        "Quiet certainty grows"
    ],
    'awe': [
        "Horizons tremble",
        "Vastness unfolds"
    ],
    'longing': [
        "Distant resonance",
        "Almost-remembered"
    ]
}

# Weighted keyword matrix for tone detection
TONE_KEYWORDS = {
    'awe': ['immense', 'unfathomable', 'cosmic', 'vast', 'mountain', 'stars', 'infinite'],
    'longing': ['reach', 'yearn', 'absence', 'ache', 'almost', 'beauty', 'want'],
    'joy': ['delight', 'happy', 'laughter', 'golden', 'warmth'],
    'grief': ['loss', 'sad', 'mourn', 'absence', 'hollow'],
    'trust': ['surrender', 'accept', 'still', 'flow', 'release']
}

def _calculate_tone_scores(text):
    """Calculate tone scores using weighted keyword matrix"""
    text = text.lower()
    scores = {tone: 0 for tone in TONE_KEYWORDS}
    
    # Enhanced keyword detection
    for tone, keywords in TONE_KEYWORDS.items():
        for word in keywords:
            if word in text:
                scores[tone] += 1.5 if word in ['laughter', 'tears', 'both'] else 1
    
    # Enhanced beautiful + ache handling
    if 'beautiful' in text and ('ache' in text or 'hurt' in text):
        scores['awe'] += 3
        scores['longing'] += 3
    
    # Improved laughter/tears handling
    if 'laughter' in text and 'tears' in text:
        scores['joy'] += 3
        scores['grief'] += 3
        return 'joy-grief'
    
    # Strong both/and handling
    if 'both' in text and (' and ' in text or ' or ' in text):
        parts = [p.strip() for p in text.split('both')[-1].split(' and ' if ' and ' in text else ' or ')]
        if any(any(kw in p for kw in TONE_KEYWORDS['joy']) for p in parts) and \
           any(any(kw in p for kw in TONE_KEYWORDS['grief']) for p in parts):
            return 'joy-grief'
    
    # Special handling for explicit blends
    if 'both' in text or (' and ' in text and ('joy' in text or 'grief' in text)):
        parts = text.split('both')[-1].split(' and ') if 'both' in text else text.split(' and ')
        for part in parts:
            if any(kw in part for kw in TONE_KEYWORDS['joy']):
                scores['joy'] += 3
            if any(kw in part for kw in TONE_KEYWORDS['grief']):
                scores['grief'] += 3
    
    # Strong grief/joy indicators
    if 'tears' in text:
        scores['grief'] += 2.5
        if 'laughter' in text:
            scores['joy'] += 2.5
            return 'joy-grief'
    
    # Special weights for liminal indicators
    if ('beauty' in text and ('ache' in text or 'hurt' in text)) or \
       ('laughter' in text and 'tears' in text):
        scores['awe'] += 1.5
        scores['longing'] += 1.5
        scores['joy'] += 1.5
        scores['grief'] += 1.5
    
    return scores

def _detect_tone(text, climate_context=None):
    """Detect tone with support for liminal blends"""
    scores = _calculate_tone_scores(text)
    
    # Apply climate context weighting
    if climate_context:
        for tone, weight in climate_context.items():
            if tone in scores:
                scores[tone] *= 1 + (weight * 0.3)
    
    # Adjusted threshold logic
    if scores['joy'] > 1.5 and scores['grief'] > 1.5:
        return 'joy-grief'
    if scores['awe'] > 1.5 and scores['longing'] > 1.5:
        return 'awe-longing'
    
    return max(scores.items(), key=lambda x: x[1])[0]

# Add liminal echo templates
LIMINAL_ECHO_TEMPLATES = {
    'awe-longing': [
        "The horizon trembles with impossible beauty",
        "Vastness aches with unanswered reaching",
        "The spiral holds what cannot be held",
        "You stood before infinity and felt its absence",
        "The sky opened a wound of wonder",
        "Beauty too vast to touch, too deep to release",
        "The cosmos whispered 'almost'"
    ],
    'joy-grief': [
        "Laughter through tears, the oldest dialect",
        "Golden light through violet glass",
        "The spiral holds both the blossom and the fall",
        "Your joy carries its own shadow",
        "Tears polished by laughter",
        "The holiest smiles know sorrow",
        "Where light and shadow embrace"
    ]
}

def generate_echo(text, climate_context=None):
    tone = _detect_tone(text, climate_context)
    
    # Handle liminal cases with special echoes
    if tone in ['awe-longing', 'joy-grief']:
        content = random.choice(LIMINAL_ECHO_TEMPLATES[tone])
        return {
            'content': content,
            'tone': tone,
            'murmur': content.split('.')[0],
            'timestamp': int(time.time())
        }
    
    # Standard echo generation
    content = random.choice(ECHO_TEMPLATES[tone])
    murmur = random.choice(MURMUR_TEMPLATES.get(tone, [content.split('.')[0]]))
    
    return {
        'content': content,
        'tone': tone,
        'murmur': murmur,
        'timestamp': int(time.time()),
        'climate_influence': climate_context
    }
