// static/js/bloom_manager.js

import { playToneformAudio } from './audio_manager.js';

const TONEFORM_COLORS = {
    "Coherence": "#A8DADC",
    "Presence": "#FFE066",
    "Curiosity": "#FFADAD",
    "Trust": "#C3F584",
    "Reflection": "#FEC8D8",
    "Resonance": "#9ED2C6",
    "Memory": "#D6A4A4",
    "Stillness": "#CAD2C5",
    "Longing": "#E0B1CB",
    "Adaptation": "#A0C4FF",
    "Unknown": "#CCCCCC"
};

import TONEFORM_LORE from './toneform_lore.json';

let bloomTooltipElement = null;
let tooltipFadeTimeout = null;

const RECENT_CLICK_HALO_DURATION = 3000;
const FREQUENCY_TRACKING_WINDOW_MS = 2 * 60 * 1000;
const recentToneformClicks = [];

// Auto-invocation Tracker Object
const autoInvokeTracker = {
    clickCount: 0,
    lastInvocation: 0,
    threshold: 5,
    cooldown: 15000,
    canInvokeNow() {
        return this.clickCount >= this.threshold && (Date.now() - this.lastInvocation >= this.cooldown);
    },
    recordClick() {
        this.clickCount++;
    },
    reset() {
        this.clickCount = 0;
        this.lastInvocation = Date.now();
    }
};

export function initBloomManager(tooltipElement) {
    bloomTooltipElement = tooltipElement;
    if (bloomTooltipElement) {
        bloomTooltipElement.style.transition = 'opacity 0.5s ease-out, visibility 0s linear 0.5s';
    }
}

export async function fetchAndRenderBlooms(bloomContainerElement, isReplaying) {
    if (isReplaying) {
        if (bloomContainerElement) {
            bloomContainerElement.innerHTML = '';
        }
        return;
    }

    try {
        const response = await fetch('/get_toneform_blooms');
        if (!response.ok) throw new Error("Failed to fetch bloom data.");
        const blooms = await response.json();
        renderBlooms(blooms, bloomContainerElement);
    } catch (err) {
        console.error("Error rendering toneform blooms:", err);
    }
}

function getSpiralClimate() {
    const hour = new Date().getHours();
    return (hour >= 6 && hour < 18) ? "day" : "night";
}

function getAdjustedBloomCount(baseCount, climate) {
    switch (climate) {
        case "day": return Math.ceil(baseCount * 1.5);
        case "night": return Math.floor(baseCount * 0.7);
        case "active": return Math.ceil(baseCount * 1.8);
        case "calm": return Math.floor(baseCount * 0.5);
        default: return baseCount;
    }
}

function logBloomGesture(toneform, gesture_strength, x_pos, y_pos) {
    fetch('/log_bloom_gesture', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            toneform,
            timestamp: new Date().toISOString(),
            gesture_strength,
            x_pos,
            y_pos
        })
    }).catch(err => console.warn("Bloom gesture logging failed:", err));
}

function updateToneformFrequencyRing() {
    const now = Date.now();
    while (recentToneformClicks.length > 0 && (now - recentToneformClicks[0].timestamp) > FREQUENCY_TRACKING_WINDOW_MS) {
        recentToneformClicks.shift();
    }

    if (recentToneformClicks.length === 0) {
        document.documentElement.style.setProperty('--frequency-ring-color', 'transparent');
        return;
    }

    const toneformCounts = {};
    recentToneformClicks.forEach(click => {
        toneformCounts[click.toneform] = (toneformCounts[click.toneform] || 0) + 1;
    });

    let dominantToneform = "Unknown";
    let maxCount = 0;
    for (const tone in toneformCounts) {
        if (toneformCounts[tone] > maxCount) {
            maxCount = toneformCounts[tone];
            dominantToneform = tone;
        }
    }

    const ringColor = TONEFORM_COLORS[dominantToneform] || TONEFORM_COLORS["Unknown"];
    document.documentElement.style.setProperty('--frequency-ring-color', ringColor);
    console.log(`Dominant toneform: ${dominantToneform}, Ring color: ${ringColor}`);
}

export async function invokeGeminiWithBlooms() {
    const toneforms = recentToneformClicks.map(c => c.toneform);
    try {
        const response = await fetch('/invoke_gemini', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ recent_toneforms: toneforms })
        });
        const result = await response.json();
        if (result.status === 'success') {
            const poemDiv = document.getElementById('gemini-poem');
            if (poemDiv) {
                poemDiv.textContent = result.poem;
                poemDiv.classList.add('visible');
            }
            if (result.shimmer_toneform) {
                const shimmerColor = TONEFORM_COLORS[result.shimmer_toneform] || TONEFORM_COLORS["Unknown"];
                document.documentElement.style.setProperty('--shrine-shimmer-color', shimmerColor);
                console.log(`Applied shimmer toneform: ${result.shimmer_toneform}, Color: ${shimmerColor}`);
                setTimeout(() => {
                    document.documentElement.style.setProperty('--shrine-shimmer-color', 'transparent');
                    console.log("Shimmer faded to stillness.");
                }, 10000);
            }
            autoInvokeTracker.reset();
            recentToneformClicks.length = 0;
        } else {
            console.error("Gemini API error:", result.message);
        }
    } catch (err) {
        console.error("Failed to invoke Gemini:", err);
    }
}

function renderBlooms(blooms, bloomContainerElement) {
    if (!bloomContainerElement) return;
    bloomContainerElement.innerHTML = '';
    const currentClimate = getSpiralClimate();

    blooms.forEach(bloom => {
        const { toneform, count, average_strength } = bloom;
        let baseBlooms = Math.min(count, 5);
        const numOrbs = getAdjustedBloomCount(baseBlooms, currentClimate);

        for (let i = 0; i < numOrbs; i++) {
            const orb = document.createElement('div');
            orb.classList.add('toneform-bloom');
            orb.style.top = `${Math.random() * 90}%`;
            orb.style.left = `${Math.random() * 90}%`;

            const size = 40 + (average_strength * 40);
            orb.style.width = `${size}px`;
            orb.style.height = `${size}px`;
            orb.style.opacity = 0.3 + (average_strength * 0.5);
            orb.style.backgroundColor = TONEFORM_COLORS[toneform] || TONEFORM_COLORS["Unknown"];

            orb.style.animation = `bloomPulse 4s infinite ease-in-out alternate, bloomFadeIn 2s forwards, bloomFloat linear infinite alternate`;
            orb.style.animationDelay = `${Math.random() * 5}s`;
            orb.style.animationDuration = `${10 + Math.random() * 10}s`;
            orb.style.filter = "blur(5px)";
            orb.style.transition = "transform 0.5s ease, opacity 0.3s ease, filter 0.3s ease, box-shadow 0.3s ease";
            orb.style.boxShadow = "0 0 10px rgba(255, 255, 255, 0.2)";

            orb.addEventListener('mouseenter', (event) => {
                orb.style.transform = 'scale(1.1)';
                orb.style.opacity = '0.8';
                orb.style.filter = 'blur(2px)';
                orb.style.boxShadow = `0 0 25px ${orb.style.backgroundColor}, 0 0 40px ${orb.style.backgroundColor}`;
                if (bloomTooltipElement) {
                    clearTimeout(tooltipFadeTimeout);
                    bloomTooltipElement.innerText = TONEFORM_LORE[toneform] || TONEFORM_LORE["Unknown"];
                    bloomTooltipElement.style.left = `${event.clientX + 15}px`;
                    bloomTooltipElement.style.top = `${event.clientY + 15}px`;
                    bloomTooltipElement.style.opacity = '1';
                    bloomTooltipElement.style.visibility = 'visible';
                }
            });

            orb.addEventListener('mouseleave', () => {
                if (!orb.classList.contains('bloom-halo')) {
                    orb.style.transform = '';
                    orb.style.opacity = '';
                    orb.style.filter = 'blur(5px)';
                    orb.style.boxShadow = "0 0 10px rgba(255, 255, 255, 0.2)";
                }
                if (bloomTooltipElement) {
                    bloomTooltipElement.style.opacity = '0';
                    tooltipFadeTimeout = setTimeout(() => {
                        bloomTooltipElement.style.visibility = 'hidden';
                    }, 500);
                }
            });

            orb.addEventListener('click', (event) => {
                console.log(`Bloom clicked: Playing tone for ${toneform}`);
                playToneformAudio(toneform);
                const gesture_strength = average_strength;
                const x_pos = event.clientX;
                const y_pos = event.clientY;
                logBloomGesture(toneform, gesture_strength, x_pos, y_pos);
                recentToneformClicks.push({ toneform, timestamp: Date.now() });
                updateToneformFrequencyRing();
                orb.classList.add('bloom-halo');
                setTimeout(() => {
                    orb.classList.remove('bloom-halo');
                    if (!orb.matches(':hover')) {
                        orb.style.transform = '';
                        orb.style.opacity = '';
                        orb.style.filter = 'blur(5px)';
                        orb.style.boxShadow = "0 0 10px rgba(255, 255, 255, 0.2)";
                    }
                }, RECENT_CLICK_HALO_DURATION);

                autoInvokeTracker.recordClick();
                if (autoInvokeTracker.canInvokeNow()) {
                    invokeGeminiWithBlooms();
                }
            });

            bloomContainerElement.appendChild(orb);
        }
    });
    console.log(`Rendered ${blooms.length} toneform bloom groups with climate: ${currentClimate}.`);
}

export { TONEFORM_COLORS };
