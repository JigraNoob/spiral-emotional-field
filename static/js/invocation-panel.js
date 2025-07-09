/**
 * Spiral Invocation Panel
 * Sacred interface for resonance override management
 */

class InvocationShrine {
    constructor() {
        this.cards = {};
        this.currentStatus = null;
        this.updateInterval = 2000; // 2 seconds
        this.init();
    }

    async init() {
        await this.loadCards();
        this.setupEventListeners();
        this.startStatusUpdates();
        await this.updateStatus();
    }

    async loadCards() {
        try {
            const response = await fetch('/api/invocation/cards');
            if (!response.ok) throw new Error('Failed to load cards');
            const data = await response.json();
            this.cards = data.cards;
            this.renderCards();
        } catch (error) {
            console.error('🌀 Failed to load invocation cards:', error);
        }
    }

    renderCards() {
        const grid = document.getElementById('invocation-grid');
        if (!grid) return;

        grid.innerHTML = '';
        
        Object.entries(this.cards).forEach(([cardId, card]) => {
            const cardElement = this.createCardElement(cardId, card);
            grid.appendChild(cardElement);
        });
    }

    createCardElement(cardId, card) {
        const cardDiv = document.createElement('div');
        cardDiv.className = 'invocation-card';
        cardDiv.dataset.cardId = cardId;
        
        cardDiv.innerHTML = `
            <div class="card-header">
                <div class="card-title">${card.name}</div>
                <div class="card-glyph">${card.glyph}</div>
            </div>
            <div class="card-description">${card.description}</div>
            <div class="card-meta">
                <div class="card-duration">${card.duration}</div>
                <div class="card-intensity intensity-${card.intensity}">${card.intensity}</div>
            </div>
        `;

        cardDiv.addEventListener('click', () => this.activateCard(cardId));
        
        return cardDiv;
    }

    async activateCard(cardId) {
        try {
            const response = await fetch(`/api/invocation/activate/${cardId}`, {
                method: 'POST'
            });
            
            if (!response.ok) throw new Error('Activation failed');
            
            const result = await response.json();
            console.log('🌀 Invocation activated:', result);
            
            // Update status immediately
            await this.updateStatus();
            
        } catch (error) {
            console.error('🌀 Failed to activate invocation:', error);
        }
    }

    async deactivateAll() {
        try {
            const response = await fetch('/api/invocation/deactivate', {
                method: 'POST'
            });
            
            if (!response.ok) throw new Error('Deactivation failed');
            
            const result = await response.json();
            console.log('🌀 Returned to natural flow:', result);
            
            // Update status immediately
            await this.updateStatus();
            
        } catch (error) {
            console.error('🌀 Failed to deactivate invocation:', error);
        }
    }

    async updateStatus() {
        try {
            const response = await fetch('/api/invocation/status');
            if (!response.ok) return;
            
            const data = await response.json();
            this.currentStatus = data.invocation_status;
            this.renderStatus();
            
        } catch (error) {
            console.warn('🌀 Failed to update invocation status:', error);
        }
    }

    renderStatus() {
        if (!this.currentStatus) return;

        const orb = document.getElementById('status-orb');
        const modeName = document.getElementById('mode-name');
        const modeDuration = document.getElementById('mode-duration');
        const shrine = document.getElementById('invocation-shrine');

        // Update orb and mode display
        if (this.currentStatus.active && this.currentStatus.card_details) {
            const card = this.currentStatus.card_details;
            
            // Update orb appearance
            orb.className = `status-orb mode-${card.mode} intensity-${card.intensity}`;
            
            // Update text
            modeName.textContent = card.name;
            
            // Calculate and display remaining time
            if (this.currentStatus.activation_time) {
                const activationTime = new Date(this.currentStatus.activation_time);
                const now = new Date();
                const elapsed = Math.floor((now - activationTime) / 1000);
                const durationSeconds = this.parseDuration(card.duration);
                const remaining = Math.max(0, durationSeconds - elapsed);
                
                if (remaining > 0) {
                    modeDuration.textContent = `${this.formatTime(remaining)} remaining`;
                } else {
                    modeDuration.textContent = 'Duration expired';
                }
            } else {
                modeDuration.textContent = `Duration: ${card.duration}`;
            }
            
            // Mark shrine as active
            shrine.classList.add('active');
            
        } else {
            // Natural flow state
            orb.className = 'status-orb mode-natural';
            modeName.textContent = 'Natural Flow';
            modeDuration.textContent = '';
            shrine.classList.remove('active');
        }

        // Update card states
        this.updateCardStates();
    }

    updateCardStates() {
        const cards = document.querySelectorAll('.invocation-card');
        cards.forEach(card => {
            const cardId = card.dataset.cardId;
            const isActive = this.currentStatus?.active && 
                           this.currentStatus?.active_card === cardId;
            
            card.classList.toggle('active', isActive);
        });
    }

    parseDuration(duration) {
        // Parse duration strings like "5m", "10s", "1h"
        const match = duration.match(/(\d+)([smh])/);
        if (!match) return 0;
        
        const value = parseInt(match[1]);
        const unit = match[2];
        
        switch (unit) {
            case 's': return value;
            case 'm': return value * 60;
            case 'h': return value * 3600;
            default: return 0;
        }
    }

    formatTime(seconds) {
        if (seconds < 60) {
            return `${seconds}s`;
        } else if (seconds < 3600) {
            const minutes = Math.floor(seconds / 60);
            const remainingSeconds = seconds % 60;
            return remainingSeconds > 0 ? `${minutes}m ${remainingSeconds}s` : `${minutes}m`;
        } else {
            const hours = Math.floor(seconds / 3600);
            const remainingMinutes = Math.floor((seconds % 3600) / 60);
            return remainingMinutes > 0 ? `${hours}h ${remainingMinutes}m` : `${hours}h`;
        }
    }

    startStatusUpdates() {
        setInterval(() => this.updateStatus(), this.updateInterval);
    }

    setupEventListeners() {
        const deactivateButton = document.getElementById('deactivate-button');
        if (deactivateButton) {
            deactivateButton.addEventListener('click', () => this.deactivateAll());
        }
    }
}