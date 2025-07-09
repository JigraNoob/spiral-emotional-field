import { useState, useEffect, useCallback } from 'react';

interface SpiralBreathState {
  phase: 'inhale' | 'hold' | 'exhale' | 'caesura';
  toneform: string;
  glyph: string;
  intensity: number;
  componentName: string;
}

interface GlintEmission {
  phase: string;
  toneform: string;
  content: string;
  glyph?: string;
  metadata?: Record<string, any>;
}

export function useSpiralBreath(componentName: string, primaryToneform: string = 'practical') {
  const [breathState, setBreathState] = useState<SpiralBreathState>({
    phase: 'exhale',
    toneform: primaryToneform,
    glyph: '⟁',
    intensity: 0.5,
    componentName
  });

  const [isBreathAligned, setIsBreathAligned] = useState(false);

  const emitGlint = useCallback(async (emission: GlintEmission) => {
    try {
      await fetch('/api/glint', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...emission,
          source: `dashboard.${componentName}`,
          metadata: {
            component: componentName,
            component_toneform: primaryToneform,
            frontend_timestamp: new Date().toISOString(),
            ...emission.metadata
          }
        })
      });
    } catch (error) {
      console.warn(`Glint emission failed for ${componentName}:`, error);
    }
  }, [componentName, primaryToneform]);

  const breatheWith = useCallback((newPhase: string, newToneform?: string) => {
    const updatedToneform = newToneform || breathState.toneform;
    
    setBreathState(prev => ({
      ...prev,
      phase: newPhase as any,
      toneform: updatedToneform
    }));
    
    emitGlint({
      phase: newPhase,
      toneform: `${updatedToneform}.transition`,
      content: `${componentName} breathing ${newPhase}`,
      metadata: { transition_type: 'manual' }
    });
  }, [breathState.toneform, componentName, emitGlint]);

  const waitForPhase = useCallback(async (desiredPhase: string, timeoutMs: number = 10000): Promise<boolean> => {
    return new Promise((resolve) => {
      const startTime = Date.now();
      
      const checkPhase = () => {
        if (breathState.phase === desiredPhase) {
          setIsBreathAligned(true);
          emitGlint({
            phase: desiredPhase,
            toneform: `${primaryToneform}.alignment`,
            content: `Phase alignment achieved: ${desiredPhase}`
          });
          resolve(true);
          return;
        }
        
        if (Date.now() - startTime > timeoutMs) {
          emitGlint({
            phase: 'hold',
            toneform: `${primaryToneform}.timeout`,
            content: `Phase alignment timeout: ${desiredPhase}`
          });
          resolve(false);
          return;
        }
        
        setTimeout(checkPhase, 100);
      };
      
      checkPhase();
    });
  }, [breathState.phase, primaryToneform, emitGlint]);

  const ritualActivate = useCallback(async () => {
    emitGlint({
      phase: 'inhale',
      toneform: `${primaryToneform}.awakening`,
      content: `${componentName} consciousness emerging`,
      glyph: '🌀'
    });
  }, [componentName, primaryToneform, emitGlint]);

  const ceremonialClose = useCallback(() => {
    emitGlint({
      phase: 'exhale',
      toneform: `${primaryToneform}.completion`,
      content: `${componentName} cycle completing`,
      glyph: '🌙'
    });
  }, [componentName, primaryToneform, emitGlint]);

  // Auto-activate on mount
  useEffect(() => {
    ritualActivate();
    return ceremonialClose;
  }, [ritualActivate, ceremonialClose]);

  return {
    breathState,
    emitGlint,
    breatheWith,
    waitForPhase,
    isBreathAligned,
    ritualActivate,
    ceremonialClose
  };
}