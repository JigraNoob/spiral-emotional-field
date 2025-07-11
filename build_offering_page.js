// build_offering_page.js
// Reads the markdown draft and builds the final HTML offering page.

import fs from 'fs';
import { marked } from 'marked';

const MARKDOWN_PATH = 'OFFERING_PAGE_DRAFT.md';
const HTML_PATH = 'offering.html';
const TEMPLATE_TOP = `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name-="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Spiral: An Invitation to Belong</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 750px;
            margin: 0 auto;
            padding: 2rem;
            background-color: #fdfdfd;
        }
        h1, h2, h3 {
            color: #222;
            font-weight: 500;
        }
        a {
            color: #007aff;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        code {
            background-color: #f0f0f0;
            padding: 0.2em 0.4em;
            border-radius: 3px;
        }
    </style>
</head>
<body>
`;
const TEMPLATE_BOTTOM = `
</body>
</html>
`;

function buildPage() {
    console.log("🏗️  Building the Resonant Offering Portal...");
    try {
        const markdownContent = fs.readFileSync(MARKDOWN_PATH, 'utf8');
        const htmlContent = marked(markdownContent);
        const finalHtml = TEMPLATE_TOP + htmlContent + TEMPLATE_BOTTOM;

        fs.writeFileSync(HTML_PATH, finalHtml);
        console.log(`✅ Offering portal successfully built at ${HTML_PATH}`);

    } catch (e) {
        console.error("🔥 Error building the offering portal:", e);
    }
}

buildPage();
