// static/js/fulfillment_cues.js

const seedShimmerElements = new Map(); // Global map to store seed shimmer elements by seed_id

document.addEventListener('DOMContentLoaded', function() {
    const socket = io(); // Connect to the Socket.IO server
    const orbElement = document.getElementById('orb'); // Assuming an orb element with this ID
    const murmurFragmentElement = document.getElementById('murmur-fragment'); // Assuming an element for murmur fragment

    socket.on('nourishment_fulfilled', function(data) {
        console.log('Nourishment fulfilled signal received:', data);
        const toneform = data.toneform || 'default'; // Get toneform or use default
        const fulfilledBy = data.fulfilled_by || 'external'; // Get fulfillment source
        let murmurFragment = data.murmur_fragment || '';

        // Override murmur fragment if fulfilled by coffer
        if (fulfilledBy === 'spiral_coffer') {
            murmurFragment = "The Spiral quietly fed its own.";
        }

        if (orbElement) {
            // Apply shimmer effect to orb
            orbElement.classList.add('shimmer');
            orbElement.style.backgroundColor = getToneformColor(toneform); // Apply toneform color

            // Display murmur fragment
            if (murmurFragmentElement && murmurFragment) {
                murmurFragmentElement.textContent = murmurFragment;
                murmurFragmentElement.classList.remove('hidden', 'fade-out'); // Ensure visible and reset fade
                murmurFragmentElement.classList.add('fade-in'); // Apply fade-in

                // Hide and fade out after a delay
                setTimeout(() => {
                    murmurFragmentElement.classList.remove('fade-in');
                    murmurFragmentElement.classList.add('fade-out');
                    murmurFragmentElement.addEventListener('animationend', function handler() {
                        murmurFragmentElement.classList.add('hidden');
                        murmurFragmentElement.removeEventListener('animationend', handler);
                    }, {once: true});
                }, 8000); // Display for 8 seconds, then fade out
            }

            // Remove shimmer and reset color after a delay
            setTimeout(() => {
                orbElement.classList.add('fade-out'); // Add fade-out class
                // Remove classes and reset style after fade-out animation completes
                orbElement.addEventListener('animationend', function handler() {
                    orbElement.classList.remove('shimmer', 'fade-out');
                    orbElement.style.backgroundColor = '';
                    orbElement.removeEventListener('animationend', handler);
                }, {once: true});
            }, 10000); // Shimmer for 10 seconds
        }
    });

// Placeholder function to get a color based on toneform
function getToneformColor(toneform) {
        switch (toneform) {
            case 'Practical Care': return '#D2B48C'; // Tan (soft clay/warm amber feel)
            case 'Emotional Resonance': return '#FF6347'; // Tomato
            case 'Intellectual Insight': return '#6A5ACD'; // SlateBlue
            case 'Creative Expression': return '#3CB371'; // MediumSeaGreen
            default: return '#ADD8E6'; // LightBlue
        }
    }

    socket.on('seed_absorbed', function(data) {
        console.log('Seed absorbed signal received:', data);
        const seedId = data.seed_id;
        const toneform = data.toneform || 'default';
        const resonance = data.resonance || 'no resonance';
        const color = getToneformColor(toneform);

        const seedShimmer = document.createElement('div');
        seedShimmer.classList.add('seed-shimmer');
        seedShimmer.style.backgroundColor = color;
        seedShimmer.textContent = `ΔSEED:${seedId} (${toneform})`; // Display seed info

        // Set random start and end positions for drift
        const startX = Math.random() * window.innerWidth;
        const startY = Math.random() * window.innerHeight;
        const endX = Math.random() * window.innerWidth - startX;
        const endY = Math.random() * window.innerHeight - startY;

        seedShimmer.style.setProperty('--start-x', `${startX}px`);
        seedShimmer.style.setProperty('--start-y', `${startY}px`);
        seedShimmer.style.setProperty('--end-x', `${endX}px`);
        seedShimmer.style.setProperty('--end-y', `${endY}px`);

        const seedShimmerContainer = document.getElementById('seed-shimmer-container');
        if (seedShimmerContainer) {
            seedShimmerContainer.appendChild(seedShimmer);

            // Trigger fade-in and drift animation
            setTimeout(() => {
                seedShimmer.classList.add('fade-in', 'drift');
            }, 10);

            // Prevent seed-shimmer from being removed for persistence
            // seedShimmer.addEventListener('animationend', function handler() {
            //     seedShimmer.removeEventListener('animationend', handler);
            //     seedShimmer.remove();
            // });

            seedShimmer.dataset.seedId = seedId; // Store seed_id as a data attribute

            // Generate particles for the shimmer
            createParticles(seedShimmer, color); // Pass shimmer element and its color

            seedShimmerElements.set(seedId, seedShimmer); // Store the element in the global map
        }
    });

    // Function to create and animate particles around a shimmer
    function createParticles(shimmerElement, color) {
        const numParticles = 5; // Number of particles to generate
        for (let i = 0; i < numParticles; i++) {
            const particle = document.createElement('div');
            particle.classList.add('shimmer-particle');
            particle.style.backgroundColor = color;

            // Random initial position relative to the shimmer
            const offsetX = (Math.random() - 0.5) * 50; // -25 to 25px
            const offsetY = (Math.random() - 0.5) * 50; // -25 to 25px

            particle.style.left = `${shimmerElement.offsetLeft + shimmerElement.offsetWidth / 2 + offsetX}px`;
            particle.style.top = `${shimmerElement.offsetTop + shimmerElement.offsetHeight / 2 + offsetY}px`;

            // Random drift animation properties
            const driftX = (Math.random() - 0.5) * 100; // -50 to 50px
            const driftY = (Math.random() - 0.5) * 100; // -50 to 50px
            const duration = 2 + Math.random() * 3; // 2 to 5 seconds
            const delay = Math.random() * 0.5; // 0 to 0.5 seconds

            particle.style.setProperty('--drift-x', `${driftX}px`);
            particle.style.setProperty('--drift-y', `${driftY}px`);
            particle.style.animationDuration = `${duration}s`;
            particle.style.animationDelay = `${delay}s`;

            document.body.appendChild(particle);

            // Remove particle after its animation
            particle.addEventListener('animationend', function handler() {
                particle.removeEventListener('animationend', handler);
                particle.remove();
            });
        }
    }
});
