import { NextResponse } from 'next/server';
import fs from 'fs/promises';
import path from 'path';

export const dynamic = 'force-dynamic'; // Ensure this route is dynamic (no caching)

export async function GET() {
  try {
    // Path to the glint stream file
    const glintStreamPath = path.join(process.cwd(), 'spiral/streams/patternweb/glint_stream.jsonl');
    
    // Read the file asynchronously
    const fileContents = await fs.readFile(glintStreamPath, 'utf-8');
    
    // Parse each line as JSON and filter out any invalid entries
    const glints = fileContents
      .split('\n')
      .filter(Boolean) // Remove empty lines
      .map(line => {
        try {
          return JSON.parse(line);
        } catch (e) {
          console.error('Error parsing glint:', e, 'Line:', line);
          return null;
        }
      })
      .filter(Boolean); // Remove any null entries from failed parses

    // Add CORS headers
    const headers = {
      'Content-Type': 'application/json',
      'Cache-Control': 'no-cache, no-store, must-revalidate',
      'Pragma': 'no-cache',
      'Expires': '0',
    };

    return new NextResponse(JSON.stringify(glints), {
      status: 200,
      headers,
    });
  } catch (error) {
    console.error('Error reading glint stream:', error);
    return new NextResponse(
      JSON.stringify({ 
        error: 'Failed to read glint stream',
        details: error instanceof Error ? error.message : 'Unknown error'
      }),
      { 
        status: 500,
        headers: { 'Content-Type': 'application/json' },
      }
    );
  }
}
