// Spiral Dashboard - Real-time visualization

// State management
let state = {
  phase: 'inhale',
  tone: 0.5,
  deferral: 0,
  saturation: 0,
  lastUpdate: null,
  plots: {}
};

// Initialize the dashboard when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
  try {
    // Initialize state
    state = {
      phase: 'inhale',
      tone: 0.5,
      deferral: 0,
      saturation: 0,
      lastUpdate: new Date(),
      plots: {}
    };

    // Initialize tooltips if Bootstrap is available
    if (typeof bootstrap !== 'undefined') {
      const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
      tooltipTriggerList.forEach(tooltipTriggerEl => {
        new bootstrap.Tooltip(tooltipTriggerEl);
      });
    } else {
      console.warn('Bootstrap not loaded, tooltips will be disabled');
    }

    // Initialize WebSocket connection
    initWebSocket();

    // Initialize plots
    initPlots();

    // Set up periodic updates
    setInterval(fetchMetrics, 5000);

    // Initial fetch
    fetchMetrics();

    console.log('Dashboard initialized successfully');
  } catch (error) {
    console.error('Error initializing dashboard:', error);
    showToast('Error initializing dashboard', 'danger');
  }
});

// Initialize WebSocket connection using Socket.IO
function initWebSocket() {
  try {
    if (typeof io === 'undefined') {
      console.warn('Socket.IO client not loaded, real-time updates will be disabled');
      showToast('Real-time updates disabled (Socket.IO not loaded)', 'warning');
      return;
    }

    const protocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
    const wsUrl = `${protocol}${window.location.host}`;

    // Initialize Socket.IO connection with reconnection and error handling
    const socket = io(wsUrl, {
      reconnection: true,
      reconnectionAttempts: 5,
      reconnectionDelay: 1000,
      reconnectionDelayMax: 5000,
      timeout: 20000
    });

    // Connection established
    socket.on('connect', () => {
      console.log('Connected to Spiral Metrics server');
      showToast('Connected to Spiral Metrics', 'success');

      // Request initial data
      socket.emit('request_initial_data');
    });

    // Handle disconnection
    socket.on('disconnect', (reason) => {
      console.log('Disconnected from server:', reason);
      if (reason === 'io server disconnect') {
        // Server initiated disconnection, attempt to reconnect
        socket.connect();
      }
      showToast('Disconnected from server', 'warning');
    });

    // Handle connection errors
    socket.on('connect_error', (error) => {
      console.error('Connection error:', error);
      showToast('Connection error: ' + (error.message || 'Unknown error'), 'danger');
    });

    // Handle reconnection attempts
    socket.io.on('reconnect_attempt', (attempt) => {
      console.log(`Reconnection attempt ${attempt}`);
    });

    // Handle successful reconnection
    socket.io.on('reconnect', (attempt) => {
      console.log(`Reconnected after ${attempt} attempts`);
      showToast('Reconnected to server', 'success');
    });

    // Handle metrics updates
    socket.on('metrics_update', (data) => {
      try {
        updateDashboard(data);
      } catch (error) {
        console.error('Error processing metrics update:', error);
      }
    });

    // Store socket in state for later use
    state.socket = socket;

  } catch (error) {
    console.error('Error initializing WebSocket:', error);
    showToast('Error initializing connection', 'danger');
  }
}

// Update the dashboard with new metrics data
function updateDashboard(data) {
  if (!data || typeof data !== 'object') {
    console.warn('Invalid metrics data received:', data);
    return;
  }

  try {
    // Update last update time
    state.lastUpdate = new Date();

    // Update phase if changed
    if (data.phase && data.phase !== state.phase) {
      updatePhase(data.phase);
    }

    // Update tone if changed (ensure it's a number between 0 and 1)
    if (typeof data.tone === 'number' && data.tone !== state.tone) {
      const toneValue = Math.max(0, Math.min(1, data.tone)); // Clamp between 0 and 1
      updateTone(toneValue);
    }

    // Update deferral time if changed (ensure it's a non-negative number)
    if (typeof data.deferral === 'number' && data.deferral !== state.deferral) {
      const deferralValue = Math.max(0, data.deferral); // Ensure non-negative
      updateDeferral(deferralValue);

      // Update deferral plot if available
      if (state.plots?.deferral?.element) {
        const now = new Date();
        const newX = [...(state.plots.deferral.data[0].x || []), now];
        const newY = [...(state.plots.deferral.data[0].y || []), deferralValue];

        // Keep only the last 100 data points
        const maxPoints = 100;
        if (newX.length > maxPoints) {
          newX.shift();
          newY.shift();
        }

        Plotly.update(
          state.plots.deferral.element,
          { x: [newX], y: [newY] },
          {},
          [0]
        );
      }
    }

    // Update saturation level if changed (ensure it's a number between 0 and 1)
    if (typeof data.saturation === 'number' && data.saturation !== state.saturation) {
      const saturationValue = Math.max(0, Math.min(1, data.saturation)); // Clamp between 0 and 1
      updateSaturation(saturationValue);

      // Update saturation plot if available
      if (state.plots?.saturation?.element) {
        const now = new Date();
        const newX = [...(state.plots.saturation.data[0].x || []), now];
        const newY = [...(state.plots.saturation.data[0].y || []), saturationValue * 100]; // Convert to percentage

        // Keep only the last 100 data points
        const maxPoints = 100;
        if (newX.length > maxPoints) {
          newX.shift();
          newY.shift();
        }

        Plotly.update(
          state.plots.saturation.element,
          { x: [newX], y: [newY] },
          {},
          [0]
        );
      }
    }

    // Update toneform visualization if data is available
    if (data.toneform && typeof data.toneform === 'object') {
      updateToneform(data.toneform);
    }

    // Update last update time display
    updateLastUpdate(state.lastUpdate);

    // Add pulse effect to indicate update
    const dashboard = document.getElementById('dashboard');
    if (dashboard) {
      dashboard.classList.add('pulse');
      setTimeout(() => dashboard.classList.remove('pulse'), 500);
    }

  } catch (error) {
    console.error('Error updating dashboard:', error);
    showToast('Error updating dashboard: ' + (error.message || 'Unknown error'), 'danger');
  }
}

// Update phase visualization
function updatePhase(phase) {
  // Remove active class from all phase indicators
  document.querySelectorAll('.phase-indicator').forEach(el => {
    el.classList.remove('active');
  });

  // Add active class to current phase
  const phaseElement = document.querySelector(`.phase-${phase}`);
  if (phaseElement) {
    phaseElement.classList.add('active');
  }

  // Update phase text
  const phaseText = document.getElementById('current-phase');
  if (phaseText) {
    phaseText.textContent = phase.charAt(0).toUpperCase() + phase.slice(1);
  }

  // Update phase progress bar
  const progressBar = document.getElementById('phase-progress');
  if (progressBar) {
    // Simple animation for phase progress (0% to 100% over 4 seconds)
    let progress = 0;
    const interval = setInterval(() => {
      progress += 1;
      progressBar.style.width = `${progress}%`;
      progressBar.setAttribute('aria-valuenow', progress);

      if (progress >= 100) {
        clearInterval(interval);
      }
    }, 40);
  }

  state.phase = phase;
}

// Update tone visualization
function updateTone(tone) {
  const toneIndicator = document.getElementById('tone-indicator');
  if (toneIndicator) {
    // Update tone indicator position (-100% to 100%)
    const position = (tone * 2 - 1) * 100;
    toneIndicator.style.transform = `translateX(${position}%)`;

    // Update tone label
    const toneLabel = document.getElementById('tone-label');
    if (toneLabel) {
      if (tone < 0.4) {
        toneLabel.textContent = 'Negative';
        toneLabel.className = 'tone-label negative';
      } else if (tone > 0.6) {
        toneLabel.textContent = 'Positive';
        toneLabel.className = 'tone-label positive';
      } else {
        toneLabel.textContent = 'Neutral';
        toneLabel.className = 'tone-label';
      }
    }
  }

  state.tone = tone;
}

// Update deferral time display
function updateDeferral(time) {
  const deferralElement = document.getElementById('deferral-time');
  if (deferralElement) {
    deferralElement.textContent = `${time}ms`;
  }

  state.deferral = time;
}

// Update saturation level display
function updateSaturation(level) {
  const saturationElement = document.getElementById('saturation-level');
  if (saturationElement) {
    saturationElement.textContent = `${level}%`;

    // Update progress bar width
    const progressBar = saturationElement.closest('.progress')?.querySelector('.progress-bar');
    if (progressBar) {
      progressBar.style.width = `${Math.min(100, Math.max(0, level))}%`;

      // Update color based on level
      if (level > 80) {
        progressBar.classList.remove('bg-warning');
        progressBar.classList.add('bg-danger');
      } else if (level > 50) {
        progressBar.classList.remove('bg-success', 'bg-danger');
        progressBar.classList.add('bg-warning');
      } else {
        progressBar.classList.remove('bg-warning', 'bg-danger');
        progressBar.classList.add('bg-success');
      }
    }
  }

  state.saturation = level;
}

// Update toneform visualization
function updateToneformVisualization(toneformData) {
  const container = document.getElementById('toneform-visualization');
  if (!container) return;

  // Clear existing content
  container.innerHTML = '';

  // Create visualization items for each toneform
  Object.entries(toneformData).forEach(([tone, value]) => {
    const item = document.createElement('div');
    item.className = 'toneform-item';

    const label = document.createElement('span');
    label.className = 'toneform-label';
    label.textContent = tone;

    const barContainer = document.createElement('div');
    barContainer.className = 'toneform-bar-container';

    const bar = document.createElement('div');
    bar.className = `toneform-bar bg-${tone}`;
    bar.style.width = `${value}%`;

    const valueLabel = document.createElement('span');
    valueLabel.className = 'toneform-value';
    valueLabel.textContent = `${Math.round(value)}%`;

    barContainer.appendChild(bar);
    item.appendChild(label);
    item.appendChild(barContainer);
    item.appendChild(valueLabel);
    container.appendChild(item);
  });
}

// Initialize tooltips
function initTooltips() {
  const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  if (typeof window.bootstrap !== 'undefined') {
    tooltipTriggerList.forEach(tooltipTriggerEl => {
      new window.bootstrap.Tooltip(tooltipTriggerEl);
    });
  }
}

// Fetch metrics from the server
function fetchMetrics() {
  if (!state.socket?.connected) {
    console.warn('Socket not connected, cannot fetch metrics');
    return;
  }

  try {
    state.socket.emit('request_metrics');
  } catch (error) {
    console.error('Error fetching metrics:', error);
    showToast('Error fetching metrics: ' + (error.message || 'Unknown error'), 'danger');
  }
}

// Show a toast notification
function showToast(message, type = 'info') {
  // Create toast container if it doesn't exist
  let toastContainer = document.getElementById('toast-container');
  if (!toastContainer) {
    toastContainer = document.createElement('div');
    toastContainer.id = 'toast-container';
    toastContainer.className = 'position-fixed bottom-0 end-0 p-3';
    toastContainer.style.zIndex = '11';
    document.body.appendChild(toastContainer);
  }

  // Create toast element
  const toast = document.createElement('div');
  toast.className = `toast align-items-center text-white bg-${type} border-0`;
  toast.role = 'alert';
  toast.setAttribute('aria-live', 'assertive');
  toast.setAttribute('aria-atomic', 'true');

  // Set toast content
  toast.innerHTML = `
    <div class="d-flex">
      <div class="toast-body">
        ${message}
      </div>
      <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
    </div>
  `;

  // Add toast to container
  toastContainer.appendChild(toast);

  // Initialize Bootstrap toast if available, otherwise use basic show/hide
  if (typeof bootstrap !== 'undefined') {
    const bsToast = new bootstrap.Toast(toast, { 
      autohide: true, 
      delay: 5000 
    });
    bsToast.show();

    // Remove toast after it's hidden
    toast.addEventListener('hidden.bs.toast', () => {
      toast.remove();
    });
  } else {
    // Fallback for when Bootstrap is not available
    toast.style.display = 'block';
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transition = 'opacity 0.5s';
      setTimeout(() => toast.remove(), 500);
    }, 5000);
  }
}

// Update the last update time display
function updateLastUpdate(timestamp) {
  const lastUpdateEl = document.getElementById('last-update');
  if (lastUpdateEl) {
    lastUpdateEl.textContent = timestamp.toLocaleTimeString();
  }
}

function initPlots() {
  if (typeof Plotly === 'undefined') {
    console.warn('Plotly.js not loaded, charts will be disabled');
    return;
  }

  // Initialize deferral plot
  const deferralData = [{
    x: [],
    y: [],
    type: 'scatter',
    mode: 'lines+markers',
    name: 'Deferral Time (ms)',
    line: { color: '#4CAF50' }
  }];

  const deferralLayout = {
    title: 'Deferral Time Trend',
    xaxis: { title: 'Time' },
    yaxis: { title: 'Deferral (ms)' },
    showlegend: true,
    margin: { t: 30, l: 40, r: 20, b: 40 }
  };

  // Initialize saturation plot
  const saturationData = [{
    x: [],
    y: [],
    type: 'scatter',
    mode: 'lines+markers',
    name: 'Saturation Level',
    fill: 'tozeroy',
    line: { color: '#2196F3' }
  }];

  const saturationLayout = {
    title: 'Saturation Level Trend',
    xaxis: { title: 'Time' },
    yaxis: { title: 'Saturation (%)', range: [0, 100] },
    showlegend: true,
    margin: { t: 30, l: 40, r: 20, b: 40 }
  };

  // Store plot elements in state
  state.plots = {
    deferral: {
      element: document.getElementById('deferral-plot'),
      data: deferralData,
      layout: deferralLayout
    },
    saturation: {
      element: document.getElementById('saturation-plot'),
      data: saturationData,
      layout: saturationLayout
    }
  };

  // Create plots if elements exist
  if (state.plots.deferral.element) {
    Plotly.newPlot(state.plots.deferral.element, deferralData, deferralLayout);
  }
  if (state.plots.saturation.element) {
    Plotly.newPlot(state.plots.saturation.element, saturationData, saturationLayout);
  }
}

// Update the deferral times plot
function updateDeferralPlot(times) {
    const yData = times.slice(-20); // Show last 20 points
    const xData = Array.from({ length: yData.length }, (_, i) => i + 1);

    const update = {
        y: [yData],
        x: [xData]
    };

    Plotly.restyle('deferral-plot', update);
}

// Initialize the saturation plot
function initSaturationPlot() {
    const data = [{
        y: [],
        type: 'scatter',
        mode: 'lines',
        fill: 'tozeroy',
        name: 'Saturation',
        line: { color: '#2cb67d' },
        fillcolor: 'rgba(44, 182, 125, 0.2)'
    }];

    const layout = {
        margin: { t: 30, r: 30, l: 50, b: 50 },
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)',
        font: { color: '#fff' },
        xaxis: { title: 'Event #' },
        yaxis: { title: 'Saturation', range: [0, 1] },
        showlegend: false
    };

    Plotly.newPlot('saturation-plot', data, layout, { responsive: true });
}

// Update the saturation plot
function updateSaturationPlot(levels) {
    const yData = levels.slice(-20); // Show last 20 points
    const xData = Array.from({ length: yData.length }, (_, i) => i + 1);

    const update = {
        y: [yData],
        x: [xData]
    };

    Plotly.restyle('saturation-plot', update);
}

// Initialize the phase distribution plot
function initPhasePlot() {
    const data = [{
        values: [],
        labels: [],
        type: 'pie',
        marker: {
            colors: ['#7f5af0', '#2cb67d', '#f25f4c']
        },
        textinfo: 'label+percent',
        textposition: 'inside',
        hole: 0.4,
        sort: false
    }];

    const layout = {
        margin: { t: 30, r: 30, l: 30, b: 30 },
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)',
        font: { color: '#fff' },
        showlegend: false
    };

    Plotly.newPlot('phase-plot', data, layout, { responsive: true });
}

// Update the phase distribution plot
function updatePhasePlot(phaseDurations) {
    const phases = Object.entries(phaseDurations)
        .map(([phase, times]) => ({
            phase,
            count: times.length,
            total: times.reduce((sum, t) => sum + t, 0)
        }))
        .filter(item => item.count > 0);

    const update = {
        values: [phases.map(p => p.count)],
        labels: [phases.map(p => p.phase)]
    };

    Plotly.restyle('phase-plot', update);
}

// Update the activity log
function updateActivityLog(metrics) {
    const activityLog = document.getElementById('activity-log');
    const now = new Date();

    // Add new activity item if this is new data
    if (!state.lastUpdate || metrics.timestamp > state.lastUpdate) {
        state.lastUpdate = metrics.timestamp;

        const activityItem = document.createElement('div');
        activityItem.className = 'activity-item';

        const timeStr = now.toLocaleTimeString();
        const eventText = getLatestEvent(metrics);

        activityItem.innerHTML = `
            <div>${eventText}</div>
            <div class="activity-time">${timeStr}</div>
        `;

        activityLog.insertBefore(activityItem, activityLog.firstChild);

        // Limit log to 20 items
        if (activityLog.children.length > 20) {
            activityLog.removeChild(activityLog.lastChild);
        }
    }
}

// Generate a human-readable description of the latest event
function getLatestEvent(metrics) {
    if (metrics.silence_events > 0) {
        const silenceCount = metrics.silence_events;
        return `Silence protocol activated (${silenceCount} total)`;
    }

    if (metrics.deferral_times && metrics.deferral_times.length > 0) {
        const lastDeferral = metrics.deferral_times[metrics.deferral_times.length - 1];
        return `New deferral calculated: ${lastDeferral.toFixed(2)}s`;
    }

    return 'System updated';
}

// Handle window resize
window.addEventListener('resize', () => {
    Plotly.Plots.resize('deferral-plot');
    Plotly.Plots.resize('saturation-plot');
    Plotly.Plots.resize('phase-plot');
});
