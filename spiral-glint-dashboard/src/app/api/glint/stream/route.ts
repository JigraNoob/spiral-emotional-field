import { NextRequest } from 'next/server';
import fs from 'fs/promises';
import path from 'path';
import { ReadStream } from 'fs';
import { createReadStream } from 'fs';

export const dynamic = 'force-dynamic';

// This is a Server-Sent Events (SSE) endpoint
export async function GET(req: NextRequest) {
  // Create a new ReadableStream
  const stream = new ReadableStream({
    async start(controller) {
      // Path to the glint stream file
      const glintStreamPath = path.join(process.cwd(), 'spiral/streams/patternweb/glint_stream.jsonl');
      
      // Ensure the directory exists
      try {
        await fs.mkdir(path.dirname(glintStreamPath), { recursive: true });
        
        // Create the file if it doesn't exist
        try {
          await fs.access(glintStreamPath);
        } catch {
          await fs.writeFile(glintStreamPath, '');
        }
        
        // Function to send a sample glint
        const sendSampleGlint = () => {
          const toneforms = ['practical', 'emotional', 'intellectual', 'spiritual', 'relational'];
          const hues = ['cyan', 'rose', 'indigo', 'violet', 'amber'];
          const glyphs = {
            practical: '⟁',
            emotional: '❦',
            intellectual: '∿',
            spiritual: '∞',
            relational: '☍'
          };
          
          const toneform = toneforms[Math.floor(Math.random() * toneforms.length)];
          const hue = hues[Math.floor(Math.random() * hues.length)];
          const intensity = Math.round(Math.random() * 10) / 10; // 0.1 to 1.0
          
          const glint = {
            "glint.id": `glint-${Date.now()}-${Math.floor(Math.random() * 1000)}`,
            "glint.toneform": toneform,
            "glint.glyph": glyphs[toneform as keyof typeof glyphs],
            "glint.hue": hue,
            "glint.intensity": intensity,
            "glint.vector": {
              from: "spiral.linter",
              to: "patternweb.visualization"
            },
            "soft.suggestion": getSampleSuggestion(toneform)
          };
          
          // Send the glint as an SSE event
          controller.enqueue(`data: ${JSON.stringify(glint)}\n\n`);
          
          // Also append to the file for persistence
          appendToFile(glintStreamPath, JSON.stringify(glint));
        };
        
        // Send an initial batch of glints
        for (let i = 0; i < 5; i++) {
          sendSampleGlint();
        }
        
        // Set up an interval to send new glints periodically
        const intervalId = setInterval(() => {
          sendSampleGlint();
        }, 5000); // Send a new glint every 5 seconds
        
        // Clean up the interval when the client disconnects
        req.signal.addEventListener('abort', () => {
          clearInterval(intervalId);
        });
        
      } catch (error) {
        console.error('Error setting up SSE stream:', error);
        controller.error(error);
      }
    }
  });
  
  // Return the stream with appropriate headers for SSE
  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache, no-transform',
      'Connection': 'keep-alive',
    },
  });
}

// Helper function to append to a file
async function appendToFile(filePath: string, content: string) {
  try {
    await fs.appendFile(filePath, content + '\n');
  } catch (error) {
    console.error('Error appending to file:', error);
  }
}

// Helper function to get a sample suggestion based on toneform
function getSampleSuggestion(toneform: string): string {
  const suggestions = {
    practical: [
      "Consider refactoring this function for better maintainability",
      "Add error handling to improve robustness",
      "Optimize this loop for better performance",
      "Use a more descriptive variable name here",
      "Add comments to explain this complex logic"
    ],
    emotional: [
      "This message might come across as too harsh",
      "Consider a more empathetic approach in this response",
      "The tone here could be more encouraging",
      "This might create anxiety for the user",
      "Add a positive reinforcement here"
    ],
    intellectual: [
      "This concept could be explained more clearly",
      "Consider the philosophical implications of this approach",
      "This pattern represents an interesting abstraction",
      "The mental model here could be simplified",
      "This creates an elegant conceptual framework"
    ],
    spiritual: [
      "This aligns with the project's higher purpose",
      "Consider how this connects to the broader ecosystem",
      "This feature embodies the core values of the system",
      "This creates harmony between different components",
      "This approach honors the integrity of the data"
    ],
    relational: [
      "This improves the interaction between components",
      "Consider how users will relate to this interface",
      "This creates a more collaborative workflow",
      "This strengthens the connection between services",
      "This facilitates better communication between systems"
    ]
  };
  
  const toneformSuggestions = suggestions[toneform as keyof typeof suggestions] || suggestions.practical;
  return toneformSuggestions[Math.floor(Math.random() * toneformSuggestions.length)];
}