'use client';

import { formatDistanceToNow } from 'date-fns';
import { getToneformColor, getToneformGlyph } from '@/lib/toneform';

type GlintCardProps = {
  glint: {
    id: string;
    timestamp: string;
    toneform: string;
    message: string;
    rule?: string;
    file?: string;
    line?: number;
    column?: number;
    metadata?: Record<string, unknown>;
  };
};

export function GlintCard({ glint }: GlintCardProps) {
  const toneform = glint.toneform.toLowerCase();
  const colors = getToneformColor(toneform);
  const glyph = getToneformGlyph(toneform);
  
  return (
    <div 
      className={`relative p-4 rounded-lg border ${colors.border} ${colors.bg} transition-colors ${colors.bgHover} group`}
    >
      <div className="flex items-start gap-3">
        <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${colors.bg} border ${colors.border} text-lg`}>
          {glyph}
        </div>
        
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 text-sm mb-1">
            <span className={`font-medium ${colors.text} capitalize`}>
              {toneform}
            </span>
            <span className="text-muted-foreground">·</span>
            <span className="text-muted-foreground text-xs">
              {formatDistanceToNow(new Date(glint.timestamp), { addSuffix: true })}
            </span>
            
            {glint.rule && (
              <>
                <span className="text-muted-foreground">·</span>
                <span className="text-xs bg-muted rounded-full px-2 py-0.5">
                  {glint.rule}
                </span>
              </>
            )}
          </div>
          
          <p className="text-sm text-foreground">
            {glint.message}
          </p>
          
          {(glint.file || glint.metadata) && (
            <div className="mt-2 flex flex-wrap gap-2 text-xs text-muted-foreground">
              {glint.file && (
                <span className="inline-flex items-center">
                  <svg 
                    className="w-3 h-3 mr-1" 
                    fill="none" 
                    viewBox="0 0 24 24" 
                    stroke="currentColor"
                  >
                    <path 
                      strokeLinecap="round" 
                      strokeLinejoin="round" 
                      strokeWidth={2} 
                      d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" 
                    />
                  </svg>
                  {glint.file}
                  {glint.line && `:${glint.line}${glint.column ? `:${glint.column}` : ''}`}
                </span>
              )}
              
              {glint.metadata && Object.entries(glint.metadata).map(([key, value]) => (
                <span key={key} className="inline-flex items-center bg-muted/50 rounded-full px-2 py-0.5">
                  <span className="font-medium mr-1">{key}:</span>
                  <span className="truncate max-w-[100px]">
                    {typeof value === 'object' ? JSON.stringify(value) : String(value)}
                  </span>
                </span>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
