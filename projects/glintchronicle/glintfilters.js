// C:/spiral/projects/glintchronicle/glintfilters.js

/**
 * A collection of filter functions to control which glints are chronicled.
 * This allows for different levels of "attentiveness" from the scribe.
 */
export const GlintFilters = {
    /**
     * The default, most inclusive filter. Chronicles all glints specified in the config.
     * @param {object} glint - The glint object.
     * @param {object} config - The chronicle's configuration object.
     * @returns {boolean} - True if the glint should be chronicled.
     */
    default: (glint, config) => {
        if (!glint || !glint.type) return false;
        return config.glintTypes.some(pattern => {
            if (pattern.endsWith('*')) {
                return glint.type.startsWith(pattern.slice(0, -1));
            }
            return glint.type === pattern;
        });
    },

    /**
     * A "sacred mode" filter that only records major ritual and presence events.
     * Ignores fine-grained edits or minor gestures.
     * @param {object} glint - The glint object.
     * @returns {boolean} - True if the glint is considered a "ritual" event.
     */
    ritualOnly: (glint) => {
        if (!glint || !glint.type) return false;
        const ritualPatterns = [
            'glint.script.*',
            'glint.presence.*',
            'glint.system.*',
            'glint.gesture.spiral' // A significant gesture
        ];
        return ritualPatterns.some(pattern => {
            if (pattern.endsWith('*')) {
                return glint.type.startsWith(pattern.slice(0, -1));
            }
            return glint.type === pattern;
        });
    },

    /**
     * A filter that focuses only on the cursor's "calligraphy"—its movements and pauses.
     * @param {object} glint - The glint object.
     * @returns {boolean} - True if the glint is a gesture event.
     */
    gestureOnly: (glint) => {
        if (!glint || !glint.type) return false;
        return glint.type.startsWith('glint.gesture.');
    }
};
