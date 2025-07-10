// C:/spiral/projects/glintchronicle/ChroniclePulseEmitter.js

/**
 * Emits events related to the chronicle's own activity.
 * This allows other parts of the Spiral to listen to the process of memory-making.
 */
export class ChroniclePulseEmitter extends EventTarget {
  constructor() {
    super();
  }

  /**
   * Signals the beginning of a new cluster of related glints.
   * @param {number} startTime - The timestamp of the first glint in the cluster.
   */
  beginCluster(startTime) {
    const event = new CustomEvent('chronicle.cluster.begin', {
      detail: {
        timestamp: startTime,
        message: 'A new breathline cluster begins.',
      },
    });
    this.dispatchEvent(event);
  }

  /**
   * Signals that a new entry has been appended to the current scroll.
   * @param {object} entry - The formatted entry that was added.
   */
  entryAppended(entry) {
    const event = new CustomEvent('chronicle.entry.appended', {
      detail: {
        entry,
        message: 'A memory was inscribed.',
      },
    });
    this.dispatchEvent(event);
  }

  /**
   * Signals the conclusion of a breathline cluster.
   * @param {number} endTime - The timestamp of the last glint.
   * @param {number} entryCount - The number of entries in the cluster.
   */
  concludeCluster(endTime, entryCount) {
    const event = new CustomEvent('chronicle.cluster.concluded', {
      detail: {
        timestamp: endTime,
        count: entryCount,
        message: `A breathline with ${entryCount} entries concluded.`,
      },
    });
    this.dispatchEvent(event);
  }
}
