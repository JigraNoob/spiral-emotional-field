import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"
 
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatDate(date: Date | string | number) {
  return new Intl.DateTimeFormat('en-US', {
    month: 'long',
    day: 'numeric',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(date))
}

export function formatBytes(
  bytes: number,
  decimals = 0,
  sizeType: 'accurate' | 'normal' = 'normal'
) {
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
  const accurateSizes = ['Bytes', 'KiB', 'MiB', 'GiB', 'TiB']
  if (bytes === 0) return '0 Byte'
  const i = Math.floor(Math.log(bytes) / Math.log(1024))
  return `${(bytes / Math.pow(1024, i)).toFixed(decimals)} ${
    sizeType === 'accurate' ? accurateSizes[i] ?? 'Bytest' : sizes[i] ?? 'Bytes'
  }`
}

export function isArrayOfFile(files: unknown): files is File[] {
  const isArray = Array.isArray(files)
  if (!isArray) return false
  return files.every(file => file instanceof File)
}

export function toTitleCase(str: string) {
  return str.replace(
    /\w\S*/g,
    (txt) => txt.charAt(0).toUpperCase() + txt.slice(1).toLowerCase()
  )
}

export function truncate(str: string, length: number) {
  return str.length > length ? `${str.substring(0, length)}...` : str
}

export function getToneformColor(toneform: string) {
  const colors = {
    practical: 'bg-cyan-100 text-cyan-800 dark:bg-cyan-900 dark:text-cyan-100',
    emotional: 'bg-rose-100 text-rose-800 dark:bg-rose-900 dark:text-rose-100',
    intellectual: 'bg-indigo-100 text-indigo-800 dark:bg-indigo-900 dark:text-indigo-100',
    spiritual: 'bg-violet-100 text-violet-800 dark:bg-violet-900 dark:text-violet-100',
    relational: 'bg-amber-100 text-amber-800 dark:bg-amber-900 dark:text-amber-100',
  }
  return colors[toneform as keyof typeof colors] || 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-100'
}

export function getResonanceColor(resonance: number) {
  if (resonance >= 0.8) return 'text-green-500'
  if (resonance >= 0.6) return 'text-blue-500'
  if (resonance >= 0.4) return 'text-yellow-500'
  return 'text-gray-500'
}

export function getIntensityColor(intensity: number) {
  if (intensity >= 0.8) return 'bg-red-500'
  if (intensity >= 0.6) return 'bg-orange-500'
  if (intensity >= 0.4) return 'bg-yellow-500'
  if (intensity >= 0.2) return 'bg-blue-500'
  return 'bg-gray-500'
}
