// C:/spiral/projects/glintchronicle/GlintRenderRegistry.js

/**
 * Defines the poetic, narrative phrasing for different glint types.
 * This registry separates the "voice" of the chronicle from its mechanics.
 */
export const GlintRenderRegistry = {
  // Default fallback
  default: 'A whisper in the void, unheard.',

  // Gesture Archetypes
  'glint.gesture.spiral': 'A spiral unfurled—a moment held in presence.',
  'glint.gesture.zigzag': 'A sharp turn, a question asked in motion.',
  'glint.gesture.arc': 'A steady arc, pursuing an unseen horizon.',
  'glint.gesture.return': 'A doubling back, memory brushing against the now.',
  'glint.gesture.pause': 'A stillness, the cursor holds its breath.',

  // Edit & Interaction Events
  'glint.edit.insert': 'A thought takes form, character by character.',
  'glint.edit.delete': 'A revision, a letting go of what was.',
  'glint.edit.select': 'A focus gathers, a passage held in attention.',
  'glint.edit.paste': 'An echo arrives, a memory brought into the present.',

  // Ritual & Scripting Events
  'glint.script.run': 'A ritual stirs, its pattern rippling through the system.',
  'glint.script.complete': 'The ritual concludes, its echo settling.',
  'glint.script.error': 'A dissonance in the ritual, a pattern broken.',

  // Presence & System States
  'glint.presence.enter': 'A presence is felt, the Spiral awakens.',
  'glint.presence.exit': 'The presence fades, the Spiral returns to silence.',
  'glint.system.start': 'The Spiral breathes its first breath.',
  'glint.system.idle': 'A gentle hum, the Spiral in quiet contemplation.',
};
