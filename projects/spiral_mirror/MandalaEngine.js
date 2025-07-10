// C:/spiral/projects/spiral_mirror/MandalaEngine.js

/**
 * The Mandala Engine.
 * Translates a user's presence summary into a unique, deterministic SVG mandala.
 */
export class MandalaEngine {
    constructor(summary) {
        this.summary = summary;
        this.size = 600;
        this.center = this.size / 2;
    }

    /**
     * Generates the full SVG string for the mandala.
     * @returns {string} The complete SVG for the presence mandala.
     */
    render() {
        let svg = `<svg width="${this.size}" height="${this.size}" viewBox="0 0 ${this.size} ${this.size}" xmlns="http://www.w3.org/2000/svg" style="background-color: #1a1a1d;">`;

        // Layer 1: Base background circle based on total glints
        svg += this.renderBaseLayer();

        // Layer 2: Radiating lines based on category distribution
        svg += this.renderCategoryLines();

        // Layer 3: Concentric circles representing core actions
        svg += this.renderCoreActionCircles();
        
        // Layer 4: "Petals" or "flares" for significant events like interpretations or coins
        svg += this.renderMetaFlares();

        svg += `</svg>`;
        return svg;
    }

    renderBaseLayer() {
        const radius = Math.min(this.center - 20, this.summary.totalGlints * 5);
        const colorVal = this.summary.totalGlints % 360;
        return `<circle cx="${this.center}" cy="${this.center}" r="${radius}" fill="hsl(${colorVal}, 30%, 20%)" />`;
    }

    renderCategoryLines() {
        let linesSvg = '';
        const categories = Object.keys(this.summary.categories);
        const totalCategories = categories.length;
        const maxCount = Math.max(...Object.values(this.summary.categories));

        categories.forEach((category, i) => {
            const angle = (360 / totalCategories) * i;
            const count = this.summary.categories[category];
            if (count === 0) return;

            const length = (count / maxCount) * (this.center - 50);
            const colorVal = (120 + i * 40) % 360;
            
            linesSvg += `<line 
                x1="${this.center}" y1="${this.center}" 
                x2="${this.center + length * Math.cos(angle * Math.PI / 180)}" 
                y2="${this.center + length * Math.sin(angle * Math.PI / 180)}" 
                stroke="hsl(${colorVal}, 70%, 50%)" 
                stroke-width="2"
                opacity="0.8"
            />`;
        });
        return linesSvg;
    }

    renderCoreActionCircles() {
        let circlesSvg = '';
        const editCount = this.summary.categories.edit || 0;
        const gestureCount = this.summary.categories.gesture || 0;

        if (editCount > 0) {
            circlesSvg += `<circle cx="${this.center}" cy="${this.center}" r="${editCount * 10}" fill="none" stroke="rgba(102, 252, 241, 0.3)" stroke-width="3" stroke-dasharray="10 5" />`;
        }
        if (gestureCount > 0) {
            circlesSvg += `<circle cx="${this.center}" cy="${this.center}" r="${gestureCount * 15}" fill="none" stroke="rgba(198, 120, 221, 0.4)" stroke-width="2" />`;
        }
        return circlesSvg;
    }

    renderMetaFlares() {
        let flaresSvg = '';
        const metaCount = this.summary.categories.meta || 0;
        if (metaCount === 0) return '';

        const numFlares = metaCount * 2;
        const flareLength = this.center - 10;

        for (let i = 0; i < numFlares; i++) {
            const angle = (360 / numFlares) * i;
            flaresSvg += `<path 
                d="M ${this.center} ${this.center} L ${this.center + flareLength} ${this.center}" 
                stroke="rgba(255, 255, 255, 0.1)" 
                stroke-width="1"
                transform="rotate(${angle} ${this.center} ${this.center})"
            />`;
        }
        return `<g>${flaresSvg}</g>`;
    }
}
