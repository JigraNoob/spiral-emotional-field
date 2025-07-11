// This module is responsible for creating and emitting glints,
// and passing them to the sensory chronicle.
class GlintAttunement {
    constructor(chronicle) {
        this.chronicle = chronicle;
    }

    emit(source, payload) {
        const timestamp = new Date().toISOString();
        const glint = {
            timestamp,
            source,
            payload
        };
        
        const glintString = `∷GLINT @ ${timestamp} | Source: ${source} | Payload: ${JSON.stringify(payload)}∷`;
        console.log(glintString);

        if (this.chronicle) {
            this.chronicle.addGlint(glint);
        }
    }
}

export { GlintAttunement };