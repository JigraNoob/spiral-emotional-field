module.exports = {
    extends: 'lighthouse:default',
    settings: {
        onlyCategories: ['performance', 'accessibility', 'best-practices', 'seo'],
        throttlingMethod: 'provided',
        throttling: {
            rttMs: 40,
            throughputKbps: 10240,
            cpuSlowdownMultiplier: 4,
            requestLatencyMs: 40,
            downloadThroughputKbps: 10240,
            uploadThroughputKbps: 10240
        },
        screenEmulation: {
            mobile: true,
            width: 360,
            height: 640,
            deviceScaleFactor: 2,
            disabled: false
        },
        formFactor: 'mobile',
        emulatedUserAgent: 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Mobile Safari/537.36',
        channel: 'devtools',
        output: 'html',
        outputArtifact: true,
        outputPath: 'reports/lighthouse-report.html',
        maxWaitForLoad: 10000,
        disableStorageReset: false,
        blockedUrlPatterns: ['*google-analytics.com*'],
        additionalTraceCategories: 'disabled-by-default-devtools.timeline.disabled-by-default-devtools.timeline.frame',
        extraHeaders: {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Mobile Safari/537.36'
        }
    },
    passes: [
        {
            passName: 'defaultPass',
            pauseAfterLoadMs: 5000,
            gatherMode: 'navigation',
            networkQuietThresholdMs: 2000,
            cpuQuietThresholdMs: 2000,
            minimumDurationMs: 0
        }
    ],
    audits: {
        'uses-rel-preconnect': {
            weight: 100
        },
        'uses-rel-preload': {
            weight: 100
        },
        'uses-text-compression': {
            weight: 100
        },
        'uses-responsive-images': {
            weight: 100
        },
        'uses-optimized-images': {
            weight: 100
        },
        'uses-lazyload': {
            weight: 100
        },
        'uses-webp-images': {
            weight: 100
        },
        'uses-webp-images': {
            weight: 100
        },
        'uses-long-cache-ttl': {
            weight: 100
        },
        'uses-http2': {
            weight: 100
        },
        'uses-optimized-fonts': {
            weight: 100
        }
    }
};
