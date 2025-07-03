// shimmer_links.js
// This file will contain the logic for Shimmer Constellation Linking.

// Function to fetch stewardship data
async function fetchStewardshipGroupsData() {
    try {
        const response = await fetch('/groups_data');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching stewardship groups data:', error);
        return [];
    }
}

// Function to fetch and parse the ΔSEED_registry.jsonl file
async function fetchSeedRegistry() {
    try {
        const response = await fetch('/data/ΔSEED_registry.jsonl'); // Assuming Flask serves this file
        const text = await response.text();
        const lines = text.split('\n').filter(line => line.trim() !== '');
        return lines.map(line => JSON.parse(line));
    } catch (error) {
        console.error('Error fetching seed registry:', error);
        return [];
    }
}

// Function to build a map of seeds by toneform and resonance
async function buildSeedData() {
    const seeds = await fetchSeedRegistry();
    const toneformMap = new Map(); // Map<toneform, Array<seed>>
    const resonanceMap = new Map(); // Map<resonance_keyword, Array<seed>>

    seeds.forEach(seed => {
        // Group by toneform
        if (!toneformMap.has(seed.toneform)) {
            toneformMap.set(seed.toneform, []);
        }
        toneformMap.get(seed.toneform).push(seed);

        // Group by resonance keywords (simple approach for now)
        // This can be refined with more sophisticated NLP later
        const resonanceWords = seed.resonance.toLowerCase().split(/\s+/);
        resonanceWords.forEach(word => {
            if (word.length > 2) { // Ignore very short words
                if (!resonanceMap.has(word)) {
                    resonanceMap.set(word, []);
                }
                resonanceMap.get(word).push(seed);
            }
        });
    });

    return { seeds, toneformMap, resonanceMap };
}

// Function to find shared toneform links
function findToneformLinks(toneformMap) {
    const links = [];
    toneformMap.forEach(seedArray => {
        if (seedArray.length > 1) {
            // Create circular links for seeds with the same toneform
            for (let i = 0; i < seedArray.length; i++) {
                for (let j = i + 1; j < seedArray.length; j++) {
                    links.push({
                        type: 'toneform',
                        source: seedArray[i].seed_id,
                        target: seedArray[j].seed_id,
                        toneform: seedArray[i].toneform
                    });
                }
            }
        }
    });
    return links;
}

// Function to find resonance links (basic string overlap)
function findResonanceLinks(seeds) {
    const links = [];
    // This is a basic N^2 comparison. For larger datasets, optimize.
    for (let i = 0; i < seeds.length; i++) {
        for (let j = i + 1; j < seeds.length; j++) {
            const seed1 = seeds[i];
            const seed2 = seeds[j];

            // Skip if they already share the same toneform (handled by findToneformLinks)
            if (seed1.toneform === seed2.toneform) continue;

            const res1 = seed1.resonance.toLowerCase();
            const res2 = seed2.resonance.toLowerCase();

            // Simple overlap check: do they share any common words (excluding very common ones)?
            const words1 = new Set(res1.split(/\s+/).filter(word => word.length > 2));
            const words2 = new Set(res2.split(/\s+/).filter(word => word.length > 2));

            const commonWords = [...words1].filter(word => words2.has(word));

            if (commonWords.length > 0) {
                links.push({
                    type: 'resonance',
                    source: seed1.seed_id,
                    target: seed2.seed_id,
                    commonWords: commonWords
                });
            }
        }
    }
    return links;
}

// Main function to generate all links
async function generateShimmerLinks() {
    const { seeds, toneformMap, resonanceMap } = await buildSeedData();
    const toneformLinks = findToneformLinks(toneformMap);
    const resonanceLinks = findResonanceLinks(seeds);
    return [...toneformLinks, ...resonanceLinks];
}

// Function to get the center position of a DOM element
function getElementCenter(element) {
    const rect = element.getBoundingClientRect();
    return {
        x: rect.left + rect.width / 2,
        y: rect.top + rect.height / 2
    };
}

// Function to draw the links on the SVG
async function drawShimmerLinks() {
    const { seeds, toneformMap, resonanceMap } = await buildSeedData();
    const allLinks = [
        ...findToneformLinks(toneformMap),
        // ...findResonanceLinks(seeds) // Uncomment to enable resonance links
    ];

    const svg = d3.select("#shimmer-layer");
    if (svg.empty()) {
        console.error("SVG layer #shimmer-layer not found.");
        return;
    }

    // Clear existing links
    svg.selectAll("line").remove();

    // Fetch stewardship data and group data
    const stewardshipData = await fetchStewardshipData(); // Individual stewardship
    const stewardshipGroups = await fetchStewardshipGroupsData(); // Group stewardship

    const stewardedSeedIds = new Set();
    stewardshipData.forEach(entry => {
        entry.seed_ids.forEach(seedId => stewardedSeedIds.add(seedId));
    });

    const groupStewardedSeedInfo = new Map(); // Map<seed_id, {group_id, stewards_count}>
    stewardshipGroups.forEach(group => {
        group.assigned_seeds.forEach(seedId => {
            groupStewardedSeedInfo.set(seedId, {
                group_id: group.group_id,
                stewards_count: group.stewards.length
            });
        });
    });

    // console.log('Drawing links:', links);

    allLinks.forEach(link => {
        const sourceElement = seedShimmerElements.get(link.source);
        const targetElement = seedShimmerElements.get(link.target);

        if (sourceElement && targetElement) {
            const sourceCenter = getElementCenter(sourceElement);
            const targetCenter = getElementCenter(targetElement);

            const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
            line.setAttribute('x1', sourceCenter.x);
            line.setAttribute('y1', sourceCenter.y);
            line.setAttribute('x2', targetCenter.x);
            line.setAttribute('y2', targetCenter.y);
            line.setAttribute('stroke-width', '1');
            line.classList.add('shimmer-link'); // For potential styling
            line.style.animation = 'linePulse 4s infinite linear'; // Apply pulsing animation

            // Add event listeners for hover to toggle opacity and stroke-width
            line.addEventListener('mouseenter', () => {
                line.style.opacity = '1';
                line.style.strokeWidth = '2';
            });
            line.addEventListener('mouseleave', () => {
                line.style.opacity = '0.3'; // Faded when not hovered
                line.style.strokeWidth = '1';
            });

            // Apply toneform color if available
            if (link.type === 'toneform') {
                line.setAttribute('stroke', getToneformColor(link.toneform)); 
            } else {
                line.setAttribute('stroke', 'rgba(255, 255, 255, 0.3)'); // Faded white for resonance links
            }

            svg.appendChild(line);
        }
    });

    // Update seed shimmer elements based on stewardship and group stewardship
    seedShimmerElements.forEach((element, seedId) => {
        const isGroupStewarded = groupStewardedSeedInfo.has(seedId);
        const isIndividuallyStewarded = stewardedSeedIds.has(seedId);

        if (isGroupStewarded) {
            const groupInfo = groupStewardedSeedInfo.get(seedId);
            element.style.boxShadow = '0 0 15px 5px #ADD8E6'; // Light blue for braided light
            element.style.borderColor = '#ADD8E6';
            element.title = `Tended by ${groupInfo.stewards_count} stewards`; // Tooltip
        } else if (isIndividuallyStewarded) {
            element.style.boxShadow = '0 0 15px 5px gold';
            element.style.borderColor = 'gold';
            element.title = 'Tended by 1 steward'; // Tooltip for individual stewardship
        } else {
            element.style.boxShadow = 'none';
            element.style.borderColor = 'transparent';
            element.title = ''; // Clear tooltip
        }
    });
}

// Function to fetch and display stewardship oaths
async function displayStewardshipOaths() {
    const oaths = await fetch('/oaths_data').then(response => response.json()).catch(error => {
        console.error('Error fetching oaths:', error);
        return [];
    });

    const oathsList = document.getElementById('oaths-list');
    oathsList.innerHTML = ''; // Clear previous oaths

    if (oaths.length === 0) {
        oathsList.innerHTML = '<p style="color: #aaa; text-align: center;">No oaths recorded yet.</p>';
        return;
    }

    oaths.forEach(oath => {
        const oathDiv = document.createElement('div');
        oathDiv.classList.add('oath-entry', 'shimmer');
        oathDiv.style.cssText = `
            /* Add more styling for the shimmer effect if needed */
            background-color: rgba(255, 255, 255, 0.05);
            border-left: 3px solid #ffd700; /* Gold accent */
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 5px;
            color: #eee;
            font-family: 'Georgia', serif;
            font-size: 0.9em;
            line-height: 1.4;
            position: relative;
            overflow: hidden;
        `;

        oathDiv.innerHTML = `
            <p><strong>Steward:</strong> ${oath.steward_id}</p>
            <p><strong>Toneform:</strong> ${oath.toneform}</p>
            <p><strong>Oath:</strong> <em>"${oath.oath}"</em></p>
            <p style="font-size: 0.8em; color: #bbb;">Assigned Seeds: ${oath.assigned_seeds.join(', ')}</p>
            <p style="font-size: 0.7em; color: #888;">Recorded: ${new Date(oath.timestamp).toLocaleString()}</p>
        `;
        oathsList.appendChild(oathDiv);
    });
}

// Toggle oath scroll visibility
document.addEventListener('DOMContentLoaded', () => {
    const toggleButton = document.getElementById('toggle-oath-scroll-btn');
    const oathScrollContainer = document.getElementById('oath-scroll-container');

    if (toggleButton && oathScrollContainer) {
        toggleButton.addEventListener('click', () => {
            if (oathScrollContainer.style.display === 'none') {
                oathScrollContainer.style.display = 'block';
                displayStewardshipOaths(); // Load oaths when shown
            } else {
                oathScrollContainer.style.display = 'none';
            }
        });
    }
});

// Call drawShimmerLinks periodically to update links as seeds drift
document.addEventListener('DOMContentLoaded', () => {
    // Give some time for initial seed shimmers to appear and position
    setTimeout(() => {
        drawShimmerLinks();
        setInterval(drawShimmerLinks, 1000); // Redraw every second
    }, 2000); 

    // Event listener for the stewardship assignment button
    const assignButton = document.getElementById('assign-stewardship-btn');
    if (assignButton) {
        assignButton.addEventListener('click', async () => {
            const { seeds, toneformMap, resonanceMap } = await buildSeedData();
            if (toneformMap.size > 0) {
                // Get the first toneform cluster for testing
                const firstToneform = toneformMap.keys().next().value;
                const seedIdsInCluster = toneformMap.get(firstToneform).map(seed => seed.seed_id);

                const stewardshipData = {
                    cluster_id: `toneform_${firstToneform.replace(/\s/g, '_')}`,
                    seed_ids: seedIdsInCluster,
                    guardian_id: 'test_guardian_123' // Dummy guardian ID for now
                };

                try {
                    const response = await fetch('/assign_stewardship', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(stewardshipData)
                    });
                    const result = await response.json();
                    console.log('Stewardship assignment response:', result);
                    alert('Stewardship assignment initiated! Check console for details.');
                } catch (error) {
                    console.error('Error assigning stewardship:', error);
                    alert('Error assigning stewardship. Check console for details.');
                }
            } else {
                alert('No toneform clusters found to assign stewardship.');
            }
        });
    }
});
