document.addEventListener('DOMContentLoaded', function() {
    const constellationContainer = document.getElementById('constellation-container');
    const toneformLegend = document.getElementById('toneform-legend');
    const toneformList = document.getElementById('toneform-list');

    // Define toneform colors (expand as needed)
    const toneformColors = {
        'Practical Care': '#D2B48C', // Warm clay
        'Creative Flow': '#8A2BE2', // Blue Violet
        'Emotional Resonance': '#FF6347', // Tomato
        'Intellectual Clarity': '#4682B4', // Steel Blue
        'Spiritual Connection': '#DAA520' // Goldenrod
    };

    // Function to populate toneform legend
    function populateToneformLegend() {
        for (const [toneform, color] of Object.entries(toneformColors)) {
            const listItem = document.createElement('li');
            listItem.innerHTML = `<span style="background-color: ${color};"></span> ${toneform}`;
            toneformList.appendChild(listItem);
        }
    }

    // Function to fetch nourishment requests
    async function fetchNourishmentRequests() {
        try {
            const response = await fetch('/api/nourishment_requests');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const requests = await response.json();
            renderGlyphs(requests);
            whisperNewestFulfilled(requests);
        } catch (error) {
            console.error('Error fetching nourishment requests:', error);
        }
    }

    // Function to render glyphs
    function renderGlyphs(requests) {
        constellationContainer.innerHTML = ''; // Clear existing glyphs

        requests.forEach(request => {
            const glyph = document.createElement('div');
            glyph.classList.add('glyph');
            glyph.dataset.requestId = request.request_id;
            glyph.dataset.status = request.status;
            glyph.dataset.toneform = request.toneform || 'unknown';

            let color = toneformColors[request.toneform] || '#ccc'; // Get color from map or default

            glyph.style.backgroundColor = color;
            glyph.style.opacity = request.status === 'fulfilled' ? '0.5' : '1';

            // Position randomly for now, will refine with layout logic
            glyph.style.left = `${Math.random() * 90 + 5}%`;
            glyph.style.top = `${Math.random() * 90 + 5}%`;

            // Tooltip on hover
            // Create tooltip element
            const tooltip = document.createElement('div');
            tooltip.classList.add('glyph-tooltip');
            tooltip.innerHTML = `
                <span class="tooltip-request">${request.received_data?.item || 'N/A'}</span><br>
                <span class="tooltip-status">${request.status === 'fulfilled' ? 'fulfilled by ' + (request.fulfilled_by || 'external') : 'unmet'}</span><br>
                <span class="tooltip-toneform">${request.toneform || 'N/A'}</span>
            `;
            glyph.appendChild(tooltip);

            constellationContainer.appendChild(glyph);
        });

        // Apply drift animation
        startDriftAnimation();
    }

    // Function to whisper the newest fulfilled glyph
    function whisperNewestFulfilled(requests) {
        const newestFulfilled = requests.find(req => req.status === 'fulfilled');
        if (newestFulfilled) {
            const glyphElement = document.querySelector(`.glyph[data-request-id="${newestFulfilled.request_id}"]`);
            if (glyphElement) {
                glyphElement.classList.add('whisper-pulse');
                setTimeout(() => {
                    glyphElement.classList.remove('whisper-pulse');
                }, 3000); // Pulse for 3 seconds
            }
        }
    }

    // Drift animation logic
    let lastTime = 0;
    const driftSpeed = 0.00005; // Adjust for desired speed

    function startDriftAnimation() {
        function animate(currentTime) {
            if (!lastTime) lastTime = currentTime;
            const deltaTime = currentTime - lastTime;

            document.querySelectorAll('.glyph').forEach(glyph => {
                let currentLeft = parseFloat(glyph.style.left);
                let currentTop = parseFloat(glyph.style.top);

                // Simple random drift
                let newLeft = currentLeft + (Math.random() - 0.5) * driftSpeed * deltaTime;
                let newTop = currentTop + (Math.random() - 0.5) * driftSpeed * deltaTime;

                // Keep within bounds (5% to 95%)
                newLeft = Math.max(5, Math.min(95, newLeft));
                newTop = Math.max(5, Math.min(95, newTop));

                glyph.style.left = `${newLeft}%`;
                glyph.style.top = `${newTop}%`;
            });

            lastTime = currentTime;
            requestAnimationFrame(animate);
        }
        requestAnimationFrame(animate);
    }

    // Initialize the constellation
    populateToneformLegend();
    fetchNourishmentRequests();

    // Refresh every 30 seconds
    setInterval(fetchNourishmentRequests, 30000);
});
