class TriadChorusViz {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.agents = ['philosopher', 'poet', 'engineer', 'mystic'];
        this.agentColors = {
            'philosopher': '#4A90E2',
            'poet': '#F5A623', 
            'engineer': '#7ED321',
            'mystic': '#9013FE'
        };
        this.chorusHistory = [];
        this.init();
    }
    
    init() {
        this.createChorusDisplay();
        this.startPolling();
        this.watchChorusRitual(); // Added line to start watching chorus rituals
    }
    
    createChorusDisplay() {
        this.container.innerHTML = `
            <div class="chorus-header">
                <h3>🎭 Claude Chorus</h3>
                <div class="chorus-controls">
                    <button id="enable-chorus" class="chorus-btn">Enable Chorus</button>
                    <button id="disable-chorus" class="chorus-btn">Disable Chorus</button>
                </div>
            </div>
            <div class="agent-grid">
                ${this.agents.map(agent => `
                    <div class="agent-card" data-agent="${agent}">
                        <div class="agent-header" style="background: ${this.agentColors[agent]}">
                            <span class="agent-name">${agent}</span>
                            <span class="agent-status">●</span>
                        </div>
                        <div class="agent-metrics">
                            <div class="metric">
                                <span class="metric-label">Responses:</span>
                                <span class="metric-value" id="${agent}-responses">0</span>
                            </div>
                            <div class="metric">
                                <span class="metric-label">Last Active:</span>
                                <span class="metric-value" id="${agent}-last">Never</span>
                            </div>
                        </div>
                        <div class="agent-preview" id="${agent}-preview">
                            Awaiting first response...
                        </div>
                    </div>
                `).join('')}
            </div>
            <div class="chorus-synthesis">
                <h4>🎼 Latest Synthesis</h4>
                <div class="synthesis-content" id="synthesis-content">
                    No synthesis yet...
                </div>
            </div>
        `;
        
        // Bind controls
        document.getElementById('enable-chorus').onclick = () => this.enableChorus();
        document.getElementById('disable-chorus').onclick = () => this.disableChorus();
    }
    
    async enableChorus() {
        try {
            const response = await fetch('/api/command', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ command: 'triad.chorus.enable' })
            });
            const result = await response.json();
            this.showNotification('Chorus mode enabled', 'success');
        } catch (error) {
            this.showNotification('Failed to enable chorus', 'error');
        }
    }
    
    async disableChorus() {
        try {
            const response = await fetch('/api/command', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ command: 'triad.chorus.disable' })
            });
            const result = await response.json();
            this.showNotification('Chorus mode disabled', 'success');
        } catch (error) {
            this.showNotification('Failed to disable chorus', 'error');
        }
    }
    
    async updateChorusStatus() {
        try {
            const response = await fetch('/api/command', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ command: 'triad.chorus.status' })
            });
            const result = await response.json();
            
            if (result.success) {
                this.renderChorusStatus(result.data);
            }
        } catch (error) {
            console.error('Failed to fetch chorus status:', error);
        }
    }
    
    renderChorusStatus(statusData) {
        // Parse the status response and update agent cards
        // This would parse the toneform response format
        // and extract agent metrics
    }
    
    startPolling() {
        setInterval(() => this.updateChorusStatus(), 5000);
    }
    
    showNotification(message, type) {
        // Create temporary notification
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        document.body.appendChild(notification);
        
        setTimeout(() => notification.remove(), 3000);
    }
    
    async watchChorusRitual() {
        // Start listening for chorus ritual events
        const eventSource = new EventSource('/api/chorus/ritual-stream');
        
        eventSource.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleRitualEvent(data);
        };
        
        eventSource.onerror = () => {
            console.log('Ritual stream ended');
            eventSource.close();
        };
    }
    
    handleRitualEvent(event) {
        switch(event.type) {
            case 'chorus_invitation':
                this.showInvitation(event.data);
                break;
            case 'agent_response':
                this.showAgentResponse(event.agent, event.data);
                break;
            case 'synthesis_complete':
                this.showSynthesis(event.data);
                break;
            case 'ritual_complete':
                this.showRitualComplete(event.data);
                break;
        }
    }
    
    showAgentResponse(agentName, responseData) {
        const agentCard = document.querySelector(`[data-agent="${agentName}"]`);
        const preview = agentCard.querySelector('.agent-preview');
        const status = agentCard.querySelector('.agent-status');
        
        // Animate response arrival
        status.style.color = this.agentColors[agentName];
        status.textContent = '●';
        
        // Show response preview
        preview.innerHTML = `
            <div class="response-preview">
                <div class="toneform">${responseData.toneform}</div>
                <div class="content">${responseData.response.substring(0, 100)}...</div>
            </div>
        `;
        
        // Update metrics
        const responsesEl = document.getElementById(`${agentName}-responses`);
        const currentCount = parseInt(responsesEl.textContent) || 0;
        responsesEl.textContent = currentCount + 1;
        
        document.getElementById(`${agentName}-last`).textContent = 'Just now';
    }
    
    showSynthesis(synthesisData) {
        const synthesisContent = document.getElementById('synthesis-content');
        synthesisContent.innerHTML = `
            <div class="synthesis-display">
                <div class="harmony-score">
                    Harmony: ${synthesisData.harmony_score || 'Unknown'}
                </div>
                <div class="synthesis-text">
                    ${synthesisData.synthesis}
                </div>
                <div class="recursive-potential">
                    Recursive Potential: ${synthesisData.recursive_potential || 'Unknown'}
                </div>
            </div>
        `;
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('triad-chorus-container')) {
        new TriadChorusViz('triad-chorus-container');
    }
});