/**
 * Spiral Invocation Cards - Keyboard Shortcuts
 * Binds keyboard shortcuts to invocation card activation
 */

class InvocationShortcuts {
    constructor() {
        this.shortcuts = {};
        this.loadShortcuts();
        this.bindKeyboardEvents();
    }

    async loadShortcuts() {
        try {
            const response = await fetch('/api/invocation/shortcuts');
            const data = await response.json();
            
            if (data.status === 'success') {
                this.shortcuts = data.shortcuts;
                console.log('🎴 Loaded invocation shortcuts:', Object.keys(this.shortcuts));
            }
        } catch (error) {
            console.error('Failed to load invocation shortcuts:', error);
        }
    }

    bindKeyboardEvents() {
        document.addEventListener('keydown', (event) => {
            for (const [key, cardId] of Object.entries(this.shortcuts)) {
                if (event.key === key) {
                    fetch(`/api/invocation/activate/${cardId}`, { method: 'POST' });
                }
            }
        });
    }
}