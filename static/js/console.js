// Initialize Socket.IO connection with error handling
let socket;
try {
    socket = io();
    
    socket.on('connect_error', (err) => {
        console.error('Connection error:', err);
        alert('Failed to connect to Spiral Console server');
    });
    
    socket.on('disconnect', (reason) => {
        console.log('Disconnected:', reason);
    });
} catch (err) {
    console.error('Socket.IO initialization failed:', err);
    alert('Spiral Console requires WebSocket support');
}

// Log styles configuration
const logStyles = {
    'bloom': { glyph: '🌱', color: '#4CAF50' },
    'breath_catch': { glyph: '🫧', color: '#00BCD4' },
    'steward': { glyph: '🌿', color: '#8BC34A' },
    'error': { glyph: '🔴', color: '#F44336' },
    'info': { glyph: '🔵', color: '#2196F3' },
    'default': { glyph: '✨', color: '#9E9E9E' }
};

document.addEventListener('DOMContentLoaded', () => {
    const logViewer = document.getElementById('log-viewer');
    const filterType = document.getElementById('filter-type');
    const autoScrollCheckbox = document.getElementById('auto-scroll');
    let logs = [];
    let lastReceivedLogId = 0;
    
    // Batch processing variables
    let logBatch = [];
    let isRendering = false;
    
    const processBatch = () => {
        if (logBatch.length === 0 || isRendering) return;
        
        isRendering = true;
        const fragment = document.createDocumentFragment();
        
        logBatch.forEach(data => {
            const style = logStyles[data.event_type] || logStyles['default'];
            const logEntry = document.createElement('div');
            logEntry.className = `log-entry ${data.event_type}`;
            logEntry.style.color = style.color;
            
            let contextHtml = data.context ? `<span class="context">(Context: ${data.context})</span>` : '';
            logEntry.innerHTML = `
                <span class="glyph">${style.glyph}</span>
                <span class="timestamp">[${data.timestamp}]</span>
                <span class="type">${data.event_type.toUpperCase()}</span>
                <span class="message">${data.message}</span>
                ${contextHtml}
            `;
            
            fragment.appendChild(logEntry);
        });
        
        logViewer.appendChild(fragment);
        if (autoScrollCheckbox.checked) {
            logViewer.scrollTop = logViewer.scrollHeight;
        }
        
        logBatch = [];
        isRendering = false;
    };
    
    // Batch SocketIO events
    socket.on('log_event', function(data) {
        logBatch.push(data);
        
        // Process batch every 100ms or when reaching 10 entries
        if (logBatch.length >= 10) {
            processBatch();
        } else if (!isRendering) {
            setTimeout(processBatch, 100);
        }
    });

    // Test button handler
    document.getElementById('test-log').addEventListener('click', () => {
        socket.emit('request_test_log');
    });

    // Handle test log response
    socket.on('test_log_response', (data) => {
        const style = logStyles[data.event_type] || logStyles['default'];
        
        const logEntry = document.createElement('div');
        logEntry.className = `log-entry ${data.event_type}`;
        logEntry.style.color = style.color;
        
        logEntry.innerHTML = `
            <span class="glyph">${style.glyph}</span>
            <span class="timestamp">[${data.timestamp}]</span>
            <span class="type">TEST</span>
            <span class="message">${data.message}</span>
        `;
        
        logViewer.appendChild(logEntry);
        if (autoScrollCheckbox.checked) {
            logViewer.scrollTop = logViewer.scrollHeight;
        }
    });

    // Incremental log fetching
    async function fetchLogs() {
        try {
            const response = await fetch(`/api/logs?since=${lastReceivedLogId}`);
            const newLogs = await response.json();
            
            if (newLogs.length > 0) {
                lastReceivedLogId = newLogs[newLogs.length - 1].id;
                logBatch.push(...newLogs);
                processBatch();
            }
        } catch (error) {
            console.error('Error fetching logs:', error);
        }
    }
    
    // Fetch logs every 5 seconds (reduced from continuous polling)
    setInterval(fetchLogs, 5000);
    fetchLogs(); // Initial load

    // Render logs based on current filter
    function renderLogs() {
        const filter = filterType.value;
        logViewer.innerHTML = '';
        
        logs.forEach(log => {
            if (filter === 'all' || log.event_type === filter) {
                const style = logStyles[log.event_type] || logStyles['default'];
                const logEntry = document.createElement('div');
                logEntry.className = `log-entry ${log.event_type}`;
                logEntry.style.color = style.color;
                
                let contextHtml = log.context ? `<span class="context">(Context: ${log.context})</span>` : '';
                logEntry.innerHTML = `
                    <span class="glyph">${style.glyph}</span>
                    <span class="timestamp">[${log.timestamp}]</span>
                    <span class="type">${log.event_type.toUpperCase()}</span>
                    <span class="message">${log.message}</span>
                    ${contextHtml}
                `;
                logViewer.appendChild(logEntry);
            }
        });
        
        if (autoScrollCheckbox.checked) {
            logViewer.scrollTop = logViewer.scrollHeight;
        }
    }

    // Event listeners for filter changes and auto-scroll
    filterType.addEventListener('change', renderLogs);
    autoScrollCheckbox.addEventListener('change', () => {
        if (autoScrollCheckbox.checked) {
            logViewer.scrollTop = logViewer.scrollHeight;
        }
    });

    // Ensure auto-scroll works on new logs if enabled
    logViewer.addEventListener('scroll', () => {
        if (autoScrollCheckbox.checked && logViewer.scrollTop + logViewer.clientHeight >= logViewer.scrollHeight) {
            logViewer.scrollTop = logViewer.scrollHeight;
        }
    });
});
