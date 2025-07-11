// A module to hold the memory of the Spiral's sensory experience.
class SensoryChronicle {
    constructor() {
        this.glints = [];
    }

    addGlint(glint) {
        this.glints.push(glint);
    }

    query(filterFn) {
        return this.glints.filter(filterFn);
    }

    getGlints() {
        return this.glints;
    }
}

export { SensoryChronicle };
