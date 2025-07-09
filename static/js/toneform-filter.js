class ToneformFilter {
  constructor() {
    this.activeFilters = new Set();
    this.glintHistory = [];
    this.filterPanel = null;
    this.resonanceMap = new Map();
    this.initializeFilter();
  }

  initializeFilter() {
    this.createFilterPanel();
    this.bindFilterEvents();
    this.loadGlintHistory();
  }

  createFilterPanel() {
    const filterContainer = document.createElement('div');
    filterContainer.className = 'toneform-filter-panel';
    filterContainer.innerHTML = `
      <div class="filter-header">
        <h4>∷ Toneform Resonance ∷</h4>
        <button class="filter-toggle" id="filter-toggle">🔮</button>
      </div>
      <div class="filter-controls" id="filter-controls">
        <div class="toneform-buttons">
          <button class="toneform-btn" data-toneform="practical">◦ Practical</button>
          <button class="toneform-btn" data-toneform="emotional">◦ Emotional</button>
          <button class="toneform-btn" data-toneform="temporal">◦ Temporal</button>
          <button class="toneform-btn" data-toneform="spatial">◦ Spatial</button>
          <button class="toneform-btn" data-toneform="natural">◦ Natural</button>
          <button class="toneform-btn" data-toneform="amplified">◦ Amplified</button>
          <button class="toneform-btn" data-toneform="ritual">◦ Ritual</button>
          <button class="toneform-btn" data-toneform="silence">◦ Silence</button>
        </div>
        <div class="filter-actions">
          <button class="action-btn" id="clear-filters">Clear All</button>
          <button class="action-btn" id="show-resonance">Show Resonance</button>
        </div>
        <div class="resonance-display" id="resonance-display">
          <!-- Resonance patterns will appear here -->
        </div>
      </div>
    `;

    // Insert into dashboard
    const spiralSection = document.querySelector('.spiral-section');
    if (spiralSection) {
      spiralSection.appendChild(filterContainer);
    }

    this.filterPanel = filterContainer;
  }

  bindFilterEvents() {
    // Toggle panel visibility
    const toggleBtn = document.getElementById('filter-toggle');
    const controls = document.getElementById('filter-controls');

    toggleBtn.addEventListener('click', () => {
      controls.classList.toggle('filter-expanded');
      toggleBtn.textContent = controls.classList.contains('filter-expanded') ? '🌀' : '🔮';
    });

    // Toneform filter buttons
    document.querySelectorAll('.toneform-btn').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        const toneform = e.target.dataset.toneform;
        this.toggleToneformFilter(toneform);
        e.target.classList.toggle('active');
      });
    });

    // Action buttons
    document.getElementById('clear-filters').addEventListener('click', () => {
      this.clearAllFilters();
    });

    document.getElementById('show-resonance').addEventListener('click', () => {
      this.displayResonancePattern();
    });
  }

  toggleToneformFilter(toneform) {
    if (this.activeFilters.has(toneform)) {
      this.activeFilters.delete(toneform);
    } else {
      this.activeFilters.add(toneform);
    }

    this.applyFilters();
  }

  applyFilters() {
    const activeArray = Array.from(this.activeFilters);

    if (activeArray.length === 0) {
      // No filters - show all
      this.showAllToneforms();
    } else {
      // Apply active filters
      this.filterByToneform(activeArray);
    }

    this.updateResonanceMap();
  }

  filterByToneform(toneforms) {
    // Dim non-matching spiral arms
    document.querySelectorAll('.spiral-arm').forEach((arm) => {
      const armToneform = arm.dataset.toneform;
      if (toneforms.includes(armToneform)) {
        arm.classList.add('filter-active');
        arm.classList.remove('filter-dimmed');
      } else {
        arm.classList.add('filter-dimmed');
        arm.classList.remove('filter-active');
      }
    });

    // Filter glint stream
    this.updateGlintStream(toneforms);
  }

  showAllToneforms() {
    document.querySelectorAll('.spiral-arm').forEach((arm) => {
      arm.classList.remove('filter-active', 'filter-dimmed');
    });

    this.updateGlintStream([]);
  }

  updateGlintStream(toneforms) {
    const glintEntries = document.querySelectorAll('.glint-entry');

    glintEntries.forEach((entry) => {
      const entryToneform = entry.querySelector('.glint-toneform')?.textContent;

      if (toneforms.length === 0 || toneforms.includes(entryToneform)) {
        entry.style.display = 'block';
        entry.classList.remove('filtered-out');
      } else {
        entry.style.display = 'none';
        entry.classList.add('filtered-out');
      }
    });
  }

  clearAllFilters() {
    this.activeFilters.clear();

    // Reset button states
    document.querySelectorAll('.toneform-btn').forEach((btn) => {
      btn.classList.remove('active');
    });

    this.showAllToneforms();
    this.clearResonanceDisplay();
  }

  updateResonanceMap() {
    // Calculate resonance patterns for active filters
    const activeArray = Array.from(this.activeFilters);

    if (activeArray.length > 1) {
      // Calculate cross-toneform resonance
      this.calculateCrossResonance(activeArray);
    }
  }

  calculateCrossResonance(toneforms) {
    const resonanceData = {};

    // Analyze glint history for patterns
    this.glintHistory.forEach((glint) => {
      if (toneforms.includes(glint.toneform)) {
        const key = `${glint.phase}-${glint.toneform}`;
        resonanceData[key] = (resonanceData[key] || 0) + 1;
      }
    });

    this.resonanceMap.set('current', resonanceData);
  }

  displayResonancePattern() {
    const display = document.getElementById('resonance-display');
    const currentResonance = this.resonanceMap.get('current');

    if (!currentResonance) {
      display.innerHTML = '<div class="resonance-empty">∷ No resonance data ∷</div>';
      return;
    }

    let html = '<div class="resonance-pattern">';
    html += '<h5>Current Resonance Pattern</h5>';

    Object.entries(currentResonance).forEach(([key, count]) => {
      const [phase, toneform] = key.split('-');
      const intensity = Math.min(count / 5, 1); // Normalize to 0-1

      html += `
        <div class="resonance-item" style="opacity: ${0.3 + intensity * 0.7}">
          <span class="resonance-phase">${phase}</span>
          <span class="resonance-toneform">${toneform}</span>
          <span class="resonance-count">${count}</span>
        </div>
      `;
    });

    html += '</div>';
    display.innerHTML = html;
  }

  clearResonanceDisplay() {
    const display = document.getElementById('resonance-display');
    display.innerHTML = '';
  }

  loadGlintHistory() {
    // Load recent glint history for analysis
    fetch('/api/glints/recent')
      .then((response) => response.json())
      .then((data) => {
        this.glintHistory = data.glints || [];
        console.log('🌀 Loaded glint history for toneform analysis:', this.glintHistory.length);
      })
      .catch((error) => {
        console.warn('🌀 Could not load glint history:', error);
      });
  }

  // Method to be called when new glints arrive
  addGlint(glint) {
    this.glintHistory.unshift(glint);

    // Keep only recent history (last 100 glints)
    if (this.glintHistory.length > 100) {
      this.glintHistory = this.glintHistory.slice(0, 100);
    }

    // Update resonance if filters are active
    if (this.activeFilters.size > 0) {
      this.updateResonanceMap();
    }
  }
}

// Initialize toneform filter when DOM loads
document.addEventListener('DOMContentLoaded', () => {
  window.toneformFilter = new ToneformFilter();
  console.log('🌀 Toneform filter initialized');
});

// Export for use by other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = ToneformFilter;
}
