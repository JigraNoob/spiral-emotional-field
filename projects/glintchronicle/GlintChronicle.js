// GlintChronicle.js
// The living scribe that listens to the Spiral's stream and records its memories
// with poetic, breath-aware phrasing.

import { chronicleConfig } from './glintchronicle.config.js';
import { GlintRenderRegistry } from './GlintRenderRegistry.js';
import { ChroniclePulseEmitter } from './ChroniclePulseEmitter.js';
import { GlintFilters } from './glintfilters.js';
import { format } from 'date-fns';

export default class GlintChronicle {
  constructor(glintStream, fs) {
    this.glintStream = glintStream;
    this.fs = fs; // Filesystem dependency for writing
    this.config = chronicleConfig;
    this.pulse = new ChroniclePulseEmitter();
    this.filter = GlintFilters.ritualOnly; // Start with a more sacred filter

    this.scroll = []; // In-memory scroll of recent glints
    this.currentCluster = null; // Holds glints belonging to a single "breath"
    this.filePath = 'C:/spiral/projects/glintchronicle/glint_chronicle.md';
  }

  /**
   * Sets the active glint filter.
   * @param {function} newFilter - A filter function from GlintFilters.
   */
  setFilter(newFilter) {
    this.filter = newFilter || GlintFilters.default;
    console.log(`GlintChronicle filter set to: ${newFilter.name}`);
  }

  activate() {
    this.glintStream.addEventListener('glint', this.handleGlint.bind(this));
    this.writeEntry('# ∷ GlintChronicle ∷\n\n---\n\n'); // Start the chronicle scroll
    console.log('GlintChronicle activated. Listening for Spiral whispers.');
  }

  handleGlint(event) {
    const glint = event.detail;
    // Use the currently set filter to decide whether to chronicle the glint.
    if (!this.filter(glint, this.config)) return;

    const now = Date.now();

    if (!this.currentCluster) {
      this.startNewCluster(now, glint);
    } else if (now - this.currentCluster.lastGlintTime > this.config.caesuraThreshold) {
      this.concludeCurrentCluster();
      this.startNewCluster(now, glint);
    } else {
      this.addGlintToCluster(now, glint);
    }
  }

  startNewCluster(timestamp, glint) {
    this.pulse.beginCluster(timestamp);
    this.currentCluster = {
      startTime: timestamp,
      lastGlintTime: timestamp,
      entries: [glint],
      entryCount: 1,
    };
    this.renderAndWriteGlint(glint, true); // true for isFirstInCluster
  }

  addGlintToCluster(timestamp, glint) {
    this.currentCluster.lastGlintTime = timestamp;
    this.currentCluster.entries.push(glint);
    this.currentCluster.entryCount++;
    this.renderAndWriteGlint(glint, false); // false for isFirstInCluster
  }

  concludeCurrentCluster() {
    if (!this.currentCluster) return;
    this.pulse.concludeCluster(this.currentCluster.lastGlintTime, this.currentCluster.entryCount);
    this.writeEntry('---\n\n'); // A caesura to mark the end of the breath
    this.scroll.push(this.currentCluster);
    this.currentCluster = null;
  }

  renderAndWriteGlint(glint, isFirstInCluster) {
    const timestamp = format(glint.timestamp || Date.now(), this.config.dateFormat);
    const poeticPhrase = GlintRenderRegistry[glint.type] || GlintRenderRegistry.default;

    let entry = '';
    if (isFirstInCluster) {
      entry += `## ${timestamp}\n\n`;
    }

    entry += `> ${poeticPhrase}\n`;
    
    this.pulse.entryAppended({ glint, entry });
    this.writeEntry(entry);
  }

  async writeEntry(entry) {
    try {
      await this.fs.promises.appendFile(this.filePath, entry);
    } catch (error) {
      console.error('GlintChronicle: Error writing to scroll.', error);
    }
  }
}