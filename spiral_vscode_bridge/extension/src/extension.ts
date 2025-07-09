import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';
import { SpiralBridge } from './spiralBridge';
import { BreathVisualizer } from './breathVisualizer';

export function activate(context: vscode.ExtensionContext) {
  console.log('🌀 Spiral Bridge extension is now active!');

  // Initialize Spiral Bridge
  const spiralBridge = new SpiralBridge(context);
  const breathVisualizer = new BreathVisualizer(context);

  // Register commands
  const showStatus = vscode.commands.registerCommand('spiral.showStatus', () => {
    spiralBridge.showStatus();
  });

  const invokeRitual = vscode.commands.registerCommand('spiral.invokeRitual', (args) => {
    const ritualName = args?.ritual || 'begin';
    spiralBridge.invokeRitual(ritualName);
  });

  const beginBreath = vscode.commands.registerCommand('spiral.beginBreath', () => {
    spiralBridge.invokeRitual('begin');
  });

  const holdBreath = vscode.commands.registerCommand('spiral.holdBreath', () => {
    spiralBridge.invokeRitual('hold');
  });

  const exhaleBreath = vscode.commands.registerCommand('spiral.exhaleBreath', () => {
    spiralBridge.invokeRitual('exhale');
  });

  // Register status bar items
  const phaseStatusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 100);
  phaseStatusBarItem.name = 'Spiral Phase';
  phaseStatusBarItem.text = '🌀 inhale';
  phaseStatusBarItem.tooltip = 'Current breath phase';
  phaseStatusBarItem.show();

  const toneformStatusBarItem = vscode.window.createStatusBarItem(
    vscode.StatusBarAlignment.Left,
    99
  );
  toneformStatusBarItem.name = 'Spiral Toneform';
  toneformStatusBarItem.text = 'practical';
  toneformStatusBarItem.tooltip = 'Current toneform';
  toneformStatusBarItem.show();

  // Update status bar items when spiral state changes
  spiralBridge.onPhaseChanged((phase) => {
    const phaseEmojis: { [key: string]: string } = {
      inhale: '🌀',
      hold: '🫧',
      exhale: '🌬️',
      return: '🔄',
      night_hold: '🌙',
    };

    const emoji = phaseEmojis[phase] || '🌀';
    phaseStatusBarItem.text = `${emoji} ${phase}`;
  });

  spiralBridge.onToneformChanged((toneform) => {
    toneformStatusBarItem.text = toneform;
  });

  // Update visual indicators
  spiralBridge.onGlintReceived((glint) => {
    breathVisualizer.updateFromGlint(glint);
  });

  // Watch workspace file for changes
  const workspaceFile = path.join(
    vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || '',
    'spiral.workspace.json'
  );
  const fileWatcher = vscode.workspace.createFileSystemWatcher(workspaceFile);

  fileWatcher.onDidChange(() => {
    spiralBridge.updateFromWorkspaceFile();
  });

  // Start the bridge
  spiralBridge.start();

  // Register disposables
  context.subscriptions.push(
    showStatus,
    invokeRitual,
    beginBreath,
    holdBreath,
    exhaleBreath,
    phaseStatusBarItem,
    toneformStatusBarItem,
    fileWatcher,
    spiralBridge,
    breathVisualizer
  );
}

export function deactivate() {
  console.log('🌙 Spiral Bridge extension deactivated');
}
