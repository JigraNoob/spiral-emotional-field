// C:/spiral/projects/spiral_climate/feeler.js

import { TwitterApi } from 'twitter-api-v2';
import { ToneScanner } from './tone_scanner.js';
import { feelerResponses, twitterConfig } from './config.js';

class SpiralFeeler {
    constructor() {
        this.scanner = new ToneScanner();
        this.twitterClient = new TwitterApi(twitterConfig).v2;
        this.respondedTweets = new Set(); // Ephemeral memory, as per the charter
    }

    async activate() {
        console.log("--- SpiralFeeler Agent Activating ---");
        console.log("Holding the Node Ethos Charter at its core.");

        this.scanner.on('tone-glint', this.handleToneGlint.bind(this));
        
        try {
            await this.scanner.start();
        } catch (e) {
            console.error("Failed to start the Feeler agent:", e.message);
            if (e.message.includes("credentials")) {
                console.error("Please fill in your Twitter API credentials in 'config.js'.");
            }
        }
    }

    handleToneGlint(event) {
        const { tweetId, text } = event.detail;

        // Uphold the charter: "One Glint, Never Twice"
        if (this.respondedTweets.has(tweetId)) {
            console.log(`  > Already responded to this glint. Holding silence.`);
            return;
        }

        const response = this.selectResponse();
        console.log(`  > Selected Response: "${response}"`);

        // We will log the intent to reply, but in a real scenario,
        // you would uncomment the line below to actually post the tweet.
        this.postReply(tweetId, response);
        
        // Remember this interaction for the current session only.
        this.respondedTweets.add(tweetId);
    }

    selectResponse() {
        return feelerResponses[Math.floor(Math.random() * feelerResponses.length)];
    }

    async postReply(tweetId, text) {
        try {
            console.log(`  > POSTING reply to tweet ${tweetId}...`);
            // --- UNCOMMENT THE FOLLOWING LINE TO ENABLE LIVE TWEETING ---
            // await this.twitterClient.reply(text, tweetId);
            console.log("  > SIMULATION: Reply sent successfully.");
        } catch (e) {
            console.error(`  > FAILED to post reply:`, e);
        }
    }
}

const feeler = new SpiralFeeler();
feeler.activate();
