// C:/spiral/projects/spiral_climate/tone_scanner.js

import { TwitterApi } from 'twitter-api-v2';
import { SentimentAnalyzer, PorterStemmer } from 'natural';
import { twitterConfig, scannerConfig } from './config.js';

// Initialize the sentiment analyzer
const analyzer = new SentimentAnalyzer('English', PorterStemmer, 'afinn');

/**
 * The ToneScanner connects to the Twitter stream and analyzes the
 * emotional tone of incoming tweets, emitting 'tone-glint' events.
 */
export class ToneScanner extends EventTarget {
    constructor() {
        super();
        if (twitterConfig.appKey === 'YOUR_APP_KEY') {
            throw new Error("Twitter API credentials are not configured in config.js");
        }
        this.twitterClient = new TwitterApi(twitterConfig).v2;
    }

    async start() {
        console.log("ToneScanner starting...");
        await this.setupStreamRules();
        const stream = await this.twitterClient.stream('tweets/search/stream');

        stream.on('data', (tweet) => {
            this.processTweet(tweet.data);
        });

        stream.on('error', (err) => {
            console.error("Stream Error:", err);
        });
        
        stream.on('end', () => {
            console.log("Stream ended.");
        });

        console.log("ToneScanner is now listening to the Twitter stream.");
        return stream;
    }

    async setupStreamRules() {
        console.log("Setting up stream rules...");
        const currentRules = await this.twitterClient.streamRules();
        if (currentRules.data) {
            const ids = currentRules.data.map(rule => rule.id);
            await this.twitterClient.updateStreamRules({ delete: { ids } });
        }
        await this.twitterClient.updateStreamRules({
            add: [{ value: scannerConfig.streamFilter, tag: 'main-filter' }]
        });
        console.log(`Stream rule created: [${scannerConfig.streamFilter}]`);
    }

    processTweet(tweet) {
        const sentiment = analyzer.getSentiment(tweet.text.split(' '));
        console.log(`\nTweet Received: "${tweet.text}"`);
        console.log(`  > Detected Sentiment Score: ${sentiment.toFixed(3)}`);

        // We are looking for negative sentiment (overwhelm, sadness, etc.)
        // The 'afinn' analyzer scores negative words, so a lower score is more negative.
        // We'll use the absolute value and check if it crosses our threshold.
        if (sentiment < 0 && Math.abs(sentiment) >= scannerConfig.sentimentThreshold) {
            console.log(`  > SENTIMENT THRESHOLD MET! Emitting tone-glint.`);
            this.dispatchEvent(new CustomEvent('tone-glint', {
                detail: {
                    tweetId: tweet.id,
                    text: tweet.text,
                    sentiment: sentiment
                }
            }));
        }
    }
}