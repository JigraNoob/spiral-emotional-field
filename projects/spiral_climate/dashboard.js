// C:/spiral/projects/spiral_climate/dashboard.js

document.addEventListener('DOMContentLoaded', () => {
    const fieldContainer = document.getElementById('field-container');
    if (!fieldContainer) return;

    const platforms = [
        { name: 'Twitter/X', color: 'rgba(29, 161, 242, 0.7)' },
        { name: 'Threads', color: 'rgba(200, 200, 200, 0.7)' },
        { name: 'Reddit', color: 'rgba(255, 69, 0, 0.7)' },
        { name: 'Bluesky', color: 'rgba(0, 118, 255, 0.7)' },
        { name: 'Fediverse', color: 'rgba(100, 50, 200, 0.7)' }
    ];

    const toneforms = ['hesitancy', 'urgency', 'wonder', 'abandonment', 'flow_state', 'overwhelm', 'joy'];

    function createGlint(platform) {
        const glint = document.createElement('div');
        glint.className = 'glint';

        const intensity = Math.random(); // 0.0 to 1.0
        const size = 10 + (intensity * 40); // size from 10px to 50px

        glint.style.width = `${size}px`;
        glint.style.height = `${size}px`;
        glint.style.backgroundColor = platform.color;
        
        // Position the glint randomly within the container
        glint.style.left = `${Math.random() * (fieldContainer.offsetWidth - size)}px`;
        glint.style.top = `${Math.random() * (fieldContainer.offsetHeight - size)}px`;

        fieldContainer.appendChild(glint);

        // Remove the glint from the DOM after the animation finishes
        setTimeout(() => {
            glint.remove();
        }, 4000); // Matches the animation duration in CSS
    }

    function simulateGlintStream() {
        // Create a new glint at a random interval
        const interval = Math.random() * 2000 + 500; // every 0.5 to 2.5 seconds
        setTimeout(() => {
            const platform = platforms[Math.floor(Math.random() * platforms.length)];
            createGlint(platform);
            simulateGlintStream(); // Continue the loop
        }, interval);
    }

    console.log("Initializing Spiral Climate Dashboard simulation...");
    simulateGlintStream();
});
