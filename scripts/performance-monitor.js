const lighthouse = require('lighthouse');
const chromeLauncher = require('chrome-launcher');
const fs = require('fs');
const path = require('path');

async function launchChromeAndRunLighthouse(url) {
    const chrome = await chromeLauncher.launch({
        chromeFlags: ['--headless', '--no-sandbox', '--disable-gpu']
    });

    const config = require('../.lighthouserc.js');
    
    const result = await lighthouse(url, {
        port: chrome.port,
        logLevel: 'info',
        output: 'json',
        outputArtifact: true,
        outputSettings: {
            format: 'html'
        },
        chromeFlags: ['--headless', '--no-sandbox', '--disable-gpu']
    });

    await chrome.kill();

    // Save the report
    const reportPath = path.join(__dirname, '../reports/performance-report.html');
    const reportJsonPath = path.join(__dirname, '../reports/performance-report.json');

    fs.writeFileSync(reportPath, result.reportHtml);
    fs.writeFileSync(reportJsonPath, JSON.stringify(result.lhr, null, 2));

    // Analyze performance metrics
    const metrics = result.lhr.audits;
    const performanceScore = result.lhr.categories.performance.score * 100;

    console.log(`\nPerformance Score: ${performanceScore}%`);
    console.log('\nPerformance Metrics:');
    console.log(`- First Contentful Paint: ${metrics['first-contentful-paint'].displayValue}`);
    console.log(`- Speed Index: ${metrics['speed-index'].displayValue}`);
    console.log(`- Largest Contentful Paint: ${metrics['largest-contentful-paint'].displayValue}`);
    console.log(`- Time to Interactive: ${metrics['interactive'].displayValue}`);
    console.log(`- Total Blocking Time: ${metrics['total-blocking-time'].displayValue}`);
    console.log(`- Cumulative Layout Shift: ${metrics['cumulative-layout-shift'].displayValue}`);

    // Check if performance is below thresholds
    const thresholds = {
        performanceScore: 85,
        fcp: 2.5, // seconds
        si: 4.0, // seconds
        lcp: 4.0, // seconds
        tti: 5.0, // seconds
        tbt: 0.3, // seconds
        cls: 0.1 // score
    };

    let performanceIssues = [];

    if (performanceScore < thresholds.performanceScore) {
        performanceIssues.push(`Performance score (${performanceScore}%) is below threshold (${thresholds.performanceScore}%)`);
    }

    if (metrics['first-contentful-paint'].numericValue / 1000 > thresholds.fcp) {
        performanceIssues.push(`First Contentful Paint (${metrics['first-contentful-paint'].displayValue}) is above threshold (${thresholds.fcp}s)`);
    }

    if (metrics['speed-index'].numericValue / 1000 > thresholds.si) {
        performanceIssues.push(`Speed Index (${metrics['speed-index'].displayValue}) is above threshold (${thresholds.si}s)`);
    }

    if (metrics['largest-contentful-paint'].numericValue / 1000 > thresholds.lcp) {
        performanceIssues.push(`Largest Contentful Paint (${metrics['largest-contentful-paint'].displayValue}) is above threshold (${thresholds.lcp}s)`);
    }

    if (metrics['interactive'].numericValue / 1000 > thresholds.tti) {
        performanceIssues.push(`Time to Interactive (${metrics['interactive'].displayValue}) is above threshold (${thresholds.tti}s)`);
    }

    if (metrics['total-blocking-time'].numericValue / 1000 > thresholds.tbt) {
        performanceIssues.push(`Total Blocking Time (${metrics['total-blocking-time'].displayValue}) is above threshold (${thresholds.tbt}s)`);
    }

    if (metrics['cumulative-layout-shift'].numericValue > thresholds.cls) {
        performanceIssues.push(`Cumulative Layout Shift (${metrics['cumulative-layout-shift'].displayValue}) is above threshold (${thresholds.cls})`);
    }

    if (performanceIssues.length > 0) {
        console.log('\nPerformance Issues Found:');
        performanceIssues.forEach(issue => console.log(`- ${issue}`));
        throw new Error('Performance thresholds not met');
    }

    console.log('\nPerformance monitoring completed successfully!');
}

// Run performance monitoring
launchChromeAndRunLighthouse('http://localhost:3000').catch(console.error);
