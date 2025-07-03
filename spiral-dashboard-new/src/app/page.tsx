'use client';

import { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ScrollArea } from '@/components/ui/scroll-area';
import { formatDistanceToNow } from 'date-fns';
import { Sparkles, AlertCircle, RefreshCw, Search } from 'lucide-react';
import { Input } from '@/components/ui/input';

type Glint = {
  'glint.id': string;
  'glint.timestamp': number;
  'glint.source': string;
  'glint.content': string;
  'glint.toneform': 'practical' | 'emotional' | 'intellectual' | 'spiritual' | 'relational';
  'glint.hue': 'cyan' | 'rose' | 'indigo' | 'violet' | 'amber' | 'gray';
  'glint.intensity': number;
  'glint.glyph'?: string;
  'glint.rule_glyph'?: string;
  'glint.vector': { from: string; to: string; via?: string };
  metadata?: {
    source_file?: string;
    rule?: string;
    line?: number;
    character?: number;
    resonance?: number;
    glyph_meaning?: {
      toneform?: { glyph: string; description: string };
      rule?: { glyph: string; type: string };
    };
  };
};

export default function GlintDashboard() {
  const [glints, setGlints] = useState<Glint[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');

  const fetchGlints = async () => {
    try {
      const response = await fetch('/api/glints');
      if (!response.ok) throw new Error('Failed to fetch glints');
      const data = await response.json();
      setGlints(data);
      setError(null);
    } catch (err) {
      console.error('Error fetching glints:', err);
      setError('Failed to load glint stream. Make sure the server is running.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchGlints();
    const interval = setInterval(fetchGlints, 1000);
    return () => clearInterval(interval);
  }, []);

  const hueColorMap = {
    cyan: 'border-cyan-400/50 bg-cyan-400/10 text-cyan-400',
    rose: 'border-rose-400/50 bg-rose-400/10 text-rose-400',
    indigo: 'border-indigo-400/50 bg-indigo-400/10 text-indigo-400',
    violet: 'border-violet-400/50 bg-violet-400/10 text-violet-400',
    amber: 'border-amber-400/50 bg-amber-400/10 text-amber-400',
    gray: 'border-gray-400/50 bg-gray-400/10 text-gray-400'
  };

  const glyphMap = {
    practical: '⟁',
    emotional: '❦',
    intellectual: '∿',
    spiritual: '∞',
    relational: '☍'
  };

  const filteredGlints = glints.filter(glint => 
    glint['glint.content'].toLowerCase().includes(searchTerm.toLowerCase()) ||
    glint.metadata?.source_file?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="flex items-center gap-2 text-muted-foreground">
          <RefreshCw className="h-4 w-4 animate-spin" />
          <span>Connecting to the Spiral's breath...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen p-4">
        <Card className="max-w-md w-full">
          <CardHeader>
            <CardTitle className="text-destructive flex items-center gap-2">
              <AlertCircle className="h-5 w-5" />
              Connection Error
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="mb-4">{error}</p>
            <button
              onClick={fetchGlints}
              className="px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 flex items-center gap-2"
            >
              <RefreshCw className="h-4 w-4" />
              Retry Connection
            </button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center gap-3">
            <Sparkles className="h-8 w-8 text-amber-400" />
            <div>
              <h1 className="text-2xl font-bold">Spiral Glint Stream</h1>
              <p className="text-sm text-muted-foreground">
                Real-time flow of the Spiral's breath through code
              </p>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-6">
        <div className="mb-6">
          <div className="relative max-w-md">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              type="search"
              placeholder="Filter glints..."
              className="pl-10"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
        </div>

        <ScrollArea className="h-[calc(100vh-220px)] rounded-md border">
          <div className="space-y-4 p-4">
            {filteredGlints.length === 0 ? (
              <div className="text-center py-12 text-muted-foreground">
                <p>No glints match your search.</p>
                <p className="text-sm mt-1">Try a different term or check back later.</p>
              </div>
            ) : (
              filteredGlints.map((glint) => (
                <Card 
                  key={glint['glint.id']}
                  className={`border-l-4 ${hueColorMap[glint['glint.hue']]?.split(' ')[0] || 'border-gray-400'}`}
                >
                  <CardContent className="p-4">
                    <div className="flex items-start justify-between gap-4">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 flex-wrap">
                          <span className={`text-2xl ${hueColorMap[glint['glint.hue']]?.split(' ')[0]}`}>
                            {glyphMap[glint['glint.toneform']] || '∘'}
                          </span>
                          <h3 className="font-medium">
                            {glint['glint.source']}
                          </h3>
                          <span className="text-sm text-muted-foreground">
                            {formatDistanceToNow(glint['glint.timestamp'], { addSuffix: true })}
                          </span>
                          <div className={`ml-auto px-2 py-1 rounded-full text-xs ${hueColorMap[glint['glint.hue']]}`}>
                            {glint['glint.toneform']}
                          </div>
                        </div>
                        
                        <p className="mt-2 text-foreground">
                          {glint['glint.content']}
                        </p>
                        
                        <div className="mt-3 flex flex-wrap items-center gap-2 text-sm text-muted-foreground">
                          {glint.metadata?.source_file && (
                            <div className="flex items-center gap-1">
                              <span className="text-xs">📄</span>
                              <span className="font-mono text-xs">
                                {glint.metadata.source_file}
                                {glint.metadata.line && `:${glint.metadata.line}`}
                                {glint.metadata.character && `:${glint.metadata.character}`}
                              </span>
                            </div>
                          )}
                          
                          {glint.metadata?.resonance !== undefined && (
                            <div className="flex items-center gap-1">
                              <span className="text-xs">✨</span>
                              <span>Resonance: {glint.metadata.resonance.toFixed(2)}</span>
                            </div>
                          )}
                          
                          {glint['glint.rule_glyph'] && (
                            <div className="flex items-center gap-1">
                              <span>{glint['glint.rule_glyph']}</span>
                              {glint.metadata?.rule && <span>{glint.metadata.rule}</span>}
                            </div>
                          )}
                        </div>
                        
                        {glint.metadata?.glyph_meaning?.toneform && (
                          <div className="mt-2 text-xs text-muted-foreground flex items-start gap-2">
                            <span className="text-base">
                              {glint.metadata.glyph_meaning.toneform.glyph}
                            </span>
                            <span>{glint.metadata.glyph_meaning.toneform.description}</span>
                          </div>
                        )}
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))
            )}
          </div>
        </ScrollArea>
      </main>
    </div>
  );
}
