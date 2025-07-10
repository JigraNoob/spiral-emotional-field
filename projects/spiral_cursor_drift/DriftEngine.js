// C:/spiral/projects/spiral_cursor_drift/DriftEngine.js

/**
 * A base class for mathematical attractors used for cursor drift.
 */
class Attractor {
    constructor(x = 0, y = 0, z = 0) {
        this.x = x;
        this.y = y;
        this.z = z;
    }

    step(dt) {
        throw new Error("Attractor.step() must be implemented by a subclass.");
    }

    getPosition() {
        // Returns a 2D position for the cursor, typically ignoring the z-axis.
        return { x: this.x, y: this.y };
    }
}

/**
 * The Lorenz attractor, which produces a chaotic, butterfly-shaped pattern.
 * Represents a more complex, contemplative drift.
 */
export class LorenzAttractor extends Attractor {
    constructor(x = 0.1, y = 0, z = 0, sigma = 10, rho = 28, beta = 8 / 3) {
        super(x, y, z);
        this.sigma = sigma;
        this.rho = rho;
        this.beta = beta;
        this.name = 'lorenz';
    }

    step(dt) {
        const dx = this.sigma * (this.y - this.x);
        const dy = this.x * (this.rho - this.z) - this.y;
        const dz = this.x * this.y - this.beta * this.z;

        this.x += dx * dt;
        this.y += dy * dt;
        this.z += dz * dt;
    }
}

/**
 * A Lissajous curve, which produces smooth, harmonic, and often looping patterns.
 * Represents a more stable, gentle drift.
 */
export class LissajousAttractor extends Attractor {
    constructor(a = 1, b = 2, phase = Math.PI / 2, speed = 1) {
        super();
        this.a = a; // Frequency in x
        this.b = b; // Frequency in y
        this.phase = phase;
        this.speed = speed;
        this.time = 0;
        this.name = 'lissajous';
    }

    step(dt) {
        this.time += dt * this.speed;
        this.x = Math.sin(this.a * this.time + this.phase);
        this.y = Math.sin(this.b * this.time);
    }
}

/**
 * The main engine that drives the cursor drift.
 * It selects an attractor and updates the cursor's position on each animation frame.
 */
export class DriftEngine extends EventTarget {
    constructor(canvas, attractor) {
        super();
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.attractor = attractor || new LissajousAttractor();
        this.isRunning = false;
        this.lastTime = 0;

        this.ctx.strokeStyle = 'rgba(102, 252, 241, 0.7)';
        this.ctx.lineWidth = 1;
        this.ctx.fillStyle = 'rgba(26, 26, 29, 0.1)'; // For a fading trail effect
    }

    setAttractor(newAttractor) {
        if (this.attractor.name !== newAttractor.name) {
            this.dispatchEvent(new CustomEvent('glint', {
                detail: {
                    type: 'glint.drift.pattern',
                    message: `Drift pattern changed to ${newAttractor.name}.`,
                    pattern: newAttractor.name,
                    timestamp: Date.now()
                }
            }));
        }
        this.attractor = newAttractor;
    }

    start() {
        if (this.isRunning) return;
        this.isRunning = true;
        this.lastTime = performance.now();
        this.dispatchEvent(new CustomEvent('glint', {
            detail: {
                type: 'glint.drift.begin',
                message: 'Drift ritual has begun.',
                timestamp: Date.now()
            }
        }));
        this.animate(this.lastTime);
    }

    stop() {
        if (!this.isRunning) return;
        this.isRunning = false;
        this.dispatchEvent(new CustomEvent('glint', {
            detail: {
                type: 'glint.drift.end',
                message: 'Drift ritual has ended.',
                timestamp: Date.now()
            }
        }));
    }

    animate(currentTime) {
        if (!this.isRunning) return;

        const dt = (currentTime - this.lastTime) / 1000; // Delta time in seconds

        // Fading effect for the trail
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        this.ctx.beginPath();
        const startPos = this.attractor.getPosition();
        const canvasCenter = { x: this.canvas.width / 2, y: this.canvas.height / 2 };
        const scale = 100; // Scale the attractor's coordinates to canvas size

        this.ctx.moveTo(canvasCenter.x + startPos.x * scale, canvasCenter.y + startPos.y * scale);

        this.attractor.step(dt);

        const endPos = this.attractor.getPosition();
        this.ctx.lineTo(canvasCenter.x + endPos.x * scale, canvasCenter.y + endPos.y * scale);
        this.ctx.stroke();

        this.lastTime = currentTime;
        requestAnimationFrame(this.animate.bind(this));
    }
}
