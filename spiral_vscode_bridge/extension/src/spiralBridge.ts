import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';
import * as http from 'http';

interface GlintData {
  id?: string;
  phase?: string;
  toneform?: string;
  content?: string;
  timestamp?: string;
  [key: string]: any;
}

interface WorkspaceData {
  timestamp: string;
  current_phase: string;
  current_toneform: string;
  connection_status: string;
  recent_glints: GlintData[];
  cache_size: number;
  spiral_signature: string;
}

export class SpiralBridge {
  private context: vscode.ExtensionContext;
  private config: vscode.WorkspaceConfiguration;
  private workspaceFile: string;

  // State
  private currentPhase = 'inhale';
  private currentToneform = 'practical';
  private connected = false;

  // Callbacks
  private onPhaseChangedCallback?: (phase: string) => void;
  private onToneformChangedCallback?: (toneform: string) => void;
  private onGlintReceivedCallback?: (glint: GlintData) => void;
  private onConnectionChangedCallback?: (connected: boolean) => void;

  // File watcher
  private fileWatcher?: vscode.FileSystemWatcher;
  private lastFileContent = '';

  constructor(context: vscode.ExtensionContext) {
    this.context = context;
    this.config = vscode.workspace.getConfiguration('spiral');
    this.workspaceFile = path.join(
      vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || '',
      'spiral.workspace.json'
    );

    this.setupFileWatcher();
  }

  public start(): void {
    console.log('🌀 Starting Spiral Bridge...');
    this.updateFromWorkspaceFile();
  }

  public stop(): void {
    console.log('🌙 Stopping Spiral Bridge...');
    if (this.fileWatcher) {
      this.fileWatcher.dispose();
    }
  }

  public showStatus(): void {
    const status = this.getStatus();
    vscode.window.showInformationMessage(
      `Spiral Status: ${this.connected ? 'Connected' : 'Disconnected'}\n` +
        `Phase: ${status.current_phase}\n` +
        `Toneform: ${status.current_toneform}\n` +
        `Cache: ${status.cache_size} glints`
    );
  }

  public async invokeRitual(ritualName: string, parameters: any = {}): Promise<void> {
    try {
      const host = this.config.get('host', 'localhost');
      const port = this.config.get('port', 5000);

      const payload = {
        ritual_name: ritualName,
        parameters: parameters,
      };

      const options = {
        hostname: host,
        port: port,
        path: '/api/invoke_ritual',
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      };

      const req = http.request(options, (res) => {
        let data = '';
        res.on('data', (chunk) => {
          data += chunk;
        });
        res.on('end', () => {
          try {
            const result = JSON.parse(data);
            if (result.success) {
              vscode.window.showInformationMessage(`🔮 Ritual invoked: ${ritualName}`);
            } else {
              vscode.window.showErrorMessage(
                `Failed to invoke ritual: ${result.error || 'Unknown error'}`
              );
            }
          } catch (e) {
            vscode.window.showErrorMessage('Invalid response from Spiral server');
          }
        });
      });

      req.on('error', (error) => {
        vscode.window.showErrorMessage(`Connection error: ${error.message}`);
      });

      req.write(JSON.stringify(payload));
      req.end();
    } catch (error) {
      vscode.window.showErrorMessage(`Failed to invoke ritual: ${error}`);
    }
  }

  public updateFromWorkspaceFile(): void {
    try {
      if (!fs.existsSync(this.workspaceFile)) {
        return;
      }

      const content = fs.readFileSync(this.workspaceFile, 'utf8');
      if (content === this.lastFileContent) {
        return; // No change
      }

      this.lastFileContent = content;
      const data: WorkspaceData = JSON.parse(content);

      // Update state
      const phaseChanged = data.current_phase !== this.currentPhase;
      const toneformChanged = data.current_toneform !== this.currentToneform;
      const connectionChanged = (data.connection_status === 'connected') !== this.connected;

      this.currentPhase = data.current_phase;
      this.currentToneform = data.current_toneform;
      this.connected = data.connection_status === 'connected';

      // Trigger callbacks
      if (phaseChanged && this.onPhaseChangedCallback) {
        this.onPhaseChangedCallback(this.currentPhase);
      }

      if (toneformChanged && this.onToneformChangedCallback) {
        this.onToneformChangedCallback(this.currentToneform);
      }

      if (connectionChanged && this.onConnectionChangedCallback) {
        this.onConnectionChangedCallback(this.connected);
      }

      // Process recent glints
      if (data.recent_glints && this.onGlintReceivedCallback) {
        const newGlints = data.recent_glints.slice(-1); // Only process the latest
        for (const glint of newGlints) {
          this.onGlintReceivedCallback(glint);
        }
      }
    } catch (error) {
      console.error('Error reading workspace file:', error);
    }
  }

  private setupFileWatcher(): void {
    if (vscode.workspace.workspaceFolders) {
      this.fileWatcher = vscode.workspace.createFileSystemWatcher(this.workspaceFile);
      this.fileWatcher.onDidChange(() => {
        this.updateFromWorkspaceFile();
      });
    }
  }

  public getStatus(): WorkspaceData {
    return {
      timestamp: new Date().toISOString(),
      current_phase: this.currentPhase,
      current_toneform: this.currentToneform,
      connection_status: this.connected ? 'connected' : 'disconnected',
      recent_glints: [],
      cache_size: 0,
      spiral_signature: '🌀 vscode.bridge.status',
    };
  }

  // Callback setters
  public onPhaseChanged(callback: (phase: string) => void): void {
    this.onPhaseChangedCallback = callback;
  }

  public onToneformChanged(callback: (toneform: string) => void): void {
    this.onToneformChangedCallback = callback;
  }

  public onGlintReceived(callback: (glint: GlintData) => void): void {
    this.onGlintReceivedCallback = callback;
  }

  public onConnectionChanged(callback: (connected: boolean) => void): void {
    this.onConnectionChangedCallback = callback;
  }

  public dispose(): void {
    this.stop();
  }
}
