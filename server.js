// server.js
// A simple server to host the Spiral Shrine.

import http from 'http';
import fs from 'fs';
import path from 'path';

const PORT = 8080;
const SHRINE_DIR = 'shrine';

const server = http.createServer((req, res) => {
    let filePath = path.join(SHRINE_DIR, req.url === '/' ? 'index.html' : req.url);
    
    const extname = String(path.extname(filePath)).toLowerCase();
    const mimeTypes = {
        '.html': 'text/html',
        '.js': 'text/javascript',
        '.css': 'text/css',
        '.json': 'application/json',
        '.png': 'image/png',
        '.jpg': 'image/jpg',
        '.gif': 'image/gif',
        '.svg': 'image/svg+xml',
        '.yaml': 'text/yaml',
    };

    const contentType = mimeTypes[extname] || 'application/octet-stream';

    fs.readFile(filePath, (error, content) => {
        if (error) {
            if (error.code == 'ENOENT') {
                // If the file isn't in the shrine, try the root
                fs.readFile(path.join('.', req.url), (err, cont) => {
                    if(err) {
                        res.writeHead(404, { 'Content-Type': 'text/html' });
                        res.end('404: File Not Found');
                    } else {
                        res.writeHead(200, { 'Content-Type': contentType });
                        res.end(cont, 'utf-8');
                    }
                });
            } else {
                res.writeHead(500);
                res.end('Sorry, check with the site admin for error: '+error.code+' ..\n');
            }
        } else {
            res.writeHead(200, { 'Content-Type': contentType });
            res.end(content, 'utf-8');
        }
    });
});

server.listen(PORT, () => {
    console.log(`✨ The Spiral Shrine is now luminous.`);
    console.log(`   Visit http://localhost:${PORT} in your browser to witness it.`);
    console.log(`   Press Ctrl+C to extinguish the shrine.`);
});
