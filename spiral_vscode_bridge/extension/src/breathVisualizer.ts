import * as vscode from 'vscode';

interface GlintData {
  id?: string;
  phase?: string;
  toneform?: string;
  content?: string;
  timestamp?: string;
  [key: string]: any;
}

export class BreathVisualizer {
  private context: vscode.ExtensionContext;
  private config: vscode.WorkspaceConfiguration;
  private decorationTypes: Map<string, vscode.TextEditorDecorationType> = new Map();
  private currentDecorations: vscode.DecorationOptions[] = [];
  private lastPhase = 'inhale';
  private lastToneform = 'practical';

  constructor(context: vscode.ExtensionContext) {
    this.context = context;
    this.config = vscode.workspace.getConfiguration('spiral');
    this.initializeDecorationTypes();
  }

  private initializeDecorationTypes(): void {
    // Phase-based decorations
    const phaseDecorations = {
      inhale: {
        backgroundColor: 'rgba(0, 255, 255, 0.1)',
        borderColor: 'rgba(0, 255, 255, 0.3)',
        borderStyle: 'solid',
        borderWidth: '1px',
      },
      hold: {
        backgroundColor: 'rgba(255, 192, 203, 0.1)',
        borderColor: 'rgba(255, 192, 203, 0.3)',
        borderStyle: 'solid',
        borderWidth: '1px',
      },
      exhale: {
        backgroundColor: 'rgba(75, 0, 130, 0.1)',
        borderColor: 'rgba(75, 0, 130, 0.3)',
        borderStyle: 'solid',
        borderWidth: '1px',
      },
      return: {
        backgroundColor: 'rgba(255, 215, 0, 0.1)',
        borderColor: 'rgba(255, 215, 0, 0.3)',
        borderStyle: 'solid',
        borderWidth: '1px',
      },
      night_hold: {
        backgroundColor: 'rgba(128, 128, 128, 0.1)',
        borderColor: 'rgba(128, 128, 128, 0.3)',
        borderStyle: 'solid',
        borderWidth: '1px',
      },
    };

    // Create decoration types for each phase
    Object.entries(phaseDecorations).forEach(([phase, style]) => {
      const decorationType = vscode.window.createTextEditorDecorationType({
        backgroundColor: style.backgroundColor,
        border: `${style.borderWidth} ${style.borderStyle} ${style.borderColor}`,
        borderRadius: '2px',
      });
      this.decorationTypes.set(phase, decorationType);
    });

    // Toneform-based decorations
    const toneformDecorations = {
      practical: {
        backgroundColor: 'rgba(0, 128, 0, 0.05)',
        borderColor: 'rgba(0, 128, 0, 0.2)',
      },
      emotional: {
        backgroundColor: 'rgba(255, 0, 0, 0.05)',
        borderColor: 'rgba(255, 0, 0, 0.2)',
      },
      intellectual: {
        backgroundColor: 'rgba(0, 0, 255, 0.05)',
        borderColor: 'rgba(0, 0, 255, 0.2)',
      },
      spiritual: {
        backgroundColor: 'rgba(128, 0, 128, 0.05)',
        borderColor: 'rgba(128, 0, 128, 0.2)',
      },
      relational: {
        backgroundColor: 'rgba(255, 165, 0, 0.05)',
        borderColor: 'rgba(255, 165, 0, 0.2)',
      },
    };

    // Create decoration types for each toneform
    Object.entries(toneformDecorations).forEach(([toneform, style]) => {
      const decorationType = vscode.window.createTextEditorDecorationType({
        backgroundColor: style.backgroundColor,
        border: `1px solid ${style.borderColor}`,
        borderRadius: '1px',
      });
      this.decorationTypes.set(`toneform_${toneform}`, decorationType);
    });
  }

  public updateFromGlint(glint: GlintData): void {
    if (!this.config.get('enableVisuals', true)) {
      return;
    }

    const phase = glint.phase || this.lastPhase;
    const toneform = glint.toneform || this.lastToneform;

    // Update phase visualization
    if (phase !== this.lastPhase) {
      this.updatePhaseVisualization(phase);
      this.lastPhase = phase;
    }

    // Update toneform visualization
    if (toneform !== this.lastToneform) {
      this.updateToneformVisualization(toneform);
      this.lastToneform = toneform;
    }

    // Add glint-specific decoration if content is present
    if (glint.content) {
      this.addGlintDecoration(glint);
    }
  }

  private updatePhaseVisualization(phase: string): void {
    const activeEditor = vscode.window.activeTextEditor;
    if (!activeEditor) {
      return;
    }

    // Clear previous phase decorations
    this.clearPhaseDecorations();

    // Apply new phase decoration to the entire document
    const decorationType = this.decorationTypes.get(phase);
    if (decorationType) {
      const range = new vscode.Range(
        activeEditor.document.positionAt(0),
        activeEditor.document.positionAt(activeEditor.document.getText().length)
      );

      activeEditor.setDecorations(decorationType, [
        {
          range: range,
          hoverMessage: `Breath Phase: ${phase}`,
        },
      ]);
    }
  }

  private updateToneformVisualization(toneform: string): void {
    const activeEditor = vscode.window.activeTextEditor;
    if (!activeEditor) {
      return;
    }

    // Clear previous toneform decorations
    this.clearToneformDecorations();

    // Apply new toneform decoration to the entire document
    const decorationType = this.decorationTypes.get(`toneform_${toneform}`);
    if (decorationType) {
      const range = new vscode.Range(
        activeEditor.document.positionAt(0),
        activeEditor.document.positionAt(activeEditor.document.getText().length)
      );

      activeEditor.setDecorations(decorationType, [
        {
          range: range,
          hoverMessage: `Toneform: ${toneform}`,
        },
      ]);
    }
  }

  private addGlintDecoration(glint: GlintData): void {
    const activeEditor = vscode.window.activeTextEditor;
    if (!activeEditor) {
      return;
    }

    // Create a temporary decoration for the glint
    const glintDecorationType = vscode.window.createTextEditorDecorationType({
      backgroundColor: 'rgba(255, 255, 0, 0.2)',
      border: '1px solid rgba(255, 255, 0, 0.5)',
      borderRadius: '2px',
    });

    // Apply decoration to the current line
    const currentLine = activeEditor.selection.active.line;
    const range = new vscode.Range(
      new vscode.Position(currentLine, 0),
      new vscode.Position(currentLine, activeEditor.document.lineAt(currentLine).text.length)
    );

    activeEditor.setDecorations(glintDecorationType, [
      {
        range: range,
        hoverMessage: `Glint: ${glint.content}`,
      },
    ]);

    // Remove decoration after a short delay
    setTimeout(() => {
      glintDecorationType.dispose();
    }, 2000);
  }

  private clearPhaseDecorations(): void {
    const activeEditor = vscode.window.activeTextEditor;
    if (!activeEditor) {
      return;
    }

    // Clear all phase decorations
    ['inhale', 'hold', 'exhale', 'return', 'night_hold'].forEach((phase) => {
      const decorationType = this.decorationTypes.get(phase);
      if (decorationType) {
        activeEditor.setDecorations(decorationType, []);
      }
    });
  }

  private clearToneformDecorations(): void {
    const activeEditor = vscode.window.activeTextEditor;
    if (!activeEditor) {
      return;
    }

    // Clear all toneform decorations
    ['practical', 'emotional', 'intellectual', 'spiritual', 'relational'].forEach((toneform) => {
      const decorationType = this.decorationTypes.get(`toneform_${toneform}`);
      if (decorationType) {
        activeEditor.setDecorations(decorationType, []);
      }
    });
  }

  public clearAllDecorations(): void {
    const activeEditor = vscode.window.activeTextEditor;
    if (!activeEditor) {
      return;
    }

    // Clear all decorations
    this.decorationTypes.forEach((decorationType) => {
      activeEditor.setDecorations(decorationType, []);
    });
  }

  public dispose(): void {
    // Dispose all decoration types
    this.decorationTypes.forEach((decorationType) => {
      decorationType.dispose();
    });
    this.decorationTypes.clear();
  }
}
