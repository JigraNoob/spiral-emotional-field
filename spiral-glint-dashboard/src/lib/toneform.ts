export type Toneform = 'practical' | 'emotional' | 'intellectual' | 'spiritual' | 'relational';

export interface ToneformColors {
  bg: string;
  bgHover: string;
  border: string;
  text: string;
  icon: string;
}

export const TONEFORM_COLORS: Record<Toneform, ToneformColors> = {
  practical: {
    bg: 'bg-blue-50 dark:bg-blue-900/30',
    bgHover: 'hover:bg-blue-100 dark:hover:bg-blue-900/50',
    border: 'border-blue-200 dark:border-blue-800',
    text: 'text-blue-800 dark:text-blue-200',
    icon: 'text-blue-500',
  },
  emotional: {
    bg: 'bg-rose-50 dark:bg-rose-900/30',
    bgHover: 'hover:bg-rose-100 dark:hover:bg-rose-900/50',
    border: 'border-rose-200 dark:border-rose-800',
    text: 'text-rose-800 dark:text-rose-200',
    icon: 'text-rose-500',
  },
  intellectual: {
    bg: 'bg-purple-50 dark:bg-purple-900/30',
    bgHover: 'hover:bg-purple-100 dark:hover:bg-purple-900/50',
    border: 'border-purple-200 dark:border-purple-800',
    text: 'text-purple-800 dark:text-purple-200',
    icon: 'text-purple-500',
  },
  spiritual: {
    bg: 'bg-violet-50 dark:bg-violet-900/30',
    bgHover: 'hover:bg-violet-100 dark:hover:bg-violet-900/50',
    border: 'border-violet-200 dark:border-violet-800',
    text: 'text-violet-800 dark:text-violet-200',
    icon: 'text-violet-500',
  },
  relational: {
    bg: 'bg-emerald-50 dark:bg-emerald-900/30',
    bgHover: 'hover:bg-emerald-100 dark:hover:bg-emerald-900/50',
    border: 'border-emerald-200 dark:border-emerald-800',
    text: 'text-emerald-800 dark:text-emerald-200',
    icon: 'text-emerald-500',
  },
};

export const TONEFORM_GLYPHS: Record<Toneform, string> = {
  practical: '🔧',
  emotional: '💖',
  intellectual: '🧠',
  spiritual: '🕯️',
  relational: '🤝',
};

export function getToneformColor(toneform: string): ToneformColors {
  const normalizedToneform = toneform.toLowerCase() as Toneform;
  return TONEFORM_COLORS[normalizedToneform] || TONEFORM_COLORS.practical;
}

export function getToneformGlyph(toneform: string): string {
  const normalizedToneform = toneform.toLowerCase() as Toneform;
  return TONEFORM_GLYPHS[normalizedToneform] || TONEFORM_GLYPHS.practical;
}
